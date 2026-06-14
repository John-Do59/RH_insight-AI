# Import the new common Base
from backend.app.models.base import Base

# Import all models so Alembic can discover them via Base.metadata
from backend.app.models.user import User
from backend.app.models.skill import Skill, CandidateSkill, JobSkill
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.embedding import CandidateEmbedding, JobEmbedding
from backend.app.models.matching import CandidateJobMatch
from backend.app.models.github import GithubProfile

__all__ = [
    "Base",
    "User",
    "Skill",
    "CandidateSkill",
    "JobSkill",
    "Candidate",
    "Job",
    "CandidateEmbedding",
    "JobEmbedding",
    "CandidateJobMatch",
    "GithubProfile",
]
