from typing import List, Dict, Any, Optional, AsyncGenerator
from backend.app.graph.graph import app as agent_graph
from backend.app.schemas.chat import ChatMessage
from backend.app.core.monitoring import profile_async
from backend.app.llm.ollama_client import get_llm, get_fast_llm
from backend.app.utils.logger import logger

class ChatService:
    @staticmethod
    @profile_async("Global Chat Request")
    async def process_question(question: str, history: List[ChatMessage] = None) -> AsyncGenerator[str, None]:
        """
        Process a user question with model routing and yield tokens for streaming.
        """
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
            "response": "",
            "final_prompt": ""
        }
        
        # 1. Run the graph to get the final prompt (context assembly)
        result = await agent_graph.ainvoke(initial_state)
        final_prompt = result.get("final_prompt")
        intent = result.get("intent", "general")
        
        if not final_prompt:
            yield "Erreur : impossible de générer le prompt."
            return

        # 2. Model Routing
        # Use Llama 1B for general questions, DeepSeek-R1 for actual CV analysis
        if intent == "general":
            llm = get_fast_llm()
            logger.info("Routing to Fast LLM (Llama 1B) for general intent")
        else:
            llm = get_llm()
            logger.info(f"Routing to Reasoning LLM (DeepSeek-R1) for {intent} intent")

        # 3. Stream the LLM response
        async for chunk in llm.astream(final_prompt):
            if chunk.content:
                yield chunk.content

chat_service = ChatService()
