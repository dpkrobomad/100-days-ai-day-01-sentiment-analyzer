# Workflow & architecture

**Workflow diagram (HTML canvas — open in a browser):** [`workflow.html`](workflow.html)  

The page is a **node-and-arrow** diagram: SVG flowchart (entry → API stack → VADER), a horizontal **HTTP sequence** strip, and a **Path A** in-process line. Download or clone and open the file locally (`file://…`); GitHub’s UI won’t run HTML as a page.

## Text summary

1. **Streamlit** can score in two ways: **Path A** — in-process `analyze_sentiment` (default); **Path B** — `POST` to the running Uvicorn app when “Call HTTP API” is on.  
2. **curl, tests, OpenAPI** only use the **HTTP** path: FastAPI → Pydantic → `service.py` / VADER.  
3. **Path A** skips FastAPI; both paths use the same **service** module.  
4. On startup, **lifespan** runs `warm_vader()`.

## File map

| Piece            | Role                                      |
| ---------------- | ----------------------------------------- |
| `streamlit_app.py` | UI; local scoring **or** `httpx` → API  |
| `main.py`        | App, CORS, routes, lifespan                |
| `service.py`     | VADER, `analyze_sentiment`                 |
| `schemas.py`     | Request/response models                      |
| `config.py`      | `SENTIMENT_*` env                            |

## Plain-text flow (for README / slides)

```text
[Streamlit local]  import  →  service.py → VADER
[Streamlit HTTP]  POST  →  Uvicorn → FastAPI → Pydantic → service.py → VADER
[Others / /docs]  POST  →  Uvicorn → FastAPI → Pydantic → service.py → VADER
```
