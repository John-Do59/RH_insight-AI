"""
Job Parser Service — Domain Model V2
Pipeline: Raw Text → LLM Extraction → Pydantic Validation → DB Insert + ChromaDB Indexation
"""
import json
from typing import Tuple

from sqlalchemy.orm import Session

from backend.app.llm.ollama_client import get_fast_llm
from backend.app.models.job import Job
from backend.app.models.skill import Skill, JobSkill
from backend.app.schemas.job_schema import JobParsedData
from backend.app.rag.vector_store import get_vector_store
from backend.app.utils.logger import logger
from langfuse.decorators import observe


@observe()
def _extract_job_data_with_llm(raw_text: str) -> JobParsedData:
    """
    Uses an LLM to extract structured data from raw job description text.
    Returns a validated JobParsedData object.
    """
    llm = get_fast_llm()

    prompt = f"""Tu es un expert RH. Analyse l'offre d'emploi ci-dessous et extrais toutes les informations demandées.

Retourne UNIQUEMENT du JSON valide (sans Markdown, sans backticks) avec exactement ces clés :
{{
  "title": "string — titre du poste",
  "description": "string — résumé de l'offre en 2-3 phrases",
  "required_skills": ["liste des compétences requises"],
  "preferred_skills": ["liste des compétences souhaitées/optionnelles"],
  "experience_years": null ou entier — années d'expérience requises,
  "education_level": null ou "string" — niveau d'études (ex: Master, Bac+3),
  "certifications": ["liste des certifications mentionnées"],
  "languages": ["liste des langues requises"],
  "location": null ou "string" — localisation du poste,
  "contract_type": null ou "string" — type de contrat (CDI, CDD, Freelance...)
}}

Offre d'emploi :
---
{raw_text[:6000]}
---"""

    response = llm.invoke([
        ("system", "Vous êtes un assistant RH expert. Répondez UNIQUEMENT en JSON valide."),
        ("human", prompt)
    ])

    response_text = response.content
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in LLM response")
        json_str = response_text[start_idx:end_idx]
        data = json.loads(json_str)
        return JobParsedData(**data)
    except Exception as e:
        logger.error(f"JobParserService: LLM parsing failed: {e}. Using fallback.")
        return JobParsedData(
            title="Poste non identifié",
            description=raw_text[:500],
            required_skills=[],
        )


@observe()
def _persist_job(parsed: JobParsedData, raw_text: str, db: Session, overrides: dict) -> Tuple[Job, list[str]]:
    """
    Persists a parsed job offer to PostgreSQL with all its structured data and skills.
    """
    job = Job(
        title=overrides.get("title") or parsed.title,
        company=overrides.get("company"),
        description=parsed.description,
        location=overrides.get("location") or parsed.location,
        contract_type=overrides.get("contract_type") or parsed.contract_type,
        experience_years=parsed.experience_years,
        education_level=parsed.education_level,
        certifications=parsed.certifications or [],
        languages=parsed.languages or [],
    )
    db.add(job)
    db.flush()

    all_skills = list(set(parsed.required_skills + parsed.preferred_skills))
    for skill_name in all_skills:
        skill_name = skill_name.strip()
        if not skill_name:
            continue
        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.add(skill)
            db.flush()

        is_required = skill_name in parsed.required_skills
        assoc = JobSkill(job_id=job.id, skill_id=skill.id, is_required=is_required)
        db.add(assoc)

    db.commit()
    db.refresh(job)
    return job, all_skills


@observe()
def _index_in_chromadb(job: Job, parsed: JobParsedData) -> None:
    """
    Indexes the job description in ChromaDB for RAG retrieval.
    """
    try:
        vector_store = get_vector_store()
        doc_text = (
            f"Offre d'emploi: {job.title}\n"
            f"Description: {parsed.description}\n"
            f"Compétences requises: {', '.join(parsed.required_skills)}\n"
            f"Compétences souhaitées: {', '.join(parsed.preferred_skills)}\n"
            f"Expérience: {parsed.experience_years} ans\n"
            f"Localisation: {job.location}\n"
            f"Contrat: {job.contract_type}"
        )
        vector_store.add_texts(
            texts=[doc_text],
            metadatas=[{"source": "job_offer", "job_id": str(job.id), "title": job.title}]
        )
        logger.info(f"JobParserService: Job '{job.title}' indexed in ChromaDB.")
    except Exception as e:
        logger.warning(f"JobParserService: ChromaDB indexation failed (non-blocking): {e}")


@observe()
def run_job_parser_pipeline(raw_text: str, db: Session, overrides: dict = {}) -> Tuple[Job, list[str]]:
    """
    Full pipeline: Extract → Validate → Persist → Index.
    This is the entry point to call from the API endpoint.
    """
    logger.info("JobParserService: Starting parsing pipeline...")
    parsed = _extract_job_data_with_llm(raw_text)
    job, skills = _persist_job(parsed, raw_text, db, overrides)
    _index_in_chromadb(job, parsed)
    logger.info(f"JobParserService: Pipeline complete for job_id={job.id}")
    return job, skills
