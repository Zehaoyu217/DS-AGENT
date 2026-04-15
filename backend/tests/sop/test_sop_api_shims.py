from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import create_app


def _trace_doc(session_id: str) -> dict[str, object]:
    return {
        "trace_schema_version": 1,
        "summary": {
            "session_id": session_id, "started_at": "t", "ended_at": "t",
            "duration_ms": 1, "level": 3, "level_label": "eval-level3",
            "turn_count": 0, "llm_call_count": 0,
            "total_input_tokens": 0, "total_output_tokens": 0,
            "outcome": "ok", "final_grade": "F",
            "step_ids": [], "trace_mode": "on_failure", "judge_runs_cached": 1,
        },
        "judge_runs": [{"dimensions": {"accuracy": 0.5}}],
        "events": [
            {
                "kind": "session_start", "seq": 1, "timestamp": "t",
                "session_id": session_id, "started_at": "t",
                "level": 3, "level_label": "eval-level3", "input_query": "q",
            },
        ],
    }


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("TRACE_DIR", str(tmp_path))
    (tmp_path / "sess-1.yaml").write_text(
        yaml.safe_dump(_trace_doc("sess-1")), encoding="utf-8",
    )
    return TestClient(create_app())


def test_legacy_judge_variance_shim_delegates_to_trace(client: TestClient) -> None:
    r = client.get("/api/sop/judge-variance/sess-1")
    assert r.status_code == 200
    body = r.json()
    assert "variance" in body
    assert "threshold_exceeded" in body


def test_legacy_prompt_assembly_shim_returns_empty_sections_on_missing_step(
    client: TestClient,
) -> None:
    r = client.get("/api/sop/prompt-assembly/sess-1/s99")
    assert r.status_code == 200
    body = r.json()
    assert body["sections"] == []


def test_legacy_timeline_shim_delegates_to_trace(client: TestClient) -> None:
    r = client.get("/api/sop/timeline/sess-1")
    assert r.status_code == 200
    body = r.json()
    assert "turns" in body
    assert "events" in body
