"""
Endpoint d'ingestion des candidats (CV) — Domain Model V2
Supporte : PDF, DOCX, TXT.
Le parsing structuré est délégué au cv_parser_service et exécuté en BackgroundTask.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.services.cv_parser_service import run_cv_parser_pipeline
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.utils.document_parser import extract_text

router = APIRouter()


class CandidateResponse(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    experience_years: Optional[int] = None
    summary: Optional[str] = None
    certifications: list[str] = []
    languages: list[str] = []
    skills: list[str] = []

    class Config:
        from_attributes = True


def _build_candidate_response(candidate: Candidate) -> CandidateResponse:
    skills = [a.skill.name for a in candidate.skill_associations if a.skill]
    return CandidateResponse(
        id=str(candidate.id),
        first_name=candidate.first_name,
        last_name=candidate.last_name,
        email=candidate.email,
        title=candidate.title,
        location=candidate.location,
        experience_years=candidate.experience_years,
        summary=candidate.summary,
        certifications=candidate.certifications or [],
        languages=candidate.languages or [],
        skills=skills,
    )


@router.post("/upload", response_model=dict, summary="Ingérer un CV candidat")
async def upload_candidate_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload un CV (PDF, DOCX ou TXT).
    Retourne immédiatement — le parsing structuré (LLM + DB + ChromaDB)
    est traité en arrière-plan (BackgroundTask non-bloquant).
    """
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 10 MB).")

    try:
        raw_text = extract_text(contents, file.filename or "cv.pdf")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erreur de lecture: {e}")

    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="Le fichier ne contient pas de texte lisible.")

    # Non-blocking: parse + persist + index in background
    background_tasks.add_task(run_cv_parser_pipeline, raw_text, db, {})

    return {
        "status": "processing",
        "message": "Le CV est en cours d'analyse par l'IA. Le profil sera disponible dans quelques instants.",
        "filename": file.filename,
    }


@router.get("/", response_model=list[CandidateResponse], summary="Lister les candidats")
def list_candidates(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return [_build_candidate_response(c) for c in candidates]


@router.get("/{candidate_id}", response_model=CandidateResponse, summary="Détail d'un candidat")
def get_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate = db.query(Candidate).filter(Candidate.id == uuid.UUID(candidate_id)).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidat introuvable.")
    return _build_candidate_response(candidate)


@router.delete("/{candidate_id}", summary="Supprimer un candidat")
def delete_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate = db.query(Candidate).filter(Candidate.id == uuid.UUID(candidate_id)).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidat introuvable.")
    db.delete(candidate)
    db.commit()
    return {"message": "Candidat supprimé."}
