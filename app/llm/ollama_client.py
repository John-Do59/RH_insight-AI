from langchain_ollama import ChatOllama
from app.config.settings import OLLAMA_BASE_URL, LLM_MODEL

_llm_instance = None

def get_llm():
    """
    Returns a singleton instance of the ChatOllama client.
    Avoids recreating the connection on every agent call.
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=LLM_MODEL,
            temperature=0
        )
    return _llm_instance

