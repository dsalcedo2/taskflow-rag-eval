"""Generate answers from retrieved context using local Ollama."""

from __future__ import annotations

from app.config import REFUSAL_PHRASE
from app.llm import chat
from app.retrieve import RetrievedChunk

SYSTEM_PROMPT = f"""You are a helpful assistant for the fictional TaskFlow REST API.
Answer ONLY using the provided documentation context.
If the context does not contain enough information to answer, respond exactly with:
"{REFUSAL_PHRASE}"
Be concise and precise. Include endpoint paths, HTTP methods, and error codes when relevant.
"""


def format_context(chunks: list[RetrievedChunk]) -> str:
    sections: list[str] = []
    for chunk in chunks:
        sections.append(f"[Source: {chunk.source}]\n{chunk.text}")
    return "\n\n---\n\n".join(sections)


def generate_answer(question: str, chunks: list[RetrievedChunk]) -> tuple[str, list[str]]:
    context = format_context(chunks)
    sources = sorted({chunk.source for chunk in chunks})
    user_prompt = f"Documentation context:\n{context}\n\nQuestion: {question}"
    answer = chat(SYSTEM_PROMPT, user_prompt)
    return answer, sources
