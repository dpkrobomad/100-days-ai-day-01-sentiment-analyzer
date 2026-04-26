# Sentiment analyzer API (Day 1)

Small FastAPI service: send text, get **positive / negative / neutral** plus VADER’s scores. Optional Streamlit app for a quick look without curl.

- **API docs (when running):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Repository:** <https://github.com/dpkrobomad/100-days-ai-day-01-sentiment-analyzer>  
- **License:** MIT — see `LICENSE`

## What this is

VADER is a simple lexicon-based scorer for short English (reviews, short posts, etc.). It’s not the latest transformer — it *is* something you can run anywhere and explain. Swap the backend later; keep the same route shape if you want.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev,ui]"
```

`ui` pulls in Streamlit for the demo app. API-only: `pip install -e .`

## Run the API

```bash
uvicorn sentiment_analyzer.main:app --host 0.0.0.0 --port 8000 --reload
```

Health: `GET http://127.0.0.1:8000/health`  
Scoring: `POST http://127.0.0.1:8000/api/v1/sentiment` with `{"text": "..."}`

### curl example

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}' | python3 -m json.tool
```

## Run Streamlit (optional)

```bash
streamlit run streamlit_app.py
```

Sidebar has an option to call the live API — start Uvicorn first if you use that.

## Tests / lint

```bash
pytest -q
ruff check src tests
```

## Architecture

- **HTML diagram (recommended):** open [docs/workflow.html](docs/workflow.html) in a browser.  
- **Text summary + links:** [docs/WORKFLOW.md](docs/WORKFLOW.md)

## Layout

| Path | What it does |
|------|----------------|
| `src/sentiment_analyzer/main.py` | App, routes, CORS |
| `src/sentiment_analyzer/service.py` | VADER call |
| `src/sentiment_analyzer/schemas.py` | Request/response |
| `src/sentiment_analyzer/config.py` | Env: `SENTIMENT_*` |
| `streamlit_app.py` | UI |

## Author

**Deepak Radhakrishnan** — AEROSPACE | AI | ROBOTICS — <https://www.deepakradhakrishnan.com>  
Code on GitHub: [@dpkrobomad](https://github.com/dpkrobomad)
