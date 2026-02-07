from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    """
    Represents the state of the LangGraph agent.
    """
    # L'entrée de l'utilisateur
    question: str
    
    # Intention détectée (rag, sql, general)
    intent: str
    
    # Documents récupérés par le RAG
    documents: List[str]
    
    # Données récupérées par SQL
    sql_data: Any
    
    # Requête SQL générée (optionnel, pour debug)
    sql_query: str
    
    # Réponse finale générée
    response: str
    
    # Historique des messages (optionnel pour l'instant)
    messages: Annotated[List[Dict[str, str]], operator.add]
