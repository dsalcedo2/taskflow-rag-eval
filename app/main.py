"""FastAPI server for TaskFlow API documentation Q&A."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.pipeline import ask

app = FastAPI(
    title="TaskFlow API Doc Assistant",
    description="RAG over synthetic TaskFlow API documentation",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, examples=["How do I authenticate requests?"])
    mode: str = Field(default="rag", pattern="^(rag|prompt_only)$")


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    mode: str
    chunks_used: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest) -> AskResponse:
    try:
        result = ask(request.question, mode=request.mode)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AskResponse(
        answer=str(result["answer"]),
        sources=list(result["sources"]),
        mode=str(result["mode"]),
        chunks_used=int(result["chunks_used"]),
    )
