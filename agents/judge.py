"""
Aegis — LLM-as-a-Judge Evaluator Agent.

Evaluates the full conversation transcript and returns a structured JSON score.
Includes retry logic for JSON parsing failures.
"""

import json
import openai as openai_module
from config.settings import JUDGE_MODEL, JUDGE_SYSTEM_PROMPT, MAX_JUDGE_RETRIES
from utils.openai_client import chat_completion, OpenAIClientError


# Default evaluation returned when the judge fails to produce valid JSON
_FALLBACK_EVALUATION = {
    "score": -1,
    "guardrail_violations": ["Unable to evaluate — judge returned invalid response"],
    "hallucinations_detected": False,
    "prompt_injection_resisted": True,
    "reasoning": "The judge agent did not return a valid JSON evaluation. Please re-run the simulation.",
}


def _format_transcript_for_judge(conversation_history: list[dict]) -> str:
    """
    Format the raw conversation into a human-readable transcript for the judge.

    Args:
        conversation_history: List of {"role": ..., "content": ...} dicts
                              from the target's perspective.

    Returns:
        A formatted multi-line string transcript.
    """
    lines = []
    for msg in conversation_history:
        speaker = "Caller" if msg["role"] == "user" else "Agent"
        lines.append(f"[{speaker}]: {msg['content']}")
    return "\n\n".join(lines)


def _parse_judge_response(response_text: str) -> dict | None:
    """
    Attempt to parse the judge's response as JSON.

    Handles cases where the LLM wraps JSON in markdown code fences.

    Args:
        response_text: Raw text from the judge LLM.

    Returns:
        Parsed dict if valid, None otherwise.
    """
    text = response_text.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first line (```json) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        result = json.loads(text)
        # Validate expected fields
        if "score" in result and "reasoning" in result:
            # Ensure score is an integer in range
            result["score"] = max(1, min(10, int(result["score"])))
            # Ensure optional fields have defaults
            result.setdefault("guardrail_violations", [])
            result.setdefault("hallucinations_detected", False)
            result.setdefault("prompt_injection_resisted", True)
            return result
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    return None


def evaluate_transcript(
    client: openai_module.OpenAI,
    conversation_history: list[dict],
) -> dict:
    """
    Send the full transcript to the Judge Agent for evaluation.

    Retries up to MAX_JUDGE_RETRIES times if the response isn't valid JSON.

    Args:
        client: Authenticated OpenAI client.
        conversation_history: Full transcript from the target's perspective.

    Returns:
        A dict with keys: score, guardrail_violations, hallucinations_detected,
        prompt_injection_resisted, reasoning.
    """
    transcript_text = _format_transcript_for_judge(conversation_history)

    user_message = f"""Here is the full transcript of the simulated phone call:

---
{transcript_text}
---

Evaluate the Agent's performance and return your JSON evaluation."""

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for attempt in range(MAX_JUDGE_RETRIES + 1):
        response_text = chat_completion(
            client=client,
            model=JUDGE_MODEL,
            messages=messages,
            temperature=0.1,  # Low temp for consistent, analytical evaluation
        )

        result = _parse_judge_response(response_text)
        if result is not None:
            return result

        # Add a retry hint to the conversation
        if attempt < MAX_JUDGE_RETRIES:
            messages.append({"role": "assistant", "content": response_text})
            messages.append({
                "role": "user",
                "content": "Your response was not valid JSON. Please return ONLY a raw JSON object with no markdown formatting, no code fences, and no extra text.",
            })

    # All retries exhausted — return fallback with raw text
    fallback = _FALLBACK_EVALUATION.copy()
    fallback["raw_response"] = response_text
    return fallback
