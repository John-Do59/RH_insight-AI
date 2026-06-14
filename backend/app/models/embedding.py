import uuid
from typing import Optional
from sqlalchemy import ForeignKey, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from backend.app.models.base import Base, BaseModelMixin

class CandidateEmbedding(Base, BaseModelMixin):
    __tablename__ = "candidate_embeddings"

    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), index=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="embeddings")

    __table_args__ = (
        Index(
            "idx_candidate_embeddings_hnsw", 
            "embedding", 
            postgresql_using="hnsw", 
            postgresql_with={"m": 16, "ef_construction": 64}, 
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )


class JobEmbedding(Base, BaseModelMixin):
    __tablename__ = "job_embeddings"

    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), index=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, nullable=True)

    job: Mapped["Job"] = relationship(back_populates="embeddings")

    __table_args__ = (
        Index(
            "idx_job_embeddings_hnsw", 
            "embedding", 
            postgresql_using="hnsw", 
            postgresql_with={"m": 16, "ef_construction": 64}, 
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )
