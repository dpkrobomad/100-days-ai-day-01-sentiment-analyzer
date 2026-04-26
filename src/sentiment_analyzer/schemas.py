from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SentimentRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=50_000,
        description="Text to analyze (English works best for VADER).",
        examples=["I love this product!"],
    )

    @field_validator("text", mode="before")
    @classmethod
    def non_empty_stripped(cls, v: Any) -> str:
        if isinstance(v, str):
            s = v.strip()
            if not s:
                raise ValueError("text must not be empty or whitespace only")
            return s
        return v


class SentimentResponse(BaseModel):
    label: SentimentLabel
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Lexicon confidence for the predicted class (VADER pos/neg/neu proportion).",
    )
    compound: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="VADER compound score: -1 (most negative) to +1 (most positive).",
    )
    scores: dict[str, float] = Field(
        ...,
        description="Raw VADER: neg, neu, pos (each 0..1) plus compound in scores dict if needed",
    )
    model: str = Field(default="VADER (vaderSentiment)")
