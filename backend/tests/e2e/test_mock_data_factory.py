import pytest
from backend.app.database.session import SessionLocal
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import Skill

def test_mock_data_generation():
    """
    Validates that the database seeding successfully injected candidates, jobs, and skills.
    """
    db = SessionLocal()
    try:
        candidates = db.query(Candidate).all()
        jobs = db.query(Job).all()
        skills = db.query(Skill).all()

        assert len(candidates) > 0, "No candidates seeded"
        assert len(jobs) > 0, "No jobs seeded"
        assert len(skills) > 0, "No skills seeded"
        
        # Verify specific fields
        c1 = candidates[0]
        assert c1.title is not None
        assert len(c1.embedding) == 768

    finally:
        db.close()
