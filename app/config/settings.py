import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-r1:7b")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL_DB_PATH = os.path.join(BASE_DIR, os.getenv("SQL_DB_PATH", "data/sql/recruiter.db"))
VECTOR_DB_PATH = os.path.join(BASE_DIR, os.getenv("VECTOR_DB_PATH", "data/vector_store/"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
