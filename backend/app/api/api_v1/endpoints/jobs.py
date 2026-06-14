"""
Endpoint d'ingestion des offres d'emploi — Domain Model V2
Supporte : PDF, DOCX, TXT ou texte brut.
Les opérations de parsing sont déclenchées en BackgroundTask (non-bloquant).
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from backend.app.database.session import get_db
from backend.app.models.job import Job
from backend.app.models.skill import Skill, JobSkill
from backend.app.services.job_parser_service import run_job_parser_pipeline
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.utils.document_parser import extract_text
from backend.app.utils.logger import logger

router = APIRouter()


class JobCreateText(BaseModel):
    """Création d'une offre via texte brut."""
    content: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    contract_type: Optional[str] = None


class JobResponse(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    contract_type: Optional[str] = None
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    certifications: list[str] = []
    languages: list[str] = []
    required_skills: list[str] = []
    preferred_skills: list[str] = []

    class Config:
        from_attributes = True


def _build_job_response(job: Job) -> JobResponse:
    """Build a rich JobResponse from a Job ORM object."""
    required = [a.skill.name for a in job.skill_associations if a.skill and a.is_required]
    preferred = [a.skill.name for a in job.skill_associations if a.skill and not a.is_required]
    return JobResponse(
        id=str(job.id),
        title=job.title,
        company=job.company,
        description=job.description,
        location=job.location,
        contract_type=job.contract_type,
        experience_years=job.experience_years,
        education_level=job.education_level,
        certifications=job.certifications or [],
        languages=job.languages or [],
        required_skills=required,
        preferred_skills=preferred,
    )


@router.post("/upload", response_model=dict, summary="Ingérer une offre (PDF/DOCX/TXT)")
async def upload_job_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    contract_type: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload un fichier PDF, DOCX ou TXT contenant une offre d'emploi.
    Retourne immédiatement un ticket de confirmation — le parsing complet
    (LLM + DB + ChromaDB) est traité en arrière-plan (BackgroundTask).
    """
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 10 MB).")

    try:
        raw_text = extract_text(contents, file.filename or "file.pdf")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Impossible de lire le fichier : {e}")

    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="Le fichier ne contient pas de texte lisible.")

    overrides = {"company": company, "location": location, "contract_type": contract_type}

    # Non-blocking: parse + persist in background
    background_tasks.add_task(run_job_parser_pipeline, raw_text, db, overrides)

    return {
        "status": "processing",
        "message": "L'offre est en cours d'analyse par l'IA. Elle sera disponible dans quelques instants.",
        "filename": file.filename,
    }


@router.post("/text", response_model=dict, summary="Ingérer une offre (texte brut)")
def create_job_from_text(
    background_tasks: BackgroundTasks,
    payload: JobCreateText,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crée une offre d'emploi à partir d'un texte brut.
    Le parsing est effectué en arrière-plan.
    """
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Le contenu est vide.")

    overrides = {
        "title": payload.title,
        "company": payload.company,
        "location": payload.location,
        "contract_type": payload.contract_type,
    }

    background_tasks.add_task(run_job_parser_pipeline, payload.content, db, overrides)

    return {
        "status": "processing",
        "message": "L'offre est en cours d'analyse par l'IA. Elle sera disponible dans quelques instants.",
    }


@router.get("/", response_model=list[JobResponse], summary="Lister toutes les offres")
def list_jobs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return [_build_job_response(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse, summary="Détail d'une offre")
def get_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Offre introuvable.")
    return _build_job_response(job)


@router.delete("/{job_id}", summary="Supprimer une offre")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Offre introuvable.")
    db.delete(job)
    db.commit()
    return {"message": "Offre supprimée."}
