from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str
    name: str | None = None
    tool_use_id: str | None = None


@dataclass(frozen=True, slots=True)
class ToolSchema:
    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class CompletionRequest:
    system: str
    messages: tuple[Message, ...]
    tools: tuple[ToolSchema, ...] = field(default_factory=tuple)
    max_tokens: int = 2048
    temperature: float | None = None
    thinking_budget: int | None = None


@dataclass(frozen=True, slots=True)
class CompletionResponse:
    text: str
    tool_calls: tuple[ToolCall, ...]
    stop_reason: str
    usage: dict[str, int] = field(default_factory=dict)
    raw: Any = None


@runtime_checkable
class ModelClient(Protocol):
    name: str
    tier: str

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...

    def warmup(self) -> None: ...
