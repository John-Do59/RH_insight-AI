from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL, 
    # Use connect_args for SQLite specifically to avoid threading issues
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is now imported from backend.app.models

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
