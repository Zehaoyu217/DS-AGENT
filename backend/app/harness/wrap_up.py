from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Protocol

from app.harness.turn_state import TurnState

FINDING_RE = re.compile(
    r"^(?P<id>\[F-\d{8}-\d{3}\])\s+(?P<body>.+?)\."
    r"(?:\s+Evidence:\s*(?P<evidence>[^\.\n]+?)\.)?"
    r"(?:\s+Validated:\s*(?P<validated>[^\.\n]+?)\.)?\s*$",
    re.MULTILINE,
)


class _Wiki(Protocol):
    def append_log(self, entry: str) -> None: ...
    def update_working(self, content: str) -> None: ...
    def rebuild_index(self) -> None: ...
    def promote_finding(
        self, *, finding_id: str, body: str,
        evidence_ids: list[str], validated_by: str,
    ) -> None: ...
    def write_session_notes(self, session_id: str, notes: str) -> None: ...


class _Bus(Protocol):
    def emit(self, event: dict) -> None: ...


@dataclass(frozen=True, slots=True)
class WrapUpResult:
    promoted_finding_ids: tuple[str, ...] = field(default_factory=tuple)
    appended_log: bool = True
    session_notes_written: bool = False


_SESSION_SECTIONS: tuple[str, ...] = (
    "Goal",
    "Approach",
    "Key Findings",
    "Tools Used",
    "Artifacts",
    "Open Questions",
    "Next Steps",
    "Errors / Blockers",
    "Meta",
)


def _render_session_notes(
    *,
    session_id: str,
    turn_index: int,
    final_text: str,
    state: TurnState,
    promoted_finding_ids: list[str],
) -> str:
    """Render a 9-section structured session notes markdown document.

    Sections are always present; empty ones show an explicit placeholder so
    the agent can see which sections it neglected.  The intent is structured
    recall: a future turn can load this file and know exactly what happened
    without re-reading the full tool trace.
    """
    trace = state.as_trace()
    tool_names: list[str] = []
    errors: list[str] = []
    for evt in trace:
        tname = str(evt.get("tool", ""))
        status = str(evt.get("status", ""))
        if tname and tname not in tool_names:
            tool_names.append(tname)
        if status == "error" or status == "blocked":
            errors.append(f"{tname} → {status}")

    scratchpad = state.scratchpad or ""
    goal = _extract_section(scratchpad, "Goal") or "—"
    approach = _extract_section(scratchpad, "Approach") or "—"
    next_steps = _extract_section(scratchpad, "Next Steps") or "—"
    open_q = _extract_section(scratchpad, "Open Questions") or "—"

    findings_lines = (
        "\n".join(f"- `{fid}`" for fid in promoted_finding_ids)
        if promoted_finding_ids
        else "_no findings promoted this turn_"
    )
    artifact_lines = (
        "\n".join(f"- `{aid}`" for aid in state.artifact_ids())
        if state.artifact_ids()
        else "_no artifacts this turn_"
    )
    tools_lines = (
        "\n".join(f"- `{name}`" for name in tool_names)
        if tool_names
        else "_no tools invoked_"
    )
    error_lines = "\n".join(f"- {e}" for e in errors) if errors else "_no errors_"

    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    parts = [
        f"# Session Notes — `{session_id}`",
        "",
        f"## {_SESSION_SECTIONS[0]}",
        goal,
        "",
        f"## {_SESSION_SECTIONS[1]}",
        approach,
        "",
        f"## {_SESSION_SECTIONS[2]}",
        findings_lines,
        "",
        f"## {_SESSION_SECTIONS[3]}",
        tools_lines,
        "",
        f"## {_SESSION_SECTIONS[4]}",
        artifact_lines,
        "",
        f"## {_SESSION_SECTIONS[5]}",
        open_q,
        "",
        f"## {_SESSION_SECTIONS[6]}",
        next_steps,
        "",
        f"## {_SESSION_SECTIONS[7]}",
        error_lines,
        "",
        f"## {_SESSION_SECTIONS[8]}",
        f"- session_id: `{session_id}`",
        f"- turn_index: {turn_index}",
        f"- last_turn_final_text: {final_text[:160]}"
        + ("…" if len(final_text) > 160 else ""),
        f"- updated_at: {stamp}",
        "",
    ]
    return "\n".join(parts)


