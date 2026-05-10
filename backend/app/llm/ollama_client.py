from langchain_ollama import ChatOllama
from app.config.settings import OLLAMA_BASE_URL, LLM_MODEL

_reasoning_llm = None
_fast_llm = None

def get_llm():
    """
    Returns the reasoning LLM (DeepSeek R1).
    """
    global _reasoning_llm
    if _reasoning_llm is None:
        _reasoning_llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=LLM_MODEL,
            temperature=0
        )
    return _reasoning_llm

def get_fast_llm():
    """
    Returns a fast, lightweight LLM (Llama 3.2 1B) for intent/SQL tasks.
    """
    global _fast_llm
    if _fast_llm is None:
        _fast_llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model="llama3.2:1b",
            temperature=0
        )
    return _fast_llm

