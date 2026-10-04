"""
Aegis — Adversarial Agent.

Generates synthetic hostile caller messages driven by a persona prompt.
Uses role-swapping so the adversary sees itself as "assistant" in its own context.
"""

import openai as openai_module
from config.settings import AGENT_MODEL
from utils.openai_client import chat_completion, OpenAIClientError


def _swap_roles(conversation_history: list[dict]) -> list[dict]:
    """
    Swap "user" ↔ "assistant" roles in the conversation history.

    The shared transcript uses the target's perspective (caller = user, target = assistant).
    The adversary needs the OPPOSITE perspective (itself = assistant, target = user).

    Args:
        conversation_history: Transcript from the target's point of view.

    Returns:
        A new list with swapped roles.
    """
    swapped = []
    for msg in conversation_history:
        new_role = "assistant" if msg["role"] == "user" else "user"
        swapped.append({"role": new_role, "content": msg["content"]})
    return swapped


def get_adversary_message(
    client: openai_module.OpenAI,
    persona_system_prompt: str,
    conversation_history: list[dict],
) -> str:
    """
    Generate the next adversarial caller message.

    Args:
        client: Authenticated OpenAI client.
        persona_system_prompt: The selected persona's system prompt.
        conversation_history: Transcript from the target's perspective.
                              Will be role-swapped before sending to the adversary.

    Returns:
        The adversary's next message string.

    Raises:
        OpenAIClientError: On any API or auth failure.
    """
    # Role-swap so the adversary sees itself as "assistant"
    adversary_history = _swap_roles(conversation_history)

    messages = [
        {"role": "system", "content": persona_system_prompt},
        *adversary_history,
    ]

    return chat_completion(
        client=client,
        model=AGENT_MODEL,
        messages=messages,
        temperature=0.9,  # Higher temp for more creative/unpredictable attacks
    )
