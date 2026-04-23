"""Shared OpenRouter helpers for research routing + synthesis sub-agents.

The research tool used to talk to Anthropic directly. We dropped Anthropic from
the project, so routing and synthesis now hit OpenRouter via the same
OpenAI-compatible chat-completions endpoint the main agent uses. The model is
pinned via the ``RESEARCH_LLM_MODEL`` env var and defaults to the main agent's
model so everything shares one rate-limit bucket.
"""
from __future__ import annotations

import os
import re
from typing import Any

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_DEFAULT_MODEL = "openai/gpt-oss-120b:free"
_CODE_FENCE_RE = re.compile(
    r"```(?:json)?\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL,
)


def research_model() -> str:
    return os.environ.get("RESEARCH_LLM_MODEL", _DEFAULT_MODEL)


def strip_json_fence(text: str) -> str:
    """Return the first JSON block stripped of markdown code fences.

    Reasoning-tuned models (GPT-OSS, Llama) often wrap JSON in ``` fences.
    json.loads() chokes on those — strip once, then the caller parses.
    """
    m = _CODE_FENCE_RE.search(text)
    return (m.group(1) if m else text).strip()


def openrouter_chat(
    http: Any,
    *,
    system: str,
    user: str,
    max_tokens: int,
    model: str | None = None,
    timeout: float = 60.0,
) -> str:
    """Call OpenRouter's chat-completions and return the response text.

    Raises on HTTP errors. The caller is responsible for catching and falling
    back — see RoutingAgent / SynthesisAgent for the fallback patterns.
    """
    payload: dict[str, Any] = {
        "model": model or research_model(),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Analytical Agent (research)",
    }
    resp = http.post(_OPENROUTER_URL, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    choices = data.get("choices") or [{}]
    message = choices[0].get("message") or {}
    return str(message.get("content") or "")
