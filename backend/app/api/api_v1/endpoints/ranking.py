from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from typing import List
from pydantic import BaseModel

from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.matching import CandidateJobMatch
from backend.app.graph.matching_nodes import (
    load_data_node,
    vector_retrieval_node,
    skill_comparison_node,
    reasoning_node,
    scoring_node,
)

router = APIRouter()


class RankedCandidate(BaseModel):
    candidate_id: str
    name: str
    title: str | None
    score: float
    strengths: List[str]
    gaps: List[str]
    experience_years: int | None


class RankedJob(BaseModel):
    job_id: str
    title: str
    company: str | None
    score: float
    strengths: List[str]
    gaps: List[str]


def _score_pair(candidate: Candidate, job: Job, db: Session) -> dict:
    """Helper: run scoring pipeline for a candidate/job pair."""
    # Check cache first
    cached = db.query(CandidateJobMatch).filter_by(
        candidate_id=candidate.id, job_id=job.id
    ).first()
    if cached:
        return {
            "score": cached.score,
            "strengths": cached.strengths or [],
            "gaps": cached.gaps or [],
        }

    # Run pipeline
    state: dict = {
        "candidate_id": candidate.id,
        "job_id": job.id,
    }
    state = load_data_node(state)
    state = vector_retrieval_node(state)
    state = skill_comparison_node(state)
    state = reasoning_node(state)
    state = scoring_node(state)

    # Persist in cache
    match = CandidateJobMatch(
        candidate_id=candidate.id,
        job_id=job.id,
        score=state["final_score"],
        strengths=state.get("strengths", []),
        gaps=state.get("gaps", []),
        explanation=state.get("explanation", ""),
    )
    try:
        db.add(match)
        db.commit()
    except Exception:
        db.rollback()

    return {
        "score": state["final_score"],
        "strengths": state.get("strengths", []),
        "gaps": state.get("gaps", []),
    }


@router.post("/job/{job_id}", response_model=List[RankedCandidate])
def rank_candidates_for_job(
    job_id: UUID,
    top_n: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return the top N candidates ranked for a given job.
    Uses the existing hybrid scoring engine + cache.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = db.query(Candidate).limit(100).all()
    results = []

    for c in candidates:
        scored = _score_pair(c, job, db)
        name = f"{c.first_name or ''} {c.last_name or ''}".strip() or f"Candidat {str(c.id)[:8]}"
        results.append(
            RankedCandidate(
                candidate_id=str(c.id),
                name=name,
                title=c.title,
                score=scored["score"],
                strengths=scored["strengths"],
                gaps=scored["gaps"],
                experience_years=c.experience_years,
            )
        )

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_n]


@router.post("/candidate/{candidate_id}", response_model=List[RankedJob])
def rank_jobs_for_candidate(
    candidate_id: UUID,
    top_n: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return the top N jobs ranked for a given candidate.
    Uses the existing hybrid scoring engine + cache.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Candidate not found")

    jobs = db.query(Job).limit(100).all()
    results = []

    for j in jobs:
        scored = _score_pair(candidate, j, db)
        results.append(
            RankedJob(
                job_id=str(j.id),
                title=j.title,
                company=j.company,
                score=scored["score"],
                strengths=scored["strengths"],
                gaps=scored["gaps"],
            )
        )

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_n]
