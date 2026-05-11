import os
import shutil
import sys
from loguru import logger

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.config.settings import VECTOR_DB_PATH
from backend.app.rag.embeddings import get_embeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def reindex():
    logger.info(f"Starting vector store re-initialization (Model: Qwen3-0.6B)")
    
    # 1. Purge existing vector store
    if os.path.exists(VECTOR_DB_PATH):
        logger.warning(f"Purging existing vector store at {VECTOR_DB_PATH}")
        shutil.rmtree(VECTOR_DB_PATH)
    
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    
    # 2. Prepare embeddings and text splitter
    embeddings = get_embeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # 3. Load sample documents
    # Note: In a real app, we'd loop through a 'data/docs' directory.
    # Here we'll re-ingest the candidate summary for testing.
    sample_docs = [
        """Amaury Rammanat est un Développeur IA en formation chez Simplon. 
        Son profil est orienté vers le Machine Learning, l'IA générative et l'IA agentique. 
        Il a 15 ans d'expérience professionnelle et recherche une alternance pour septembre 2026. 
        Ses compétences clés incluent Python, SQL, LangChain, RAG et Streamlit.""",
        
        """Le projet RH Insight AI est un outil d'analyse de CV et d'aide au recrutement. 
        Il utilise des technologies comme LangGraph pour l'orchestration des agents, 
        ChromaDB pour le stockage vectoriel et des modèles comme Qwen3 et DeepSeek pour le raisonnement."""
    ]
    
    logger.info(f"Processing {len(sample_docs)} sample documents...")
    chunks = text_splitter.create_documents(sample_docs)
    
    # 4. Create new vector store
    logger.info("Generating embeddings and storing in ChromaDB...")
    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        logger.success("Vector store successfully re-indexed with dimension 1024!")
    except Exception as e:
        logger.error(f"Failed to create vector store: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    reindex()
