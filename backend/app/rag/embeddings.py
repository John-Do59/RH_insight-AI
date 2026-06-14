from langchain_ollama import OllamaEmbeddings
from backend.app.config.settings import EMBEDDING_MODEL, EMBEDDING_PROVIDER, OLLAMA_BASE_URL

from functools import lru_cache


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Returns a cached instance of embeddings based on the configuration.
    Defaults to Qwen3 via Ollama for performance on Mac M4 (and Docker prod).

    EMBEDDING_PROVIDER=ollama  → use Ollama (default, lightweight, no torch)
    EMBEDDING_PROVIDER=huggingface → lazy-import HuggingFaceEmbeddings
        (requires sentence-transformers installed, dev only)
    """
    if EMBEDDING_PROVIDER == "ollama":
        return OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
    else:
        # Lazy import: sentence-transformers/torch are NOT installed in prod image.
        # Set EMBEDDING_PROVIDER=huggingface only in local dev with venv.
        try:
            from langchain_huggingface import HuggingFaceEmbeddings  # noqa: PLC0415
            return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        except ImportError:
            raise RuntimeError(
                "HuggingFace embeddings requested but 'sentence-transformers' is not installed. "
                "Use EMBEDDING_PROVIDER=ollama in production, "
                "or install requirements-dev.txt for local dev."
            )
