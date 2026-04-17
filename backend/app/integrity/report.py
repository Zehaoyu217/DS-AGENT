from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .issue import IntegrityIssue, carry_first_seen
from .protocol import ScanResult


@dataclass(frozen=True)
class ReportPaths:
    report_json: Path
    report_md: Path
    latest_md: Path
    trend_md: Path
    run_dir: Path


def _run_dir(repo_root: Path, today: date) -> Path:
    d = repo_root / "integrity-out" / today.isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_prior_issues(repo_root: Path, today: date) -> list[IntegrityIssue]:
    """Walk integrity-out/* for the most recent report.json older than today."""
    base = repo_root / "integrity-out"
    if not base.exists():
        return []
    candidates: list[date] = []
    for child in base.iterdir():
        if not child.is_dir():
            continue
        try:
            d = date.fromisoformat(child.name)
        except ValueError:
            continue
        if d < today and (child / "report.json").exists():
            candidates.append(d)
    if not candidates:
        return []
    latest = max(candidates)
    data = json.loads((base / latest.isoformat() / "report.json").read_text())
    return [IntegrityIssue.from_dict(item) for item in data.get("issues", [])]


def _render_report_md(today: date, results: list[ScanResult], counts: dict[str, int]) -> str:
    lines = [
        f"# Integrity report — {today.isoformat()}",
        "",
        "## Counts by severity",
        "",
    ]
    for sev in ("CRITICAL", "ERROR", "WARN", "INFO"):
        lines.append(f"- **{sev}**: {counts.get(sev, 0)}")
    lines.append("")
    for r in results:
        lines.append(f"## {r.plugin_name} (v{r.plugin_version})")
        lines.append("")
        if r.failures:
            lines.append("**Failures:**")
            for f in r.failures:
                lines.append(f"- {f}")
            lines.append("")
        if not r.issues:
            lines.append("_No issues._")
            lines.append("")
            continue
        lines.append("| Rule | Severity | Node | Location | Message |")
        lines.append("|------|----------|------|----------|---------|")
        for i in r.issues:
            msg = i.message.replace("|", "\\|")
            lines.append(f"| {i.rule} | {i.severity} | `{i.node_id}` | {i.location} | {msg} |")
        lines.append("")
    return "\n".join(lines)


def _render_latest_md(today: date, results: list[ScanResult], counts: dict[str, int]) -> str:
    lines = [
        f"# Health — {today.isoformat()}",
        "",
        f"_Last run: {today.isoformat()}_",
        "",
        "## Summary",
        "",
    ]
    for sev in ("ERROR", "WARN", "INFO"):
        lines.append(f"- **{sev}**: {counts.get(sev, 0)}")
    lines.append("")
    for r in results:
        lines.append(f"## {r.plugin_name}")
        lines.append("")
        per_rule: dict[str, int] = Counter(i.rule for i in r.issues)
        if not per_rule:
            lines.append("_Clean._")
        else:
            for rule, n in sorted(per_rule.items()):
                lines.append(f"- `{rule}`: {n}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"Full report: `integrity-out/{today.isoformat()}/report.md`")
    return "\n".join(lines)


def _append_trend(
    trend_path: Path, today: date, results: list[ScanResult], retention_days: int
) -> None:
    header = "| date | plugin | severity | count |"
    sep = "|------|--------|----------|-------|"
    rows: list[str] = []
    if trend_path.exists():
        for raw in trend_path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("|--") or line.startswith("| date"):
                continue
            rows.append(line)
    # Collect all row dates to determine the true newest date (handles out-of-order writes)
    existing_dates: list[date] = []
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if not cells:
            continue
        try:
            existing_dates.append(date.fromisoformat(cells[0]))
        except ValueError:
            continue
    newest = max([today, *existing_dates]) if existing_dates else today
    cutoff = newest - timedelta(days=retention_days - 1)
    kept: list[str] = []
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if not cells:
            continue
        try:
            row_date = date.fromisoformat(cells[0])
        except ValueError:
            continue
        if row_date >= cutoff:
            kept.append(row)
    today_iso = today.isoformat()
    kept = [r for r in kept if not r.startswith(f"| {today_iso} ")]
    # Only append today's rows if today itself falls within the retention window
    new_rows: list[str] = []
    if today >= cutoff:
        by_plugin_sev: dict[tuple[str, str], int] = defaultdict(int)
        for r in results:
            for i in r.issues:
                by_plugin_sev[(r.plugin_name, i.severity)] += 1
        new_rows = [
            f"| {today_iso} | {plugin} | {sev} | {count} |"
            for (plugin, sev), count in sorted(by_plugin_sev.items())
        ]
    trend_path.parent.mkdir(parents=True, exist_ok=True)
    trend_path.write_text("\n".join([header, sep, *kept, *new_rows]) + "\n")


def write_report(
    repo_root: Path, results: list[ScanResult], today: date, retention_days: int = 30
) -> ReportPaths:
    prior = _load_prior_issues(repo_root, today)
    final_results: list[ScanResult] = []
    all_issues_today: list[IntegrityIssue] = []
    for r in results:
        carried = carry_first_seen(list(r.issues), prior)
        all_issues_today.extend(carried)
        final_results.append(
            ScanResult(
                plugin_name=r.plugin_name,
                plugin_version=r.plugin_version,
                issues=carried,
                artifacts=list(r.artifacts),
                failures=list(r.failures),
            )
        )

    counts: dict[str, int] = Counter(i.severity for i in all_issues_today)
    run_dir = _run_dir(repo_root, today)

    payload: dict[str, Any] = {
        "date": today.isoformat(),
        "counts": dict(counts),
        "plugins": [
            {
                "name": r.plugin_name,
                "version": r.plugin_version,
                "failures": r.failures,
                "issue_count": len(r.issues),
            }
            for r in final_results
        ],
        "issues": [i.to_dict() for i in all_issues_today],
    }
    report_json = run_dir / "report.json"
    report_json.write_text(json.dumps(payload, indent=2, sort_keys=True))

    report_md = run_dir / "report.md"
    report_md.write_text(_render_report_md(today, final_results, counts))

    latest_md = repo_root / "docs" / "health" / "latest.md"
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    latest_md.write_text(_render_latest_md(today, final_results, counts))

    trend_md = repo_root / "docs" / "health" / "trend.md"
    _append_trend(trend_md, today, final_results, retention_days)

    latest_link = repo_root / "integrity-out" / "latest"
    if latest_link.is_symlink() or latest_link.exists():
        latest_link.unlink()
    latest_link.symlink_to(today.isoformat(), target_is_directory=True)

    return ReportPaths(
        report_json=report_json,
        report_md=report_md,
        latest_md=latest_md,
        trend_md=trend_md,
        run_dir=run_dir,
    )
