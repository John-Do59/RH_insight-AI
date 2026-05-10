from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.chat import ChatRequest, ChatResponse
# Assuming the graph is already set up and can be imported here:
from backend.app.graph.graph import app as agent_graph
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """
    Endpoint principal du chat de l'IA RH Insight.
    Prend une question en entrée et la fait passer par le graphe multi-agents (LangGraph).
    """
    try:
        initial_state = {
            "question": request.question,
            "messages": [{"role": "user", "content": request.question}],
            "documents": [],
            "sql_data": [],
            "sql_query": "",
            "github_data": [],
            "agent_sources": [],
            "intent": "general",
            "response": ""
        }
        
        # Async execution of the LangGraph workflow
        result = await agent_graph.ainvoke(initial_state)
        
        return ChatResponse(
            response=result.get("response", "Erreur : aucune réponse générée."),
            intent=result.get("intent", "unknown"),
            sources=result.get("agent_sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
