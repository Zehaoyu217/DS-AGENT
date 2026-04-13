from __future__ import annotations

from app.harness.clients.base import ToolCall
from app.harness.guardrails.pre_tool import pre_tool_gate
from app.harness.guardrails.types import Severity


def test_sandbox_blocked_without_dataset_loaded() -> None:
    call = ToolCall(id="1", name="sandbox.run",
                    arguments={"code": "print(df.head())"})
    findings = pre_tool_gate(call, turn_trace=[], dataset_loaded=False)
    assert any(f.code == "df_without_dataset" for f in findings)
    assert all(f.severity is Severity.FAIL
               for f in findings if f.code == "df_without_dataset")


def test_sandbox_ok_with_dataset_loaded() -> None:
    call = ToolCall(id="1", name="sandbox.run",
                    arguments={"code": "print(df.head())"})
    findings = pre_tool_gate(call, turn_trace=[], dataset_loaded=True)
    assert not findings


def test_promote_finding_without_validate_is_blocked() -> None:
    call = ToolCall(id="2", name="promote_finding",
                    arguments={"text": "X correlates with Y"})
    findings = pre_tool_gate(call, turn_trace=[], dataset_loaded=True)
    assert any(f.code == "promote_without_validate" for f in findings)


def test_promote_finding_after_passing_validate_allowed() -> None:
    trace = [{"tool": "stat_validate.validate",
              "result": {"status": "PASS"}}]
    call = ToolCall(id="3", name="promote_finding",
                    arguments={"text": "X relates to Y"})
    findings = pre_tool_gate(call, turn_trace=trace, dataset_loaded=True)
    assert not findings


def test_lag_correlate_non_stationary_without_override_blocked() -> None:
    call = ToolCall(id="4", name="time_series.lag_correlate",
                    arguments={"x": "a", "y": "b", "accept_non_stationary": False})
    trace = [{"tool": "time_series.characterize",
              "result": {"stationary": False}}]
    findings = pre_tool_gate(call, turn_trace=trace, dataset_loaded=True)
    assert any(f.code == "lag_corr_non_stationary" for f in findings)
