from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

from fastapi.responses import StreamingResponse
import json

@router.post("/")
async def chat_endpoint(
    request: ChatRequest, 
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint principal du chat avec Streaming.
    """
    async def stream_tokens():
        async for token in chat_service.process_question(
            question=request.question,
            history=request.history
        ):
            # On envoie du JSON ou du texte brut. Pour simplifier le frontend, texte brut.
            yield token

    return StreamingResponse(stream_tokens(), media_type="text/event-stream")
