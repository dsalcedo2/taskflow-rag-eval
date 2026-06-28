"""Load markdown docs, chunk, embed, and store in Chroma."""

from __future__ import annotations

import hashlib
from pathlib import Path

import chromadb

from app.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    DOCS_DIR,
)
from app.embeddings import get_embedding_function


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - overlap
    return [c for c in chunks if c]


def load_documents(docs_dir: Path = DOCS_DIR) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    for path in sorted(docs_dir.glob("*.md")):
        documents.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return documents


def ingest(docs_dir: Path = DOCS_DIR, reset: bool = True) -> int:
    documents = load_documents(docs_dir)
    if not documents:
        raise FileNotFoundError(f"No markdown files found in {docs_dir}")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        try:
            chroma.delete_collection(COLLECTION_NAME)
        except (ValueError, chromadb.errors.NotFoundError):
            pass

    collection = chroma.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )

    ids: list[str] = []
    texts: list[str] = []
    metadatas: list[dict[str, str]] = []

    for doc in documents:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            chunk_id = hashlib.md5(f"{doc['source']}:{i}:{chunk[:80]}".encode()).hexdigest()
            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({"source": doc["source"], "chunk_index": str(i)})

    collection.add(ids=ids, documents=texts, metadatas=metadatas)
    return len(texts)


if __name__ == "__main__":
    count = ingest()
    print(f"Ingested {count} chunks into Chroma collection '{COLLECTION_NAME}'.")
