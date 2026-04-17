import json
from pathlib import Path

from backend.app.integrity.plugins.graph_lint.wrappers.knip import (
    parse_knip_output,
    run_knip,
)

SAMPLE = json.dumps({
    "files": ["frontend/src/dead/orphan.tsx"],
    "issues": [
        {
            "file": "frontend/src/api.ts",
            "exports": [{"name": "unusedExport", "line": 12, "col": 1}],
        }
    ],
})


def test_parse_extracts_unused_files():
    findings = parse_knip_output(SAMPLE)
    files = [f for f in findings if f.kind == "file"]
    assert len(files) == 1
    assert files[0].path == "frontend/src/dead/orphan.tsx"


def test_parse_extracts_unused_exports():
    findings = parse_knip_output(SAMPLE)
    exports = [f for f in findings if f.kind == "export"]
    assert len(exports) == 1
    assert exports[0].name == "unusedExport"
    assert exports[0].path == "frontend/src/api.ts"
    assert exports[0].line == 12


def test_parse_handles_empty_input():
    assert parse_knip_output("{}") == []
    assert parse_knip_output("") == []


def test_run_knip_handles_missing_binary(tmp_path: Path, monkeypatch):
    result = run_knip(tmp_path, knip_bin="definitely_not_a_binary")
    assert result.findings == []
    assert "definitely_not_a_binary" in result.failure_message


def test_run_knip_resolves_node_modules_binary(tmp_path: Path, monkeypatch):
    """When repo_root is provided and frontend node_modules/.bin/knip exists, use it directly."""
    bin_dir = tmp_path / "frontend" / "node_modules" / ".bin"
    bin_dir.mkdir(parents=True)
    fake_knip = bin_dir / "knip"
    fake_knip.write_text("#!/bin/sh\necho '{}'\nexit 0\n")
    fake_knip.chmod(0o755)

    captured: list[list[str]] = []

    import subprocess as _sp

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))

        class FakeProc:
            returncode = 0
            stdout = "{}"
            stderr = ""

        return FakeProc()

    monkeypatch.setattr(_sp, "run", fake_run)

    frontend_dir = tmp_path / "frontend"
    result = run_knip(frontend_dir, repo_root=tmp_path)
    assert result.failure_message == ""
    assert len(captured) == 1
    assert captured[0][0] == str(fake_knip), (
        f"Expected node_modules knip to be called, got {captured[0][0]}"
    )
    # Should NOT include 'npx' or 'knip' as second token
    assert "npx" not in captured[0]


def test_run_knip_falls_back_to_npx_when_no_node_modules(tmp_path: Path, monkeypatch):
    """When repo_root is given but node_modules binary doesn't exist, fall back to npx."""
    import subprocess as _sp

    captured: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))

        class FakeProc:
            returncode = 2  # non-0/1 exit -> failure
            stdout = ""
            stderr = "some error"

        return FakeProc()

    monkeypatch.setattr(_sp, "run", fake_run)
    frontend_dir = tmp_path / "frontend"
    frontend_dir.mkdir(parents=True)
    run_knip(frontend_dir, repo_root=tmp_path)
    # node_modules binary doesn't exist -> fell back to npx -> failure_message from bad exit
    assert len(captured) == 1
    assert captured[0][0] == "npx"
