import uuid
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from backend.app.models.base import Base, BaseModelMixin

class GithubProfile(Base, BaseModelMixin):
    __tablename__ = "github_profiles"

    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), unique=True)  # noqa: F821
    username: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    repositories_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    languages: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    contribution_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="github_profile")  # noqa: F821
