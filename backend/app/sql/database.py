import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.app.config.settings import SQL_DB_PATH

# Sync Engine (for migrations/initialization)
def get_engine():
    os.makedirs(os.path.dirname(SQL_DB_PATH), exist_ok=True)
    db_url = f"sqlite:///{SQL_DB_PATH}"
    return create_engine(db_url, echo=False)

# Async Engine (for production chat requests)
def get_async_engine():
    os.makedirs(os.path.dirname(SQL_DB_PATH), exist_ok=True)
    # Using aiosqlite for async SQLite
    db_url = f"sqlite+aiosqlite:///{SQL_DB_PATH}"
    return create_async_engine(db_url, echo=False)

async def get_async_session():
    engine = get_async_engine()
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
