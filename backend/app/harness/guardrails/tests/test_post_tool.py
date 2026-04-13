from __future__ import annotations

from app.harness.dispatcher import ToolResult
from app.harness.guardrails.post_tool import post_tool


def _res(name: str, payload: dict) -> ToolResult:
    return ToolResult(
        tool_use_id="t", tool_name=name, ok=True, payload=payload,
    )


def test_artifact_id_is_recorded() -> None:
    report = post_tool(_res("correlation.correlate",
                            {"artifact_id": "c1-abc"}))
    assert "c1-abc" in report.new_artifact_ids


def test_large_stdout_gets_trimmed_to_artifact_reference() -> None:
    big = "x" * 5000
    report = post_tool(_res("sandbox.run", {"stdout": big, "stderr": ""}))
    assert report.trimmed_stdout is not None
    assert len(report.trimmed_stdout) < 1000


def test_stat_validate_warning_surfaces_gotcha_refs() -> None:
    res = _res("stat_validate.validate", {
        "status": "WARN",
        "gotcha_refs": ["simpsons_paradox", "confounding"],
    })
    report = post_tool(res)
    assert report.gotcha_injections == ("simpsons_paradox", "confounding")


def test_event_emitted_for_each_artifact() -> None:
    report = post_tool(_res("group_compare.compare",
                            {"artifact_id": "g1-xyz"}))
    assert report.events
    assert any(e["type"] == "artifact_emitted" for e in report.events)
