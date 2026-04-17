"""Tests for structured session notes (P18)."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from app.harness.turn_state import TurnState
from app.harness.wrap_up import (
    _SESSION_SECTIONS,
    TurnWrapUp,
    _extract_section,
    _render_session_notes,
)
from app.wiki.engine import WikiEngine, _safe_session_filename


def test_render_session_notes_has_all_nine_sections() -> None:
    state = TurnState(scratchpad="")
    md = _render_session_notes(
        session_id="abc",
        turn_index=1,
        final_text="done",
        state=state,
        promoted_finding_ids=[],
    )
    for section in _SESSION_SECTIONS:
        assert f"## {section}" in md, f"missing section: {section}"
    assert "Session Notes — `abc`" in md


def test_render_session_notes_pulls_goal_from_scratchpad() -> None:
    scratchpad = (
        "## Goal\nInvestigate correlation between X and Y.\n\n"
        "## Approach\nRun spearman + permutation test.\n\n"
        "## Next Steps\nTry segmented regression.\n"
    )
    state = TurnState(scratchpad=scratchpad)
    md = _render_session_notes(
        session_id="s-1",
        turn_index=2,
        final_text="final",
        state=state,
        promoted_finding_ids=["F-1"],
    )
    assert "Investigate correlation between X and Y." in md
    assert "Run spearman + permutation test." in md
    assert "Try segmented regression." in md
    assert "`F-1`" in md


def test_render_session_notes_lists_tools_and_artifacts() -> None:
    state = TurnState()
    state.record_tool("execute_python", {"ok": True}, status="ok")
    state.record_tool("save_artifact", {"artifact_id": "a1"}, status="ok")
    state.record_tool("stat_validate.validate", {"status": "ERROR"}, status="error")
    state.record_artifact("a1")
    state.record_artifact("a2")
    md = _render_session_notes(
        session_id="s", turn_index=1, final_text="",
        state=state, promoted_finding_ids=[],
    )
    assert "`execute_python`" in md
    assert "`save_artifact`" in md
    assert "`a1`" in md
    assert "`a2`" in md
    assert "stat_validate.validate → error" in md


def test_render_session_notes_placeholder_when_empty() -> None:
    state = TurnState(scratchpad="")
    md = _render_session_notes(
        session_id="s", turn_index=0, final_text="",
        state=state, promoted_finding_ids=[],
    )
    assert "no tools invoked" in md
    assert "no artifacts this turn" in md
    assert "no findings promoted this turn" in md
    assert "no errors" in md


def test_extract_section_reads_body_until_next_h2() -> None:
    text = (
        "## Goal\nbody of goal\nline 2\n\n"
        "## Approach\nbody of approach\n"
    )
    assert _extract_section(text, "Goal") == "body of goal\nline 2"
    assert _extract_section(text, "Approach") == "body of approach"
    assert _extract_section(text, "Missing") == ""
    assert _extract_section("", "Goal") == ""


def test_turn_wrap_up_writes_session_notes() -> None:
    wiki = MagicMock()
    bus = MagicMock()
    state = TurnState(scratchpad="## Goal\ntest goal\n")
    state.record_artifact("a1")

    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    result = wrap.finalize(
        state=state, final_text="ok", session_id="sess-42", turn_index=5,
    )
    wiki.write_session_notes.assert_called_once()
    args = wiki.write_session_notes.call_args
    assert args.args[0] == "sess-42"
    assert "test goal" in args.args[1]
    assert result.session_notes_written is True


def test_turn_wrap_up_tolerates_session_notes_failure() -> None:
    wiki = MagicMock()
    wiki.write_session_notes.side_effect = OSError("disk full")
    bus = MagicMock()
    state = TurnState(scratchpad="## Goal\ntest\n")
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    result = wrap.finalize(
        state=state, final_text="", session_id="s", turn_index=1,
    )
    assert result.session_notes_written is False
    # turn_completed event still emits, and its payload records the failure.
    assert bus.emit.called
    evt = bus.emit.call_args_list[-1].args[0]
    assert evt["session_notes_written"] is False


def test_wiki_engine_writes_session_notes(tmp_path: Path) -> None:
    wiki = WikiEngine(root=tmp_path)
    path = wiki.write_session_notes("session-abc-123", "# test notes\n")
    assert path == tmp_path / "sessions" / "session-abc-123.md"
    assert path.read_text() == "# test notes\n"

    # Overwrite test: second call replaces the file.
    wiki.write_session_notes("session-abc-123", "# updated\n")
    assert path.read_text() == "# updated\n"


def test_safe_session_filename_strips_unsafe_chars() -> None:
    assert _safe_session_filename("abc123") == "abc123"
    assert _safe_session_filename("a/b\\c") == "a-b-c"
    assert _safe_session_filename("") == "unknown"
    # Length cap.
    assert len(_safe_session_filename("x" * 500)) <= 96


# --- New tests for min-turns guard, Worklog, and 3000-char cap ---

def test_notes_skipped_for_trivial_turn() -> None:
    """No tools called, turn_index=1 → notes must NOT be written."""
    wiki = MagicMock()
    bus = MagicMock()
    state = TurnState(dataset_loaded=False)  # no tools called
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="hi", session_id="s1", turn_index=1)
    wiki.write_session_notes.assert_not_called()


def test_notes_written_when_tools_used_on_turn_1() -> None:
    """Tools called on turn 1 → notes SHOULD be written."""
    wiki = MagicMock()
    bus = MagicMock()
    state = TurnState(dataset_loaded=False)
    state.record_tool("execute_python", {}, "ok")
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="result", session_id="s2", turn_index=1)
    wiki.write_session_notes.assert_called_once()


def test_notes_written_on_turn_2_without_tools() -> None:
    """turn_index=2 with no tools → notes SHOULD be written (turn threshold met)."""
    wiki = MagicMock()
    bus = MagicMock()
    state = TurnState(dataset_loaded=False)
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="hi again", session_id="s3", turn_index=2)
    wiki.write_session_notes.assert_called_once()


def test_notes_capped_at_3000_chars() -> None:
    """Notes must be ≤ 3000 chars when written."""
    wiki = MagicMock()
    bus = MagicMock()
    state = TurnState(dataset_loaded=False)
    state.record_tool("execute_python", {}, "ok")
    # Bloat final_text to force notes over 3000 chars.
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(
        state=state,
        final_text="x" * 3000,
        session_id="cap-test",
        turn_index=2,
    )
    assert wiki.write_session_notes.called
    written = wiki.write_session_notes.call_args[0][1]
    assert len(written) <= 3000


def test_worklog_auto_populated_from_trace() -> None:
    """Worklog section lists each tool call with step index and status."""
    state = TurnState()
    state.record_tool("execute_python", {}, "ok")
    state.record_tool("save_artifact", {"artifact_id": "a1"}, "ok")
    state.record_tool("stat_validate.validate", {}, "error")
    md = _render_session_notes(
        session_id="wl-test",
        turn_index=3,
        final_text="done",
        state=state,
        promoted_finding_ids=[],
    )
    assert "## Worklog" in md
    assert "step 1: `execute_python` → ok" in md
    assert "step 2: `save_artifact` → ok" in md
    assert "step 3: `stat_validate.validate` → error" in md


def test_worklog_placeholder_when_no_tools() -> None:
    """Worklog shows placeholder when no tools were called."""
    state = TurnState()
    md = _render_session_notes(
        session_id="wl-empty",
        turn_index=0,
        final_text="",
        state=state,
        promoted_finding_ids=[],
    )
    assert "## Worklog" in md
    assert "_no tool activity_" in md
