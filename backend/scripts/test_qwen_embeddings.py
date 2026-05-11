import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.rag.embeddings import get_embeddings
from loguru import logger

def test_qwen_embeddings():
    try:
        logger.info("Initializing Qwen3-0.6B embeddings...")
        embeddings = get_embeddings()
        
        test_text = "Ceci est un test pour les embeddings Qwen3 sur Mac M4."
        logger.info(f"Generating embedding for text: '{test_text}'")
        
        vector = embeddings.embed_query(test_text)
        
        if vector and isinstance(vector, list):
            logger.success(f"Successfully generated embedding!")
            logger.info(f"Vector dimension: {len(vector)}")
            logger.info(f"First 5 elements: {vector[:5]}")
            return True
        else:
            logger.error("Generated vector is empty or invalid.")
            return False
            
    except Exception as e:
        logger.error(f"Error during embedding generation: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_qwen_embeddings()
    sys.exit(0 if success else 1)
