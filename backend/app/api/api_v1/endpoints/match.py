from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import List

from backend.app.database.session import get_db
from backend.app.models.matching import CandidateJobMatch
from backend.app.graph.matching_graph import matching_agent

router = APIRouter()

class MatchRequest(BaseModel):
    candidate_id: UUID
    job_id: UUID

class MatchResponse(BaseModel):
    candidate_id: UUID
    job_id: UUID
    score: float
    strengths: List[str]
    gaps: List[str]
    explanation: str
    computed_at: str

@router.post("/", response_model=MatchResponse)
def compute_match(request: MatchRequest, db: Session = Depends(get_db)):
    """
    Compute compatibility score between a candidate and a job.
    Uses cached result if available.
    """
    # Check cache
    cached_match = db.query(CandidateJobMatch).filter(
        CandidateJobMatch.candidate_id == request.candidate_id,
        CandidateJobMatch.job_id == request.job_id
    ).first()
    
    if cached_match:
        return {
            "candidate_id": cached_match.candidate_id,
            "job_id": cached_match.job_id,
            "score": cached_match.score,
            "strengths": cached_match.strengths or [],
            "gaps": cached_match.gaps or [],
            "explanation": cached_match.explanation or "",
            "computed_at": str(cached_match.updated_at)
        }
        
    # If not cached, run matching agent
    try:
        initial_state = {
            "candidate_id": request.candidate_id,
            "job_id": request.job_id
        }
        final_state = matching_agent.invoke(initial_state)
        
        # Save to cache
        new_match = CandidateJobMatch(
            candidate_id=request.candidate_id,
            job_id=request.job_id,
            score=final_state.get("final_score", 0.0),
            strengths=final_state.get("strengths", []),
            gaps=final_state.get("gaps", []),
            explanation=final_state.get("explanation", "")
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        
        return {
            "candidate_id": new_match.candidate_id,
            "job_id": new_match.job_id,
            "score": new_match.score,
            "strengths": new_match.strengths,
            "gaps": new_match.gaps,
            "explanation": new_match.explanation,
            "computed_at": str(new_match.updated_at)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing match: {str(e)}")


@router.get("/candidate/{candidate_id}", response_model=List[MatchResponse])
def get_candidate_matches(candidate_id: UUID, db: Session = Depends(get_db)):
    """
    Get all pre-computed matches for a specific candidate.
    """
    matches = db.query(CandidateJobMatch).filter(CandidateJobMatch.candidate_id == candidate_id).order_by(CandidateJobMatch.score.desc()).all()
    
    return [
        {
            "candidate_id": match.candidate_id,
            "job_id": match.job_id,
            "score": match.score,
            "strengths": match.strengths or [],
            "gaps": match.gaps or [],
            "explanation": match.explanation or "",
            "computed_at": str(match.updated_at)
        }
        for match in matches
    ]

@router.get("/job/{job_id}", response_model=List[MatchResponse])
def get_job_matches(job_id: UUID, db: Session = Depends(get_db)):
    """
    Get all pre-computed matches for a specific job.
    """
    matches = db.query(CandidateJobMatch).filter(CandidateJobMatch.job_id == job_id).order_by(CandidateJobMatch.score.desc()).all()
    
    return [
        {
            "candidate_id": match.candidate_id,
            "job_id": match.job_id,
            "score": match.score,
            "strengths": match.strengths or [],
            "gaps": match.gaps or [],
            "explanation": match.explanation or "",
            "computed_at": str(match.updated_at)
        }
        for match in matches
    ]
