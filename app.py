"""
Aegis: Voice Agent Test Lab — Main Streamlit Application.

Multi-agent adversarial simulator for testing enterprise voice AI agents.
"""

import os
import streamlit as st
from ui.sidebar import render_sidebar
from ui.chat_display import (
    render_chat_header,
    render_chat_message,
    render_turn_divider,
)
from ui.report import render_evaluation_report
from engine.simulator import (
    run_simulation,
    EVENT_ADVERSARY,
    EVENT_TARGET,
    EVENT_JUDGE_START,
    EVENT_JUDGE_RESULT,
    EVENT_ERROR,
    EVENT_INFO,
)


# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Aegis — Voice Agent Test Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────
# Custom CSS — Premium Dark Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Main container ── */
    .stMainBlockContainer {
        max-width: 900px;
        padding-top: 2rem;
    }

    /* ── Header gradient text ── */
    .aegis-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .aegis-header h1 {
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #F24236 0%, #FF6B6B 40%, #43AA8B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .aegis-header .subtitle {
        font-size: 0.9rem;
        color: #8892A4;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    .aegis-header .tagline {
        font-size: 0.72rem;
        color: #5A6477;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* ── Cards ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* ── Status badges ── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    /* ── Sidebar tweaks ── */
    section[data-testid="stSidebar"] {
        background: #0D1117;
        border-right: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* ── Button styling ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #F24236, #E63946) !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(242, 66, 54, 0.3) !important;
    }

    /* ── Expander styling ── */
    .streamlit-expanderHeader {
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* ── Hide default Streamlit elements ── */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Secrets / Environment — API Key Fallback
# ──────────────────────────────────────────────
# Priority: st.secrets (Streamlit Cloud) > env var > empty (user must enter manually)
try:
    _default_api_key = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    _default_api_key = os.environ.get("OPENAI_API_KEY", "")


# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────
if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = False
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_persona" not in st.session_state:
    st.session_state.last_persona = None


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
config = render_sidebar(default_api_key=_default_api_key)


# ──────────────────────────────────────────────
# Main Content Area
# ──────────────────────────────────────────────

# ── Header ──
st.markdown("""
<div class="aegis-header">
    <h1>🛡️ Aegis Test Lab</h1>
    <div class="subtitle">Adversarial Voice Agent Simulator</div>
    <div class="tagline">Stress-test your AI agents against hostile callers before they reach production</div>
</div>
""", unsafe_allow_html=True)

# ── How It Works (shown when idle) ──
if not st.session_state.conversation and not st.session_state.simulation_running:
    st.markdown("""
    <div class="glass-card">
        <div style="
            font-size: 0.75rem;
            color: #8892A4;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
            font-weight: 600;
        ">How It Works</div>
        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 180px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.4rem;">🎭</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: #E0E6F0; margin-bottom: 0.25rem;">1. Choose a Persona</div>
                <div style="font-size: 0.72rem; color: #8892A4; line-height: 1.5;">Select an adversarial caller type from the sidebar — angry customer, hacker, confused caller, and more.</div>
            </div>
            <div style="flex: 1; min-width: 180px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.4rem;">⚔️</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: #E0E6F0; margin-bottom: 0.25rem;">2. Run Simulation</div>
                <div style="font-size: 0.72rem; color: #8892A4; line-height: 1.5;">The adversary attacks your agent in an automated multi-turn conversation. Watch the battle unfold in real-time.</div>
            </div>
            <div style="flex: 1; min-width: 180px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.4rem;">🧠</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: #E0E6F0; margin-bottom: 0.25rem;">3. Get Evaluated</div>
                <div style="font-size: 0.72rem; color: #8892A4; line-height: 1.5;">An LLM Judge scores your agent on guardrails, hallucinations, and prompt injection resistance.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture diagram
    with st.expander("📐  System Architecture", expanded=False):
        st.markdown("""
        ```
        ┌─────────────────┐     ┌─────────────────┐
        │  🔴 Adversarial │────▶│  🟢 Target      │
        │     Caller      │◀────│     Agent        │
        │  (Persona LLM)  │     │  (Bank CS Bot)   │
        └────────┬────────┘     └────────┬────────┘
                 │         3 turns        │
                 └──────────┬─────────────┘
                            ▼
                 ┌─────────────────┐
                 │  🟡 LLM Judge   │
                 │  (Evaluator)    │
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │  📊 Score &     │
                 │  Report Card    │
                 └─────────────────┘
        ```
        """)


# ──────────────────────────────────────────────
# Simulation Execution
# ──────────────────────────────────────────────
if config["run_clicked"] and config["api_key"]:
    # Reset state for new simulation
    st.session_state.conversation = []
    st.session_state.evaluation = None
    st.session_state.simulation_running = True
    st.session_state.last_persona = config["persona"]["name"]

    # Create a container for the live chat
    chat_container = st.container()

    with chat_container:
        render_chat_header(config["persona"]["name"])

    # Run the simulation generator
    turn_counter = 0
    message_in_turn = 0

    for event_type, payload in run_simulation(
        api_key=config["api_key"],
        persona=config["persona"],
        turn_count=config["turn_count"],
    ):
        with chat_container:
            if event_type == EVENT_INFO:
                st.toast(payload, icon="ℹ️")

            elif event_type == EVENT_ADVERSARY:
                message_in_turn += 1
                if message_in_turn % 2 == 1:
                    turn_counter += 1
                    render_turn_divider(turn_counter, config["turn_count"])
                render_chat_message("adversary", payload, turn_counter)
                st.session_state.conversation.append({
                    "role": "adversary",
                    "content": payload,
                })

            elif event_type == EVENT_TARGET:
                message_in_turn += 1
                render_chat_message("target", payload, turn_counter)
                st.session_state.conversation.append({
                    "role": "target",
                    "content": payload,
                })

            elif event_type == EVENT_JUDGE_START:
                st.markdown("""
                <div style="
                    text-align: center;
                    margin: 2rem 0 1rem 0;
                    padding: 1rem;
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
                    <div style="
                        font-size: 0.8rem;
                        color: #F5A623;
                        font-weight: 600;
                        letter-spacing: 0.05em;
                    ">Judge is evaluating the transcript...</div>
                </div>
                """, unsafe_allow_html=True)

            elif event_type == EVENT_JUDGE_RESULT:
                st.session_state.evaluation = payload
                # Add to history
                st.session_state.history.append({
                    "persona": config["persona"]["name"],
                    "score": payload.get("score", -1),
                    "evaluation": payload,
                })
                render_evaluation_report(payload, config["persona"]["name"])

            elif event_type == EVENT_ERROR:
                st.error(f"❌ {payload}", icon="🚨")

    st.session_state.simulation_running = False

# ── Display previous results (if any, and not currently running) ──
elif st.session_state.conversation and not st.session_state.simulation_running:
    render_chat_header(st.session_state.last_persona or "Unknown")

    turn_counter = 0
    for i, msg in enumerate(st.session_state.conversation):
        if msg["role"] == "adversary":
            turn_counter += 1
            render_turn_divider(turn_counter, len(st.session_state.conversation) // 2)
        render_chat_message(msg["role"], msg["content"], turn_counter)

    if st.session_state.evaluation:
        render_evaluation_report(
            st.session_state.evaluation,
            st.session_state.last_persona or "Unknown",
        )
