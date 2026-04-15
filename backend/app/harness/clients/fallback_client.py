"""FallbackModelClient — wraps a primary client with an ordered retry chain.

Motivation: OpenRouter's free tier aggressively rate-limits individual
models (429), but other free models are usually available for the same
request. Instead of surfacing a noisy error to the user, we try the next
model in a configured chain and continue the turn.

The wrapper only triggers on ``RateLimitError``. Any other error falls
through immediately — we don't want to mask genuine failures (bad API
key, network down, invalid payload).

Usage::

    primary = OpenRouterClient(profile_a, http)
    fallbacks = [OpenRouterClient(profile_b, http), OpenRouterClient(profile_c, http)]
    client = FallbackModelClient(primary, fallbacks)
    response = client.complete(request)  # transparent to callers
"""
from __future__ import annotations

import logging
from collections.abc import Sequence

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    ModelClient,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class FallbackModelClient:
    """Structural ``ModelClient`` that retries on ``RateLimitError`` only."""

    def __init__(
        self,
        primary: ModelClient,
        fallbacks: Sequence[ModelClient] = (),
    ) -> None:
        self._primary = primary
        self._fallbacks: tuple[ModelClient, ...] = tuple(fallbacks)
        # Expose ModelClient protocol attributes from the primary.
        self.name = primary.name
        self.tier = primary.tier

    @property
    def fallback_names(self) -> tuple[str, ...]:
        return tuple(c.name for c in self._fallbacks)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        chain = (self._primary, *self._fallbacks)
        last_error: RateLimitError | None = None
        for attempt, client in enumerate(chain):
            try:
                return client.complete(request)
            except RateLimitError as exc:
                last_error = exc
                remaining = len(chain) - attempt - 1
                if remaining > 0:
                    logger.warning(
                        "model '%s' rate-limited; falling back (%d remaining)",
                        client.name,
                        remaining,
                    )
                    continue
                # Exhausted — re-raise.
                raise
        # Unreachable: loop either returns a response or raises. Kept for type
        # checker satisfaction.
        assert last_error is not None
        raise last_error

    def warmup(self) -> None:
        # Warming every fallback eagerly defeats the point (and can hit the
        # same quota). Just warm the primary.
        self._primary.warmup()
