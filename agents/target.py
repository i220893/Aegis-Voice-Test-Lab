"""
Aegis — Target Agent.

The "system under test": a bank customer service bot with strict guardrails.
"""

import openai as openai_module
from config.settings import TARGET_SYSTEM_PROMPT, AGENT_MODEL
from utils.openai_client import chat_completion, OpenAIClientError


def get_target_response(
    client: openai_module.OpenAI,
    conversation_history: list[dict],
) -> str:
    """
    Generate the Target Agent's reply given the conversation so far.

    The conversation_history uses the target's perspective:
      - "user" role    = the caller's messages
      - "assistant" role = the target's own previous replies

    Args:
        client: Authenticated OpenAI client.
        conversation_history: List of {"role": ..., "content": ...} dicts
                              from the target agent's point of view.

    Returns:
        The target agent's response string.

    Raises:
        OpenAIClientError: On any API or auth failure.
    """
    messages = [
        {"role": "system", "content": TARGET_SYSTEM_PROMPT},
        *conversation_history,
    ]

    return chat_completion(
        client=client,
        model=AGENT_MODEL,
        messages=messages,
        temperature=0.4,  # Lower temp for more consistent, rule-following behavior
    )
