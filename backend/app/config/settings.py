import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL_REASONING = os.getenv("LLM_MODEL_REASONING", "deepseek-r1:7b")
LLM_MODEL_STANDARD = os.getenv("LLM_MODEL_STANDARD", "qwen3.5:4b")

# Embeddings
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL_DB_PATH = os.path.join(BASE_DIR, os.getenv("SQL_DB_PATH", "data/sql/recruiter.db"))
VECTOR_DB_PATH = os.path.join(BASE_DIR, os.getenv("VECTOR_DB_PATH", "data/vector_store/"))

# Database PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") # Obligatoire en prod
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rh_insight")

if not POSTGRES_PASSWORD and os.getenv("ENV") == "prod":
    raise ValueError("POSTGRES_PASSWORD must be set in production")

# Build DATABASE_URL safely
if POSTGRES_PASSWORD:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
else:
    # Fallback for development/testing if password not provided
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rh_insight.db")

ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Security
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY and os.getenv("ENV") == "prod":
    raise ValueError("SECRET_KEY must be set in production environment")

# Fallback for local dev only
if not SECRET_KEY:
    SECRET_KEY = "dev_secret_key_not_for_production"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 week

# CORS
CORS_ORIGINS_STR = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8000")
BACKEND_CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(",") if origin.strip()]

