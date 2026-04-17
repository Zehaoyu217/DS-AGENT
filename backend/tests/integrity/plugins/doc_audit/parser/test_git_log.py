import subprocess
from pathlib import Path

import pytest

from backend.app.integrity.plugins.doc_audit.parser.git_log import GitLog


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True)


@pytest.fixture
def tiny_git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "a.txt").write_text("hello\n")
    _git(repo, "add", "a.txt")
    _git(repo, "commit", "-q", "-m", "initial")
    return repo


def test_returns_iso_timestamp_for_committed_file(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    iso = gl.last_commit_iso("a.txt")
    assert iso is not None
    # Strict ISO 8601-ish: starts with YYYY-MM-DD
    assert len(iso) >= 10 and iso[4] == "-" and iso[7] == "-"


def test_returns_none_for_unknown_path(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    assert gl.last_commit_iso("does/not/exist.txt") is None


def test_returns_none_when_not_a_git_repo(tmp_path: Path):
    not_a_repo = tmp_path / "plain"
    not_a_repo.mkdir()
    (not_a_repo / "a.txt").write_text("hi\n")
    gl = GitLog(not_a_repo)
    assert gl.last_commit_iso("a.txt") is None


def test_caches_results(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    first = gl.last_commit_iso("a.txt")
    second = gl.last_commit_iso("a.txt")
    assert first == second
    # Cache hit: same dict-stored value identity
    assert gl._cache["a.txt"] == first
