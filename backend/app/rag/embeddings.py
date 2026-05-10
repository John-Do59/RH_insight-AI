from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from backend.app.config.settings import EMBEDDING_MODEL, EMBEDDING_PROVIDER, OLLAMA_BASE_URL

def get_embeddings():
    """
    Returns an instance of embeddings based on the configuration.
    Defaults to Qwen3 via Ollama for performance on Mac M4.
    """
    if EMBEDDING_PROVIDER == "ollama":
        return OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
    else:
        # Fallback to HuggingFace if requested (legacy or other models)
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

