from __future__ import annotations

from pathlib import Path

import pytest

from app.sop.log import list_entries, next_session_id, read_entry, write_entry
from app.sop.types import (
    FixApplied,
    IterationLogEntry,
    PreflightResult,
    TriageDecision,
)


def _entry(session_id: str, level: int = 3, bucket: str = "context") -> IterationLogEntry:
    return IterationLogEntry(
        date=session_id[:10],
        session_id=session_id,
        level=level,
        overall_grade_before="C",
        preflight=PreflightResult(evaluation_bias="pass", data_quality="pass", determinism="pass"),
        triage=TriageDecision(bucket=bucket, evidence=["e"], hypothesis="h"),
        fix=FixApplied(
            ladder_id=f"{bucket}-01", name="n", files_changed=["f"],
            model_used_for_fix="sonnet", cost_bucket="trivial",
        ),
        outcome={"grade_after": "B", "regressions": "none", "iterations": 1, "success": True},
        trace_links={"before": "a.json", "after": "b.json"},
    )


def test_next_session_id_starts_at_001(tmp_path: Path) -> None:
    assert next_session_id(tmp_path, level=3, date="2026-04-12") == "2026-04-12-level3-001"


def test_next_session_id_increments(tmp_path: Path) -> None:
    write_entry(_entry("2026-04-12-level3-001"), tmp_path)
    write_entry(_entry("2026-04-12-level3-002"), tmp_path)
    assert next_session_id(tmp_path, level=3, date="2026-04-12") == "2026-04-12-level3-003"


def test_write_and_read_roundtrip(tmp_path: Path) -> None:
    entry = _entry("2026-04-12-level3-001")
    write_entry(entry, tmp_path)
    loaded = read_entry("2026-04-12-level3-001", tmp_path)
    assert loaded == entry


def test_list_entries_sorted(tmp_path: Path) -> None:
    write_entry(_entry("2026-04-12-level3-002"), tmp_path)
    write_entry(_entry("2026-04-12-level3-001"), tmp_path)
    sids = [e.session_id for e in list_entries(tmp_path)]
    assert sids == ["2026-04-12-level3-001", "2026-04-12-level3-002"]


def test_read_missing_entry_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_entry("2026-04-12-level3-999", tmp_path)


def test_next_session_id_skips_non_numeric_suffix(tmp_path: Path) -> None:
    """A malformed YAML like 2026-04-12-level3-draft.yaml must not crash next_session_id."""
    write_entry(_entry("2026-04-12-level3-001"), tmp_path)
    # Create a rogue file with a non-numeric suffix
    (tmp_path / "2026-04-12-level3-draft.yaml").write_text("garbage: true")
    assert next_session_id(tmp_path, level=3, date="2026-04-12") == "2026-04-12-level3-002"


def test_entry_with_nullable_triage_and_fix(tmp_path: Path) -> None:
    """IterationLogEntry must accept triage=None and fix=None (e.g. preflight fail)."""
    entry = IterationLogEntry(
        date="2026-04-12",
        session_id="2026-04-12-level3-010",
        level=3,
        overall_grade_before="C",
        preflight=PreflightResult(evaluation_bias="fail", data_quality="pass", determinism="pass"),
        triage=None,
        fix=None,
        outcome={"success": False, "reason": "preflight_failed"},
        trace_links={},
    )
    write_entry(entry, tmp_path)
    loaded = read_entry("2026-04-12-level3-010", tmp_path)
    assert loaded.triage is None
    assert loaded.fix is None
    assert loaded.outcome == {"success": False, "reason": "preflight_failed"}
