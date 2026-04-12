from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import create_app
from app.trace import bus
from app.trace.events import JudgeRun, PromptSection
from app.trace.publishers import (
    TraceSession,
    publish_compaction,
    publish_final_output,
    publish_llm_call,
    publish_scratchpad_write,
    publish_tool_call,
)


@pytest.fixture(autouse=True)
def _reset_bus() -> None:
    bus.reset()


def _judge_runner(_text: str, n: int) -> list[JudgeRun]:
    return [
        JudgeRun(dimensions={"accuracy": float(i) / max(n - 1, 1)})
        for i in range(n)
    ]


def test_synthetic_agent_run_produces_readable_trace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TRACE_DIR", str(tmp_path))

    with TraceSession(
        session_id="sess-int", level=3, level_label="eval-level3",
        input_query="q", trace_mode="always",
        output_dir=tmp_path, judge_runner=_judge_runner,
    ) as session:
        publish_llm_call(
            step_id="s1", turn=1, model="claude-opus-4-6",
            temperature=1.0, max_tokens=4096, prompt_text="prompt 1",
            sections=[
                PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="..."),
                PromptSection(source="user_query", lines="51-52", text="..."),
            ],
            response_text="use a tool", tool_calls=[{"name": "read_file"}],
            stop_reason="tool_use", input_tokens=500, output_tokens=50,
            cache_read_tokens=0, cache_creation_tokens=0, latency_ms=120,
        )
        publish_tool_call(
            turn=1, tool_name="read_file",
            tool_input={"path": "/x"}, tool_output="content",
            duration_ms=10, error=None,
        )
        publish_compaction(
            turn=1, before_token_count=2000, after_token_count=1500,
            dropped_layers=["old_context"], kept_layers=["system", "task"],
        )
        publish_scratchpad_write(turn=1, key="findings", value_preview="...")
        publish_llm_call(
            step_id="s2", turn=2, model="claude-opus-4-6",
            temperature=1.0, max_tokens=4096, prompt_text="prompt 2",
            sections=[PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="...")],
            response_text="done", tool_calls=[], stop_reason="end_turn",
            input_tokens=1500, output_tokens=100,
            cache_read_tokens=0, cache_creation_tokens=0, latency_ms=150,
        )
        publish_final_output(
            output_text="final answer", final_grade="F",
            judge_dimensions={"accuracy": 0.5},
        )
        session.set_final_grade("F")

    trace_path = tmp_path / "sess-int.yaml"
    assert trace_path.exists()

    data = yaml.safe_load(trace_path.read_text())
    assert data["trace_schema_version"] == 1
    assert data["summary"]["llm_call_count"] == 2
    assert data["summary"]["step_ids"] == ["s1", "s2"]
    assert data["summary"]["turn_count"] == 2
    assert data["summary"]["final_grade"] == "F"
    assert len(data["judge_runs"]) == 5

    client = TestClient(create_app())

    r = client.get("/api/trace/traces")
    assert r.status_code == 200
    assert any(t["session_id"] == "sess-int" for t in r.json()["traces"])

    r = client.get("/api/trace/traces/sess-int/prompt/s1")
    assert r.status_code == 200
    body = r.json()
    assert len(body["sections"]) == 2

    r = client.get("/api/trace/traces/sess-int/timeline")
    assert r.status_code == 200
    body = r.json()
    assert len(body["turns"]) == 2

    r = client.get("/api/trace/traces/sess-int/judge-variance?refresh=0")
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "cached"
    assert "accuracy" in body["variance"]
