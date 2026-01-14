import streamlit as st
import requests
import uuid
import random

UPLOAD_API_URL = "http://127.0.0.1:8000/documents/upload"
STREAM_API_URL = "http://127.0.0.1:8000/ask/stream"
ALLOWED_TYPES = ["pdf", "csv", "xlsx"]

st.set_page_config(page_title="RAG Assistant", layout="centered")
st.title("📄 Document Assistant")

# -------------------------
# SESSION STATE
# -------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "question" not in st.session_state:
    st.session_state.question = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------
# FILE UPLOAD
# -------------------------
st.subheader("📤 Upload document")

uploaded_file = st.file_uploader("Choose file", type=ALLOWED_TYPES)

if st.button("Upload"):
    if not uploaded_file:
        st.warning("Select a file")
    else:
        with st.spinner("Uploading & embedding…"):
            res = requests.post(
                UPLOAD_API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },
                data={"user_id": st.session_state.user_id},
            )

        if res.status_code == 200:
            st.success("✅ File uploaded & embedded")
        else:
            st.error(res.text)

# -------------------------
# QUESTION INPUT
# -------------------------
st.subheader("💬 Ask a question")

st.text_area(
    "Question",
    key="question",
    height=80,
    placeholder="What are the highest sales?"
)

ask = st.button("Ask")

answer_box = st.empty()

# -------------------------
# ASK LOGIC (FIXED)
# -------------------------
if ask:
    q = st.session_state.question.strip()

    if not q:
        st.warning("Enter a question")
        st.stop()

    with requests.post(
        STREAM_API_URL,
        json={"question": q, "user_id": st.session_state.user_id},
        stream=True,
        timeout=600,
    ) as r:

        if r.status_code != 200:
            st.error(r.text)
            st.stop()

        answer = ""
        for chunk in r.iter_content(chunk_size=32, decode_unicode=True):
            if chunk:
                answer += chunk
                answer_box.markdown(answer)

    st.session_state.chat.append((q, answer))

# -------------------------
# CHAT HISTORY
# -------------------------
if st.session_state.chat:
    st.subheader("🧠 Chat history")
    for q, a in st.session_state.chat:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Assistant:** {a}")
