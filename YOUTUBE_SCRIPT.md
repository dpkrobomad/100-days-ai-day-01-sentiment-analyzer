# YouTube walkthrough script — Day 1: Sentiment Analyzer API

**Purpose:** Record a **clear, full-screen** walkthrough: viewers should always see **what you are doing** (entire browser window or a deliberate split) — no “mystery clicks” off-camera.

**Target length:** ~8–10 minutes (long-form) or cut down to a **~60s Shorts** (see [Shorts variant](#youtube-shorts-60s-variant)).

**Repo to promote:** <https://github.com/dpkrobomad/100-days-ai-day-01-sentiment-analyzer>

---

## Before you record

| Setting | Recommendation |
|--------|------------------|
| **Resolution** | **1920×1080** (16:9) — YouTube’s default. |
| **Capture** | **Full screen** of the monitor you demo on, **or** “Application window” capture of a **maximized** browser (address bar + page fully visible; no crooked partial window). |
| **Cursor / text** | **150%+ browser zoom** if viewers read small Swagger text; test readability at **1080p** on a phone. |
| **Clutter** | Close tabs you won’t use; **hide bookmarks bar** or use a clean profile; **no private info** in other tabs. |
| **Terminals** | **Large font** (16–20 pt), light-on-dark or high contrast; **no API keys** on screen. |
| **Audio** | Quiet room; **normalize** in edit if possible. |
| **Optional** | Simple **lower-third** in OBS (name + “Day 1 / Sentiment API”) for the first 20s and after chapter breaks. |

**Software (pick one):** OBS Studio (Display or Window capture), QuickTime (screen), or Camtasia. **Do not** capture only a tiny Swagger panel at 400×300 — the point is the **entire** interaction context.

---

## Suggested YouTube metadata

**Title (pick one or tweak)**  
- `I Built a Sentiment API in Python (FastAPI + VADER) — 100 Days of AI, Day 1`  
- `Day 1: Sentiment Analyzer REST API with Auto Docs | Python FastAPI`  

**Description (template)**  
```text
Day 1 of my 100-day AI build: a production-style Sentiment Analysis REST API in Python
using FastAPI + VADER, plus a Streamlit demo. OpenAPI/Swagger included.

GitHub: https://github.com/dpkrobomad/100-days-ai-day-01-sentiment-analyzer

Timestamps: (paste from “Chapters” below after upload)

#Python #FastAPI #NLP #MachineLearning #VADER #Streamlit
```

**Tags (first ~10)**  
`python`, `fastapi`, `api`, `nlp`, `sentiment analysis`, `vader`, `streamlit`, `machine learning`, `beginner`, `100 days of code`

---

## Chapters (copy into YouTube description after upload)

| Start | Chapter |
|-------|---------|
| 0:00 | Hook — what we’re building today |
| 0:40 | What’s in the GitHub repo |
| 1:20 | Open project + install (terminal, full font) |
| 3:00 | Run API + full-screen Swagger at /docs |
| 5:30 | Three live requests (happy / sad / neutral) |
| 7:30 | Streamlit “Sentiment Lab” (full app window) |
| 9:00 | Why VADER + what’s next + CTA / GitHub |

**Adjust times** to your real recording.

---

## Scene A — Hook + repo (0:00–~1:20)

**Screen layout:** **Full screen:** browser, **one tab** — your GitHub repo `100-days-ai-day-01-sentiment-analyzer`. **Or** 70% browser / 30% black margin if you use a “talking head” side — *GitHub must stay readable*.

**On screen:**  
- GitHub: **Code** tab, default branch `main`, `README` visible (scroll so **title + “Repository:”** line and folder list are visible).  
- Optional overlay text (5s): `Day 1 | Sentiment API | Python`

**Narration (script):**  
> “In this video, Day 1 of a 100-day AI series, I’m showing a **Sentiment Analyzer** you can run locally: a **FastAPI** service with **automatic OpenAPI docs**, and a small **Streamlit** UI. Under the hood we use **VADER** — a classic lexicon for short, emotional English text. If you want to code along, the repo is **public** — link in the description.”

**[CUT]** — do not read the whole README; tease the stack only.

---

## Scene B — Clone / open project + venv (optional if “from machine”) (~1:20–3:00)

**Screen layout:** **Full-screen terminal** (or **IDE** with terminal panel large enough to read, **entire** window captured — not a sliver).

**On screen (example flow):**  
- `cd` into `day-01-sentiment-analyzer-api` (or your path).  
- Show **only:** `python3 -m venv .venv` → `source .venv/bin/activate` (or Windows equivalent) → `pip install -e ".[dev,ui]"` — **no secrets**, no `.env` with real keys.  
- Scroll so **success** of install is visible; **no need** to read every line.

**Narration:**  
> “I’m in a **virtual environment** and installing the project in **editable** mode, including the Streamlit extra for the demo UI. This matches the **README** so you can reproduce it.”

**[ON-SCREEN CALLOUT optional]:** `pip install -e ".[dev,ui]"`

---

## Scene C — API + full Swagger (3:00–5:30)

**Screen layout:** **Browser window maximized** — **entire** window including **address bar** so viewers see `http://127.0.0.1:8000/docs`. **No DevTools** unless you show them on purpose. **100% of the Swagger “Try it out”** block must be visible when you click.

**Prep:** Terminal **already running** in background or small PiP: `uvicorn sentiment_analyzer.main:app --host 0.0.0.0 --port 8000 --reload` — or start it **on screen** in the previous scene, then **switch** to browser full screen.

**On screen, in order:**  
1. **Navigate** to `http://127.0.0.1:8000/docs` — **zoom** if the title is hard to read.  
2. **Expand** `GET /health` → **Try it out** → **Execute** — **scroll** so the **Response body** (JSON) is **fully** in frame.  
3. **Expand** `POST /api/v1/sentiment` → **Try it out** — **entire** request body box visible.  
4. **Example 1 (positive):** body **exactly:**  
   `{"text": "I love this product — best launch we've had."}`  
   **Execute** — **scroll** to show `label`, `confidence`, `compound`, `scores` in the response. **Pause 2 seconds** on the response.  
5. **Example 2 (negative):** replace with:  
   `{"text": "Terrible support, still no refund. Very disappointed."}`  
   **Execute** — again **full** response in frame.  
6. **Example 3 (neutral):**  
   `{"text": "The meeting is at 3pm tomorrow."}`  
   **Execute**.

**Narration:**  
> “This is the **OpenAPI** UI FastAPI gives you for free. **Health** is for uptime checks. **Sentiment** takes JSON text and returns a **label**, a **confidence** from VADER’s masses, a **compound** score from minus one to plus one, and the raw **neg, neu, pos** split — so the result is **explainable**, not a black box.”

**[ON-SCREEN CALLOUT optional]:** `compound: -1 … +1`

---

## Scene D — Streamlit “Sentiment Lab” (5:30–8:00)

**Screen layout:** **Browser** **maximized** on the **Streamlit** tab — full **address bar** (e.g. `localhost:8501`). The **entire** app: title, text area, **Analyze** button, and **Settings** expander in sidebar should be visible; **scroll down only** when you show metrics + progress bar + JSON expander.

**On screen, in order:**  
1. Start from terminal if needed: `streamlit run streamlit_app.py` (can be **before** this scene).  
2. **Default** view: pre-filled text → click **Analyze** — **entire** result row: **Label**, **Class confidence**, **Compound**, **Model**, then the **progress bar** — keep **all** in one frame if possible; **one slow scroll** if not.  
3. Open **“Sample phrases”** — click **one** sample; **Execute** with **Analyze**; show **contrast** vs previous.  
4. **Sidebar:** expand **Settings**; toggle **“Call HTTP API”** **ON** (Uvicorn still running) — **re-analyze** — “same engine, this time over **HTTP**.”

**Narration:**  
> “The Streamlit app is a **stakeholder-friendly** view of the same logic: you can work **in-process** for fast demos, or point it at the **HTTP API** to mimic how a real client would call your service in production — same schema, same numbers.”

---

## Scene E — Recap, why VADER, CTA (8:00–9:30)

**Screen layout:** **GitHub** tab **full** again, or **README** file in IDE with **entire** “Run the API” section visible; **or** a simple **end card** (1920×1080 PNG) with: **subscribe**, **GitHub link**, “Day 2 coming.”

**Narration:**  
> “VADER is a **practical baseline** for short English: **fast**, **no training set**, and **interpretable** scores. Next steps in a real product might be a **transformer** or **multilingual** model — but the **API contract** you keep can stay the same. **Star the repo** if it helps, **subscribe** for the next day in the series, and I’ll see you in the next video.”

**End screen (if YouTube end cards):**  
- **Link 1:** GitHub repo.  
- **Link 2:** Your channel / playlist “100 Days of AI.”  
- **Subscribe** button.

---

## B-roll (optional, 2–4s each)

- Blurred code scroll in `src/sentiment_analyzer/service.py` (no need to read; **VADER** import visible).  
- **Terminal** with `uvicorn` line only (no environment secrets).

---

## Thumbnail (suggestion)

**Text (large, 2 lines max):**  
- Line 1: `Day 1`  
- Line 2: `SENTIMENT API` or `FastAPI + VADER`  
**Image:** Split — left: Swagger `POST` with green **200**; right: **Streamlit** with a bold “POSITIVE” metric. **High contrast**; readable on mobile.

---

## YouTube Shorts (60s variant)

1. **0:00–0:08** — Face or title card: “**Sentiment API in 15 seconds?** I’ll show the result.” **Vertical 1080×1920** if true Shorts; or crop 1:1.  
2. **0:08–0:25** — **Full-screen** `/docs` → one **POST** → **only** the **JSON response** zoomed, **spelled out:** “positive, confidence, compound.”  
3. **0:25–0:40** — **Streamlit** full screen → **Analyze** once → **metrics** in frame.  
4. **0:40–0:55** — GitHub on screen: “**Link below**.”  
5. **0:55–0:60** — **Subscribe** + repo URL as text on screen.  

**No** long terminal installs in Shorts — say “**full tutorial on the long video**.”

---

## Checklist before upload

- [ ] Every critical click shows **fingers** or **cursor** on the **right** control; **no** empty dead air >3s.  
- [ ] **No** secrets, **no** extra inbox/email tabs.  
- [ ] Chapters pasted; **link** to GitHub in description **first** line under first sentence.  
- [ ] Thumbnail and title both mention **Day 1** or **100 Days** (series discoverability).  

---

*File: `YOUTUBE_SCRIPT.md` — part of the Day 1 project deliverables. Update timestamps after you record.*
