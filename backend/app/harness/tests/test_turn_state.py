from __future__ import annotations

from app.harness.turn_state import TurnState


def test_turn_state_records_events_in_order() -> None:
    state = TurnState()
    state.record_tool(name="skill", result_payload={"name": "correlation"}, status="ok")
    state.record_tool(name="correlation.correlate",
                      result_payload={"coefficient": 0.5, "p_value": 0.01},
                      status="ok")
    trace = state.as_trace()
    assert [evt["tool"] for evt in trace] == ["skill", "correlation.correlate"]
    assert trace[1]["result"]["coefficient"] == 0.5


def test_turn_state_artifact_ids_accumulate() -> None:
    state = TurnState()
    state.record_artifact("a1")
    state.record_artifact("a2")
    state.record_artifact("a1")  # duplicates ignored
    assert state.artifact_ids() == ("a1", "a2")
