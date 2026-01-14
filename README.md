# 📄 RAG Document Assistant (Local, Streaming, Scalable)

A **production-ready Retrieval-Augmented Generation (RAG) system** that allows users to upload documents (PDF / CSV / Excel) and ask questions with **live streaming AI responses**, running **entirely locally** using Ollama.

This project demonstrates **real-world AI backend engineering**, not a toy example.

---

## 🚀 Features

- 📤 Upload documents (PDF, CSV, Excel)
- 🧠 Automatic document parsing & chunking
- 🔢 Vector embeddings using PostgreSQL + pgvector
- 🔍 Semantic search over document content
- 💬 Streaming answers (token-by-token)
- 🧑 Multi-user safe (user-scoped data)
- 🏠 Fully local setup (no OpenAI required)
- ⚡ FastAPI + async PostgreSQL backend
- 🎨 Streamlit frontend UI

---

## 🧱 Architecture Overview

User (Streamlit UI)
    ↓
Upload Document
    ↓
FastAPI Backend
    ├─ Parse document
    ├─ Chunk text
    ├─ Generate embeddings (Ollama)
    ├─ Store in PostgreSQL (pgvector)
    ↓
Ask Question
    ↓
Vector similarity search
    ↓
Prompt construction
    ↓
Streaming LLM answer (Ollama)

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- PostgreSQL + pgvector
- asyncpg

### AI / NLP
- Ollama
  - qwen2:1.5b (LLM)
  - nomic-embed-text (Embeddings)

### Frontend
- Streamlit
- Live streaming UI

---

## ⚙️ Setup Instructions

### PostgreSQL + pgvector
Install PostgreSQL and pgvector, then enable the extension:

CREATE EXTENSION vector;

### Ollama
Install and pull models:

ollama pull qwen2:1.5b
ollama pull nomic-embed-text

### Backend
Run:
uvicorn app.main:app --reload

### Frontend
Run:
streamlit run streamlit.py

---

## 👨‍💻 Author

Shubham Singh



## System Architecture Diagram

┌──────────────┐
│  Streamlit   │
│   Frontend   │
│ (File Upload │
│  + Questions)│
└──────┬───────┘
       │ HTTP (REST)
       ▼
┌──────────────────────┐
│      FastAPI         │
│   Application API    │
│----------------------│
│ /documents/upload    │
│ /documents/embed     │
│ /ask/stream          │
└──────┬───────────────┘
       │ async DB / IO
       ▼
┌─────────────────────────────┐
│       PostgreSQL             │
│------------------------------│
│ documents table              │
│ embeddings table (pgvector)  │
│ vector indexes (future)      │
└──────┬──────────────────────┘
       │ similarity search
       ▼
┌──────────────────────────┐
│   Retrieval Layer         │
│---------------------------│
│ cosine similarity search  │
│ top-K chunk selection     │
└──────┬───────────────────┘
       │ context chunks
       ▼
┌──────────────────────────┐
│   Prompt Builder          │
│---------------------------│
│ strict grounding rules    │
│ summary / numeric logic   │
└──────┬───────────────────┘
       │ prompt
       ▼
┌──────────────────────────┐
│   LLM (Ollama)            │
│---------------------------│
│ local inference           │
│ token streaming           │
└──────────┬───────────────┘
           │ streamed tokens
           ▼
┌──────────────────────┐
│  Streamlit UI        │
│ (Live response)     │
└──────────────────────┘
