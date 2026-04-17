"""Acceptance-gate proof: SkillsBuilder == SkillRegistry._index parity.

Runs against the *real* backend/app/skills/ directory (not a fixture).
This is the structural guarantee for gate δ #2.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.integrity.plugins.config_registry.builders.skills import (
    SkillsBuilder,
)


REPO_ROOT = Path(__file__).resolve().parents[6]
SKILLS_ROOT = REPO_ROOT / "backend" / "app" / "skills"


@pytest.mark.skipif(not SKILLS_ROOT.exists(), reason="real skills tree not present")
def test_builder_count_matches_registry() -> None:
    from backend.app.skills.registry import SkillRegistry

    registry = SkillRegistry(SKILLS_ROOT)
    registry.discover()
    builder = SkillsBuilder(skills_root=SKILLS_ROOT, repo_root=REPO_ROOT)
    entries, failures = builder.build()
    assert failures == [], f"builder failures: {failures}"
    assert len(entries) == len(registry._index), (
        f"manifest skills: {len(entries)} != registry._index: "
        f"{len(registry._index)}\n"
        f"missing in builder: {set(registry._index) - {e.id for e in entries}}\n"
        f"extra in builder:   {set(e.id for e in entries) - set(registry._index)}"
    )


@pytest.mark.skipif(not SKILLS_ROOT.exists(), reason="real skills tree not present")
def test_builder_ids_match_registry_keys() -> None:
    from backend.app.skills.registry import SkillRegistry

    registry = SkillRegistry(SKILLS_ROOT)
    registry.discover()
    builder = SkillsBuilder(skills_root=SKILLS_ROOT, repo_root=REPO_ROOT)
    entries, _ = builder.build()
    assert {e.id.split(".")[-1] for e in entries} == set(registry._index)
