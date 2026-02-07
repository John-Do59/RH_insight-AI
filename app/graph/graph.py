from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.agents.intent_agent import classify_intent
from app.agents.rag_agent import rag_agent
from app.agents.sql_agent import sql_agent
from app.agents.response_agent import response_agent
from app.config.constants import INTENT_RAG, INTENT_SQL

def router(state):
    """
    Determines which node to visit next based on the intent.
    """
    intent = state["intent"]
    if intent == "hybrid":
        return "sql"  # Route to SQL first, then SQL will route to RAG
    elif intent == INTENT_RAG:
        return "rag"
    elif intent == INTENT_SQL:
        return "sql"
    else:
        return "response"

def create_graph():
    """
    Assembles the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("intent", classify_intent)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("sql", sql_agent)
    workflow.add_node("response", response_agent)
    
    # Set Entry Point
    workflow.set_entry_point("intent")
    
    # Add Conditional Edges
    workflow.add_conditional_edges(
        "intent",
        router,
        {
            "rag": "rag",
            "sql": "sql",
            "response": "response"
        }
    )
    
    # Add logic for Hybrid flow: SQL -> RAG -> Response
    workflow.add_conditional_edges(
        "sql",
        lambda state: "rag" if state.get("intent") == "hybrid" else "response",
        {
            "rag": "rag",
            "response": "response"
        }
    )
    
    # Add Direct Edges
    workflow.add_edge("rag", "response")
    workflow.add_edge("sql", "response")
    workflow.add_edge("response", END)
    
    return workflow.compile()

# Global app instance
app = create_graph()
