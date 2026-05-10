import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.app.config.settings import DATABASE_URL, ASYNC_DATABASE_URL

# Sync Engine (for migrations/initialization)
def get_engine():
    return create_engine(DATABASE_URL, echo=False)

# Async Engine (for production chat requests)
def get_async_engine():
    return create_async_engine(ASYNC_DATABASE_URL, echo=False)

async def get_async_session():
    engine = get_async_engine()
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
