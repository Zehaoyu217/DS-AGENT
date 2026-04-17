from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

KnipKind = Literal["file", "export", "dependency"]


@dataclass(frozen=True)
class KnipFinding:
    kind: KnipKind
    path: str
    name: str = ""
    line: int = 0


@dataclass(frozen=True)
class KnipResult:
    findings: list[KnipFinding] = field(default_factory=list)
    failure_message: str = ""


def parse_knip_output(text: str) -> list[KnipFinding]:
    if not text.strip():
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    out: list[KnipFinding] = []
    for path in data.get("files", []) or []:
        out.append(KnipFinding(kind="file", path=path))
    for issue in data.get("issues", []) or []:
        path = issue.get("file", "")
        for exp in issue.get("exports", []) or []:
            out.append(
                KnipFinding(
                    kind="export",
                    path=path,
                    name=exp.get("name", ""),
                    line=int(exp.get("line", 0) or 0),
                )
            )
        for dep in issue.get("dependencies", []) or []:
            out.append(KnipFinding(kind="dependency", path=path, name=dep.get("name", "")))
    return out


def _resolve_knip_cmd(
    knip_bin: str, frontend_dir: Path, repo_root: Path | None
) -> list[str]:
    """Return the command list for running knip.

    When *knip_bin* is the default ``"npx"`` and *repo_root* is provided,
    prefer the local ``frontend/node_modules/.bin/knip`` binary when it exists
    (avoids npx network lookups and PATH issues).  Falls back to the standard
    ``npx knip`` invocation otherwise.
    """
    if knip_bin == "npx" and repo_root is not None:
        candidate = repo_root / "frontend" / "node_modules" / ".bin" / "knip"
        if candidate.exists():
            return [str(candidate), "--reporter", "json"]
    if knip_bin == "npx":
        return [knip_bin, "knip", "--reporter", "json"]
    return [knip_bin, "--reporter", "json"]


def run_knip(
    frontend_dir: Path,
    *,
    knip_bin: str = "npx",
    repo_root: Path | None = None,
) -> KnipResult:
    cmd = _resolve_knip_cmd(knip_bin, frontend_dir, repo_root)
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, check=False, timeout=180,
            cwd=str(frontend_dir),
        )
    except FileNotFoundError as exc:
        return KnipResult(failure_message=f"knip binary not found: {knip_bin} ({exc})")
    except subprocess.TimeoutExpired:
        return KnipResult(failure_message="knip timed out after 180s")

    # knip exits 1 when issues are found — same shape as a successful scan with findings.
    if proc.returncode not in (0, 1):
        stderr = proc.stderr.strip()[:500]
        return KnipResult(failure_message=f"knip exited {proc.returncode}: {stderr}")

    return KnipResult(findings=parse_knip_output(proc.stdout))
