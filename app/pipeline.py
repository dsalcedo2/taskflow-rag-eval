"""RAG and baseline pipelines shared by the API and eval harness."""

from __future__ import annotations

from app.config import DOCS_DIR, REFUSAL_PHRASE
from app.generate import SYSTEM_PROMPT, generate_answer
from app.ingest import load_documents
from app.llm import chat
from app.retrieve import retrieve


def load_all_docs_text() -> str:
    parts: list[str] = []
    for doc in load_documents(DOCS_DIR):
        parts.append(f"# File: {doc['source']}\n{doc['text']}")
    return "\n\n".join(parts)


def ask_rag(question: str) -> dict[str, object]:
    chunks = retrieve(question)
    answer, sources = generate_answer(question, chunks)
    return {
        "answer": answer,
        "sources": sources,
        "mode": "rag",
        "chunks_used": len(chunks),
    }


def ask_prompt_only(question: str) -> dict[str, object]:
    all_docs = load_all_docs_text()
    user_prompt = f"Full documentation:\n{all_docs}\n\nQuestion: {question}"
    answer = chat(SYSTEM_PROMPT, user_prompt)
    return {
        "answer": answer or REFUSAL_PHRASE,
        "sources": ["all_docs"],
        "mode": "prompt_only",
        "chunks_used": 0,
    }


def ask(question: str, mode: str = "rag") -> dict[str, object]:
    if mode == "prompt_only":
        return ask_prompt_only(question)
    if mode == "rag":
        return ask_rag(question)
    raise ValueError(f"Unknown mode: {mode}")
