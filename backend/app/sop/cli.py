"""CLI entrypoint for /sop command.

Reads the latest FailureReport for the given level, runs the SOP, and prints
the result as JSON. Invoked via ``python -m app.sop.cli --level <N>`` or
``make sop level=<N>``.

Note: ``--reports-dir`` is a trusted operator input; this CLI is for developer use
and is not exposed over any network surface.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from app.sop.runner import run_sop
from app.sop.types import FailureReport


def _latest_report(reports_dir: Path, level: int) -> FailureReport:
    candidates = sorted(reports_dir.glob(f"*-level{level}.yaml"))
    if not candidates:
        raise FileNotFoundError(
            f"No FailureReport for level {level} in {reports_dir}. "
            f"Run `make eval level={level}` first."
        )
    data = yaml.safe_load(candidates[-1].read_text(encoding="utf-8"))
    if data is None:
        raise ValueError(f"Empty FailureReport: {candidates[-1]}")
    return FailureReport.model_validate(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", type=int, required=True)
    parser.add_argument(
        "--reports-dir",
        default=os.environ.get("SOP_REPORTS_DIR", "tests/evals/reports"),
    )
    args = parser.parse_args()

    try:
        report = _latest_report(Path(args.reports_dir), args.level)
        result = run_sop(
            report=report,
            judge_variance={},
            seed_fingerprint_matches=True,
            rerun_grades=[],
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: invalid report: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
