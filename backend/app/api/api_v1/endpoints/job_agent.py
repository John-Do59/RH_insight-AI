from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from typing import List, Optional
import uuid

from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.skill import CandidateSkill, Skill
from backend.app.graph.job_parser import parse_job_description
from backend.app.graph.matching_graph import matching_agent
from backend.app.models.job import Job

router = APIRouter()

class AnalyzeRequest(BaseModel):
    message: str

class CandidateResult(BaseModel):
    id: str
    name: str
    score: float
    strengths: List[str]
    gaps: List[str]

class AnalyzeResponse(BaseModel):
    job: dict
    candidates: List[CandidateResult]

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    1. Parse job using LLM
    2. Search Candidates (mocking vector search here to avoid complex DB setup in prototype)
    3. Rank Candidates via Matching Engine
    """
    # 1. Parse Job
    parsed_job = parse_job_description(request.message)
    
    # Save a temporary job in memory/DB to use the matching agent
    temp_job_id = uuid.uuid4()
    
    # 2. Retrieve Candidates (Basic filter simulating Vector/SQL search)
    # Get top 20 candidates. In a real system: ORDER BY embedding <=> job_embedding LIMIT 20
    candidates = db.query(Candidate).limit(20).all()
    
    results = []
    
    # 3. Ranking Engine
    for c in candidates:
        # We manually craft the state since the job is not actually stored yet to avoid DB bloat
        # Or we can insert it temporarily. Let's create a temporary job state
        
        # Load candidate skills
        c_skills = db.query(Skill.name).join(CandidateSkill).filter(CandidateSkill.candidate_id == c.id).all()
        c_skills_list = [s[0] for s in c_skills]
        
        state = {
            "candidate_id": c.id,
            "job_id": temp_job_id,
            "candidate_data": {
                "id": c.id,
                "title": c.title,
                "experience_years": c.experience_years,
                "embedding": c.embedding, # Would be compared against job embedding
                "summary": c.summary,
                "github": None
            },
            "job_data": {
                "id": temp_job_id,
                "title": parsed_job.get("title", ""),
                "description": request.message,
                "embedding": None # Mock
            },
            "candidate_skills": c_skills_list,
            "job_skills": parsed_job.get("skills", []),
            "vector_score": 50.0, # Mocked
            "github_score": 0.0
        }
        
        # Skip load_data_node, start at skill_comparison
        # Since we modified the standard flow, we will manually run the nodes for this agent endpoint
        from backend.app.graph.matching_nodes import skill_comparison_node, reasoning_node, scoring_node
        
        state = skill_comparison_node(state)
        state = reasoning_node(state)
        state = scoring_node(state)
        
        name = f"{c.first_name or ''} {c.last_name or ''}".strip()
        if not name:
            name = f"Candidat {str(c.id)[:8]}"
            
        results.append(CandidateResult(
            id=str(c.id),
            name=name,
            score=state["final_score"],
            strengths=state.get("strengths", []),
            gaps=state.get("gaps", [])
        ))
        
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    
    return AnalyzeResponse(
        job=parsed_job,
        candidates=results[:5] # Return top 5
    )
