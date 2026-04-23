from __future__ import annotations

import logging
from typing import Any

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    ToolCall,
)
from app.harness.config import ModelProfile

logger = logging.getLogger(__name__)

# Error substrings that signal the model doesn't support thinking at all.
_THINKING_UNSUPPORTED_PATTERNS = (
    "thinking is not supported",
    "extended thinking is not supported",
    "does not support thinking",
)

# Error substrings that signal the budget value is invalid (too low, too high,
# or not accepted for this model). We retry without thinking in this case too.
_THINKING_BUDGET_INVALID_PATTERNS = (
    "budget_tokens",
    "thinking budget",
    "minimum budget",
    "maximum budget",
)


def _is_thinking_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(p in msg for p in _THINKING_UNSUPPORTED_PATTERNS + _THINKING_BUDGET_INVALID_PATTERNS)


class AnthropicClient:
    def __init__(self, profile: ModelProfile, api_client: Any) -> None:
        self.profile = profile
        self.name = profile.name
        self.tier = profile.tier
        self._api = api_client
        # Probe result: True = thinking works, False = skip thinking for this client.
        # None = not yet probed (probe happens lazily on first call that would use thinking).
        self._thinking_supported: bool | None = None

    def _build_messages(self, request: CompletionRequest) -> list[dict]:
        out: list[dict] = []
        for m in request.messages:
            if m.role == "tool":
                out.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": m.tool_use_id,
                                "content": m.content,
                            }
                        ],
                    }
                )
            else:
                out.append({"role": m.role, "content": m.content})
        return out

    def _build_tools(self, request: CompletionRequest) -> list[dict]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.input_schema,
            }
            for t in request.tools
        ]

    def _build_kwargs(self, request: CompletionRequest, *, with_thinking: bool) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.profile.model_id,
            "system": request.system,
            "messages": self._build_messages(request),
            "max_tokens": request.max_tokens,
        }
        if request.tools:
            kwargs["tools"] = self._build_tools(request)
        if request.temperature is not None:
            kwargs["temperature"] = request.temperature
        if with_thinking:
            budget = request.thinking_budget or self.profile.thinking_budget
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": budget}
        return kwargs

    def _wants_thinking(self, request: CompletionRequest) -> bool:
        return bool(request.thinking_budget or self.profile.thinking_budget)

    def _parse_response(self, resp: Any) -> CompletionResponse:
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in getattr(resp, "content", []) or []:
            btype = getattr(block, "type", None)
            if btype == "text":
                text_parts.append(str(getattr(block, "text", "")))
            elif btype == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=str(getattr(block, "id", "")),
                        name=str(getattr(block, "name", "")),
                        arguments=dict(getattr(block, "input", {}) or {}),
                    )
                )
        return CompletionResponse(
            text="".join(text_parts),
            tool_calls=tuple(tool_calls),
            stop_reason=str(getattr(resp, "stop_reason", "end_turn")),
            usage={
                "input_tokens": int(getattr(resp.usage, "input_tokens", 0)),
                "output_tokens": int(getattr(resp.usage, "output_tokens", 0)),
            },
            raw=resp,
        )

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        wants_thinking = self._wants_thinking(request)

        # Fast path: thinking already known unsupported — skip it.
        if wants_thinking and self._thinking_supported is False:
            kwargs = self._build_kwargs(request, with_thinking=False)
            return self._parse_response(self._api.messages.create(**kwargs))

        if not wants_thinking:
            kwargs = self._build_kwargs(request, with_thinking=False)
            return self._parse_response(self._api.messages.create(**kwargs))

        # Attempt with thinking enabled. On a thinking-related API error, fall
        # back once without thinking and cache the result so future calls skip
        # the overhead of the failed attempt.
        try:
            kwargs = self._build_kwargs(request, with_thinking=True)
            resp = self._api.messages.create(**kwargs)
            self._thinking_supported = True
            return self._parse_response(resp)
        except Exception as exc:
            if not _is_thinking_error(exc):
                raise
            logger.warning(
                "Model '%s' rejected thinking params (%s); "
                "disabling thinking for this client.",
                self.profile.model_id,
                exc,
            )
            self._thinking_supported = False
            kwargs = self._build_kwargs(request, with_thinking=False)
            return self._parse_response(self._api.messages.create(**kwargs))

    def warmup(self) -> None:
        """Probe thinking support with a minimal call so the first real request
        doesn't pay the cost of a failed thinking attempt."""
        if not self.profile.thinking_budget:
            return
        try:
            probe_kwargs: dict[str, Any] = {
                "model": self.profile.model_id,
                "system": "ping",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 16,
                "thinking": {"type": "enabled", "budget_tokens": self.profile.thinking_budget},
            }
            self._api.messages.create(**probe_kwargs)
            self._thinking_supported = True
            logger.info("Model '%s': thinking supported (budget=%d).",
                        self.profile.model_id, self.profile.thinking_budget)
        except Exception as exc:
            if _is_thinking_error(exc):
                self._thinking_supported = False
                logger.warning(
                    "Model '%s': thinking not supported, will skip thinking params. (%s)",
                    self.profile.model_id, exc,
                )
            # Transient errors (network, 5xx) don't set the flag — we'll probe lazily.
