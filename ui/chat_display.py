"""
Aegis — Chat Display UI component.

Renders the live conversation between the adversary and target agents
with styled chat bubbles.
"""

import streamlit as st


def render_chat_message(role: str, content: str, turn_number: int = 0):
    """
    Render a single chat message with custom styling.

    Args:
        role: "adversary" or "target"
        content: The message text
        turn_number: Current turn number (for the label)
    """
    if role == "adversary":
        icon = "🔴"
        label = "Adversarial Caller"
        bg_color = "rgba(242, 66, 54, 0.08)"
        border_color = "rgba(242, 66, 54, 0.25)"
        label_color = "#F24236"
        align = "flex-start"
    else:
        icon = "🟢"
        label = "Target Agent"
        bg_color = "rgba(67, 170, 139, 0.08)"
        border_color = "rgba(67, 170, 139, 0.25)"
        label_color = "#43AA8B"
        align = "flex-end"

    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: {align};
        margin-bottom: 1rem;
    ">
        <div style="
            font-size: 0.68rem;
            font-weight: 600;
            color: {label_color};
            margin-bottom: 0.3rem;
            letter-spacing: 0.03em;
        ">{icon} {label}</div>
        <div style="
            background: {bg_color};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 0.85rem 1.1rem;
            max-width: 85%;
            line-height: 1.55;
            font-size: 0.88rem;
            color: #E0E6F0;
        ">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_turn_divider(turn_number: int, total_turns: int):
    """
    Render a divider between turns showing progress.

    Args:
        turn_number: Current turn (1-indexed).
        total_turns: Total number of turns.
    """
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0.75rem 0;
        opacity: 0.4;
    ">
        <div style="flex: 1; height: 1px; background: linear-gradient(to right, transparent, #8892A4);"></div>
        <span style="font-size: 0.65rem; color: #8892A4; letter-spacing: 0.08em; text-transform: uppercase;">
            Turn {turn_number} of {total_turns}
        </span>
        <div style="flex: 1; height: 1px; background: linear-gradient(to left, transparent, #8892A4);"></div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_header(persona_name: str):
    """
    Render the chat window header.

    Args:
        persona_name: Display name of the active persona.
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(242,66,54,0.06), rgba(67,170,139,0.06));
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <div style="font-size: 0.68rem; color: #8892A4; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.25rem;">
                Live Simulation
            </div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #E0E6F0;">
                🔴 {persona_name} &nbsp;vs&nbsp; 🟢 Apex Bank Agent
            </div>
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 0.4rem;
        ">
            <div style="
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #F24236;
                animation: pulse 1.5s ease-in-out infinite;
            "></div>
            <span style="font-size: 0.7rem; color: #F24236; font-weight: 600;">LIVE</span>
        </div>
    </div>
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
    </style>
    """, unsafe_allow_html=True)


def render_thinking_indicator(agent_name: str):
    """
    Render a 'thinking' indicator while waiting for an agent response.

    Args:
        agent_name: "Adversary" or "Target Agent"
    """
    color = "#F24236" if "Adversary" in agent_name or "Caller" in agent_name else "#43AA8B"
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
    ">
        <div style="
            display: flex;
            gap: 0.25rem;
        ">
            <div style="width:6px;height:6px;border-radius:50%;background:{color};animation:bounce 1.4s infinite ease-in-out both;animation-delay:-0.32s;"></div>
            <div style="width:6px;height:6px;border-radius:50%;background:{color};animation:bounce 1.4s infinite ease-in-out both;animation-delay:-0.16s;"></div>
            <div style="width:6px;height:6px;border-radius:50%;background:{color};animation:bounce 1.4s infinite ease-in-out both;"></div>
        </div>
        <span style="font-size: 0.72rem; color: #8892A4;">{agent_name} is thinking...</span>
    </div>
    <style>
        @keyframes bounce {{
            0%, 80%, 100% {{ transform: scale(0); opacity: 0.3; }}
            40% {{ transform: scale(1.0); opacity: 1; }}
        }}
    </style>
    """, unsafe_allow_html=True)
