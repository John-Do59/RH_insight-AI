from backend.app.database.session import engine, SessionLocal
from sqlalchemy import text
from backend.app.models.base import Base
from backend.app.models.user import User
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import Skill
from backend.app.models.matching import CandidateJobMatch
from backend.app.models.github import GithubProfile
from backend.app.core.security import get_password_hash

print("Creating tables...")
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()
Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(User).filter_by(email="rammanatamaury@gmail.com").first():
    user = User(
        email="rammanatamaury@gmail.com",
        hashed_password=get_password_hash("password"),
        full_name="Amaury",
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    print("User created.")
else:
    print("User already exists.")
db.close()
print("Done.")
