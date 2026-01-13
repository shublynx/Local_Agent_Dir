from langchain_ollama import OllamaEmbeddings

_embedder = OllamaEmbeddings(model="nomic-embed-text")


def to_pgvector(vec: list[float]) -> str:
    return "[" + ",".join(str(x) for x in vec) + "]"


async def retrieve_context(
    *,
    db,
    user_id: str,
    query: str,
    k: int = 5,
):
    # 1. Embed the query
    query_vector = _embedder.embed_query(query)

    # 2. Convert to pgvector format
    query_vector_pg = to_pgvector(query_vector)

    # 3. Vector similarity search
    rows = await db.fetch(
        """
        SELECT chunk_text
        FROM embeddings
        WHERE user_id = $1
        ORDER BY embedding <-> $2::vector
        LIMIT $3
        """,
        user_id,
        query_vector_pg,  # ✅ STRING, not list
        k,
    )

    return [r["chunk_text"] for r in rows]
