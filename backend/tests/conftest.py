import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.database.session import get_db

# Use DATABASE_URL from env (set in CI) or fallback to local Postgres
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rh_user:rh_password@localhost:5432/rh_insight_test"
)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _setup_db():
    """Create tables using the alembic migrations (pgvector-compatible)."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    # Import all models to ensure they are registered on the Base metadata
    from backend.app.models import Base  # noqa: F401
    Base.metadata.create_all(bind=engine)


def _teardown_db():
    from backend.app.models import Base  # noqa: F401
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    _setup_db()
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        _teardown_db()


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
