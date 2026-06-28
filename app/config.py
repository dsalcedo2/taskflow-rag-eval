import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DOCS_DIR = PROJECT_ROOT / "data" / "docs"
EVAL_QUESTIONS_PATH = PROJECT_ROOT / "eval" / "questions.json"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "taskflow_docs"

# Local stack (free): sentence-transformers + Ollama
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3

REFUSAL_PHRASE = (
    "I don't have that information in the TaskFlow API documentation."
)
