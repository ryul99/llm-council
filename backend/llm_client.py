"""LiteLLM client for making LLM requests."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import litellm


def _extract_message_content(response: Any) -> Optional[str]:
    """
    Best-effort extraction of the first choice's message content from a LiteLLM response.
    LiteLLM generally returns an OpenAI-compatible shape, but may be dict-like or object-like.
    """
    try:
        return response["choices"][0]["message"].get("content")
    except Exception:
        pass

    try:
        return response.choices[0].message.content
    except Exception:
        return None


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0,
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via LiteLLM (direct provider calls; no proxy required).

    Args:
        model: LiteLLM model name (provider-native, e.g. "gpt-4o-mini")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' (or None if failed)
    """

    try:
        response = await litellm.acompletion(  # type: ignore[attr-defined]
            model=model,
            messages=messages,
            timeout=timeout,
        )
        return {"content": _extract_message_content(response)}
    except TypeError:
        # Some LiteLLM/provider backends may not accept `timeout`; retry without it.
        try:
            response = await litellm.acompletion(  # type: ignore[attr-defined]
                model=model,
                messages=messages,
            )
            return {"content": _extract_message_content(response)}
        except Exception as e:
            print(f"Error querying model {model}: {e}")
            return None
    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]],
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of LiteLLM model names
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model name to response dict (or None if failed)
    """
    import asyncio

    tasks = [query_model(model, messages) for model in models]
    responses = await asyncio.gather(*tasks)
    return {model: response for model, response in zip(models, responses)}
