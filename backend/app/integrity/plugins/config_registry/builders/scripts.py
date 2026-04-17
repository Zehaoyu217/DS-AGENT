"""ScriptsBuilder — inventories scripts/** with interpreter detection.

Shebang takes precedence; extension is the safe fallback.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..hashing import git_blob_sha

EXT_INTERPRETER = {
    ".py": "python3",
    ".sh": "bash",
    ".ts": "node",
    ".js": "node",
}

SHEBANG_INTERPRETERS = ("python3", "python", "bash", "sh", "node")


@dataclass(frozen=True)
class ScriptEntry:
    id: str
    path: str
    interpreter: str
    sha: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "path": self.path,
                "interpreter": self.interpreter, "sha": self.sha}


def _detect_interpreter(path: Path) -> str:
    try:
        first_line = path.open("rb").readline().decode("utf-8", errors="replace").strip()
    except OSError:
        first_line = ""
    if first_line.startswith("#!"):
        for name in SHEBANG_INTERPRETERS:
            if name in first_line:
                if name == "python":
                    return "python3"
                if name == "sh":
                    return "bash"
                return name
    return EXT_INTERPRETER.get(path.suffix, "unknown")


class ScriptsBuilder:
    def __init__(self, scripts_root: Path, repo_root: Path) -> None:
        self.scripts_root = scripts_root
        self.repo_root = repo_root

    def build(self) -> tuple[list[ScriptEntry], list[str]]:
        if not self.scripts_root.exists():
            return [], []

        entries: list[ScriptEntry] = []
        failures: list[str] = []

        for ext in sorted(EXT_INTERPRETER):
            for path in sorted(self.scripts_root.rglob(f"*{ext}")):
                if not path.is_file():
                    continue
                rel = path.relative_to(self.repo_root).as_posix()
                interp = _detect_interpreter(path)
                if interp == "unknown":
                    failures.append(f"scripts:{rel}: cannot determine interpreter")
                entries.append(ScriptEntry(
                    id=rel, path=rel, interpreter=interp,
                    sha=git_blob_sha(path),
                ))

        return entries, failures
