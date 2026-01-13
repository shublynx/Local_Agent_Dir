def build_prompt(context_chunks: list[str], question: str) -> str:
    """
    Build final RAG prompt.
    """

    context = "\n\n".join(context_chunks)


    print('context_chunks', context)
    print('question', question)


    return f"""
You are a helpful assistant answering questions strictly
based on the provided context.

You can analyze the context to provide an answer.

Only use the provided context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""