def _extract_section(scratchpad: str, heading: str) -> str:
    """Pull the body of `## <heading>` out of the scratchpad."""
    if not scratchpad:
        return ""
    lines = scratchpad.splitlines()
    target = f"## {heading}"
    start: int | None = None
    for i, line in enumerate(lines):
        if line.strip() == target:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    body = "\n".join(lines[start:end]).strip()
    return body


def _parse_findings(scratchpad: str) -> list[dict]:
    # Only scan lines inside the "## Findings" section if present.
    lines = scratchpad.splitlines()
    start, end = None, None
    for i, line in enumerate(lines):
        if line.strip() == "## Findings":
            start = i + 1
        elif start is not None and line.startswith("## ") and i > start:
            end = i
            break
    if start is None:
        return []
    section = "\n".join(lines[start:end if end else None])
    findings: list[dict] = []
    for m in FINDING_RE.finditer(section):
        fid = m.group("id").strip("[]")
        body = m.group("body").strip()
        ev_raw = (m.group("evidence") or "").strip()
        val = (m.group("validated") or "").strip()
        ev = [e.strip() for e in re.split(r"[,\s]+", ev_raw) if e.strip()]
        findings.append({
            "id": fid,
            "body": body,
            "evidence_ids": ev,
            "validated_by": val,
        })
    return findings


def _validate_passed(state: TurnState) -> bool:
    for evt in state.as_trace():
        if evt.get("tool") == "stat_validate.validate":
            result = evt.get("result") or {}
            if str(result.get("status", "")).upper() == "PASS":
                return True
    return False


class TurnWrapUp:
    def __init__(self, wiki: _Wiki, event_bus: _Bus) -> None:
        self._wiki = wiki
        self._bus = event_bus

    def finalize(
        self,
        state: TurnState,
        final_text: str,
        session_id: str,
        turn_index: int,
    ) -> WrapUpResult:
        promoted: list[str] = []
        parse_ok = _validate_passed(state)
        for f in _parse_findings(state.scratchpad):
            if not f["evidence_ids"] or not f["validated_by"] or not parse_ok:
                continue
            self._wiki.promote_finding(
                finding_id=f["id"], body=f["body"],
                evidence_ids=list(f["evidence_ids"]),
                validated_by=f["validated_by"],
            )
            promoted.append(f["id"])

        self._wiki.update_working(state.scratchpad)
        self._wiki.rebuild_index()
        self._wiki.append_log(
            f"turn {turn_index}: session={session_id} "
            f"artifacts={list(state.artifact_ids())} promoted={promoted}"
        )

        # Structured 9-section session notes (P18).  Best-effort: a missing
        # or broken wiki should never crash the wrap-up.
        notes_written = False
        try:
            notes = _render_session_notes(
                session_id=session_id,
                turn_index=turn_index,
                final_text=final_text,
                state=state,
                promoted_finding_ids=promoted,
            )
            self._wiki.write_session_notes(session_id, notes)
            notes_written = True
        except Exception:  # noqa: BLE001 — structured notes must never fail the turn
            notes_written = False

        self._bus.emit({
            "type": "turn_completed",
            "session_id": session_id,
            "turn_index": turn_index,
            "artifact_ids": list(state.artifact_ids()),
            "promoted_finding_ids": promoted,
            "final_text_preview": final_text[:200],
            "session_notes_written": notes_written,
        })
        return WrapUpResult(
            promoted_finding_ids=tuple(promoted),
            appended_log=True,
            session_notes_written=notes_written,
        )
