# Day 1 — Sentiment Analyzer API

FastAPI service that classifies text as **positive**, **negative**, or **neutral** using the [VADER](https://github.com/cjhutto/vaderSentiment) (Valence Aware Dictionary and sEntiment Reasoner) lexicon. Returns label, per-class style confidence, compound score, and raw scores. Includes a **Streamlit** “Sentiment Lab” UI with a dark, product-style layout.

- **OpenAPI / Swagger** — [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) when the API is running.

## Why VADER

Rule-based, fast, no training data, and interpretable. Suited to short social/review text in English. For other languages or long-form content, you would swap the backend for embeddings or a transformer (same API contract).

## Requirements

- Python 3.11+

## Setup

```bash
cd day-01-sentiment-analyzer-api
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,ui]"
cp .env.example .env  # optional; defaults are fine locally
```

## Run the API

```bash
# from project root, with venv active
export PYTHONPATH=src  # only if you did not pip install -e .
uvicorn sentiment_analyzer.main:app --host 0.0.0.0 --port 8000 --reload
```

- Docs: <http://127.0.0.1:8000/docs>  
- Health: <http://127.0.0.1:8000/health>

### Example (curl)

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}' | python3 -m json.tool
```

## Run the Streamlit UI

```bash
streamlit run streamlit_app.py
```

Toggle **“Call HTTP API”** in the sidebar to hit the live FastAPI service, or use the in-process engine (same logic).

## Tests

```bash
pytest -q
ruff check src tests
```

## Project layout

| Path | Purpose |
|------|---------|
| `src/sentiment_analyzer/main.py` | FastAPI app, CORS, routes |
| `src/sentiment_analyzer/service.py` | VADER analysis (shared) |
| `src/sentiment_analyzer/schemas.py` | Pydantic request/response |
| `src/sentiment_analyzer/config.py` | `SENTIMENT_*` env settings |
| `streamlit_app.py` | Optional demo UI |
| `LINKEDIN_POST.md` | Ready-to-post copy |
| `DEMO_SCRIPT.md` | Step-by-step demo script |

## Author

[dpkrobomad](https://github.com/dpkrobomad) — 100 Days of AI with Python, Day 1.
