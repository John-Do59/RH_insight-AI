import uuid
from typing import Optional
from sqlalchemy import ForeignKey, Float, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from backend.app.models.base import Base, BaseModelMixin

class CandidateJobMatch(Base, BaseModelMixin):
    __tablename__ = "candidate_job_matches"

    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), index=True)
    
    score: Mapped[float] = mapped_column(Float) # 0-100
    strengths: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    gaps: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="job_matches")
    job: Mapped["Job"] = relationship(back_populates="candidate_matches")

    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job_match"),
    )
