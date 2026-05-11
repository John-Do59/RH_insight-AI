from langchain_ollama import ChatOllama
from backend.app.config.settings import OLLAMA_BASE_URL, LLM_MODEL_REASONING, LLM_MODEL_STANDARD

_reasoning_llm = None
_standard_llm = None

def get_llm():
    """
    Returns the reasoning LLM (DeepSeek R1) for complex reasoning tasks.
    """
    global _reasoning_llm
    if _reasoning_llm is None:
        _reasoning_llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=LLM_MODEL_REASONING,
            temperature=0,
            num_predict=1000,
            keep_alive="24h" # Garde le modèle en mémoire GPU
        )
    return _reasoning_llm

def get_fast_llm():
    """
    Returns the standard/fast LLM (Qwen 3 4B Instruct) for standard tasks.
    """
    global _standard_llm
    if _standard_llm is None:
        _standard_llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=LLM_MODEL_STANDARD,
            temperature=0,
            num_ctx=2048,
            num_predict=256,
            keep_alive="24h"
        )
    return _standard_llm
