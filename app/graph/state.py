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
    
    # Données récupérées par GitHub
    github_data: Any
    
    # Données des offres d'emploi (Phase Jobs)
    job_results: List[Dict[str, Any]]
    
    # Trace des agents ayant contribué à la réponse
    agent_sources: List[str]
    
    # Réponse finale générée
    response: str
    
    # Historique des messages
    messages: Annotated[List[Dict[str, str]], operator.add]
