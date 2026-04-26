# Workflow & architecture

How requests move through the **Day 1 Sentiment Analyzer** project: FastAPI, shared scoring, and the Streamlit app (two modes).

## High-level data flow

```mermaid
flowchart TB
    subgraph clients [Clients]
        SW[Streamlit app\nstreamlit_app.py]
        BC[Other HTTP clients\ncurl, webhooks, tests]
        SWG[OpenAPI / Swagger\nbrowser at /docs]
    end

    subgraph api [FastAPI service]
        FA[Uvicorn → sentiment_analyzer.main:app]
        RT[GET /health\nPOST /api/v1/sentiment]
        PD[Pydantic\nSentimentRequest / SentimentResponse]
    end

    subgraph core [Core]
        SVC[service.py\nanalyze_sentiment + VADER]
    end

    SW -->|A. Local: import| SVC
    SW -->|B. HTTP: toggle on| RT
    BC --> RT
    SWG --> RT
    RT --> PD
    PD --> SVC
    FA --> RT
```

- **Path A (default in Streamlit):** UI calls `analyze_sentiment()` in process — no HTTP, same logic as the API.  
- **Path B (sidebar “Call HTTP API”):** UI sends `POST` to the running Uvicorn server.  
- **Path C:** Any client uses the public JSON contract; core logic is always `service.py`.

## Request sequence (API path)

```mermaid
sequenceDiagram
    autonumber
    participant C as Client (curl, Swagger, Streamlit+HTTP)
    participant F as FastAPI
    participant P as Pydantic
    participant V as VADER\n(service.py)

    C->>F: POST /api/v1/sentiment JSON body
    F->>P: validate SentimentRequest
    alt invalid text
        P-->>C: 422
    end
    P->>V: text string
    V->>V: SentimentIntensityAnalyzer
    V-->>F: SentimentResponse
    F-->>C: 200 JSON label, confidence, compound, scores
```

**Startup:** `lifespan` calls `warm_vader()` so the lexicon is loaded before the first request.

## Request sequence (Streamlit, local engine)

```mermaid
sequenceDiagram
    participant U as User
    participant St as Streamlit
    participant V as service.analyze_sentiment

    U->>St: text + Analyze
    St->>V: in-process call
    V-->>St: Pydantic model → model_dump
    St-->>U: metrics + sentiment bar
```

## Component view

```mermaid
flowchart LR
    subgraph config
        ENV[.env / SENTIMENT_*]
    end
    ENV --> CFG[config.py / Settings]
    CFG --> main[main.py]

    main --> COR[CORS]
    main --> R1[/api/v1/sentiment]
    main --> R0[/health]

    R1 --> SCH[schemas.py]
    SCH --> SVC[service.py]
    SVC --> VAD[VADER lexicon]
```

## File map (short)

| Piece | Role |
|-------|------|
| `streamlit_app.py` | UI; local scoring **or** `httpx` → API |
| `main.py` | Routes, CORS, OpenAPI, lifespan |
| `service.py` | VADER, `SentimentResponse` |
| `schemas.py` | Request/response contracts |
| `config.py` | `SENTIMENT_*` env |

GitHub and many Markdown viewers render the Mermaid blocks above. For a PNG/SVG export, use [Mermaid Live Editor](https://mermaid.live) or a docs build that supports Mermaid.
