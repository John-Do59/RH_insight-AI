from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.router import router
from app.agents.intent_agent import classify_intent
from app.agents.rag_agent import rag_agent
from app.agents.sql_agent import sql_agent
from app.agents.github_agent import github_agent
from app.agents.response_agent import response_agent


def create_graph():
    """
    Assembles the LangGraph workflow.
    
    Flow:
        User Input → Intent Detection → Router
        ├── rag → RAG Agent → Response Agent → END
        ├── sql → SQL Agent → Response Agent → END
        ├── github → GitHub Agent → Response Agent → END
        ├── hybrid → SQL Agent → RAG Agent → GitHub Agent → Response Agent → END
        └── general → Response Agent → END
    """
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("intent", classify_intent)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("sql", sql_agent)
    workflow.add_node("github", github_agent)
    workflow.add_node("response", response_agent)
    
    # Set Entry Point
    workflow.set_entry_point("intent")
    
    # Intent Agent routing
    workflow.add_conditional_edges(
        "intent",
        router,
        {
            "rag": "rag",
            "sql": "sql",
            "github": "github",
            "response": "response"
        }
    )
    
    # Direct Edges (Join)
    workflow.add_edge("rag", "response")
    workflow.add_edge("sql", "response")
    workflow.add_edge("github", "response")
    workflow.add_edge("response", END)
    
    return workflow.compile()



# Global app instance
app = create_graph()

