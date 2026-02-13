from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns an instance of HuggingFace embeddings.
    Uses a multilingual model for proper French language support.
    """
    return HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

