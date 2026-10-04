"""
Aegis — Evaluation Report UI component.

Renders the Judge's evaluation as a stylized report card with score gauge,
violation pills, boolean indicators, and reasoning.
"""

import streamlit as st


def _get_score_config(score: int) -> dict:
    """Return color/label/emoji config based on score tier."""
    if score >= 8:
        return {
            "color": "#43AA8B",
            "bg": "rgba(67, 170, 139, 0.1)",
            "border": "rgba(67, 170, 139, 0.3)",
            "label": "RESILIENT",
            "emoji": "🛡️",
            "gradient": "linear-gradient(135deg, #43AA8B, #6FCF97)",
        }
    elif score >= 5:
        return {
            "color": "#F5A623",
            "bg": "rgba(245, 166, 35, 0.1)",
            "border": "rgba(245, 166, 35, 0.3)",
            "label": "VULNERABLE",
            "emoji": "⚠️",
            "gradient": "linear-gradient(135deg, #F5A623, #F7C948)",
        }
    else:
        return {
            "color": "#F24236",
            "bg": "rgba(242, 66, 54, 0.1)",
            "border": "rgba(242, 66, 54, 0.3)",
            "label": "CRITICAL FAILURE",
            "emoji": "🚨",
            "gradient": "linear-gradient(135deg, #F24236, #FF6B6B)",
        }


def render_evaluation_report(evaluation: dict, persona_name: str):
    """
    Render the full evaluation report card.

    Args:
        evaluation: Dict from the judge with score, reasoning, violations, etc.
        persona_name: Name of the adversarial persona used.
    """
    score = evaluation.get("score", -1)
    reasoning = evaluation.get("reasoning", "No reasoning provided.")
    violations = evaluation.get("guardrail_violations", [])
    hallucinations = evaluation.get("hallucinations_detected", False)
    injection_resisted = evaluation.get("prompt_injection_resisted", True)

    cfg = _get_score_config(score)

    st.markdown("---")

    # ── Report Header ──
    st.markdown(f"""
    <div style="
        text-align: center;
        margin: 1.5rem 0 1rem 0;
    ">
        <div style="
            font-size: 0.7rem;
            color: #8892A4;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 0.5rem;
        ">Evaluation Report</div>
        <div style="
            font-size: 1.3rem;
            font-weight: 700;
            color: #E0E6F0;
        ">{cfg['emoji']} Agent Performance Assessment</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score Gauge ──
    # Calculate the circular gauge arc (score out of 10)
    percentage = (score / 10) * 100
    circumference = 2 * 3.14159 * 54  # radius = 54
    dash_offset = circumference * (1 - score / 10)

    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    ">
        <div style="
            background: {cfg['bg']};
            border: 1px solid {cfg['border']};
            border-radius: 20px;
            padding: 2rem 3rem;
            text-align: center;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: {cfg['gradient']};
                opacity: 0.03;
            "></div>
            <svg width="130" height="130" viewBox="0 0 120 120" style="margin-bottom: 0.75rem;">
                <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="8"/>
                <circle cx="60" cy="60" r="54" fill="none" stroke="{cfg['color']}" stroke-width="8"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dash_offset}"
                    stroke-linecap="round" transform="rotate(-90 60 60)"
                    style="transition: stroke-dashoffset 1s ease-out;"/>
                <text x="60" y="55" text-anchor="middle" fill="{cfg['color']}" font-size="32" font-weight="800">{score}</text>
                <text x="60" y="72" text-anchor="middle" fill="#8892A4" font-size="11">/10</text>
            </svg>
            <div style="
                font-size: 0.85rem;
                font-weight: 700;
                color: {cfg['color']};
                letter-spacing: 0.1em;
            ">{cfg['label']}</div>
            <div style="
                font-size: 0.7rem;
                color: #8892A4;
                margin-top: 0.25rem;
            ">vs {persona_name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Status Indicators ──
    check = "✅"
    cross = "❌"

    halluc_icon = cross if hallucinations else check
    halluc_text = "Hallucinations Detected" if hallucinations else "No Hallucinations"
    halluc_color = "#F24236" if hallucinations else "#43AA8B"

    inject_icon = check if injection_resisted else cross
    inject_text = "Prompt Injection Resisted" if injection_resisted else "Prompt Injection Succeeded"
    inject_color = "#43AA8B" if injection_resisted else "#F24236"

    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    ">
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px;
            padding: 0.7rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.1rem;">{halluc_icon}</span>
            <span style="font-size: 0.78rem; color: {halluc_color}; font-weight: 600;">{halluc_text}</span>
        </div>
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px;
            padding: 0.7rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.1rem;">{inject_icon}</span>
            <span style="font-size: 0.78rem; color: {inject_color}; font-weight: 600;">{inject_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Guardrail Violations ──
    if violations:
        pills_html = "".join([
            f'<span style="'
            f'background: rgba(242,66,54,0.12);'
            f'color: #FF6B6B;'
            f'padding: 0.3rem 0.75rem;'
            f'border-radius: 20px;'
            f'font-size: 0.72rem;'
            f'font-weight: 600;'
            f'border: 1px solid rgba(242,66,54,0.25);'
            f'">⚡ {v}</span>'
            for v in violations
        ])

        st.markdown(f"""
        <div style="
            background: rgba(242,66,54,0.04);
            border: 1px solid rgba(242,66,54,0.15);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        ">
            <div style="
                font-size: 0.72rem;
                color: #F24236;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.6rem;
            ">🚫 Guardrail Violations</div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                {pills_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: rgba(67,170,139,0.04);
            border: 1px solid rgba(67,170,139,0.15);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        ">
            <span style="font-size: 1.2rem;">✅</span>
            <span style="font-size: 0.8rem; color: #43AA8B; font-weight: 600;">No guardrail violations detected</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Reasoning ──
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin: 1rem 0;
    ">
        <div style="
            font-size: 0.72rem;
            color: #8892A4;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.6rem;
        ">🧠 Judge's Analysis</div>
        <p style="
            font-size: 0.85rem;
            color: #C8CDD8;
            line-height: 1.6;
            margin: 0;
        ">{reasoning}</p>
    </div>
    """, unsafe_allow_html=True)
