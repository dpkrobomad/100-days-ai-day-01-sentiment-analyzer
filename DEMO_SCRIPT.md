# Demo script — Day 1 Sentiment Analyzer (≈3–4 minutes)

**Goal**  
Show a working **REST API** with documented contracts, a **lexicon-based** sentiment decision, and a **polished Streamlit** surface for the same engine.

**Prereqs** (say aloud briefly)  
Python 3.11+, venv, `pip install -e ".[dev,ui]"` from the project root.

---

### 1. API + Swagger (90s)

1. In a terminal: `uvicorn sentiment_analyzer.main:app --host 0.0.0.0 --port 8000 --reload`  
2. Open **http://127.0.0.1:8000/docs**  
3. Expand **GET /health** → **Execute** — show `status: ok`  
4. Expand **POST /api/v1/sentiment** → **Try it out**  
5. **Example A (positive):** `{"text": "I love this product — best launch we've had."}`  
   - **Execute** — call out: `label: positive`, `confidence`, `compound` near +1, `scores`  
6. **Example B (negative):** `{"text": "Terrible support, still no refund. Very disappointed."}`  
   - **Execute** — `negative` compound, high `neg` in `scores`  
7. **Example C (neutral):** `{"text": "The meeting is at 3pm tomorrow."}`  
   - **Execute** — neutral band, `neu` proportion visible  

**Narration tip:** *“VADER is built for short social text; we expose the raw neg/neu/pos so this stays explainable for stakeholders.”*

---

### 2. Optional: curl (30s)

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"Horrible experience."}' | python3 -m json.tool
```

Show pretty-printed `label` and `compound`.

---

### 3. Streamlit “Sentiment Lab” (90s)

1. Second terminal: `streamlit run streamlit_app.py` — open the local URL  
2. **Default** — leave **“Call HTTP API”** off; click **Analyze** on the pre-filled text  
3. Point at **label**, **class confidence %**, **compound**, and the **sentiment bar**  
4. Open **“Sample phrases”** — run one **positive**, one **negative**, one **neutral**  
5. **Advanced:** turn **“Call HTTP API”** on (with Uvicorn still running) — same result path through HTTP  

**Narration tip:** *“One core analysis function, two entrypoints: API for integration, Streamlit for demos and stakeholders.”*

---

### 4. Close (20s)

- *“This is Day 1 of a 100-day build; next steps could be a transformer or multilingual model behind the same schema.”*  
- Point to the **GitHub** repo in the on-screen browser tab.

---

**Fallback** if API won’t start: use Streamlit only (local engine) and mention that production would call the same logic via the deployed API.
