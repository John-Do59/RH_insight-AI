import pytest
from backend.app.database.session import SessionLocal
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.graph.matching_graph import matching_agent

def test_pipeline_execution():
    """
    Simulates the end-to-end matching pipeline for a candidate and a job.
    Validates structure, types, and logic consistency.
    """
    db = SessionLocal()
    try:
        candidate = db.query(Candidate).first()
        job = db.query(Job).first()
        
        assert candidate is not None, "Seed data missing candidate"
        assert job is not None, "Seed data missing job"

        # Execute matching agent
        state = {
            "candidate_id": candidate.id,
            "job_id": job.id
        }
        
        result = matching_agent.invoke(state)
        
        # 1. Structure Assertions
        assert "final_score" in result
        assert "strengths" in result
        assert "gaps" in result
        assert "explanation" in result

        # 2. Score Validity
        score = result["final_score"]
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100, f"Score out of bounds: {score}"
        
        # 3. Logic Consistency
        strengths = set(result.get("strengths", []))
        gaps = set(result.get("gaps", []))
        
        intersection = strengths.intersection(gaps)
        assert len(intersection) == 0, f"Gaps and strengths have overlap: {intersection}"

    finally:
        db.close()
