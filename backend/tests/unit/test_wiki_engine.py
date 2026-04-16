from __future__ import annotations

import time
from pathlib import Path

import pytest

from app.wiki.engine import WikiEngine, _trim_log_to_size
from app.wiki.schema import Finding


@pytest.fixture
def wiki(tmp_path: Path) -> WikiEngine:
    for sub in ("findings", "hypotheses", "entities", "meta"):
        (tmp_path / sub).mkdir()
    (tmp_path / "working.md").write_text("# Working\n\n## Current Focus\n\ninitial\n")
    (tmp_path / "index.md").write_text("# Wiki Index\n\n")
    (tmp_path / "log.md").write_text("# Log\n\n")
    return WikiEngine(tmp_path)


def test_read_working_returns_file_contents(wiki: WikiEngine) -> None:
    text = wiki.read_working()
    assert "initial" in text


def test_write_working_replaces_contents(wiki: WikiEngine) -> None:
    wiki.write_working("# Working\n\n## Current Focus\n\nanalyzing customers\n")
    assert "analyzing customers" in wiki.read_working()


def test_write_working_rejects_over_200_lines(wiki: WikiEngine) -> None:
    too_long = "\n".join(f"line {i}" for i in range(250))
    with pytest.raises(ValueError, match="200"):
        wiki.write_working(too_long)


def test_append_log_adds_timestamped_line(wiki: WikiEngine) -> None:
    wiki.append_log("turn 1: profiled customers_v1")
    text = (wiki.root / "log.md").read_text()
    assert "turn 1: profiled customers_v1" in text


def test_promote_finding_writes_markdown(wiki: WikiEngine) -> None:
    finding = Finding(
        id="F-20260412-001",
        title="Revenue grew 12% QoQ",
        body="Analysis shows ...",
        evidence=["art_ab12cd"],
        stat_validate_pass=True,
    )
    path = wiki.promote_finding(finding)
    assert path.exists()
    assert path.name == "F-20260412-001.md"
    assert "Revenue grew 12% QoQ" in path.read_text()


def test_promote_finding_refuses_without_evidence(wiki: WikiEngine) -> None:
    bad = Finding(id="F-X", title="t", body="b", evidence=[], stat_validate_pass=True)
    with pytest.raises(ValueError, match="evidence"):
        wiki.promote_finding(bad)


def test_promote_finding_refuses_without_stat_validate_pass(wiki: WikiEngine) -> None:
    bad = Finding(id="F-X", title="t", body="b", evidence=["art1"], stat_validate_pass=False)
    with pytest.raises(ValueError, match="stat_validate"):
        wiki.promote_finding(bad)


def test_rebuild_index_lists_all_pages(wiki: WikiEngine) -> None:
    wiki.promote_finding(
        Finding(id="F-X", title="First", body="b", evidence=["a"], stat_validate_pass=True)
    )
    (wiki.root / "entities" / "customers.md").write_text("# customers\n\nentity notes\n")

    wiki.rebuild_index()
    text = (wiki.root / "index.md").read_text()
    assert "F-X" in text
    assert "First" in text
    assert "customers" in text


# ── session cleanup ───────────────────────────────────────────────────────────


def test_cleanup_old_sessions_removes_stale_files(wiki: WikiEngine, tmp_path: Path) -> None:
    """Files older than max_age_days must be deleted."""
    sessions_dir = wiki.root / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    old_file = sessions_dir / "old-session.md"
    old_file.write_text("# old session")
    # Back-date the file to 4 days ago.
    four_days_ago = time.time() - 4 * 86_400
    import os
    os.utime(old_file, (four_days_ago, four_days_ago))

    deleted = wiki.cleanup_old_sessions(max_age_days=3)

    assert deleted == 1
    assert not old_file.exists()


def test_cleanup_old_sessions_keeps_recent_files(wiki: WikiEngine) -> None:
    """Files newer than max_age_days must be preserved."""
    sessions_dir = wiki.root / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    recent_file = sessions_dir / "recent-session.md"
    recent_file.write_text("# recent session")
    # Leave mtime as-is (just created = now).

    deleted = wiki.cleanup_old_sessions(max_age_days=3)

    assert deleted == 0
    assert recent_file.exists()


def test_cleanup_old_sessions_returns_zero_when_no_folder(wiki: WikiEngine) -> None:
    """cleanup_old_sessions on a wiki with no sessions/ dir must not raise."""
    deleted = wiki.cleanup_old_sessions(max_age_days=3)
    assert deleted == 0


def test_write_session_notes_auto_cleans_stale_files(wiki: WikiEngine) -> None:
    """write_session_notes must trigger cleanup of files older than 3 days."""
    sessions_dir = wiki.root / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    stale = sessions_dir / "stale.md"
    stale.write_text("# stale")
    four_days_ago = time.time() - 4 * 86_400
    import os
    os.utime(stale, (four_days_ago, four_days_ago))

    wiki.write_session_notes("new-session", "# new notes")

    # Stale file must be gone; the new one must exist.
    assert not stale.exists()
    assert (sessions_dir / "new-session.md").exists()


