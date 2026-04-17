from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from backend.app.integrity.plugins.graph_lint.wrappers.vulture import (
    VultureFinding,
    parse_vulture_output,
    run_vulture,
)

SAMPLE_OUTPUT = """\
backend/app/x.py:10: unused function 'old_helper' (90% confidence)
backend/app/y.py:42: unused variable '_unused' (60% confidence)
"""


def test_parse_extracts_findings():
    findings = parse_vulture_output(SAMPLE_OUTPUT)
    assert len(findings) == 2
    assert findings[0] == VultureFinding(
        path="backend/app/x.py", line=10, kind="function", name="old_helper", confidence=90
    )
    assert findings[1].confidence == 60


def test_parse_skips_garbage_lines():
    out = "Hello there\nbackend/app/x.py:10: unused function 'old' (90% confidence)\n"
    findings = parse_vulture_output(out)
    assert len(findings) == 1


def test_run_vulture_handles_missing_binary(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PATH", "/nonexistent")
    result = run_vulture(tmp_path / "app", min_confidence=80, vulture_bin="definitely_not_a_binary")
    assert result.findings == []
    assert "definitely_not_a_binary" in result.failure_message


def test_run_vulture_resolves_venv_binary(tmp_path: Path, monkeypatch):
    """When repo_root is provided and the venv vulture binary exists, it should be used."""
    # Create a fake venv binary
    venv_bin = tmp_path / "backend" / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    fake_vulture = venv_bin / "vulture"
    script = (
        "#!/bin/sh\n"
        "echo 'backend/app/x.py:10: unused function '\"'\"'old'\"'\"' (90% confidence)'\n"
        "exit 3\n"
    )
    fake_vulture.write_text(script)
    fake_vulture.chmod(0o755)

    captured: list[list[str]] = []

    import subprocess as _sp

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))
        # Return a fake successful result with one finding
        class FakeProc:
            returncode = 3
            stdout = "backend/app/x.py:10: unused function 'old' (90% confidence)\n"
            stderr = ""
        return FakeProc()

    monkeypatch.setattr(_sp, "run", fake_run)

    pkg = tmp_path / "backend" / "app"
    pkg.mkdir(parents=True)

    result = run_vulture(pkg, min_confidence=60, repo_root=tmp_path)
    assert result.failure_message == ""
    assert len(captured) == 1
    assert captured[0][0] == str(fake_vulture), (
        f"Expected venv vulture to be called, got {captured[0][0]}"
    )


def test_run_vulture_falls_back_to_path_when_no_venv(tmp_path: Path, monkeypatch):
    """When repo_root is given but venv binary doesn't exist, fall back to PATH lookup."""
    monkeypatch.setenv("PATH", "/nonexistent")
    result = run_vulture(tmp_path / "app", min_confidence=80, repo_root=tmp_path)
    # No venv binary exists, bare "vulture" isn't on PATH -> failure_message set
    assert result.findings == []
    assert result.failure_message != ""


def test_run_vulture_no_repo_root_uses_default(tmp_path: Path, monkeypatch):
    """Without repo_root, the existing bare-binary lookup behavior is unchanged."""
    monkeypatch.setenv("PATH", "/nonexistent")
    result = run_vulture(tmp_path / "app", min_confidence=80, vulture_bin="definitely_not_a_binary")
    assert result.findings == []
    assert "definitely_not_a_binary" in result.failure_message


def test_run_vulture_executes_real_binary(tmp_path: Path):
    # Write a tiny module with one obvious unused
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "mod.py").write_text(
        "def used():\n    return 1\n\n"
        "def _unused_priv():\n    return 2\n\n"
        "used()\n"
    )
    try:
        subprocess.run(["vulture", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("vulture not installed")
    result = run_vulture(pkg, min_confidence=60)
    assert result.failure_message == ""
    names = {f.name for f in result.findings}
    assert "_unused_priv" in names or any("unused" in f.name for f in result.findings)
