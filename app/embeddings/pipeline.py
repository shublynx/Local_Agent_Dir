import uuid

from app.parsers.factory import get_parser
from app.embeddings.chunker import chunk_text
from app.embeddings.embedder import embed_chunks


def to_pgvector(vec) -> str:
    """
    Accepts:
    - list[float]
    - tuple[float]
    Converts to pgvector string
    """
    if not isinstance(vec, (list, tuple)):
        raise TypeError(f"Embedding must be list/tuple, got {type(vec)}")

    return "[" + ",".join(f"{float(x)}" for x in vec) + "]"


async def embed_document(
    *,
    db,
    document_id: str,
    user_id: str,
    file_path: str
):
    print("👉 EMBEDDING STARTED")
    print("document_id:", document_id)
    print("user_id:", user_id)
    print("file_path:", file_path)

    # ---------------------------
    # 1. Parse file
    # ---------------------------
    parser = get_parser(file_path)
    text = parser.parse(file_path)

    print("Parsed text length:", len(text))

    if not text.strip():
        raise ValueError("No text extracted")

    # ---------------------------
    # 2. Chunk text
    # ---------------------------
    chunks = chunk_text(text)
    print("Number of chunks:", len(chunks))

    if not chunks:
        print("⚠️ No chunks, stopping")
        return

    # ---------------------------
    # 3. Generate embeddings
    # ---------------------------
    vectors = embed_chunks(chunks)

    print("Type of vectors:", type(vectors))
    print("Type of first vector:", type(vectors[0]))

    # ---------------------------
    # 4. Store in DB
    # ---------------------------
    for i in range(len(chunks)):
        chunk = chunks[i]
        vector = vectors[i]

        print(f"Inserting chunk {i+1}/{len(chunks)}")
        print("Vector type before conversion:", type(vector))

        vector_pg = to_pgvector(vector)

        print("Vector PG sample:", vector_pg[:60])

        await db.execute(
            """
            INSERT INTO embeddings (
                id,
                user_id,
                document_id,
                chunk_text,
                embedding
            )
            VALUES ($1, $2, $3, $4, $5::vector)
            """,
            str(uuid.uuid4()),   # $1
            user_id,              # $2
            document_id,          # $3
            chunk,                # $4
            vector_pg             # $5 ✅ STRING
        )

    print("✅ Embedding pipeline finished")
