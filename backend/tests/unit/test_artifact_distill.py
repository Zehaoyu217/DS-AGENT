from __future__ import annotations

from app.artifacts.distill import distill_artifact, format_artifacts_for_compaction
from app.artifacts.models import Artifact


def test_distill_chart_extracts_mark_and_encodings() -> None:
    a = Artifact(
        type="chart",
        title="Revenue by month",
        content="{}",
        format="vega-lite",
        chart_data={
            "mark": "line",
            "x": {"field": "month", "type": "temporal"},
            "y": {"field": "revenue", "type": "quantitative"},
            "data_sample": {"month": ["2024-01", "2024-02"], "revenue": [100, 120]},
            "data_rows": 2,
        },
    )
    out = distill_artifact(a)
    assert "mark=line" in out
    assert "x=month" in out
    assert "y=revenue" in out


def test_distill_table_includes_row_counts() -> None:
    a = Artifact(
        type="table",
        title="Top customers",
        content="<table><thead><tr><th>name</th></tr></thead><tbody><tr><td>A</td></tr></tbody></table>",
        total_rows=200,
        displayed_rows=50,
    )
    out = distill_artifact(a)
    assert "200 rows" in out
    assert "displayed 50" in out


def test_distill_profile_prefers_profile_summary_field() -> None:
    a = Artifact(
        type="profile",
        title="customers_v1",
        content="{}",
        profile_summary="8 cols; 1 BLOCKER (duplicate_key on customer_id); 2 HIGH risks.",
    )
    out = distill_artifact(a)
    assert "BLOCKER" in out
    assert "customers_v1" in out


def test_format_artifacts_for_compaction_lists_all() -> None:
    artifacts = [
        Artifact(id="a1", type="table", title="Rows", content="<t/>"),
        Artifact(id="a2", type="chart", title="Trend", content="{}", format="vega-lite"),
    ]
    out = format_artifacts_for_compaction(artifacts)
    assert "Artifacts (2 total)" in out
    assert "a1" in out and "a2" in out
