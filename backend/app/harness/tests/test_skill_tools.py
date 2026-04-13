# backend/app/harness/tests/test_skill_tools.py
from __future__ import annotations

from unittest.mock import MagicMock

from app.harness.dispatcher import ToolDispatcher
from app.harness.skill_tools import register_core_tools


def test_register_core_tools_wires_all_expected_names() -> None:
    disp = ToolDispatcher()
    artifact_store = MagicMock()
    wiki = MagicMock()
    sandbox = MagicMock()
    register_core_tools(
        dispatcher=disp, artifact_store=artifact_store, wiki=wiki, sandbox=sandbox,
        session_id="s1",
    )
    for name in [
        "skill",
        "sandbox.run",
        "save_artifact", "update_artifact", "get_artifact",
        "write_working", "promote_finding",
        "correlation.correlate",
        "group_compare.compare",
        "stat_validate.validate",
        "time_series.characterize",
        "time_series.decompose",
        "time_series.find_anomalies",
        "time_series.find_changepoints",
        "time_series.lag_correlate",
        "distribution_fit.fit",
        "data_profiler.profile",
    ]:
        assert disp.has(name), f"missing tool: {name}"
