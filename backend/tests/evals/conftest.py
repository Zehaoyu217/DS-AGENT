"""Shared fixtures for agent evaluation tests.

These tests run the full grading pipeline with a mock agent.
They require Ollama running locally for LLM-judged dimensions.

The `_require_ollama` autouse fixture probes the Ollama HTTP API once
per session and skips every test in this dir when it's unreachable —
so `pytest tests/` is green on a laptop with no local LLM running.
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest

from app.evals.judge import JudgeConfig, LLMJudge
from app.evals.types import AgentTrace

RUBRICS_DIR = Path(__file__).parent / "rubrics"
_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
_OLLAMA_PROBE_TIMEOUT_S = 0.5
_REQUIRED_MODEL = JudgeConfig().model

# Resolved once per session so we don't re-probe for every test.
# Value is None (unchecked), "" (ready), or a skip-reason string.
_ollama_skip_reason_cache: str | None = None
_CACHE_SENTINEL_READY = ""


def _ollama_skip_reason() -> str:
    """Return an empty string if Ollama is ready, otherwise a skip reason.

    We require both `/api/tags` reachable AND the judge's model to be pulled —
    otherwise the generate call hangs until its own 60s timeout per dimension,
    which makes `pytest tests/` spend 5+ minutes timing out instead of skipping.
    """
    global _ollama_skip_reason_cache
    if _ollama_skip_reason_cache is None:
        _ollama_skip_reason_cache = _probe_ollama()
    return _ollama_skip_reason_cache


def _probe_ollama() -> str:
    try:
        resp = httpx.get(
            f"{_OLLAMA_URL}/api/tags",
            timeout=_OLLAMA_PROBE_TIMEOUT_S,
        )
    except (httpx.HTTPError, OSError):
        return f"Ollama not reachable at {_OLLAMA_URL}"
    if resp.status_code != 200:
        return f"Ollama not reachable at {_OLLAMA_URL} (HTTP {resp.status_code})"
    try:
        models = {m.get("name") for m in resp.json().get("models", [])}
    except ValueError:
        return f"Ollama at {_OLLAMA_URL} returned non-JSON from /api/tags"
    if _REQUIRED_MODEL not in models:
        return (
            f"Judge model '{_REQUIRED_MODEL}' not pulled on {_OLLAMA_URL} — "
            f"run `ollama pull {_REQUIRED_MODEL}` to enable these tests"
        )
    # Verify the model actually loads (resource constraints may prevent it even
    # when it's listed in /api/tags).
    try:
        gen_resp = httpx.post(
            f"{_OLLAMA_URL}/api/generate",
            json={"model": _REQUIRED_MODEL, "prompt": "hi", "stream": False},
            timeout=30.0,
        )
    except (httpx.HTTPError, OSError) as exc:
        return f"Judge model '{_REQUIRED_MODEL}' generate probe failed: {exc}"
    if gen_resp.status_code != 200:
        return (
            f"Judge model '{_REQUIRED_MODEL}' failed to load on {_OLLAMA_URL} "
            f"(HTTP {gen_resp.status_code}) — likely resource contention"
        )
    return _CACHE_SENTINEL_READY


@pytest.fixture(autouse=True)
def _require_ollama() -> None:
    """Skip the eval tests if Ollama isn't ready — the judge calls need it."""
    reason = _ollama_skip_reason()
    if reason:
        pytest.skip(f"{reason}; skipping LLM-judged eval")


@pytest.fixture
def rubrics_path() -> Path:
    """Path to the rubrics directory."""
    return RUBRICS_DIR


@pytest.fixture
def eval_db(tmp_path: Path) -> str:
    """Seed a fresh eval database and return its path."""
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    return str(db_path)


@pytest.fixture
def llm_judge() -> LLMJudge:
    """LLM judge using default Ollama config."""
    return LLMJudge()


class MockAgent:
    """Returns a fixed trace for any prompt."""

    def __init__(self, trace: AgentTrace) -> None:
        self._trace = trace

    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        return self._trace


class SequentialMockAgent:
    """Returns different traces for sequential calls (Level 5)."""

    def __init__(self, traces: list[AgentTrace]) -> None:
        self._traces = traces
        self._index = 0

    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        trace = self._traces[min(self._index, len(self._traces) - 1)]
        self._index += 1
        return trace
