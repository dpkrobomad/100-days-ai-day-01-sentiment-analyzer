"""VADER-based sentiment. Shared by FastAPI and Streamlit."""

from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sentiment_analyzer.schemas import SentimentLabel, SentimentResponse

_analyzer: SentimentIntensityAnalyzer | None = None


def _get_analyzer() -> SentimentIntensityAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def warm_vader() -> None:
    """Eagerly load the lexicon so the first user request is not cold."""
    _get_analyzer()


def analyze_sentiment(text: str) -> SentimentResponse:
    """
    VADER: compound in [-1,1]; pos/neg/neu are normalized proportions.
    Label uses compound bands; confidence = the VADER mass on the selected polarity.
    """
    sia = _get_analyzer()
    s = sia.polarity_scores(text)
    neg, neu, pos = s["neg"], s["neu"], s["pos"]
    compound = float(s["compound"])

    if compound > 0.05:
        label = SentimentLabel.POSITIVE
        confidence = float(pos)
    elif compound < -0.05:
        label = SentimentLabel.NEGATIVE
        confidence = float(neg)
    else:
        label = SentimentLabel.NEUTRAL
        confidence = float(neu)

    scores = {"neg": neg, "neu": neu, "pos": pos, "compound": compound}
    return SentimentResponse(
        label=label,
        confidence=round(confidence, 6),
        compound=round(compound, 6),
        scores={k: round(float(v), 6) for k, v in scores.items()},
    )
