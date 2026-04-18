#!/usr/bin/env python3
"""GAN trace-corpus CLI bridge.

Exposes the backend trace store to GAN evaluator agents as a simple
JSON-over-stdout CLI, avoiding a network hop for local workflows.

Examples
--------
List the last 20 trace summaries (JSON array on stdout)::

    python scripts/gan-trace-corpus.py --list

Load a specific trace as JSON::

    python scripts/gan-trace-corpus.py --load <session_id>

The traces directory defaults to ``$TRACE_DIR`` or ``traces`` relative
to the current working directory — override with ``--traces-dir``.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
_BACKEND = REPO_ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

# Imported after path prepend so the CLI works from any cwd.
from app.trace.store import (  # type: ignore  # noqa: E402
    TraceNotFoundError,
    list_traces,
    load_trace,
)

DEFAULT_LIMIT = 20


def _default_traces_dir() -> Path:
    env = os.environ.get("TRACE_DIR")
    if env:
        return Path(env)
    # Prefer backend/traces then backend/data/traces, else cwd/traces.
    for candidate in (
        REPO_ROOT / "backend" / "traces",
        REPO_ROOT / "backend" / "data" / "traces",
        REPO_ROOT / "traces",
    ):
        if candidate.exists():
            return candidate
    return Path.cwd() / "traces"


def _list_payload(traces_dir: Path, limit: int) -> list[dict[str, Any]]:
    summaries = list_traces(traces_dir)
    # Most recent first — summaries include started_at/ended_at strings.
    sorted_summaries = sorted(
        summaries,
        key=lambda s: (s.ended_at or "", s.started_at or ""),
        reverse=True,
    )
    trimmed = sorted_summaries[:limit]
    return [
        {
            "id": s.session_id,
            "session_id": s.session_id,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
            "duration_ms": s.duration_ms,
            "event_count": (s.turn_count or 0) + (s.llm_call_count or 0),
            "level": s.level,
            "level_label": s.level_label,
            "outcome": s.outcome,
            "final_grade": s.final_grade,
        }
        for s in trimmed
    ]


def _load_payload(traces_dir: Path, trace_id: str) -> dict[str, Any]:
    trace = load_trace(traces_dir, trace_id)
    return trace.model_dump()


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="gan-trace-corpus",
        description="Read-only view of the backend trace corpus for GAN evaluators.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List recent trace summaries as JSON.")
    group.add_argument("--load", metavar="ID", help="Print a specific trace as JSON.")
    parser.add_argument(
        "--traces-dir",
        type=Path,
        default=None,
        help="Override traces directory (default: $TRACE_DIR or traces/).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Max summaries when --list (default: {DEFAULT_LIMIT}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    traces_dir = args.traces_dir or _default_traces_dir()

    if args.list:
        payload = _list_payload(traces_dir, max(1, args.limit))
        json.dump(payload, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    assert args.load is not None  # mutual-exclusive group guarantees this
    try:
        payload = _load_payload(traces_dir, args.load)
    except TraceNotFoundError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    except ValueError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
