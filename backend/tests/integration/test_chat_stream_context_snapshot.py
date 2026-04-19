"""/api/chat/stream must emit a `context_snapshot` SSE frame on turn_start.

The Dock Context panel relies on this frame to render the per-conversation
context shape (layers, loaded files, total/budget tokens) without polling.
"""
from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.harness.clients.base import (
    CompletionRequest,
    CompletionResponse,
    ModelClient,
    ToolCall,
)


class _StubClient:
    name = "stub-model"
    tier = "advisory"

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        self.calls += 1
        return CompletionResponse(
            text="ok",
            tool_calls=tuple[ToolCall, ...](),
            stop_reason="end_turn",
            usage={"input_tokens": 10, "output_tokens": 5},
            raw={},
        )

    def warmup(self) -> None:
        return None


@pytest.fixture
def _stub_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
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


def test_context_snapshot_emitted_after_turn_start(_stub_env: Path) -> None:
    from app.main import create_app

    app = create_app()
    with TestClient(app) as client, client.stream(
        "POST",
        "/api/chat/stream",
        json={"message": "ping"},
    ) as resp:
        assert resp.status_code == 200
        saw_turn_start = False
        snapshot_payload: dict | None = None
        for raw in resp.iter_lines():
            if not raw:
                continue
            line = raw if isinstance(raw, str) else raw.decode("utf-8")
            if not line.startswith("data: "):
                continue
            evt = json.loads(line[len("data: "):])
            if evt.get("type") == "turn_start":
                saw_turn_start = True
            elif evt.get("type") == "context_snapshot":
                snapshot_payload = evt
                break

    assert saw_turn_start, "stream never emitted turn_start"
    assert snapshot_payload is not None, "stream never emitted context_snapshot"
    assert "layers" in snapshot_payload
    assert "loaded_files" in snapshot_payload
    assert "total_tokens" in snapshot_payload
    assert "budget_tokens" in snapshot_payload
    assert isinstance(snapshot_payload["layers"], list)
