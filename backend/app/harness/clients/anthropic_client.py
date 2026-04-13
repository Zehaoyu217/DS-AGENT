from __future__ import annotations

from typing import Any

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    ToolCall,
)
from app.harness.config import ModelProfile


class AnthropicClient:
    def __init__(self, profile: ModelProfile, api_client: Any) -> None:
        self.profile = profile
        self.name = profile.name
        self.tier = profile.tier
        self._api = api_client

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

    def complete(self, request: CompletionRequest) -> CompletionResponse:
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
        if request.thinking_budget or self.profile.thinking_budget:
            kwargs["thinking"] = {
                "type": "enabled",
                "budget_tokens": request.thinking_budget or self.profile.thinking_budget,
            }
        resp = self._api.messages.create(**kwargs)

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

    def warmup(self) -> None:
        return
