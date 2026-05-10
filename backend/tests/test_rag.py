import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.app.agents.rag_agent import rag_agent

@pytest.mark.asyncio
async def test_rag_agent_retrieval():
    # Mock state
    state = {"question": "Quelle est l'expérience de Amaury ?", "agent_sources": []}
    
    # Mock vector store
    mock_doc = MagicMock()
    mock_doc.page_content = "Amaury a 5 ans d'expérience en IA."
    
    mock_vector_store = MagicMock()
    mock_vector_store.asimilarity_search = AsyncMock(return_value=[mock_doc])
    
    # Mock get_vector_store
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.app.agents.rag_agent.get_vector_store", lambda: mock_vector_store)
        
        result = await rag_agent(state)
        
        assert "documents" in result
        assert len(result["documents"]) == 1
        assert "5 ans d'expérience" in result["documents"][0]
        assert "rag" in result["agent_sources"]

@pytest.mark.asyncio
async def test_rag_agent_error_handling():
    state = {"question": "Error test", "agent_sources": []}
    
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.app.agents.rag_agent.get_vector_store", lambda: MagicMock(asimilarity_search=AsyncMock(side_effect=Exception("DB Error"))))
        
        result = await rag_agent(state)
        assert result["documents"] == []
