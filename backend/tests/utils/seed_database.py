import json
import uuid
from backend.app.database.session import SessionLocal, engine
from backend.app.models.base import Base
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import Skill, CandidateSkill, JobSkill
from backend.tests.utils.mock_embeddings import generate_mock_embedding

def seed_db():
    print("Resetting test database...")
    # Be very careful: only do this in testing.
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(CandidateSkill).delete()
        db.query(JobSkill).delete()
        db.query(Candidate).delete()
        db.query(Job).delete()
        db.query(Skill).delete()
        
        print("Injecting Skills...")
        skills = ["Python", "Docker", "FastAPI", "Airflow", "Kubernetes", "SQL", "ML", "NLP"]
        skill_objs = {}
        for s in skills:
            skill_obj = Skill(id=uuid.uuid4(), name=s, category="Tech")
            db.add(skill_obj)
            skill_objs[s] = skill_obj
        db.commit()

        print("Injecting Candidates...")
        c1 = Candidate(
            id=uuid.uuid4(), title="Data Engineer Python", experience_years=4, 
            summary="Data Eng with Python and SQL", embedding=generate_mock_embedding()
        )
        c2 = Candidate(
            id=uuid.uuid4(), title="Fullstack JS", experience_years=3, 
            summary="React and Node.js", embedding=generate_mock_embedding()
        )
        c3 = Candidate(
            id=uuid.uuid4(), title="Backend FastAPI", experience_years=5, 
            summary="FastAPI expert", embedding=generate_mock_embedding()
        )
        db.add_all([c1, c2, c3])
        db.commit()

        print("Injecting Jobs...")
        j1 = Job(
            id=uuid.uuid4(), title="Data Engineer", description="Need Python and Airflow", 
            embedding=generate_mock_embedding()
        )
        j2 = Job(
            id=uuid.uuid4(), title="Backend Engineer", description="Need FastAPI and Docker", 
            embedding=generate_mock_embedding()
        )
        db.add_all([j1, j2])
        db.commit()

        print("Linking Skills...")
        db.add(CandidateSkill(candidate_id=c1.id, skill_id=skill_objs["Python"].id, level=4))
        db.add(CandidateSkill(candidate_id=c1.id, skill_id=skill_objs["SQL"].id, level=4))
        db.add(CandidateSkill(candidate_id=c3.id, skill_id=skill_objs["FastAPI"].id, level=5))
        db.add(CandidateSkill(candidate_id=c3.id, skill_id=skill_objs["Python"].id, level=4))
        
        db.add(JobSkill(job_id=j1.id, skill_id=skill_objs["Python"].id, level=3))
        db.add(JobSkill(job_id=j1.id, skill_id=skill_objs["Airflow"].id, level=3))
        db.add(JobSkill(job_id=j2.id, skill_id=skill_objs["FastAPI"].id, level=4))
        db.add(JobSkill(job_id=j2.id, skill_id=skill_objs["Docker"].id, level=3))
        
        db.commit()
        print("Database seeded successfully!")
        
        return c1.id, j1.id # Return some ids to be used in tests if needed

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
