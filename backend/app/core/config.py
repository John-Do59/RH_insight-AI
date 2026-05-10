import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RH Insight AI"
    
    # Defaults to SQLite if not provided, allowing for easy testing before Postgres is up
    DATABASE_URL: str = os.getenv("POSTGRES_URL", "sqlite:///./rh_insight.db")
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
