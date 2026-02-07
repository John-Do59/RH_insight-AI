from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    """
    Splits text into chunks for the RAG system.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_text(text)
