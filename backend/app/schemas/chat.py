from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    question: str = Field(..., description="The user's question or prompt")
    history: Optional[List[ChatMessage]] = Field(default_factory=list, description="Previous conversation history")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI's generated response")
    intent: str = Field(..., description="The detected intent of the user's question")
    sources: List[str] = Field(default_factory=list, description="Agents or data sources used (e.g., RAG, SQL, GitHub)")
