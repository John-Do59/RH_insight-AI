from typing import List, Optional
from sqlalchemy import String, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from backend.app.models.base import Base, BaseModelMixin

class Candidate(Base, BaseModelMixin):
    __tablename__ = "candidates"

    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # New parsing fields
    education: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    experiences: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    certifications: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    languages: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Global embedding for the candidate
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)

    # Relationships
    skill_associations: Mapped[List["CandidateSkill"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")  # noqa: F821
    embeddings: Mapped[List["CandidateEmbedding"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")  # noqa: F821
    job_matches: Mapped[List["CandidateJobMatch"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")  # noqa: F821
    github_profile: Mapped[Optional["GithubProfile"]] = relationship(back_populates="candidate", uselist=False, cascade="all, delete-orphan")  # noqa: F821
