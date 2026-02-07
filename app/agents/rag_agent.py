from app.rag.vector_store import get_vector_store
from app.utils.logger import logger

def rag_agent(state):
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
        
        return {"documents": doc_contents}
    except Exception as e:
        logger.error(f"Error in RAG agent: {e}")
        return {"documents": []}
