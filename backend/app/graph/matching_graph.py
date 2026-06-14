from langgraph.graph import StateGraph, END
from backend.app.graph.matching_state import MatchingState
from backend.app.graph.matching_nodes import (
    load_data_node,
    vector_retrieval_node,
    skill_comparison_node,
    reasoning_node,
    scoring_node
)

def create_matching_graph():
    """
    Assembles the LangGraph workflow for the Matching Agent.
    
    Flow:
        Load Data -> Vector Retrieval -> Skill Comparison -> Reasoning (LLM) -> Scoring -> END
    """
    workflow = StateGraph(MatchingState)
    
    # Add Nodes
    workflow.add_node("load_data", load_data_node)
    workflow.add_node("vector_retrieval", vector_retrieval_node)
    workflow.add_node("skill_comparison", skill_comparison_node)
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("scoring", scoring_node)
    
    # Set Entry Point
    workflow.set_entry_point("load_data")
    
    # Sequential Pipeline
    workflow.add_edge("load_data", "vector_retrieval")
    workflow.add_edge("vector_retrieval", "skill_comparison")
    workflow.add_edge("skill_comparison", "reasoning")
    workflow.add_edge("reasoning", "scoring")
    workflow.add_edge("scoring", END)
    
    return workflow.compile()

# Global matching agent instance
matching_agent = create_matching_graph()
