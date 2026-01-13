import os
import uuid
import asyncio

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    Body,
    Query
)
from fastapi.responses import StreamingResponse

from app.db import connect_db, disconnect_db, get_db
from app.parsers.factory import get_parser
from app.embeddings.pipeline import embed_document
from app.rag.retriever import retrieve_context
from app.rag.prompt import build_prompt
from app.rag.generator import stream_answer

# ===========================================
# FILE STORAGE CONFIG
# ===========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_BASE = os.path.join(BASE_DIR, "data", "uploads")
ALLOWED_EXTENSIONS = {".pdf", ".csv", ".xlsx"}

app = FastAPI(title="Scalable RAG Backend", version="0.1.0")

# ===========================================
# LIFECYCLE
# ===========================================

@app.on_event("startup")
async def startup():
    print("🚀 FastAPI starting...")
    await connect_db()
    print("✅ Database connected")

@app.on_event("shutdown")
async def shutdown():
    print("🛑 FastAPI shutting down...")
    await disconnect_db()

@app.get("/")
async def health_check():
    return {"status": "ok"}

# ===========================================
# DOCUMENT UPLOAD
# ===========================================

from app.embeddings.pipeline import embed_document

@app.post("/documents/upload")
async def upload_document(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db=Depends(get_db)
):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    document_id = str(uuid.uuid4())

    user_dir = os.path.join(UPLOAD_BASE, user_id)
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, f"{document_id}{file_ext}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    await db.execute(
        """
        INSERT INTO documents (id, user_id, filename, file_path)
        VALUES ($1, $2, $3, $4)
        """,
        document_id,
        user_id,
        file.filename,
        file_path
    )

    # ✅ AUTO EMBEDDING (THIS IS THE FIX)
    await embed_document(
        db=db,
        document_id=document_id,
        user_id=user_id,
        file_path=file_path
    )

    return {
        "filename": file.filename,
        "status": "uploaded_and_embedded"
    }


# ===========================================
# DOCUMENT PARSE (DEBUG ONLY)
# ===========================================

@app.get("/documents/parse")
async def parse_document(file_path: str = Query(...)):
    print("📄 Parsing document:", file_path)

    parser = get_parser(file_path)
    text = parser.parse(file_path)

    print("✂️ Parsed text length:", len(text))

    return {
        "length": len(text),
        "preview": text[:1000]
    }

# ===========================================
# DOCUMENT EMBEDDING
# ===========================================

@app.post("/documents/embed")
async def embed_uploaded_document(
    payload: dict = Body(...),
    db=Depends(get_db)
):
    print("🔥 /documents/embed endpoint HIT")
    print("Payload received:", payload)

    document_id = payload.get("document_id")
    user_id = payload.get("user_id")

    print("Embedding document_id:", document_id)
    print("Embedding user_id:", user_id)

    row = await db.fetchrow(
        "SELECT file_path FROM documents WHERE id=$1 AND user_id=$2",
        document_id,
        user_id
    )

    print("DB lookup result:", row)

    if not row:
        raise HTTPException(status_code=404, detail="Document not found")

    print("📂 File path found:", row["file_path"])
    print("➡️ Calling embed_document()")

    await embed_document(
        db=db,
        document_id=document_id,
        user_id=user_id,
        file_path=row["file_path"]
    )

    print("✅ Embedding pipeline finished")

    return {"status": "embedded"}

# ===========================================
# ASK STREAM
# ===========================================

@app.post("/ask/stream")
async def ask_stream(
    payload: dict = Body(...),
    db=Depends(get_db)
):
    print("💬 /ask/stream hit")
    print("Payload:", payload)

    question = payload["question"]
    user_id = payload["user_id"]

    context_chunks = await retrieve_context(
        db=db,
        user_id=user_id,
        query=question,
        k=5
    )

    print("📦 Retrieved chunks count:", len(context_chunks))
    print("Chunks preview:", context_chunks[:2])

    prompt = build_prompt(context_chunks, question)

    async def token_stream():
        async for token in stream_answer(prompt):
            yield token
            await asyncio.sleep(0)

    return StreamingResponse(token_stream(), media_type="text/plain")
