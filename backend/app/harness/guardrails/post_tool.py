from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.harness.dispatcher import ToolResult

STDOUT_TRIM_THRESHOLD = 500


@dataclass(frozen=True, slots=True)
class PostToolReport:
    new_artifact_ids: tuple[str, ...] = field(default_factory=tuple)
    trimmed_stdout: str | None = None
    gotcha_injections: tuple[str, ...] = field(default_factory=tuple)
    events: tuple[dict, ...] = field(default_factory=tuple)


def _extract_artifact_ids(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    ids: list[str] = []
    if payload.get("artifact_id"):
        ids.append(str(payload["artifact_id"]))
    for key in ("qq_artifact_id", "pdf_overlay_artifact_id", "report_artifact_id"):
        if payload.get(key):
            ids.append(str(payload[key]))
    return ids


def _trim_stdout(stdout: str) -> str | None:
    if len(stdout) <= STDOUT_TRIM_THRESHOLD:
        return None
    head = stdout[: STDOUT_TRIM_THRESHOLD // 2]
    tail = stdout[-STDOUT_TRIM_THRESHOLD // 2 :]
    return (
        f"{head}\n... [trimmed {len(stdout) - STDOUT_TRIM_THRESHOLD} chars] ...\n{tail}"
    )


def post_tool(result: ToolResult) -> PostToolReport:
    artifact_ids = _extract_artifact_ids(result.payload)
    events: list[dict] = []
    for aid in artifact_ids:
        events.append({"type": "artifact_emitted",
                       "artifact_id": aid,
                       "tool_name": result.tool_name})

    trimmed: str | None = None
    if isinstance(result.payload, dict):
        stdout = str(result.payload.get("stdout", ""))
        if stdout:
            trimmed = _trim_stdout(stdout)

    gotcha_refs: tuple[str, ...] = ()
    if result.tool_name == "stat_validate.validate" and isinstance(result.payload, dict):
        refs = result.payload.get("gotcha_refs") or []
        gotcha_refs = tuple(str(r) for r in refs)

    return PostToolReport(
        new_artifact_ids=tuple(artifact_ids),
        trimmed_stdout=trimmed,
        gotcha_injections=gotcha_refs,
        events=tuple(events),
    )
