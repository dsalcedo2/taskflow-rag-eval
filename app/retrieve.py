"""Retrieve relevant documentation chunks with local embeddings."""

from __future__ import annotations

import chromadb

from app.config import CHROMA_DIR, COLLECTION_NAME, TOP_K
from app.embeddings import get_embedding_function


class RetrievedChunk:
    def __init__(self, text: str, source: str, score: float) -> None:
        self.text = text
        self.source = source
        self.score = score


def get_collection():
    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return chroma.get_collection(
        COLLECTION_NAME,
        embedding_function=get_embedding_function(),
    )


def retrieve(question: str, top_k: int = TOP_K) -> list[RetrievedChunk]:
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=top_k)

    chunks: list[RetrievedChunk] = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, distance in zip(documents, metadatas, distances):
        chunks.append(
            RetrievedChunk(
                text=doc,
                source=meta.get("source", "unknown"),
                score=1 - distance,
            )
        )
    return chunks
