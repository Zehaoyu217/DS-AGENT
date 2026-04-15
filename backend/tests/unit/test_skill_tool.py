"""Tests for the enhanced skill-loading tool (P20)."""
from __future__ import annotations

from pathlib import Path

import pytest

from app.artifacts.store import ArtifactStore
from app.harness.dispatcher import ToolDispatcher, ToolCall
from app.harness.sandbox import SandboxExecutor
from app.harness.skill_tools import _closest_skill_names, register_core_tools
from app.skills.registry import SkillRegistry
from app.wiki.engine import WikiEngine


def _write_skill(root: Path, name: str, *, body: str, references: list[str] = None,
                 has_pkg: bool = True) -> None:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\nversion: 1.2\ndescription: Test skill {name}\nlevel: 2\n---\n{body}"
    )
    (skill_dir / "skill.yaml").write_text(
        "dependencies:\n  requires: [foo]\n  packages: [pandas]\n"
        "errors:\n  BadInput:\n    hint: 'check your input'\n"
    )
    if has_pkg:
        pkg = skill_dir / "pkg"
        pkg.mkdir(exist_ok=True)
        (pkg / "__init__.py").write_text("")
    if references:
        refs = skill_dir / "references"
        refs.mkdir(exist_ok=True)
        for ref in references:
            (refs / ref).write_text("ref content")


def _build_dispatcher(tmp_path: Path) -> tuple[ToolDispatcher, SkillRegistry]:
    skills_root = tmp_path / "skills"
    skills_root.mkdir()
    _write_skill(skills_root, "alpha_skill",
                 body="# Alpha Skill\nUse this for alpha analysis.",
                 references=["cheatsheet.md", "examples.md"])
    _write_skill(skills_root, "beta_skill",
                 body="# Beta Skill\nUse this for beta analysis.",
                 has_pkg=False)

    registry = SkillRegistry(skills_root)
    registry.discover()

    wiki = WikiEngine(root=tmp_path / "wiki")
    (tmp_path / "wiki").mkdir(exist_ok=True)
    artifact_store = ArtifactStore(
        db_path=tmp_path / "artifacts.db",
        disk_root=tmp_path / "artifacts",
    )
    sandbox = SandboxExecutor(python_executable="/usr/bin/env python3")

    dispatcher = ToolDispatcher()
    register_core_tools(
        dispatcher=dispatcher,
        artifact_store=artifact_store,
        wiki=wiki,
        sandbox=sandbox,
        session_id="t-1",
        registry=registry,
    )
    return dispatcher, registry


def test_skill_tool_returns_full_body_and_metadata(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={"name": "alpha_skill"}))
    assert result.ok is True
    payload = result.payload
    assert payload["name"] == "alpha_skill"
    assert "Alpha Skill" in payload["body"]
    assert "alpha analysis" in payload["body"]

    meta = payload["metadata"]
    assert meta["version"] == "1.2"
    assert meta["depth"] == 1
    assert meta["description"] == "Test skill alpha_skill"
    assert meta["requires"] == ["foo"]
    assert meta["packages"] == ["pandas"]
    assert meta["error_templates"] == {"BadInput": {"hint": "check your input"}}


def test_skill_tool_lists_reference_files(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={"name": "alpha_skill"}))
    assert result.payload["references"] == ["cheatsheet.md", "examples.md"]
    assert result.payload["has_python_package"] is True


def test_skill_tool_flags_missing_python_package(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={"name": "beta_skill"}))
    assert result.payload["has_python_package"] is False
    assert result.payload["references"] == []


def test_skill_tool_unknown_suggests_close_match(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(
        ToolCall(id="c1", name="skill", arguments={"name": "alpha_skil"}),
    )
    # Dispatcher wraps KeyError — the result should carry the suggestion text.
    assert result.ok is False
    err_text = (result.error_message or "") + str(result.payload or "")
    assert "alpha_skill" in err_text  # suggestion present


def test_skill_tool_rejects_missing_name(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={}))
    assert result.ok is False
    assert "required" in (result.error_message or "").lower()


def test_closest_skill_names_handles_typos() -> None:
    names = ["correlation", "time_series", "distribution_fit", "group_compare"]
    assert "correlation" in _closest_skill_names("correl", names)
    assert "time_series" in _closest_skill_names("timeseries", names)
    assert _closest_skill_names("", names) == []
    assert _closest_skill_names("xxxxxxxx", names) == []
