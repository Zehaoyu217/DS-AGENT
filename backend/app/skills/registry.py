from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from app.skills.base import SkillMetadata


@dataclass
class LoadedSkill:
    """A discovered and loaded skill (evals excluded)."""

    metadata: SkillMetadata
    instructions: str
    package_path: Path
    references_path: Path | None
    evals_path: None = None  # deliberately excluded — never exposed to agent


class SkillRegistry:
    """Discovers and loads skills from a directory tree."""

    def __init__(self, skills_root: Path) -> None:
        self._root = skills_root
        self._skills: dict[str, LoadedSkill] = {}

    def discover(self) -> None:
        """Scan skills_root for valid skill directories and load them."""
        self._skills.clear()
        if not self._root.exists():
            return

        for skill_dir in sorted(self._root.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_yaml = skill_dir / "skill.yaml"
            skill_md = skill_dir / "SKILL.md"
            if not skill_yaml.exists() or not skill_md.exists():
                continue

            raw = yaml.safe_load(skill_yaml.read_text())
            deps = raw.get("dependencies", {})
            metadata = SkillMetadata(
                name=raw["name"],
                version=raw.get("version", "0.0"),
                description=raw.get("description", ""),
                level=raw.get("level", 1),
                dependencies_requires=deps.get("requires", []),
                dependencies_used_by=deps.get("used_by", []),
                dependencies_packages=deps.get("packages", []),
                error_templates=raw.get("errors", {}),
            )

            instructions = skill_md.read_text()
            pkg_path = skill_dir / "pkg"
            refs_path = skill_dir / "references"

            self._skills[metadata.name] = LoadedSkill(
                metadata=metadata,
                instructions=instructions,
                package_path=pkg_path,
                references_path=refs_path if refs_path.exists() else None,
                # evals_path deliberately not set — sealed from agent
            )

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())

    def get_skill(self, name: str) -> LoadedSkill | None:
        return self._skills.get(name)

    def get_instructions(self, name: str) -> str | None:
        skill = self._skills.get(name)
        return skill.instructions if skill else None

    def get_dependency_graph(self) -> dict[str, list[str]]:
        """Return {skill_name: [required_skills]} mapping."""
        return {
            name: skill.metadata.dependencies_requires
            for name, skill in self._skills.items()
        }
