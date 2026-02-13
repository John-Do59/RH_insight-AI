"""
Router — Détection d'intention et routage vers les agents spécialisés.

Extrait la logique de routage de graph.py pour une meilleure modularité.
"""

from app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GITHUB


def router(state: dict) -> str:
    """
    Determines which node to visit next based on the detected intent.

    Args:
        state: The current LangGraph agent state containing the 'intent' key.

    Returns:
        The name of the next node to route to ('rag', 'sql', 'github', or 'response').
    """
    intent = state.get("intent", "general")

    if intent == "hybrid":
        return "sql"  # Route to SQL first, then SQL will route to RAG
    elif intent == INTENT_RAG:
        return "rag"
    elif intent == INTENT_SQL:
        return "sql"
    elif intent == INTENT_GITHUB:
        return "github"
    else:
        return "response"


def sql_router(state: dict) -> str:
    """
    Post-SQL routing: determines if the flow continues to RAG (hybrid)
    or goes directly to response.
    """
    if state.get("intent") == "hybrid":
        return "rag"
    return "response"


def rag_router(state: dict) -> str:
    """
    Post-RAG routing: determines if the flow continues to GitHub (hybrid)
    or goes directly to response.
    """
    if state.get("intent") == "hybrid":
        return "github"
    return "response"

