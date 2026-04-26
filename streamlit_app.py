"""
Premium Streamlit client — same VADER engine as the API.
Run: pip install -e .[ui] && streamlit run streamlit_app.py
"""

from __future__ import annotations

import html
import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
_src = _root / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import httpx  # noqa: E402
import streamlit as st  # noqa: E402

from sentiment_analyzer.service import analyze_sentiment  # noqa: E402

st.set_page_config(
    page_title="Sentiment Lab",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_DEFAULT = (
    "I love this product — shipping was fast and the quality exceeded my expectations."
)
if "t" not in st.session_state:
    st.session_state.t = _DEFAULT

SAMPLES = [
    "This is the best launch we've had — the team really delivered.",
    "Terrible support. Still waiting for a refund. Very disappointed.",
    "The meeting is at 3pm tomorrow. Please join the call.",
    "Absolutely thrilled — five stars, would recommend to everyone.",
    "Worst experience I've had on this platform. Never again.",
    "Please find the Q3 report attached. Let me know if you need the raw data.",
    "Flight is at 4:20pm, gate 12, terminal B. See you there.",
    "Not bad, could be a bit faster, but it gets the job done.",
    "I'm furious. Three follow-ups and nobody has called me back.",
    "Thank you — that was exactly the fix I needed. Really appreciate the quick help.",
    "Waste of money. Broke after two days and the warranty is useless.",
    "Oh great, another delay. Just what I needed today.",
    "The file is 14 pages, mostly tables. Summary is on page 2.",
    "Loving this so far! Interface is clean and the export just works.",
]


def _set_sample(s: str) -> None:
    st.session_state.t = s


def _sentiment_theme(label: str) -> dict[str, str]:
    """Colors for the result card + bar. label is 'positive' | 'negative' | 'neutral'."""
    if label == "positive":
        return {
            "name": "Positive",
            "bar_css": "linear-gradient(90deg, #0d4d3a 0%, #1fa968 50%, #3ecf8e 100%)",
            "glow": "rgba(62, 207, 142, 0.22)",
            "border": "rgba(62, 207, 142, 0.45)",
            "badge_bg": "linear-gradient(135deg, #143d32 0%, #0f2a24 100%)",
            "badge_text": "#9df5d1",
            "track": "rgba(255,255,255,0.06)",
        }
    if label == "negative":
        return {
            "name": "Negative",
            "bar_css": "linear-gradient(90deg, #5c1f2b 0%, #c73e4d 50%, #ff7a7a 100%)",
            "glow": "rgba(255, 107, 107, 0.2)",
            "border": "rgba(255, 107, 107, 0.45)",
            "badge_bg": "linear-gradient(135deg, #3d1a1f 0%, #2a1216 100%)",
            "badge_text": "#ffb8b8",
            "track": "rgba(255,255,255,0.06)",
        }
    return {
        "name": "Neutral",
        "bar_css": "linear-gradient(90deg, #3d4857 0%, #6b7b8c 50%, #9aa4b2 100%)",
        "glow": "rgba(154, 164, 178, 0.18)",
        "border": "rgba(138, 155, 175, 0.45)",
        "badge_bg": "linear-gradient(135deg, #1e242d 0%, #181d24 100%)",
        "badge_text": "#c5ced9",
        "track": "rgba(255,255,255,0.08)",
    }


def _render_sentiment_bar(width_pct: float, theme: dict[str, str]) -> None:
    w = min(max(width_pct, 0.0), 100.0)
    st.markdown(
        f"""
        <div class="sbar-wrap" style="margin: 0.25rem 0 0.1rem 0;">
          <div style="display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 0.4rem; font-size: 0.78rem; color: #7d8a9a; letter-spacing: 0.04em; text-transform: uppercase;">
            <span>Negative</span>
            <span>Neutral</span>
            <span>Positive</span>
          </div>
          <div style="height: 12px; border-radius: 999px; background: {theme['track']};
            overflow: hidden; box-shadow: inset 0 1px 2px rgba(0,0,0,0.35);">
            <div style="width: {w:.1f}%; height: 100%; border-radius: 999px; background: {theme['bar_css']};
              box-shadow: 0 0 20px {theme['glow']};
              transition: width 0.4s ease;"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


_PREMIUM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg0: #080a0d;
    --bg1: #0c0e12;
    --card: #12161d;
    --card2: #161b24;
    --border: #2a313c;
    --text: #e8edf4;
    --muted: #8b99ad;
    --pos: #3ecf8e;
    --neg: #ff6b6b;
    --neu: #9aa4b2;
  }
  html, body, .stApp { font-family: 'Outfit', system-ui, -apple-system, sans-serif !important; }
  .stApp {
    background: radial-gradient(120% 80% at 10% 0%, #141a2e 0%, var(--bg0) 45%, var(--bg1) 100%) !important;
  }
  h1, h2, h3 { color: var(--text) !important; font-weight: 600 !important; letter-spacing: -0.03em !important; }
  .subtle-h { color: #b4c0d4 !important; font-weight: 500 !important; font-size: 0.95rem !important; margin-top: 0.5rem; }
  div[data-testid="stTextArea"] textarea {
    background: var(--card) !important; color: var(--text) !important;
    border: 1px solid var(--border) !important; border-radius: 14px !important; min-height: 180px;
    font-size: 1.02rem !important; line-height: 1.5 !important;
  }
  .stButton > button {
    background: linear-gradient(145deg, #4e7dff 0%, #3b52d5 100%) !important; color: #fff !important;
    border: none !important; border-radius: 12px !important; font-weight: 600 !important;
    box-shadow: 0 4px 24px rgba(75, 120, 255, 0.25) !important; padding: 0.55rem 1.25rem !important;
  }
  .stButton > button:hover { filter: brightness(1.05); }
  [data-testid="stExpander"] {
    background: var(--card2) !important; border: 1px solid var(--border) !important; border-radius: 14px !important;
  }
  [data-testid="stExpander"] summary { font-weight: 500 !important; }
  [data-baseweb="select"] { border-radius: 10px; }
  [data-testid="column"] [data-testid="stMetric"] {
    background: rgba(0,0,0,0.2); padding: 0.9rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);
  }
  [data-testid="stMetric"] label { color: #8b9aaf !important; }
  [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f0f4fa !important; }
</style>
"""
st.markdown(_PREMIUM_CSS, unsafe_allow_html=True)

st.sidebar.title("Settings")
use_api = st.sidebar.toggle(
    "Call HTTP API",
    value=False,
    help="If on, call the running FastAPI service (start Uvicorn first). If off, local engine (identical).",
)
api_base = st.sidebar.text_input("API base URL", value=os.environ.get("SENTIMENT_API_BASE", "http://127.0.0.1:8000"))


@st.cache_data(show_spinner=False, ttl=60)
def _via_api(text: str, base: str) -> dict:
    with httpx.Client(base_url=base.rstrip("/"), timeout=30.0) as client:
        r = client.post("/api/v1/sentiment", json={"text": text})
        r.raise_for_status()
        return r.json()


top_l, top_r = st.columns([2, 1])
with top_l:
    st.title("Sentiment Lab")
    st.markdown(
        "<p class='subtle-h'>VADER lexicon · explainable scores · no training step · best on short English</p>",
        unsafe_allow_html=True,
    )
with top_r:
    st.caption("Day 1 · Deepak")
    st.caption("[deepakradhakrishnan.com](https://www.deepakradhakrishnan.com)")

st.markdown("### Analyze text")
with st.expander("**Sample phrases** — tap to load"):
    for i, s in enumerate(SAMPLES):
        st.button(
            s[:70] + ("…" if len(s) > 70 else ""),
            key=f"sample_{i}",
            on_click=_set_sample,
            args=(s,),
        )

text = st.text_area("Input", label_visibility="collapsed", key="t", height=200, placeholder="Paste or type text…")
cols = st.columns([1, 3])
with cols[0]:
    go = st.button("Analyze", type="primary", use_container_width=True)

if go:
    t = (text or "").strip()
    if not t:
        st.warning("Enter some text to analyze.")
    else:
        with st.spinner("Scoring with VADER…"):
            try:
                if use_api:
                    out = _via_api(t, api_base)
                else:
                    r = analyze_sentiment(t)
                    out = r.model_dump(mode="json")
            except httpx.HTTPError as e:  # noqa: BLE001
                st.error(f"API error: {e!s}")
            except Exception as e:  # noqa: BLE001
                st.error(f"Error: {e!s}")
            else:
                label = str(out["label"]).lower()
                conf = out["confidence"]
                compound = float(out["compound"])
                scores = out.get("scores", {})
                th = _sentiment_theme(label)
                width_pct = (compound + 1) / 2 * 100.0

                st.divider()
                st.markdown(
                    f"""
                    <div style="padding: 1rem 1.1rem; margin: 0 0 0.75rem 0; border-radius: 16px; border: 1px solid {th['border']};
                      background: linear-gradient(160deg, rgba(18, 22, 29, 0.95) 0%, rgba(10, 12, 16, 0.98) 100%);
                      box-shadow: 0 0 0 1px rgba(0,0,0,0.2), 0 12px 40px -8px {th['glow']};
                      display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                      <div style="display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
                        background: {th['badge_bg']}; color: {th['badge_text']}; border: 1px solid {th['border']};">
                        {html.escape(th['name'])}
                      </div>
                      <span style="color: #7d8a9a; font-size: 0.9rem;">Sentiment for your input</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                a, b, c, d = st.columns(4)
                with a:
                    st.metric("Label", label.upper())
                with b:
                    st.metric("Class confidence", f"{conf * 100:.1f}%" if conf <= 1 else f"{conf}")
                with c:
                    st.metric("Compound", f"{compound:+.3f}")
                with d:
                    st.metric("Model", out.get("model", "VADER"))

                _render_sentiment_bar(width_pct, th)

                with st.expander("Raw scores & JSON", expanded=False):
                    st.json({"label": out["label"], "confidence": conf, "compound": compound, "scores": scores})

st.divider()
st.caption("API: `uvicorn sentiment_analyzer.main:app --reload` → http://127.0.0.1:8000/docs · GitHub: @dpkrobomad")
