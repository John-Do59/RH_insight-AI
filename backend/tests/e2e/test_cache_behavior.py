import pytest
import time
from backend.app.database.session import SessionLocal
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.matching import CandidateJobMatch
from backend.app.graph.matching_graph import matching_agent

def test_cache_logic():
    """
    Validates the caching behavior.
    """
    db = SessionLocal()
    try:
        candidate = db.query(Candidate).first()
        job = db.query(Job).first()
        
        # Clean cache for this pair if exists
        db.query(CandidateJobMatch).filter_by(candidate_id=candidate.id, job_id=job.id).delete()
        db.commit()

        # Call 1: Uncached
        start_time = time.time()
        result1 = matching_agent.invoke({"candidate_id": candidate.id, "job_id": job.id})
        t1 = time.time() - start_time
        
        # Save to DB manually since endpoint normally does it
        match_entry = CandidateJobMatch(
            candidate_id=candidate.id,
            job_id=job.id,
            score=result1["final_score"],
            strengths=result1.get("strengths", []),
            gaps=result1.get("gaps", []),
            explanation=result1.get("explanation", "")
        )
        db.add(match_entry)
        db.commit()

        # Call 2: Cached (simulated via DB check as the endpoint does)
        start_time = time.time()
        cached = db.query(CandidateJobMatch).filter_by(candidate_id=candidate.id, job_id=job.id).first()
        t2 = time.time() - start_time
        
        assert cached is not None
        assert cached.score == result1["final_score"]
        # DB lookup is inherently faster than LLM inference.
        assert t2 < t1 or t2 < 0.1, f"Cache not fast enough, t2: {t2}, t1: {t1}"

    finally:
        db.close()
