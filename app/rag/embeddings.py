from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns an instance of HuggingFace embeddings.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
