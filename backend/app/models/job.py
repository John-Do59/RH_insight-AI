from typing import List, Optional
from sqlalchemy import String, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from backend.app.models.base import Base, BaseModelMixin

class Job(Base, BaseModelMixin):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String, index=True)
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contract_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # New parsing fields
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    education_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    certifications: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    languages: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Global embedding for the job
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)

    # Relationships
    skill_associations: Mapped[List["JobSkill"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    embeddings: Mapped[List["JobEmbedding"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    candidate_matches: Mapped[List["CandidateJobMatch"]] = relationship(back_populates="job", cascade="all, delete-orphan")
