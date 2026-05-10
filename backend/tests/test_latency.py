import pytest
import time
from unittest.mock import AsyncMock, patch, MagicMock
from backend.app.services.chat_service import ChatService

@pytest.mark.asyncio
async def test_full_chat_latency_threshold():
    """
    Vérifie que la latence globale reste sous un seuil acceptable (hors LLM).
    """
    question = "Quels sont les candidats en IA ?"
    
    # Mock du graphe d'agents
    mock_result = {
        "final_prompt": "Prompt simulé",
        "intent": "general",
        "agent_sources": ["intent", "rag"]
    }
    
    # Mock du stream LLM
    async def mock_stream(*args, **kwargs):
        yield MagicMock(content="Réponse")
        yield MagicMock(content=" simulée")

    mock_llm = MagicMock()
    mock_llm.astream = mock_stream
    
    with patch("backend.app.services.chat_service.agent_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.return_value = mock_result
        
        with patch("backend.app.services.chat_service.get_fast_llm", return_value=mock_llm):
            start_time = time.perf_counter()
            tokens = []
            async for token in ChatService.process_question(question):
                tokens.append(token)
            end_time = time.perf_counter()
            
            latency = end_time - start_time
            print(f"\nPipeline Latency (Mocked LLM): {latency:.4f}s")
            
            assert latency < 0.2, f"Latence trop élevée: {latency:.4f}s"
            assert "".join(tokens) == "Réponse simulée"

@pytest.mark.asyncio
async def test_agent_orchestration_overhead():
    """
    Mesure l'overhead de LangGraph en isolant les agents.
    On patch ChatOllama pour éviter tout appel LLM réel.
    """
    from backend.app.graph.graph import app as graph_app
    
    mock_llm_response = MagicMock()
    mock_llm_response.content = "general" # Pour classify_intent
    
    with patch("langchain_ollama.ChatOllama.ainvoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_llm_response
        
        start_time = time.perf_counter()
        await graph_app.ainvoke({"question": "hi", "messages": [], "agent_sources": []})
        end_time = time.perf_counter()
        
        latency = end_time - start_time
        print(f"\nGraph Orchestration Overhead (Mocked LLM): {latency:.4f}s")
        assert latency < 1.0 # Premier appel peut être lent
