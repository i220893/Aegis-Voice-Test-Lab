"""
Aegis — Thin wrapper around the OpenAI Python client.

Centralizes client creation, error handling, and retry logic.
"""

import openai
import time
from config.settings import API_TIMEOUT


class OpenAIClientError(Exception):
    """Custom exception for OpenAI client errors with user-friendly messages."""
    pass


def create_client(api_key: str) -> openai.OpenAI:
    """
    Create and return an OpenAI client instance.
    
    Args:
        api_key: The OpenAI API key.
    
    Returns:
        An authenticated OpenAI client.
    
    Raises:
        OpenAIClientError: If the API key is empty or invalid.
    """
    if not api_key or not api_key.strip():
        raise OpenAIClientError("API key is required. Please enter your OpenAI API key in the sidebar.")
    
    return openai.OpenAI(api_key=api_key.strip(), timeout=API_TIMEOUT)


def chat_completion(
    client: openai.OpenAI,
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_retries: int = 2,
) -> str:
    """
    Send a chat completion request with retry logic.
    
    Args:
        client: Authenticated OpenAI client.
        model: Model name (e.g., "gpt-4o-mini").
        messages: List of message dicts with "role" and "content" keys.
        temperature: Sampling temperature (0.0–2.0).
        max_retries: Number of retries on transient failures.
    
    Returns:
        The assistant's response text.
    
    Raises:
        OpenAIClientError: On authentication, rate limit, or persistent API errors.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            content = response.choices[0].message.content
            if content is None:
                return "[Agent did not respond]"
            return content.strip()

        except openai.AuthenticationError:
            raise OpenAIClientError(
                "Invalid API key. Please check your OpenAI API key and try again."
            )

        except openai.RateLimitError as e:
            last_error = e
            if attempt < max_retries:
                wait_time = 2 ** (attempt + 1)  # 2s, 4s exponential backoff
                time.sleep(wait_time)
            else:
                raise OpenAIClientError(
                    f"Rate limit exceeded after {max_retries + 1} attempts. "
                    "Please wait a moment and try again."
                )

        except openai.APITimeoutError:
            last_error = openai.APITimeoutError("Request timed out")
            if attempt < max_retries:
                time.sleep(1)
            else:
                raise OpenAIClientError(
                    f"Request timed out after {API_TIMEOUT} seconds. "
                    "The API may be experiencing high load."
                )

        except openai.APIError as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(1)
            else:
                raise OpenAIClientError(
                    f"OpenAI API error: {str(e)}"
                )

    # Should not reach here, but just in case
    raise OpenAIClientError(f"Unexpected error: {str(last_error)}")
