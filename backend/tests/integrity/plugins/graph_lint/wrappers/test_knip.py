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
