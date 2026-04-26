"""FastAPI application — OpenAPI at /docs."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sentiment_analyzer import __version__
from sentiment_analyzer.config import get_settings
from sentiment_analyzer.schemas import SentimentRequest, SentimentResponse
from sentiment_analyzer.service import analyze_sentiment


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from sentiment_analyzer.service import warm_vader  # noqa: PLC0415

    warm_vader()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Sentiment Analyzer API",
        description=(
            "Classifies English text as **positive**, **negative**, or **neutral** using the "
            "VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon. "
            "Returns label, confidence, compound score, and raw scores."
        ),
        version=__version__,
        lifespan=lifespan,
        contact={
            "name": "100 Days of AI",
            "url": "https://github.com/dpkrobomad",
        },
        license_info={"name": "MIT"},
        openapi_tags=[
            {"name": "sentiment", "description": "Text sentiment analysis"},
        ],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origin_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"], summary="Liveness / readiness")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/", tags=["meta"], include_in_schema=False)
    def root() -> dict[str, Any]:
        return {
            "service": "sentiment-analyzer-api",
            "version": __version__,
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
        }

    @app.post(
        "/api/v1/sentiment",
        response_model=SentimentResponse,
        tags=["sentiment"],
        summary="Predict sentiment for input text",
    )
    def predict_sentiment(body: SentimentRequest) -> SentimentResponse:
        try:
            return analyze_sentiment(body.text)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=str(e)) from e

    return app


app = create_app()
