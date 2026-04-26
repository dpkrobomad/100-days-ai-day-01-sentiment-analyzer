# Workflow & architecture

**Visual diagram (HTML — open in a browser for best look):** [`workflow.html`](workflow.html)  
Also viewable on GitHub if you use **Raw** + save locally, or open the file from a clone:  
`file:///.../docs/workflow.html`

The HTML page is self-contained (dark theme, **Outfit** font); no Mermaid or external diagram tools.

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
