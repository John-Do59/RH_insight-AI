import numpy as np

def generate_mock_embedding(dim: int = 768) -> list[float]:
    """
    Generate a normalized random embedding vector of the specified dimension.
    Compatible with pgvector.
    """
    vec = np.random.rand(dim)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec.tolist()
    normalized = vec / norm
    return normalized.tolist()
