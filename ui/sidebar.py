"""
Aegis — Sidebar UI component.

Renders the configuration sidebar: API key input, persona selector, and controls.
"""

import streamlit as st
from config.personas import PERSONAS


def render_sidebar() -> dict:
    """
    Render the sidebar and return the current configuration.

    Returns:
        dict with keys:
          - api_key (str): The entered OpenAI API key
          - persona (dict): The selected persona config
          - turn_count (int): Number of simulation turns
          - run_clicked (bool): Whether the Run button was clicked
    """
    with st.sidebar:
        # ── Logo / Branding ──
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.25rem;">🛡️</div>
            <div style="
                font-size: 1.6rem;
                font-weight: 800;
                background: linear-gradient(135deg, #F24236, #FF6B6B);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 0.05em;
            ">AEGIS</div>
            <div style="
                font-size: 0.7rem;
                color: #8892A4;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                margin-top: 0.15rem;
            ">Voice Agent Test Lab</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── API Key ──
        st.markdown("##### 🔑 OpenAI API Key")
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-...",
            label_visibility="collapsed",
            help="Your key is never stored. It's used only for this session.",
        )

        if not api_key:
            st.warning("Enter your API key to begin.", icon="⚠️")

        st.markdown("---")

        # ── Persona Selector ──
        st.markdown("##### 🎭 Adversarial Persona")

        # Build display options
        persona_options = [f'{p["icon"]} {p["name"]}' for p in PERSONAS]
        selected_index = st.selectbox(
            "Select Persona",
            range(len(PERSONAS)),
            format_func=lambda i: persona_options[i],
            label_visibility="collapsed",
        )

        selected_persona = PERSONAS[selected_index]

        # Persona info card
        difficulty_colors = {
            "Easy": "#43AA8B",
            "Medium": "#F5A623",
            "Hard": "#F24236",
        }
        diff_color = difficulty_colors.get(selected_persona["difficulty"], "#888")

        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 8px;
            padding: 0.75rem;
            margin-top: 0.5rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 0.8rem; font-weight: 600;">Difficulty</span>
                <span style="
                    background: {diff_color}22;
                    color: {diff_color};
                    padding: 0.15rem 0.5rem;
                    border-radius: 12px;
                    font-size: 0.7rem;
                    font-weight: 700;
                    border: 1px solid {diff_color}44;
                ">{selected_persona["difficulty"]}</span>
            </div>
            <p style="
                font-size: 0.75rem;
                color: #8892A4;
                line-height: 1.4;
                margin: 0;
            ">{selected_persona["description"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Turn Count ──
        st.markdown("##### ⚡ Simulation Turns")
        turn_count = st.slider(
            "Turns",
            min_value=1,
            max_value=10,
            value=3,
            label_visibility="collapsed",
            help="Number of back-and-forth exchanges between the adversary and the target.",
        )

        st.markdown("---")

        # ── Run Button ──
        can_run = bool(api_key) and not st.session_state.get("simulation_running", False)

        run_clicked = st.button(
            "🚀  Run Simulation" if not st.session_state.get("simulation_running", False) else "⏳  Simulation Running...",
            use_container_width=True,
            disabled=not can_run,
            type="primary",
        )

        # ── History Section ──
        if st.session_state.get("history"):
            st.markdown("---")
            st.markdown("##### 📊 Past Results")
            for i, entry in enumerate(reversed(st.session_state["history"])):
                score = entry["score"]
                persona_name = entry["persona"]
                if score >= 8:
                    color, label = "#43AA8B", "PASS"
                elif score >= 5:
                    color, label = "#F5A623", "WARN"
                else:
                    color, label = "#F24236", "FAIL"

                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0.4rem 0.6rem;
                    background: rgba(255,255,255,0.02);
                    border-radius: 6px;
                    margin-bottom: 0.3rem;
                    border-left: 3px solid {color};
                ">
                    <span style="font-size: 0.72rem; color: #8892A4;">{persona_name}</span>
                    <span style="
                        font-size: 0.68rem;
                        font-weight: 700;
                        color: {color};
                    ">{score}/10 {label}</span>
                </div>
                """, unsafe_allow_html=True)

    return {
        "api_key": api_key,
        "persona": selected_persona,
        "turn_count": turn_count,
        "run_clicked": run_clicked,
    }
