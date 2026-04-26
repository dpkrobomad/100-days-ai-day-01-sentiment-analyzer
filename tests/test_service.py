import pytest

from sentiment_analyzer.schemas import SentimentLabel
from sentiment_analyzer.service import analyze_sentiment, warm_vader


def test_warm_does_not_crash() -> None:
    warm_vader()


@pytest.mark.parametrize(
    "text,expected",
    [
        ("I love this! Amazing.", SentimentLabel.POSITIVE),
        ("Horrible experience, I hate it.", SentimentLabel.NEGATIVE),
        ("The file is 12 pages long.", SentimentLabel.NEUTRAL),
    ],
)
def test_label_buckets(text: str, expected: SentimentLabel) -> None:
    r = analyze_sentiment(text)
    assert r.label == expected
    assert 0.0 <= r.confidence <= 1.0
    assert -1.0 <= r.compound <= 1.0
    assert "neg" in r.scores and "pos" in r.scores
