# TaskFlow API Doc Assistant (RAG + Eval)

RAG pipeline and evaluation harness over **synthetic TaskFlow REST API documentation**.

**Repo:** [github.com/dsalcedo2/taskflow-rag-eval](https://github.com/dsalcedo2/taskflow-rag-eval)

TaskFlow is a fictional API created for portfolio use.

**Runs 100% free locally** — no OpenAI credits, no Together.ai, no API keys required.

## Architecture

```text
data/docs/*.md
    → ingest (chunk + local embeddings)
    → Chroma vector store
    → retrieve top-k chunks
    → Ollama LLM answer (grounded)
    → eval/run_eval.py scores fixed questions
```

| Component | Tool | Cost |
|-----------|------|------|
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) | Free (runs on CPU) |
| LLM | Ollama (`llama3.2:3b`) | Free (runs locally) |
| Vector DB | Chroma | Free |

## Setup

### 1. Install Ollama

**Option A — PowerShell (recommended on Windows):**

```powershell
irm https://ollama.com/install.ps1 | iex
```

**Option B — Direct installer download:**

- [https://ollama.com/download/windows](https://ollama.com/download/windows)
- Or direct file: [https://ollama.com/download/OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe)

**Option C — If ollama.com does not load (GitHub backup):**

- [https://github.com/ollama/ollama/releases/latest](https://github.com/ollama/ollama/releases/latest)
- Download **OllamaSetup.exe** from Assets, run it, then **close and reopen** your terminal.

After install, pull a model:

```powershell
ollama pull llama3.2:3b
```

Keep Ollama running (it starts automatically after install on Windows).

### 2. Python environment

```powershell
git clone https://github.com/dsalcedo2/taskflow-rag-eval.git
cd taskflow-rag-eval
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If `activate` fails on Windows (execution policy), run commands with `.\.venv\Scripts\python.exe` instead of `python`.

Optional: copy `.env.example` to `.env` only if you want to change the Ollama model or URL.

First ingest downloads the embedding model (~80MB) once.

### 3. Ingest documentation

```powershell
python -m app.ingest
```

### 4. Run the API

```powershell
uvicorn app.main:app --reload
```

POST `http://127.0.0.1:8000/ask`:

```json
{
  "question": "How do I authenticate requests to TaskFlow?",
  "mode": "rag"
}
```

Swagger UI: http://127.0.0.1:8000/docs

### 5. Run eval harness

```powershell
python eval/run_eval.py --mode rag --output eval/results_rag.json
python eval/run_eval.py --mode prompt_only --output eval/results_prompt_only.json
```

Eval is slower with local LLM (~30–90 seconds per question). Expect a few minutes for all 15.

## Results

| Method | Overall | Answerable | Unanswerable |
|--------|---------|------------|--------------|
| Prompt-only | 14/15 (93.3%) | 12/13 | 2/2 |
| RAG (k=3) | **15/15 (100%)** | **13/13** | 2/2 |

RAG improved over prompt-only on **q11** (user invites via `POST /v1/users`): prompt-only incorrectly refused; RAG retrieved `endpoints-users.md` and answered correctly.

## Troubleshooting

| Error | Fix |
|-------|-----|
| Connection refused to `localhost:11434` | Install Ollama and run `ollama pull llama3.2:3b` |
| Model not found | `ollama pull llama3.2:3b` or set `OLLAMA_MODEL` in `.env` |
| Slow first ingest | Normal — downloads embedding model once |
