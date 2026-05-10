"""
Router — Détection d'intention et routage vers les agents spécialisés.

Extrait la logique de routage de graph.py pour une meilleure modularité.
"""

from app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GITHUB


from typing import List, Union

def router(state: dict) -> Union[str, List[str]]:
    """
    Determines which node(s) to visit next based on the detected intent.
    Supports parallel execution (fan-out) for hybrid intent.
    """
    intent = state.get("intent", "general")

    if intent == "hybrid":
        # Fan-out: Parallel execution of all search agents
        return ["sql", "rag", "github"]
    elif intent == INTENT_RAG:
        return "rag"
    elif intent == INTENT_SQL:
        return "sql"
    elif intent == INTENT_GITHUB:
        return "github"
    else:
        return "response"

