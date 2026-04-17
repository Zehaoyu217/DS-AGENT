from __future__ import annotations

import subprocess
from pathlib import Path


class GitLog:
    """Cached `git log -1 --format=%cI` for repo-relative paths.

    Returns ISO 8601 committer date (e.g. `2026-04-17T03:21:18+00:00`) or
    `None` if the path is unknown to git, the repo has no history, or git
    is unavailable.
    """

    def __init__(self, repo_root: Path, *, git_bin: str = "git") -> None:
        self.repo_root = repo_root
        self.git_bin = git_bin
        self._cache: dict[str, str | None] = {}

    def last_commit_iso(self, rel_path: str) -> str | None:
        if rel_path in self._cache:
            return self._cache[rel_path]
        cmd = [self.git_bin, "log", "-1", "--format=%cI", "--", rel_path]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self._cache[rel_path] = None
            return None
        out = proc.stdout.strip()
        result = out if (proc.returncode == 0 and out) else None
        self._cache[rel_path] = result
        return result
