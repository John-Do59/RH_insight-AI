from backend.app.rag.vector_store import get_vector_store
from backend.app.utils.logger import logger

from backend.app.core.monitoring import profile_async

@profile_async("RAG Agent")
async def rag_agent(state):
    """
    Retrieves relevant documents from the vector store based on the question.
    """
    question = state["question"]
    logger.info(f"RAG Agent searching for: {question}")
    
    try:
        vector_store = get_vector_store()
        # Retrieve top 5 relevant chunks for better precision
        docs = vector_store.similarity_search(question, k=5)
        doc_contents = [doc.page_content for doc in docs]
        
        return {
            "documents": doc_contents,
            "agent_sources": state.get("agent_sources", []) + ["rag"]
        }
    except Exception as e:
        logger.error(f"Error in RAG agent: {e}")
        return {"documents": []}

