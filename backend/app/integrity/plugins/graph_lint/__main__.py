"""Standalone CLI: python -m backend.app.integrity.plugins.graph_lint."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ...config import load_config
from ...protocol import ScanContext
from ...schema import GraphSnapshot
from .plugin import GraphLintPlugin


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m backend.app.integrity.plugins.graph_lint")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    cfg = load_config(repo_root)
    plugin = GraphLintPlugin(config=cfg.plugins.get("graph_lint", {}), today=date.today())
    ctx = ScanContext(repo_root=repo_root, graph=GraphSnapshot.load(repo_root))
    result = plugin.scan(ctx)
    print(f"graph_lint: {len(result.issues)} issues, {len(result.failures)} failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
