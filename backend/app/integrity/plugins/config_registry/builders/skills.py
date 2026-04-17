"""SkillsBuilder — walks the skills tree and produces SkillEntry list.

Two distinct identifiers are tracked per skill:

- ``id``        : dotted filesystem path relative to ``backend/app/skills/``
                   (e.g. ``charting.altair_charts.altair_reference``). Stable,
                   collision-free, and unambiguous within the manifest.
- ``registry_key``: the ``name:`` field from each ``SKILL.md`` frontmatter —
                   the same source ``backend/app/skills/registry.SkillRegistry``
                   uses to populate ``_index``. May collide across skills
                   (last-wins, mirrors the registry behavior). ``None`` only
                   when frontmatter lacks ``name`` (in which case the
                   registry would also skip the skill — so that entry is
                   excluded from the parity check at gate δ #2).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..hashing import git_blob_sha

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class SkillEntry:
    id: str
    path: str
    yaml_path: str | None
    version: str
    description: str
    parent: str | None
    registry_key: str | None = None
    children: list[str] = field(default_factory=list)
    sha_skill_md: str = ""
    sha_skill_yaml: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "registry_key": self.registry_key,
            "path": self.path,
            "yaml_path": self.yaml_path,
            "version": self.version,
            "description": self.description,
            "parent": self.parent,
            "children": list(self.children),
            "sha_skill_md": self.sha_skill_md,
            "sha_skill_yaml": self.sha_skill_yaml,
        }


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body


class SkillsBuilder:
    def __init__(self, skills_root: Path, repo_root: Path | None = None) -> None:
        self.skills_root = skills_root
        self.repo_root = repo_root or skills_root.parent.parent.parent

    def build(self) -> tuple[list[SkillEntry], list[str]]:
        if not self.skills_root.exists():
            return [], []

        # Discover every directory containing a SKILL.md.
        entries: dict[str, SkillEntry] = {}
        failures: list[str] = []

        for skill_md in sorted(self.skills_root.rglob("SKILL.md")):
            try:
                entry = self._build_entry(skill_md)
            except Exception as exc:  # parse error, IO error, etc.
                rel = skill_md.relative_to(self.repo_root).as_posix()
                failures.append(f"skills:{rel}: {type(exc).__name__}: {exc}")
                continue
            entries[entry.id] = entry

        # Populate children + parent.
        for sid, entry in entries.items():
            children = sorted(
                cid for cid in entries
                if cid != sid and cid.startswith(f"{sid}.")
                and "." not in cid[len(sid) + 1:]
            )
            object.__setattr__(entry, "children", children)
            if "." in sid:
                parent = sid.rsplit(".", 1)[0]
                object.__setattr__(entry, "parent", parent if parent in entries else None)
            else:
                object.__setattr__(entry, "parent", None)

        return [entries[i] for i in sorted(entries)], failures

    def _build_entry(self, skill_md: Path) -> SkillEntry:
        skill_dir = skill_md.parent
        rel_dir = skill_dir.relative_to(self.skills_root).as_posix()
        sid = rel_dir.replace("/", ".") if rel_dir != "." else skill_dir.name

        text = skill_md.read_text(encoding="utf-8")
        fm, _ = _split_frontmatter(text)
        version = str(fm.get("version", "0.0.0"))
        description = str(fm.get("description", "")).strip()
        # Same source SkillRegistry uses to populate ``_index`` keys.
        registry_key_raw = fm.get("name")
        registry_key = (
            str(registry_key_raw).strip() or None
            if registry_key_raw is not None
            else None
        )

        yaml_file = skill_dir / "skill.yaml"
        yaml_rel = yaml_file.relative_to(self.repo_root).as_posix() if yaml_file.exists() else None
        sha_yaml = git_blob_sha(yaml_file) if yaml_file.exists() else None

        return SkillEntry(
            id=sid,
            path=skill_md.relative_to(self.repo_root).as_posix(),
            yaml_path=yaml_rel,
            version=version,
            description=description,
            parent=None,            # populated after pass 2
            registry_key=registry_key,
            children=[],            # populated after pass 2
            sha_skill_md=git_blob_sha(skill_md),
            sha_skill_yaml=sha_yaml,
        )
