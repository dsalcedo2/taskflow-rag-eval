"""Chat completions via local Ollama (free, no API key)."""

from __future__ import annotations

import httpx

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, REFUSAL_PHRASE


def chat(system_prompt: str, user_prompt: str) -> str:
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=120.0,
    )
    response.raise_for_status()
    content = response.json().get("message", {}).get("content")
    return (content or REFUSAL_PHRASE).strip()
