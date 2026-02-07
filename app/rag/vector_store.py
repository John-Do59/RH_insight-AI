from langchain_chroma import Chroma
from app.rag.embeddings import get_embeddings
from app.config.settings import VECTOR_DB_PATH

def get_vector_store():
    """
    Returns the Chroma vector store instance.
    """
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

def add_texts_to_vector_store(texts, metadatas=None):
    """
    Adds text chunks to the vector store.
    """
    vector_store = get_vector_store()
    vector_store.add_texts(texts=texts, metadatas=metadatas)
