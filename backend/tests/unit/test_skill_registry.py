from pathlib import Path

from app.skills.registry import SkillRegistry


def test_registry_discovers_skills(tmp_path: Path) -> None:
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: test_skill\n---\n# Test Skill\n")
    (skill_dir / "skill.yaml").write_text(
        "name: test_skill\nversion: '1.0'\ndescription: A test\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    assert "test_skill" in registry.list_skills()


def test_registry_loads_skill_instructions(tmp_path: Path) -> None:
    skill_dir = tmp_path / "eda"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: eda\n---\n# EDA\nExploratory analysis.\n")
    (skill_dir / "skill.yaml").write_text(
        "name: eda\nversion: '1.0'\ndescription: EDA\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    instructions = registry.get_instructions("eda")
    assert "Exploratory analysis" in instructions


def test_registry_excludes_evals(tmp_path: Path) -> None:
    skill_dir = tmp_path / "query_data"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: query_data\n---\n# Query\n")
    (skill_dir / "skill.yaml").write_text(
        "name: query_data\nversion: '1.0'\ndescription: Query\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")
    evals_dir = skill_dir / "evals"
    evals_dir.mkdir()
    (evals_dir / "eval.yaml").write_text("cases: []")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    skill = registry.get_skill("query_data")
    assert skill is not None
    # evals/ is in _SKIP_DIRS so it is never discovered as a child skill.
    assert skill.children == []


def test_registry_returns_none_for_unknown_skill(tmp_path: Path) -> None:
    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    assert registry.get_skill("nonexistent") is None
    assert registry.get_instructions("nonexistent") is None
