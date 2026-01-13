from langchain_ollama import OllamaLLM

_llm = OllamaLLM(
    model="qwen2:1.5b",
    temperature=0.2,
    streaming=True
)


async def stream_answer(prompt: str):
    """
    Stream answer token-by-token.
    """

    for chunk in _llm.stream(prompt):
        yield chunk
