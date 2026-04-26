"""
Premium Streamlit client — same VADER engine as the API.
Run: pip install -e .[ui] && streamlit run streamlit_app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
_src = _root / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import streamlit as st  # noqa: E402
import httpx  # noqa: E402

from sentiment_analyzer.service import analyze_sentiment  # noqa: E402

st.set_page_config(
    page_title="Sentiment Lab",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "t" not in st.session_state:
    st.session_state.t = (
        "I love this product — shipping was fast and the quality exceeded my expectations."
    )

_PREMIUM_CSS = """
<style>
  :root { --bg: #0c0e12; --card: #141820; --border: #2a313c; --text: #e8edf4;
    --muted: #8b99ad; --accent: #5b8cff; --pos: #3ecf8e; --neg: #ff6b6b; --neu: #9aa4b2; }
  .stApp { background: var(--bg); }
  h1, h2, h3 { color: var(--text) !important; font-weight: 600 !important; letter-spacing: -0.02em; }
  .muted { color: var(--muted); font-size: 0.95rem; }
  div[data-testid="stTextArea"] textarea {
    background: var(--card) !important; color: var(--text) !important;
    border: 1px solid var(--border) !important; border-radius: 12px !important; min-height: 160px;
  }
  .stButton button {
    background: linear-gradient(135deg, #4f7cff, #3d5aef) !important; color: #fff !important;
    border: none !important; border-radius: 10px !important; font-weight: 600 !important;
  }
  [data-testid="stExpander"] { background: var(--card); border: 1px solid var(--border); border-radius: 12px; }
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


c1, c2 = st.columns([2, 1])
with c1:
    st.title("Sentiment Lab")
    st.markdown(
        "<p class='muted'>VADER lexicon + compound scoring · fast, explainable, no training required. "
        "Best for English short text (reviews, social, support).</p>",
        unsafe_allow_html=True,
    )
with c2:
    st.caption("Day 1 — 100 Days of AI with Python")
    try:
        import importlib.metadata as m

        st.caption(f"Streamlit {m.version('streamlit')}")
    except Exception:  # noqa: BLE001
        pass

st.subheader("Analyze text")
text = st.text_area("Input", label_visibility="collapsed", key="t", height=200, placeholder="Paste text…")
cols = st.columns([1, 3])
with cols[0]:
    go = st.button("Analyze", type="primary", use_container_width=True)

with st.expander("Sample phrases"):
    for i, s in enumerate(
        [
            "This is the best launch we've had — the team really delivered.",
            "Terrible support. Still waiting for a refund. Very disappointed.",
            "The meeting is at 3pm tomorrow. Please join the call.",
        ]
    ):
        if st.button(s[:70] + ("…" if len(s) > 70 else ""), key=f"sample_{i}"):
            st.session_state.t = s
            st.rerun()

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
                    out = r.model_dump()
            except httpx.HTTPError as e:  # noqa: BLE001
                st.error(f"API error: {e!s}")
            except Exception as e:  # noqa: BLE001
                st.error(f"Error: {e!s}")
            else:
                label = str(out["label"]).lower()
                conf = out["confidence"]
                compound = out["compound"]
                scores = out.get("scores", {})
                st.divider()
                a, b, c, d = st.columns(4)
                with a:
                    st.metric("Label", label.upper())
                with b:
                    st.metric("Class confidence", f"{conf * 100:.1f}%" if conf <= 1 else f"{conf}")
                with c:
                    st.metric("Compound", f"{compound:+.3f}")
                with d:
                    st.metric("Model", out.get("model", "VADER"))
                st.progress(
                    min(max((float(compound) + 1) / 2, 0.0), 1.0),
                    text="← negative   neutral   positive →",
                )
                with st.expander("Raw scores & JSON", expanded=False):
                    st.json({"label": out["label"], "confidence": conf, "compound": compound, "scores": scores})

st.divider()
st.caption("API: `uvicorn sentiment_analyzer.main:app --reload` → http://127.0.0.1:8000/docs")
