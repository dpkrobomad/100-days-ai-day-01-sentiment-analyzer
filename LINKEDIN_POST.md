# LinkedIn post — Day 1: Sentiment Analyzer API

**Problem**  
Product and support teams need a quick, consistent read on **whether text is positive, negative, or neutral** (reviews, tickets, social) before routing or triaging. Manual reading doesn’t scale.

**Approach**  
I built a small **NLP** pipeline using the **VADER** lexicon (Valence Aware Dictionary and sEntiment Reasoner). It’s rule-based: no training set required, fast inference, and **interpretable** outputs (per-polarity scores + compound) instead of a black box. Labels use compound thresholds; **confidence** is the VADER mass on the selected polarity.

**Tech stack**  
Python 3.11+ · **FastAPI** (OpenAPI at `/docs`) · **Pydantic v2** · **Uvicorn** · **VADER (vaderSentiment)** · **Streamlit** demo UI (dark, product-style layout) · `httpx` for optional live API mode.

**Demo**  
Screenshot or short screen recording: (1) Swagger `POST /api/v1/sentiment` with a positive and a negative example; (2) Streamlit “Sentiment Lab” with the same phrases and the compound bar. Show JSON: `label`, `confidence`, `compound`, `scores`.

**Learning**  
For short English text, a **lexicon + compound score** is often enough to ship. **Separating the core `analyze` function** from **FastAPI** and **Streamlit** keeps one source of truth and makes tests trivial—swap VADER for a model later without changing the API contract.

**GitHub**  
https://github.com/dpkrobomad/100-days-ai-day-01-sentiment-analyzer

---
*Replace the line above with the final repo URL if it differs. Hashtags (optional): #Python #FastAPI #NLP #MachineLearning #100DaysOfCode #AIEngineering*
