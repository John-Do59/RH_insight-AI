from langchain_ollama import ChatOllama
from app.config.settings import OLLAMA_BASE_URL, LLM_MODEL

def get_llm():
    """
    Returns an instance of the ChatOllama client.
    """
    return ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=LLM_MODEL,
        temperature=0
    )
