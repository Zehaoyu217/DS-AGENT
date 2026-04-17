"""Regression test: /api/chat/stream must write a trace YAML.

Root cause of the original bug (P22 E2E): ``chat_stream_endpoint`` never
wrapped its SSE generator in a ``TraceSession``, so no YAML was ever
written — DevTools' Timeline and Prompt sub-tabs got HTTP 404 from
``/api/trace/traces/{id}/...`` for every streamed session.

This test boots the app with a stubbed ``ModelClient`` (no network, no
OpenRouter key needed), streams one turn, and asserts:

1. a YAML trace file lands under ``TRACE_DIR``
2. it contains at least one ``llm_call`` event
3. its ``summary.input_query`` matches what we streamed
"""
from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest
import yaml
from fastapi.testclient import TestClient

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    ModelClient,
    ToolCall,
)


class _StubClient:
    """Always returns a terminal (``end_turn``) text response on the first call.

    Implements ``ModelClient`` structurally (runtime-checkable Protocol).
    """

    name = "stub-model"
    tier = "advisory"

    def __init__(self, response_text: str = "stub reply ok") -> None:
        self._response_text = response_text
        self.calls: int = 0

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        self.calls += 1
        return CompletionResponse(
            text=self._response_text,
            tool_calls=tuple[ToolCall, ...](),
            stop_reason="end_turn",
            usage={"input_tokens": 10, "output_tokens": 5},
            raw={},
        )

    def warmup(self) -> None:
        return None


@pytest.fixture
def _stub_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Point every writable dir at tmp_path and swap the model client."""
    traces_dir = tmp_path / "traces"
    traces_dir.mkdir()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    monkeypatch.setenv("TRACE_DIR", str(traces_dir))
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    monkeypatch.setenv("CCAGENT_WIKI_ROOT", str(wiki_dir))

    from app.api import chat_api
    from app.harness.wiring import reset_singletons_for_tests

    reset_singletons_for_tests()

    def _fake_make_client(model_id: str, http: httpx.Client) -> ModelClient:
        return _StubClient()  # type: ignore[return-value]

    monkeypatch.setattr(chat_api, "_make_client", _fake_make_client)
    return traces_dir


def _collect_sse_lines(response: httpx.Response) -> list[str]:
    # TestClient's streaming Response exposes .iter_lines()
    lines: list[str] = []
    for raw in response.iter_lines():
        if raw:
            lines.append(raw if isinstance(raw, str) else raw.decode("utf-8"))
    return lines


def test_stream_endpoint_writes_trace_yaml(_stub_env: Path) -> None:
    from app.main import create_app

    app = create_app()
    with TestClient(app) as client, client.stream(
        "POST",
        "/api/chat/stream",
        json={"message": "what is 1+1?"},
    ) as resp:
        assert resp.status_code == 200
        lines = _collect_sse_lines(resp)

    # SSE frames include at least turn_start + turn_end.
    joined = "\n".join(lines)
    assert "turn_start" in joined, f"no turn_start in stream:\n{joined}"
    assert "turn_end" in joined, f"no turn_end in stream:\n{joined}"

    yaml_files = list(_stub_env.glob("*.yaml"))
    assert yaml_files, (
        f"expected a trace YAML under {_stub_env}, got none. "
        "TraceSession wrap on /api/chat/stream regressed."
    )

    # There should be exactly one trace for the one session we streamed.
    assert len(yaml_files) == 1, f"unexpected trace files: {yaml_files}"
    trace = yaml.safe_load(yaml_files[0].read_text(encoding="utf-8"))

    # Summary pins: ok outcome, one turn, one llm_call, always-mode.
    summary = trace["summary"]
    assert summary["outcome"] == "ok"
    assert summary["trace_mode"] == "always"
    assert summary["turn_count"] >= 1
    assert summary["llm_call_count"] >= 1

    events = trace["events"]
    event_kinds = [e.get("kind") for e in events]
    assert "session_start" in event_kinds
    assert "llm_call" in event_kinds, (
        f"no llm_call event recorded — DevTools Prompt tab will 404. "
        f"events={event_kinds}"
    )
    assert "session_end" in event_kinds

    # input_query lives on the session_start event.
    start = next(e for e in events if e.get("kind") == "session_start")
    assert start["input_query"] == "what is 1+1?"


def test_stream_endpoint_trace_includes_prompt_sections(_stub_env: Path) -> None:
    """The llm_call record must surface ``sections`` so the frontend
    PromptInspectorPanel can render system+user text."""
    from app.main import create_app

    app = create_app()
    with TestClient(app) as client, client.stream(
        "POST",
        "/api/chat/stream",
        json={"message": "hello world"},
    ) as resp:
        assert resp.status_code == 200
        _: Iterator[str] = resp.iter_lines()
        for _chunk in _:
            pass  # drain

    trace = yaml.safe_load(
        next(iter(_stub_env.glob("*.yaml"))).read_text(encoding="utf-8"),
    )
    llm_event = next(e for e in trace["events"] if e.get("kind") == "llm_call")
    sources = {s["source"] for s in llm_event["sections"]}
    assert "user_query" in sources
    assert "system_prompt" in sources
