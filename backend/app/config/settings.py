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

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "John-Do59")

# Jobs (Phase Jobs)
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
FRANCE_TRAVAIL_CLIENT_ID = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
FRANCE_TRAVAIL_CLIENT_SECRET = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

