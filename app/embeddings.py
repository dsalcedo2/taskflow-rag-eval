"""Local embedding model (free, runs on your machine)."""

from __future__ import annotations

from chromadb.utils import embedding_functions

from app.config import LOCAL_EMBEDDING_MODEL

_embedding_function = None


def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=LOCAL_EMBEDDING_MODEL
        )
    return _embedding_function
