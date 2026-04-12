"""CLI entrypoint for /sop command.

Reads the latest FailureReport for the given level, runs the SOP, and prints
the result as JSON. Invoked via ``python -m app.sop.cli --level <N>`` or
``make sop level=<N>``.
"""
from __future__ import annotations

import argparse
import json
import os
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

    report = _latest_report(Path(args.reports_dir), args.level)
    # v1: preflight inputs default to empty/passing; operators can extend later
    # via env vars or explicit CLI flags.
    result = run_sop(
        report=report,
        judge_variance={},
        seed_fingerprint_matches=True,
        rerun_grades=[],
    )
    print(json.dumps(result.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
