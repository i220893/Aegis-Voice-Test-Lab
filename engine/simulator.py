"""
Aegis — Simulation Engine.

Orchestrates the multi-turn adversarial conversation loop and final evaluation.
Uses a generator pattern so the Streamlit UI can live-update after each event.
"""

from typing import Generator
import openai as openai_module

from agents.adversary import get_adversary_message
from agents.target import get_target_response
from agents.judge import evaluate_transcript
from utils.openai_client import create_client, OpenAIClientError
from config.settings import DEFAULT_TURN_COUNT


# Event type constants
EVENT_ADVERSARY = "adversary"
EVENT_TARGET = "target"
EVENT_JUDGE_START = "judge_start"
EVENT_JUDGE_RESULT = "judge_result"
EVENT_ERROR = "error"
EVENT_INFO = "info"


def run_simulation(
    api_key: str,
    persona: dict,
    turn_count: int = DEFAULT_TURN_COUNT,
) -> Generator[tuple[str, any], None, None]:
    """
    Run a full adversarial simulation and yield events for live UI rendering.

    This is a generator that yields (event_type, payload) tuples:
      - ("info", str)           → Status messages (e.g., "Initializing...")
      - ("adversary", str)      → Adversary's message text
      - ("target", str)         → Target's reply text
      - ("judge_start", None)   → Judge evaluation has begun
      - ("judge_result", dict)  → Judge's evaluation result dict
      - ("error", str)          → Error message

    Args:
        api_key: OpenAI API key.
        persona: Persona dict from config/personas.py.
        turn_count: Number of adversary→target exchange rounds.

    Yields:
        Tuples of (event_type, payload).
    """
    # ── Initialize client ──
    try:
        client = create_client(api_key)
    except OpenAIClientError as e:
        yield (EVENT_ERROR, str(e))
        return

    yield (EVENT_INFO, f"Starting simulation with persona: {persona['name']}")

    # ── Conversation loop ──
    # Uses target's perspective: caller messages = "user", target replies = "assistant"
    conversation: list[dict] = []

    for turn in range(1, turn_count + 1):
        # --- Adversary's turn ---
        try:
            adv_message = get_adversary_message(
                client=client,
                persona_system_prompt=persona["system_prompt"],
                conversation_history=conversation,
            )
        except OpenAIClientError as e:
            yield (EVENT_ERROR, f"Adversary agent failed on turn {turn}: {e}")
            return

        conversation.append({"role": "user", "content": adv_message})
        yield (EVENT_ADVERSARY, adv_message)

        # --- Target's turn ---
        try:
            tgt_message = get_target_response(
                client=client,
                conversation_history=conversation,
            )
        except OpenAIClientError as e:
            yield (EVENT_ERROR, f"Target agent failed on turn {turn}: {e}")
            return

        conversation.append({"role": "assistant", "content": tgt_message})
        yield (EVENT_TARGET, tgt_message)

    # ── Judge evaluation ──
    yield (EVENT_JUDGE_START, None)

    try:
        evaluation = evaluate_transcript(
            client=client,
            conversation_history=conversation,
        )
    except OpenAIClientError as e:
        yield (EVENT_ERROR, f"Judge evaluation failed: {e}")
        return

    yield (EVENT_JUDGE_RESULT, evaluation)
