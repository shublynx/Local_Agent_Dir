from langchain_ollama import OllamaEmbeddings

# Load once (important for performance)
_embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for each chunk.
    """
    return _embeddings.embed_documents(chunks)
