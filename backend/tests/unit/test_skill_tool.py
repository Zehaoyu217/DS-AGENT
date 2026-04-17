"""Tests for the skill-loading tool with progressive exposure."""
from __future__ import annotations

from pathlib import Path

from app.artifacts.store import ArtifactStore
from app.harness.dispatcher import ToolCall, ToolDispatcher
from app.harness.sandbox import SandboxExecutor
from app.harness.skill_tools import _closest_skill_names, register_core_tools
from app.skills.registry import SkillRegistry
from app.wiki.engine import WikiEngine


def _write_skill(
    root: Path,
    name: str,
    *,
    description: str = "A test skill.",
    body: str = "# Body\n\nContent.",
    has_pkg: bool = False,
) -> None:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    # Quote the description to handle YAML-special chars like '[' in "[Reference]"
    safe_desc = description.replace("'", "''")
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\nversion: 1.2\ndescription: '{safe_desc}'\n---\n{body}"
    )
    (skill_dir / "skill.yaml").write_text(
        "dependencies:\n  requires: [foo]\n  packages: [pandas]\n"
        "errors:\n  BadInput:\n    hint: 'check your input'\n"
    )
    if has_pkg:
        pkg = skill_dir / "pkg"
        pkg.mkdir(exist_ok=True)
        (pkg / "__init__.py").write_text("")


def _build_dispatcher(tmp_path: Path) -> tuple[ToolDispatcher, SkillRegistry]:
    skills_root = tmp_path / "skills"
    skills_root.mkdir()

    # Hub: stat_hub with two children, one of which has a reference grandchild
    _write_skill(skills_root, "stat_hub", description="Statistical analysis hub.")
    _write_skill(
        skills_root / "stat_hub",
        "correlation",
        description="Runs correlation analysis.",
        has_pkg=True,
    )
    _write_skill(
        skills_root / "stat_hub" / "correlation",
        "corr_reference",
        description="[Reference] Mathematical details. Load only for algorithmic depth.",
    )
    _write_skill(
        skills_root / "stat_hub",
        "distribution",
        description="Fits distributions.",
    )
    # Standalone leaf
    _write_skill(skills_root, "sql_builder", description="Writes SQL queries.")

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


def _call_skill(dispatcher: ToolDispatcher, name: str) -> dict:
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={"name": name}))
    assert result.ok, f"skill({name!r}) failed: {result.error_message}"
    return result.payload


# ── Response format ───────────────────────────────────────────────────────────

def test_hub_skill_body_and_metadata_returned(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "stat_hub")
    assert "Body" in payload["body"] or "stat_hub" in payload["body"]
    meta = payload["metadata"]
    assert meta["name"] == "stat_hub"
    assert meta["version"] == "1.2"
    assert meta["description"] == "Statistical analysis hub."
    assert "level" not in meta
    assert "references" not in payload


def test_hub_skill_appends_sub_skill_catalog(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "stat_hub")
    body = payload["body"]
    assert "## Sub-skills" in body
    assert "`correlation`" in body
    assert "Runs correlation analysis." in body
    assert "`distribution`" in body
    assert "Fits distributions." in body


def test_reference_skill_description_preserved_in_catalog(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "correlation")
    body = payload["body"]
    assert "## Sub-skills" in body
    assert "[Reference]" in body
    assert "`corr_reference`" in body


def test_nested_skill_shows_breadcrumb(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "correlation")
    body = payload["body"]
    assert "stat_hub" in body
    assert "›" in body  # breadcrumb separator


def test_leaf_skill_has_no_sub_skills_section(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "sql_builder")
    assert "## Sub-skills" not in payload["body"]


def test_level_1_skill_has_no_breadcrumb(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "sql_builder")
    assert "›" not in payload["body"]


def test_direct_access_to_level3_skill(tmp_path: Path) -> None:
    """Permissive access — agent can load any skill by name directly."""
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "corr_reference")
    assert payload["metadata"]["name"] == "corr_reference"


def test_skill_unknown_suggests_close_match(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(
        ToolCall(id="c1", name="skill", arguments={"name": "correlat"}),
    )
    assert result.ok is False
    err_text = (result.error_message or "") + str(result.payload or "")
    assert "correlation" in err_text


def test_skill_rejects_missing_name(tmp_path: Path) -> None:
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
