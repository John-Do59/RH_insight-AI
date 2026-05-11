import json
import httpx
import time
from typing import List, Dict, Any, Optional, AsyncGenerator
from backend.app.graph.graph import app as agent_graph
from backend.app.schemas.chat import ChatMessage
from backend.app.core.monitoring import profile_async
from backend.app.config.settings import OLLAMA_BASE_URL, LLM_MODEL_STANDARD
from backend.app.utils.logger import logger

class ChatService:
    @staticmethod
    @profile_async("Global Chat Request")
    async def process_question(question: str, history: List[ChatMessage] = None) -> AsyncGenerator[str, None]:
        """
        Process a user question using direct httpx streaming for maximum performance (TTFT < 1s).
        """
        start_time = time.time()
        
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
        
        # 1. Context Assembly (Graph)
        result = await agent_graph.ainvoke(initial_state)
        final_prompt = result.get("final_prompt")
        
        if not final_prompt:
            yield "Erreur : impossible de générer le prompt."
            return

        # 2. Direct HTTPX Streaming to Ollama
        # Bypass LangChain for the response generation to minimize TTFT
        payload = {
            "model": LLM_MODEL_STANDARD,
            "messages": [{"role": "user", "content": final_prompt}],
            "stream": True,
            "think": False,  # Désactive le mode raisonnement interne de Qwen3 (économise RAM + tokens)
            "options": {
                "temperature": 0.2,
                "num_ctx": 2048,
                "num_predict": 512,
                "stop": ["<|im_end|>", "<|endoftext|>"]
            }
        }

        first_token_received = False
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
            async with client.stream(
                "POST", 
                f"{OLLAMA_BASE_URL}/api/chat", 
                json=payload
            ) as response:
                if response.status_code != 200:
                    yield f"Erreur Ollama ({response.status_code})"
                    return

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            
                            if not first_token_received:
                                ttft = (time.time() - start_time) * 1000
                                logger.info(f"[PERF] TTFT: {ttft:.2f}ms")
                                first_token_received = True
                            
                            yield content
                        
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

chat_service = ChatService()
