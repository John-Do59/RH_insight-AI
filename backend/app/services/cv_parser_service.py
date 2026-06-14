"""
CV Parser Service — Domain Model V2
Pipeline: Raw Text → LLM Extraction → Pydantic Validation → DB Insert + ChromaDB Indexation
Symétrique du JobParserService.
"""
import json
from typing import Tuple

from sqlalchemy.orm import Session

from backend.app.llm.ollama_client import get_fast_llm
from backend.app.models.candidate import Candidate
from backend.app.models.skill import Skill, CandidateSkill
from backend.app.schemas.candidate_schema import CandidateParsedData
from backend.app.rag.vector_store import get_vector_store
from backend.app.utils.logger import logger
from langfuse.decorators import observe


@observe()
def _extract_candidate_data_with_llm(raw_text: str) -> CandidateParsedData:
    """
    Uses an LLM to extract structured data from raw CV text.
    Returns a validated CandidateParsedData object.
    """
    llm = get_fast_llm()

    prompt = f"""Tu es un expert RH. Analyse le CV ci-dessous et extrais toutes les informations demandées.

Retourne UNIQUEMENT du JSON valide (sans Markdown, sans backticks) avec exactement ces clés :
{{
  "first_name": null ou "string",
  "last_name": null ou "string",
  "email": null ou "string",
  "title": null ou "string — titre/poste actuel ou recherché",
  "location": null ou "string",
  "experience_years": null ou entier — total années d'expérience,
  "summary": null ou "string — résumé professionnel en 2-3 phrases",
  "skills": ["liste de toutes les compétences techniques et non techniques"],
  "education": ["liste des formations (ex: 'Master IA - Université Paris, 2023')"],
  "experiences": [
    {{"company": "string", "title": "string", "duration": "string", "description": "string"}}
  ],
  "certifications": ["liste des certifications"],
  "languages": ["liste des langues parlées (ex: 'Anglais C1')"]
}}

CV :
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
        return CandidateParsedData(**data)
    except Exception as e:
        logger.error(f"CVParserService: LLM parsing failed: {e}. Using fallback.")
        return CandidateParsedData(
            summary=raw_text[:500],
            skills=[],
        )


@observe()
def _persist_candidate(parsed: CandidateParsedData, db: Session, overrides: dict) -> Tuple[Candidate, list[str]]:
    """
    Persists a parsed candidate to PostgreSQL with all structured data and skills.
    If email already exists, updates the existing record.
    """
    email = overrides.get("email") or parsed.email
    candidate = None
    if email:
        candidate = db.query(Candidate).filter(Candidate.email == email).first()

    if not candidate:
        candidate = Candidate()
        db.add(candidate)

    candidate.first_name = overrides.get("first_name") or parsed.first_name
    candidate.last_name = overrides.get("last_name") or parsed.last_name
    candidate.email = email
    candidate.title = parsed.title
    candidate.location = parsed.location
    candidate.experience_years = parsed.experience_years
    candidate.summary = parsed.summary
    candidate.education = [e for e in parsed.education] if parsed.education else []
    candidate.experiences = [e.model_dump() for e in parsed.experiences] if parsed.experiences else []
    candidate.certifications = parsed.certifications or []
    candidate.languages = parsed.languages or []

    db.flush()

    # Remove old skill associations before re-inserting
    db.query(CandidateSkill).filter(CandidateSkill.candidate_id == candidate.id).delete()
    db.flush()

    for skill_name in parsed.skills:
        skill_name = skill_name.strip()
        if not skill_name:
            continue
        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.add(skill)
            db.flush()

        assoc = CandidateSkill(candidate_id=candidate.id, skill_id=skill.id)
        db.add(assoc)

    db.commit()
    db.refresh(candidate)
    return candidate, parsed.skills


@observe()
def _index_in_chromadb(candidate: Candidate, parsed: CandidateParsedData) -> None:
    """
    Indexes the candidate profile in ChromaDB for RAG retrieval.
    """
    try:
        vector_store = get_vector_store()
        name = f"{candidate.first_name or ''} {candidate.last_name or ''}".strip() or "Candidat inconnu"
        doc_text = (
            f"Candidat: {name}\n"
            f"Titre: {candidate.title}\n"
            f"Résumé: {candidate.summary}\n"
            f"Compétences: {', '.join(parsed.skills)}\n"
            f"Formations: {', '.join(parsed.education)}\n"
            f"Langues: {', '.join(parsed.languages)}\n"
            f"Expérience: {candidate.experience_years} ans"
        )
        vector_store.add_texts(
            texts=[doc_text],
            metadatas=[{"source": "candidate_cv", "candidate_id": str(candidate.id), "name": name}]
        )
        logger.info(f"CVParserService: Candidate '{name}' indexed in ChromaDB.")
    except Exception as e:
        logger.warning(f"CVParserService: ChromaDB indexation failed (non-blocking): {e}")


@observe()
def run_cv_parser_pipeline(raw_text: str, db: Session, overrides: dict = {}) -> Tuple[Candidate, list[str]]:
    """
    Full pipeline: Extract → Validate → Persist → Index.
    This is the entry point to call from the API endpoint.
    """
    logger.info("CVParserService: Starting parsing pipeline...")
    parsed = _extract_candidate_data_with_llm(raw_text)
    candidate, skills = _persist_candidate(parsed, db, overrides)
    _index_in_chromadb(candidate, parsed)
    logger.info(f"CVParserService: Pipeline complete for candidate_id={candidate.id}")
    return candidate, skills
