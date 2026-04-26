from fastapi.testclient import TestClient

from sentiment_analyzer.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_sentiment_positive() -> None:
    r = client.post("/api/v1/sentiment", json={"text": "I love it!"})
    assert r.status_code == 200
    d = r.json()
    assert d["label"] == "positive"
    assert "confidence" in d and "scores" in d


def test_sentiment_empty_422() -> None:
    r = client.post("/api/v1/sentiment", json={"text": "   "})
    assert r.status_code == 422
