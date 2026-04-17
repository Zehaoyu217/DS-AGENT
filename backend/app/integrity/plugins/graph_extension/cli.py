from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .plugin import GraphExtensionPlugin
from ...protocol import ScanContext
from ...schema import GraphSnapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run plugin A — graph augmentation.")
    parser.add_argument(
        "--repo-root",
        default=".",
        type=Path,
        help="Path to the repository root (default: cwd).",
    )
    args = parser.parse_args(argv)
    repo = args.repo_root.resolve()

    graph = GraphSnapshot.load(repo)
    ctx = ScanContext(repo_root=repo, graph=graph)
    result = GraphExtensionPlugin().scan(ctx)

    summary = {
        "plugin": result.plugin_name,
        "version": result.plugin_version,
        "artifacts": [str(a) for a in result.artifacts],
        "failures": result.failures,
    }
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not result.failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
