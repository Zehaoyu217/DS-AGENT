"""Unit tests for ``FallbackModelClient``.

Covers the four observable behaviors that the wrapper is responsible for:

1. Primary succeeds → fallbacks are never invoked.
2. Primary returns ``RateLimitError`` → next fallback is tried; response of
   the first non-429 client is returned.
3. Every client in the chain rate-limits → the final ``RateLimitError`` is
   re-raised (and it surfaces the *last* model name, not the primary's).
4. Non-``RateLimitError`` exceptions propagate immediately — we don't want
   to mask real failures (bad key, network down, malformed payload) by
   cycling through the rest of the chain.

Also pins the structural ``ModelClient`` surface (``name``, ``tier``,
``warmup``) so that the wrapper is a drop-in replacement at the
``_make_client`` factory call site.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    Message,
    RateLimitError,
)
from app.harness.clients.fallback_client import FallbackModelClient


@dataclass
class _RecordingClient:
    """Minimal ModelClient that records calls and can raise on demand.

    Used in lieu of real OpenRouter / MLX clients so these tests don't
    depend on HTTP, API keys, or provider-specific payloads.
    """

    name: str
    tier: str = "advisory"
    response_text: str = "ok"
    raises: BaseException | None = None
    calls: int = 0
    warmups: int = 0
    recorded_requests: list[CompletionRequest] = field(default_factory=list)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        self.calls += 1
        self.recorded_requests.append(request)
        if self.raises is not None:
            raise self.raises
        return CompletionResponse(
            text=f"{self.name}:{self.response_text}",
            tool_calls=(),
            stop_reason="end_turn",
            usage={"input_tokens": 1, "output_tokens": 1},
            raw={"served_by": self.name},
        )

    def warmup(self) -> None:
        self.warmups += 1


def _request(text: str = "hello") -> CompletionRequest:
    return CompletionRequest(
        system="sys",
        messages=(Message(role="user", content=text),),
        max_tokens=64,
    )


def _rate_limit(model: str) -> RateLimitError:
    return RateLimitError(provider="openrouter", model=model, detail="quota")


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_primary_success_skips_fallbacks() -> None:
    primary = _RecordingClient(name="primary")
    fb_a = _RecordingClient(name="fb_a")
    fb_b = _RecordingClient(name="fb_b")
    client = FallbackModelClient(primary, [fb_a, fb_b])

    resp = client.complete(_request())

    assert resp.text == "primary:ok"
    assert primary.calls == 1
    # Fallbacks should never have been touched.
    assert fb_a.calls == 0
    assert fb_b.calls == 0


# ---------------------------------------------------------------------------
# Fallback triggers only on RateLimitError
# ---------------------------------------------------------------------------


def test_rate_limit_falls_through_to_next_model() -> None:
    primary = _RecordingClient(name="primary", raises=_rate_limit("primary-id"))
    fb_a = _RecordingClient(name="fb_a")  # returns cleanly
    fb_b = _RecordingClient(name="fb_b")
    client = FallbackModelClient(primary, [fb_a, fb_b])

    resp = client.complete(_request())

    assert resp.text == "fb_a:ok", "expected response from the first healthy fallback"
    assert primary.calls == 1
    assert fb_a.calls == 1
    # Once a fallback succeeds, the remainder of the chain must be skipped.
    assert fb_b.calls == 0


def test_walks_entire_chain_until_success() -> None:
    primary = _RecordingClient(name="primary", raises=_rate_limit("p"))
    fb_a = _RecordingClient(name="fb_a", raises=_rate_limit("a"))
    fb_b = _RecordingClient(name="fb_b")  # first non-429
    fb_c = _RecordingClient(name="fb_c")
    client = FallbackModelClient(primary, [fb_a, fb_b, fb_c])

    resp = client.complete(_request())

    assert resp.text == "fb_b:ok"
    assert primary.calls == 1
    assert fb_a.calls == 1
    assert fb_b.calls == 1
    assert fb_c.calls == 0


# ---------------------------------------------------------------------------
# Exhaustion
# ---------------------------------------------------------------------------


def test_all_rate_limited_raises_last_error() -> None:
    primary = _RecordingClient(name="primary", raises=_rate_limit("p-id"))
    fb_a = _RecordingClient(name="fb_a", raises=_rate_limit("a-id"))
    fb_b = _RecordingClient(name="fb_b", raises=_rate_limit("b-id"))
    client = FallbackModelClient(primary, [fb_a, fb_b])

    with pytest.raises(RateLimitError) as exc_info:
        client.complete(_request())

    # The surfaced error should name the *last* model attempted so operators
    # know the chain was exhausted, not that only the primary failed.
    assert exc_info.value.model == "b-id"
    assert primary.calls == 1
    assert fb_a.calls == 1
    assert fb_b.calls == 1


def test_no_fallbacks_rate_limit_raises_immediately() -> None:
    primary = _RecordingClient(name="only", raises=_rate_limit("only-id"))
    client = FallbackModelClient(primary, [])  # empty chain

    with pytest.raises(RateLimitError) as exc_info:
        client.complete(_request())

    assert exc_info.value.model == "only-id"
    assert primary.calls == 1


# ---------------------------------------------------------------------------
# Non-rate-limit errors must NOT be masked
# ---------------------------------------------------------------------------


def test_runtime_error_propagates_without_touching_fallbacks() -> None:
    boom = RuntimeError("bad api key")
    primary = _RecordingClient(name="primary", raises=boom)
    fb_a = _RecordingClient(name="fb_a")
    client = FallbackModelClient(primary, [fb_a])

    with pytest.raises(RuntimeError, match="bad api key"):
        client.complete(_request())

    assert primary.calls == 1
    # Crucial: a non-429 error must NOT cascade into trying fallbacks.
    # Otherwise a misconfigured primary would silently burn fallback quota.
    assert fb_a.calls == 0


def test_value_error_propagates_without_touching_fallbacks() -> None:
    primary = _RecordingClient(name="primary", raises=ValueError("bad payload"))
    fb_a = _RecordingClient(name="fb_a")
    client = FallbackModelClient(primary, [fb_a])

    with pytest.raises(ValueError):
        client.complete(_request())
    assert fb_a.calls == 0


# ---------------------------------------------------------------------------
# Protocol surface (name / tier / warmup / fallback_names)
# ---------------------------------------------------------------------------


def test_exposes_primary_name_and_tier() -> None:
    primary = _RecordingClient(name="primary-model", tier="strict")
    fb = _RecordingClient(name="fb-model", tier="advisory")
    client = FallbackModelClient(primary, [fb])

    # The wrapper is opaque to trace/logging code, so it must impersonate
    # the primary's identity.
    assert client.name == "primary-model"
    assert client.tier == "strict"


def test_fallback_names_reflects_chain() -> None:
    primary = _RecordingClient(name="p")
    fb_a = _RecordingClient(name="a")
    fb_b = _RecordingClient(name="b")
    client = FallbackModelClient(primary, [fb_a, fb_b])

    assert client.fallback_names == ("a", "b")


def test_warmup_only_touches_primary() -> None:
    primary = _RecordingClient(name="p")
    fb_a = _RecordingClient(name="a")
    fb_b = _RecordingClient(name="b")
    client = FallbackModelClient(primary, [fb_a, fb_b])

    client.warmup()

    # Warming every fallback would double-bill the same quota before we
    # even need them. Only the primary should be touched.
    assert primary.warmups == 1
    assert fb_a.warmups == 0
    assert fb_b.warmups == 0


# ---------------------------------------------------------------------------
# Request forwarding fidelity
# ---------------------------------------------------------------------------


def test_request_passed_through_unchanged_to_fallback() -> None:
    primary = _RecordingClient(name="primary", raises=_rate_limit("p"))
    fb_a = _RecordingClient(name="fb_a")
    client = FallbackModelClient(primary, [fb_a])

    req = _request("can you analyze this?")
    client.complete(req)

    # Same request object should reach both clients. The wrapper must not
    # silently rewrite it (which would corrupt trace reproducibility).
    assert primary.recorded_requests == [req]
    assert fb_a.recorded_requests == [req]


# Typing sanity: ensure the annotation is used (keeps linters happy and
# documents the intended shape of `_RecordingClient.recorded_requests`).
_: Any = _RecordingClient