# ── log trimming ──────────────────────────────────────────────────────────────


def test_trim_log_to_size_preserves_header() -> None:
    """Header lines must survive trimming."""
    header = "# Log\n\n"
    entries = "".join(f"- 2026-01-01T00:00:{i:02d} — turn {i}\n" for i in range(100))
    content = header + entries
    # Shrink to just the header + last few entries.
    max_bytes = len((header + "- 2026-01-01T00:00:99 — turn 99\n").encode("utf-8")) + 10
    trimmed = _trim_log_to_size(content, max_bytes)
    assert trimmed.startswith("# Log")
    assert "turn 99" in trimmed


def test_trim_log_to_size_drops_oldest_entries() -> None:
    """The oldest entries (lowest index) must be dropped first."""
    header = "# Log\n\n"
    entries = "".join(f"- entry-{i}\n" for i in range(200))
    content = header + entries
    # Force aggressive trimming — keep only ~last entry + header.
    max_bytes = len((header + "- entry-199\n").encode("utf-8")) + 5
    trimmed = _trim_log_to_size(content, max_bytes)
    assert "entry-0" not in trimmed
    assert "entry-199" in trimmed


def test_trim_log_to_size_noop_when_already_fits() -> None:
    """No trimming should occur when content is already within the byte limit."""
    content = "# Log\n\n- entry-1\n- entry-2\n"
    result = _trim_log_to_size(content, max_bytes=10_000)
    assert result == content


def test_append_log_trims_when_over_limit(wiki: WikiEngine, monkeypatch) -> None:
    """append_log must call trimming when the file would exceed the cap."""
    import app.wiki.engine as engine_mod

    # Set a tiny cap so we can trigger trimming without writing 100 MB.
    monkeypatch.setattr(engine_mod, "_LOG_MAX_BYTES", 200)

    # Write enough lines to exceed the cap.
    for i in range(20):
        wiki.append_log(f"entry {i} — " + "x" * 30)

    text = (wiki.root / "log.md").read_text(encoding="utf-8")
    assert len(text.encode("utf-8")) <= 200 + 200  # some slack for last entry
    assert "# Log" in text  # header must survive


# ── cleanup throttle ─────────────────────────────────────────────────────────


def test_cleanup_is_skipped_within_throttle_window(wiki: WikiEngine) -> None:
    """Stale session file must NOT be deleted when _last_cleanup_ts is recent."""
    sessions_dir = wiki.root / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    stale = sessions_dir / "stale.md"
    stale.write_text("# stale")
    four_days_ago = time.time() - 4 * 86_400
    import os
    os.utime(stale, (four_days_ago, four_days_ago))

    # Simulate that cleanup already ran "just now" — throttle must block it.
    wiki._last_cleanup_ts = time.time()
    wiki.write_session_notes("new-session", "# new notes")

    # The stale file must still be present — cleanup was throttled.
    assert stale.exists(), "Stale file should survive when throttle blocks cleanup"


def test_cleanup_runs_after_throttle_window_expires(wiki: WikiEngine) -> None:
    """Stale file must be deleted when the throttle window has expired."""
    sessions_dir = wiki.root / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    stale = sessions_dir / "stale.md"
    stale.write_text("# stale")
    four_days_ago = time.time() - 4 * 86_400
    import os
    os.utime(stale, (four_days_ago, four_days_ago))

    # Simulate that the last cleanup was 2 hours ago — throttle window expired.
    wiki._last_cleanup_ts = time.time() - 7200
    wiki.write_session_notes("new-session", "# new notes")

    # Stale file must be gone now.
    assert not stale.exists(), "Stale file should be deleted after throttle window expires"


# ── ContextManager items accumulation (regression guard) ─────────────────────


def test_context_manager_tool_items_accumulate() -> None:
    """Updating the 'Tool Results' layer must append to items, not replace them.

    This guards against the regression where add_layer was called with a
    single-item list on every tool_result, overwriting the previous items.
    """
    from app.context.manager import ContextLayer, ContextManager

    mgr = ContextManager()
    mgr.add_layer(ContextLayer(name="Tool Results", tokens=0, compactable=True, items=[]))

    items_so_far: list[dict] = []
    for i, tool_name in enumerate(("execute_python", "write_working", "skill"), start=1):
        items_so_far.append({"name": tool_name, "tokens": 100 * i})
        mgr.add_layer(ContextLayer(
            name="Tool Results",
            tokens=sum(it["tokens"] for it in items_so_far),
            compactable=True,
            items=list(items_so_far),
        ))

    snap = mgr.snapshot()
    tool_layer = next(lyr for lyr in snap["layers"] if lyr["name"] == "Tool Results")
    assert len(tool_layer["items"]) == 3, "All three tool items must be present"
    names = [it["name"] for it in tool_layer["items"]]
    assert names == ["execute_python", "write_working", "skill"]
    assert tool_layer["tokens"] == 100 + 200 + 300
