"""
Router — Détection d'intention et routage vers les agents spécialisés.

Extrait la logique de routage de graph.py pour une meilleure modularité.
"""

from app.config.constants import INTENT_RAG, INTENT_SQL


def router(state: dict) -> str:
    """
    Determines which node to visit next based on the detected intent.

    Args:
        state: The current LangGraph agent state containing the 'intent' key.

    Returns:
        The name of the next node to route to ('rag', 'sql', or 'response').
    """
    intent = state.get("intent", "general")

    if intent == "hybrid":
        return "sql"  # Route to SQL first, then SQL will route to RAG
    elif intent == INTENT_RAG:
        return "rag"
    elif intent == INTENT_SQL:
        return "sql"
    else:
        return "response"


def sql_router(state: dict) -> str:
    """
    Post-SQL routing: determines if the flow continues to RAG (hybrid)
    or goes directly to response.

    Args:
        state: The current LangGraph agent state.

    Returns:
        'rag' if intent is hybrid, 'response' otherwise.
    """
    if state.get("intent") == "hybrid":
        return "rag"
    return "response"
