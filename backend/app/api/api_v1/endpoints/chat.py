from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint principal du chat. Nécessite une authentification JWT.
    """
    try:
        result = await chat_service.process_question(
            question=request.question,
            history=request.history
        )
        return ChatResponse(**result)
    except Exception as e:
        # En production, loggez l'erreur réelle ici
        raise HTTPException(status_code=500, detail=str(e))
