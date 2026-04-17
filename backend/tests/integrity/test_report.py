import json
from datetime import date
from pathlib import Path

import pytest
from backend.app.integrity.issue import IntegrityIssue
from backend.app.integrity.protocol import ScanResult
from backend.app.integrity.report import write_report


def issue(
    rule: str = "graph.dead_code", node_id: str = "x", severity: str = "WARN"
) -> IntegrityIssue:
    return IntegrityIssue(
        rule=rule, severity=severity, node_id=node_id,
        location="x.py:1", message="m", evidence={}, first_seen="2026-04-17",
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def test_writes_report_json_and_md(repo: Path):
    results = [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[issue()])]
    paths = write_report(repo, results, today=date(2026, 4, 17))
    rj = repo / "integrity-out" / "2026-04-17" / "report.json"
    rm = repo / "integrity-out" / "2026-04-17" / "report.md"
    assert rj.exists() and rm.exists()
    data = json.loads(rj.read_text())
    assert data["date"] == "2026-04-17"
    assert data["counts"]["WARN"] == 1
    assert "graph.dead_code" in rm.read_text()
    assert paths.report_json == rj


def test_writes_docs_health_latest_md(repo: Path):
    results = [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[issue()])]
    write_report(repo, results, today=date(2026, 4, 17))
    latest = repo / "docs" / "health" / "latest.md"
    assert latest.exists()
    assert "graph_lint" in latest.read_text()


def test_appends_to_trend_md(repo: Path):
    r1 = [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[issue()])]
    write_report(repo, r1, today=date(2026, 4, 17))
    r2 = [ScanResult(
        plugin_name="graph_lint", plugin_version="1.0.0",
        issues=[issue(node_id="y"), issue(node_id="z")]
    )]
    write_report(repo, r2, today=date(2026, 4, 18))
    trend = (repo / "docs" / "health" / "trend.md").read_text()
    assert "2026-04-17" in trend and "2026-04-18" in trend
    # second day has 2 WARN
    lines = [row for row in trend.splitlines() if "2026-04-18" in row and "graph_lint" in row]
    assert any("2" in row for row in lines)


def test_trend_md_trims_to_30_days(repo: Path):
    from datetime import timedelta
    base = date(2026, 4, 17)
    for i in range(0, 35):
        write_report(
            repo,
            [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[issue()])],
            today=base - timedelta(days=i),
        )
    trend = (repo / "docs" / "health" / "trend.md").read_text()
    # Oldest row should be base - 29 days, NOT base - 34 days
    assert (base - timedelta(days=29)).isoformat() in trend
    assert (base - timedelta(days=34)).isoformat() not in trend


def test_carries_first_seen_from_previous_report(repo: Path):
    today_issue = IntegrityIssue(
        rule="graph.dead_code", severity="WARN", node_id="x",
        location="x.py:1", message="m", evidence={}, first_seen="2026-04-17",
    )
    write_report(
        repo,
        [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[today_issue])],
        today=date(2026, 4, 17),
    )
    later_issue = IntegrityIssue(
        rule="graph.dead_code", severity="WARN", node_id="x",
        location="x.py:1", message="m", evidence={}, first_seen="2026-04-20",
    )
    write_report(
        repo,
        [ScanResult(plugin_name="graph_lint", plugin_version="1.0.0", issues=[later_issue])],
        today=date(2026, 4, 20),
    )
    later_data = json.loads((repo / "integrity-out" / "2026-04-20" / "report.json").read_text())
    issue_x = next(i for i in later_data["issues"] if i["node_id"] == "x")
    assert issue_x["first_seen"] == "2026-04-17"
