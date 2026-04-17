from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

import pytest


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True)


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    """Synthetic mini-repo exercising every doc_audit rule.

    Layout (relative to returned path):
      CLAUDE.md                # links to all "good" docs
      docs/dev-setup.md        # required (coverage)
      docs/testing.md          # required
      docs/gotchas.md          # required
      docs/skill-creation.md   # required
      docs/log.md              # required
      docs/orphan.md           # NOT linked → unindexed
      docs/broken.md           # links to gone.md → broken_link
      docs/anchor-broken.md    # links to dev-setup.md#nope → broken_link (anchor)
      docs/dead-ref.md         # `backend/app/missing.py` + `Module.gone` → dead_code_ref
      knowledge/adr/001-real.md    # Accepted, refs live foo.py → no issue
      knowledge/adr/002-drift.md   # Accepted, refs missing.py → adr_status_drift
      knowledge/adr/template.md    # Accepted but excluded
      backend/app/foo.py
      graphify/graph.json
    """
    repo = tmp_path / "tiny"
    repo.mkdir()

    (repo / "CLAUDE.md").write_text(
        "# Index\n\n"
        "- [Dev setup](docs/dev-setup.md)\n"
        "- [Testing](docs/testing.md)\n"
        "- [Gotchas](docs/gotchas.md)\n"
        "- [Skill creation](docs/skill-creation.md)\n"
        "- [Changelog](docs/log.md)\n"
        "- [Broken](docs/broken.md)\n"
        "- [Anchor broken](docs/anchor-broken.md)\n"
        "- [Dead ref](docs/dead-ref.md)\n"
        "- [ADR 001](knowledge/adr/001-real.md)\n"
        "- [ADR 002](knowledge/adr/002-drift.md)\n"
        "- [ADR template](knowledge/adr/template.md)\n",
        encoding="utf-8",
    )
    docs = repo / "docs"
    docs.mkdir()
    for name in ("dev-setup.md", "testing.md", "gotchas.md", "skill-creation.md", "log.md"):
        (docs / name).write_text(f"# {name}\n", encoding="utf-8")
    (docs / "orphan.md").write_text("# Not linked from index\n", encoding="utf-8")
    (docs / "broken.md").write_text("See [gone](gone.md).\n", encoding="utf-8")
    (docs / "anchor-broken.md").write_text(
        "See [setup](dev-setup.md#nope).\n", encoding="utf-8"
    )
    (docs / "dead-ref.md").write_text(
        "Refs `backend/app/missing.py:7` and `Module.gone_func`.\n",
        encoding="utf-8",
    )

    adr = repo / "knowledge" / "adr"
    adr.mkdir(parents=True)
    (adr / "001-real.md").write_text(
        "# ADR 001\n\n**Status:** Accepted\n\nUses `backend/app/foo.py`.\n",
        encoding="utf-8",
    )
    (adr / "002-drift.md").write_text(
        "# ADR 002\n\n**Status:** Accepted\n\nReferences `backend/app/missing.py:1`.\n",
        encoding="utf-8",
    )
    (adr / "template.md").write_text(
        "# Template\n\n**Status:** Accepted\n\nReferences `backend/app/missing.py`.\n",
        encoding="utf-8",
    )

    (repo / "backend" / "app").mkdir(parents=True)
    (repo / "backend" / "app" / "foo.py").write_text("# real file\n", encoding="utf-8")

    g = repo / "graphify"
    g.mkdir()
    (g / "graph.json").write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "id": "foo.do_thing",
                        "label": "do_thing",
                        "source_file": "backend/app/foo.py",
                    }
                ],
                "links": [],
            }
        ),
        encoding="utf-8",
    )

    # Initialize git so stale_candidate has commit timestamps to read
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")

    return repo


@pytest.fixture
def today_fixed() -> date:
    return date(2026, 4, 17)
