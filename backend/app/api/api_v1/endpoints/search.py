from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel

from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import Skill, CandidateSkill, JobSkill
from backend.app.llm.ollama_client import get_fast_llm

router = APIRouter()


class CandidateSearchResult(BaseModel):
    id: str
    name: str
    title: Optional[str]
    experience_years: Optional[int]
    location: Optional[str]
    skills: List[str]


class JobSearchResult(BaseModel):
    id: str
    title: str
    company: Optional[str]
    location: Optional[str]
    contract_type: Optional[str]
    skills: List[str]


class SemanticSearchRequest(BaseModel):
    query: str
    target: str = "candidates"  # "candidates" or "jobs"
    top_n: int = 10


@router.get("/candidates", response_model=List[CandidateSearchResult])
def search_candidates(
    skills: Optional[str] = Query(None, description="Comma-separated list of required skills"),
    exp: Optional[int] = Query(None, description="Minimum years of experience"),
    location: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Filter candidates by skills, experience, and location.
    Results are paginated.
    """
    query = db.query(Candidate)

    if exp is not None:
        query = query.filter(Candidate.experience_years >= exp)

    if location:
        query = query.filter(Candidate.location.ilike(f"%{location}%"))

    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        # Filter candidates who have at least one of the required skills
        query = (
            query.join(CandidateSkill, CandidateSkill.candidate_id == Candidate.id)
            .join(Skill, Skill.id == CandidateSkill.skill_id)
            .filter(func.lower(Skill.name).in_(skill_list))
            .distinct()
        )

    offset = (page - 1) * page_size
    candidates = query.offset(offset).limit(page_size).all()

    results = []
    for c in candidates:
        c_skills = db.query(Skill.name).join(CandidateSkill).filter(
            CandidateSkill.candidate_id == c.id
        ).all()
        name = f"{c.first_name or ''} {c.last_name or ''}".strip() or f"Candidat {str(c.id)[:8]}"
        results.append(
            CandidateSearchResult(
                id=str(c.id),
                name=name,
                title=c.title,
                experience_years=c.experience_years,
                location=c.location,
                skills=[s[0] for s in c_skills],
            )
        )
    return results


@router.get("/jobs", response_model=List[JobSearchResult])
def search_jobs(
    skills: Optional[str] = Query(None, description="Comma-separated list of required skills"),
    location: Optional[str] = Query(None),
    contract_type: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Filter jobs by required skills, location, and contract type.
    """
    query = db.query(Job)

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    if contract_type:
        query = query.filter(Job.contract_type.ilike(f"%{contract_type}%"))

    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        query = (
            query.join(JobSkill, JobSkill.job_id == Job.id)
            .join(Skill, Skill.id == JobSkill.skill_id)
            .filter(func.lower(Skill.name).in_(skill_list))
            .distinct()
        )

    offset = (page - 1) * page_size
    jobs = query.offset(offset).limit(page_size).all()

    results = []
    for j in jobs:
        j_skills = db.query(Skill.name).join(JobSkill).filter(
            JobSkill.job_id == j.id
        ).all()
        results.append(
            JobSearchResult(
                id=str(j.id),
                title=j.title,
                company=j.company,
                location=j.location,
                contract_type=j.contract_type,
                skills=[s[0] for s in j_skills],
            )
        )
    return results


@router.post("/semantic")
def semantic_search(request: SemanticSearchRequest, db: Session = Depends(get_db)):
    """
    Semantic search using the LLM to parse the query and then filter candidates or jobs.
    This is a simplified implementation: the LLM extracts structured filters from the query,
    then applies SQL filtering. A full implementation would embed the query and use pgvector.
    """
    prompt = f"""
    Extrait les critères de recherche depuis cette requête RH :
    "{request.query}"
    
    Retourne UNIQUEMENT du JSON avec :
    - "skills": liste de compétences (strings)
    - "experience": entier (0 si non mentionné)
    - "location": chaine vide si non mentionné
    """
    
    from langchain_core.messages import SystemMessage, HumanMessage
    import json
    
    llm = get_fast_llm()
    messages = [
        SystemMessage(content="Réponds uniquement en JSON valide."),
        HumanMessage(content=prompt)
    ]
    response_text = llm.invoke(messages).content
    
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        parsed = json.loads(response_text[start:end]) if start != -1 else {}
    except Exception:
        parsed = {}

    skills_str = ",".join(parsed.get("skills", []))
    exp = parsed.get("experience", 0) or None
    location = parsed.get("location") or None

    if request.target == "jobs":
        return search_jobs(skills=skills_str, location=location, db=db)
    else:
        return search_candidates(skills=skills_str, exp=exp, location=location, db=db)
