import pytest
from backend.app.database.session import SessionLocal
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.graph.matching_graph import matching_agent

def test_consistency():
    """
    Validates that multiple runs with the same input yield stable results.
    """
    db = SessionLocal()
    try:
        candidate = db.query(Candidate).first()
        job = db.query(Job).first()
        
        state = {"candidate_id": candidate.id, "job_id": job.id}
        
        # Run twice
        r1 = matching_agent.invoke(state)
        r2 = matching_agent.invoke(state)
        
        # Check variance
        s1 = r1["final_score"]
        s2 = r2["final_score"]
        
        # Allowed variance < 2% (or absolute < 2.0)
        variance = abs(s1 - s2)
        assert variance <= 2.0, f"Score variance too high: {s1} vs {s2}"
        
        # Structure identical
        assert set(r1["strengths"]) == set(r2["strengths"])
        assert set(r1["gaps"]) == set(r2["gaps"])

    finally:
        db.close()
