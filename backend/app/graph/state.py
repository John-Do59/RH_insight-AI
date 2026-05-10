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
    documents: Annotated[List[str], operator.add]
    
    # Données récupérées par GitHub
    github_data: Any
    
    # Données récupérées par le SQL
    sql_data: Annotated[List[Dict[str, Any]], operator.add]
    sql_query: str
    
    # Données des offres d'emploi (Phase Jobs)
    job_results: Annotated[List[Dict[str, Any]], operator.add]
    
    # Trace des agents ayant contribué à la réponse
    agent_sources: Annotated[List[str], operator.add]
    
    # Prompt final pour le streaming
    final_prompt: str
    
    # Réponse finale générée
    response: str
    
    # Historique des messages
    messages: Annotated[List[Dict[str, str]], operator.add]
