from typing import List, Dict, Any, Optional
from backend.app.graph.graph import app as agent_graph
from backend.app.schemas.chat import ChatMessage

class ChatService:
    @staticmethod
    async def process_question(question: str, history: List[ChatMessage] = None) -> Dict[str, Any]:
        """
        Process a user question through the multi-agent graph.
        """
        # Convert Pydantic history to dict format for the graph if necessary
        formatted_history = []
        if history:
            for msg in history:
                formatted_history.append({"role": msg.role, "content": msg.content})
        
        initial_state = {
            "question": question,
            "messages": formatted_history + [{"role": "user", "content": question}],
            "documents": [],
            "sql_data": [],
            "sql_query": "",
            "github_data": [],
            "agent_sources": [],
            "intent": "general",
            "response": ""
        }
        
        # Invoke the LangGraph workflow
        # The result state will contain the final response and metadata
        result = await agent_graph.ainvoke(initial_state)
        
        return {
            "response": result.get("response", "Erreur : aucune réponse générée."),
            "intent": result.get("intent", "unknown"),
            "sources": result.get("agent_sources", [])
        }

chat_service = ChatService()
