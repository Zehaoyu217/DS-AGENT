"""ConfigsBuilder — type-detected inventory of well-known config files."""
from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..hashing import git_blob_sha

# Detection table: regex over relative posix path → type label.
_TYPE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^pyproject\.toml$"), "pyproject"),
    (re.compile(r"^package\.json$"), "package_json"),
    (re.compile(r"^\.claude/settings\.json$"), "claude_settings"),
    (re.compile(r"^config/integrity\.yaml$"), "integrity_yaml"),
    (re.compile(r"^vite\.config\.(ts|js|mjs)$"), "vite_config"),
    (re.compile(r"^tsconfig.*\.json$"), "tsconfig"),
    (re.compile(r"^Dockerfile.*$"), "dockerfile"),
    (re.compile(r"^Makefile$"), "makefile"),
    (re.compile(r"^\.env\.example$"), "env_example"),
    (re.compile(r"^infra/.*\.(yaml|yml)$"), "infra_yaml"),
    (re.compile(r"^infra/.*\.tf$"), "infra_terraform"),
    (re.compile(r"^config/.*$"), "generic_config"),
]


@dataclass(frozen=True)
class ConfigEntry:
    id: str
    type: str
    path: str
    sha: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "type": self.type,
                "path": self.path, "sha": self.sha}


def _match_type(rel_path: str) -> str | None:
    for pat, t in _TYPE_PATTERNS:
        if pat.match(rel_path):
            return t
    return None


class ConfigsBuilder:
    def __init__(
        self,
        repo_root: Path,
        globs: list[str],
        excluded: list[str],
    ) -> None:
        self.repo_root = repo_root
        self.globs = list(globs)
        self.excluded = list(excluded)

    def build(self) -> tuple[list[ConfigEntry], list[str]]:
        seen: dict[str, ConfigEntry] = {}
        failures: list[str] = []

        for pattern in self.globs:
            for path in sorted(self.repo_root.glob(pattern)):
                if not path.is_file():
                    continue
                rel = path.relative_to(self.repo_root).as_posix()
                if any(fnmatch.fnmatch(rel, ex) for ex in self.excluded):
                    continue
                t = _match_type(rel)
                if t is None:
                    # File matched a glob but type-table didn't classify it.
                    # Use generic_config only if under config/, else skip.
                    if rel.startswith("config/"):
                        t = "generic_config"
                    else:
                        continue
                seen[rel] = ConfigEntry(
                    id=rel, type=t, path=rel, sha=git_blob_sha(path),
                )

        entries = [seen[k] for k in sorted(seen)]
        return entries, failures
