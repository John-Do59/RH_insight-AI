from typing import List, Optional
import uuid
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from backend.app.models.base import Base

class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True)
    level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 1-5
    
    skill: Mapped["Skill"] = relationship(back_populates="candidate_associations")
    candidate: Mapped["Candidate"] = relationship(back_populates="skill_associations")

class JobSkill(Base):
    __tablename__ = "job_skills"
    
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True)
    level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 1-5 expected
    is_required: Mapped[bool] = mapped_column(default=True)
    
    skill: Mapped["Skill"] = relationship(back_populates="job_associations")
    job: Mapped["Job"] = relationship(back_populates="skill_associations")

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    category: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    candidate_associations: Mapped[List["CandidateSkill"]] = relationship(back_populates="skill", cascade="all, delete-orphan")
    job_associations: Mapped[List["JobSkill"]] = relationship(back_populates="skill", cascade="all, delete-orphan")
