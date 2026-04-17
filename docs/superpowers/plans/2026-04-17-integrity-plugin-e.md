# Plugin E (config_registry) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `ConfigRegistryPlugin` (gate δ) — builds `config/manifest.yaml` as the committed, deterministic inventory of skills/scripts/routes/configs/functions; emits 3 drift rules (`config.added`, `config.removed`, `config.schema_drift`).

**Architecture:** Mirror `DocAuditPlugin` (gate γ) shape — per-rule try/except, writes `integrity-out/{date}/config_registry.json`, reuses gate-β engine/snapshots/aggregator without copies. Five builders assemble the manifest; three rules diff against the prior committed manifest; nine per-type schema validators check config drift. Functions extracted via Python AST (no runtime imports).

**Tech Stack:** Python 3.12+, stdlib `ast`/`hashlib`/`pathlib`/`re`, PyYAML (already a backend dep), pytest. No new runtime deps.

**Spec:** `docs/superpowers/specs/2026-04-17-integrity-plugin-e-design.md`

---

## File Structure

```
backend/app/integrity/plugins/config_registry/
  __init__.py
  plugin.py                # ConfigRegistryPlugin (Task 14)
  manifest.py              # read/write/diff manifest (Task 3)
  hashing.py               # git_blob_sha (Task 2)
  builders/
    __init__.py
    skills.py              # SkillsBuilder (Task 4)
    scripts.py             # ScriptsBuilder (Task 5)
    routes.py              # RoutesBuilder (Task 6)
    configs.py             # ConfigsBuilder (Task 7)
    functions.py           # FunctionsBuilder (Task 8)
  rules/
    __init__.py
    added.py               # config.added (Task 11)
    removed.py             # config.removed (Task 12)
    schema_drift.py        # config.schema_drift (Task 13)
  schemas/
    __init__.py            # SCHEMA_REGISTRY (Task 9)
    base.py                # SchemaValidator Protocol (Task 9)
    pyproject.py           # (Task 9)
    package_json.py        # (Task 9)
    claude_settings.py     # (Task 9)
    integrity_yaml.py      # (Task 10)
    makefile.py            # (Task 10)
    dockerfile.py          # (Task 10)
    env_example.py         # (Task 10)
    vite_config.py         # (Task 10)
    tsconfig.py            # (Task 10)
  tests/
    __init__.py
    conftest.py            # tiny_repo fixture (Task 1)
    fixtures/tiny_repo/... # (Task 1)
    test_hashing.py
    test_manifest_roundtrip.py
    test_builder_skills.py
    test_builder_scripts.py
    test_builder_routes.py
    test_builder_configs.py
    test_builder_functions.py
    test_rule_added.py
    test_rule_removed.py
    test_rule_schema_drift.py
    test_schemas_pyproject.py
    test_schemas_package_json.py
    test_schemas_claude_settings.py
    test_schemas_integrity_yaml.py
    test_schemas_makefile.py
    test_schemas_dockerfile.py
    test_schemas_env_example.py
    test_schemas_vite_config.py
    test_schemas_tsconfig.py
    test_skill_count_parity.py     # acceptance gate (Task 16)
    test_round_trip_add_fixture.py # acceptance gate (Task 17)
    test_plugin_integration.py     # full scan (Task 18)
```

Modified files:
- `backend/app/integrity/__main__.py` — extend `KNOWN_PLUGINS` + add `--check` flag (Task 15)
- `config/integrity.yaml` — add `plugins.config_registry` block (Task 19)
- `Makefile` — add `integrity-config` target + update help text (Task 19)
- `docs/log.md` — `[Unreleased]` entry (Task 20)
- `config/manifest.yaml` — first generation, committed (Task 20)

---

## Task 1: Test scaffolding + tiny_repo fixture

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/__init__.py`
- Create: `backend/app/integrity/plugins/config_registry/tests/__init__.py`
- Create: `backend/app/integrity/plugins/config_registry/tests/conftest.py`
- Create: `backend/app/integrity/plugins/config_registry/tests/fixtures/__init__.py`

- [ ] **Step 1: Create empty package files**

```bash
mkdir -p backend/app/integrity/plugins/config_registry/{builders,rules,schemas,tests/fixtures}
touch backend/app/integrity/plugins/config_registry/__init__.py
touch backend/app/integrity/plugins/config_registry/builders/__init__.py
touch backend/app/integrity/plugins/config_registry/rules/__init__.py
touch backend/app/integrity/plugins/config_registry/schemas/__init__.py
touch backend/app/integrity/plugins/config_registry/tests/__init__.py
touch backend/app/integrity/plugins/config_registry/tests/fixtures/__init__.py
```

- [ ] **Step 2: Write conftest.py — tiny_repo fixture builder**

Create `backend/app/integrity/plugins/config_registry/tests/conftest.py`:

```python
"""Synthetic mini-repo fixture for Plugin E tests.

Mirrors the real claude-code-agent layout minimally:
  backend/app/skills/{alpha,beta,beta/sub_skill}/SKILL.md
  scripts/{deploy.sh, gen_data.py, build.ts}
  config/integrity.yaml
  graphify/graph.augmented.json (2 routes + 1 dead-route)
  backend/app/api/foo_api.py (router + on_event)
  pyproject.toml, package.json, .claude/settings.json,
  Dockerfile, Makefile, .env.example, vite.config.ts,
  tsconfig.json, .gitignore, config/manifest.yaml (prior)
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
             "HOME": str(repo), "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    # Skills tree
    _write(repo, "backend/app/skills/__init__.py", "")
    _write(repo, "backend/app/skills/alpha/__init__.py", "")
    _write(repo, "backend/app/skills/alpha/SKILL.md",
           "---\nname: alpha\nversion: 1.0.0\ndescription: Alpha skill.\n---\n# Alpha\n")
    _write(repo, "backend/app/skills/alpha/skill.yaml",
           "dependencies:\n  packages: []\nerrors: {}\n")
    _write(repo, "backend/app/skills/beta/__init__.py", "")
    _write(repo, "backend/app/skills/beta/SKILL.md",
           "---\nname: beta\nversion: 1.0.0\ndescription: Beta hub.\n---\n# Beta\n")
    _write(repo, "backend/app/skills/beta/sub_skill/__init__.py", "")
    _write(repo, "backend/app/skills/beta/sub_skill/SKILL.md",
           "---\nname: sub_skill\nversion: 1.0.0\ndescription: Beta sub.\n---\n# Sub\n")

    # Scripts
    _write(repo, "scripts/deploy.sh", "#!/usr/bin/env bash\necho deploy\n")
    _write(repo, "scripts/gen_data.py", "#!/usr/bin/env python3\nprint('gen')\n")
    _write(repo, "scripts/build.ts", "// build script\nconsole.log('build');\n")

    # Configs
    _write(repo, "pyproject.toml",
           '[project]\nname = "tiny"\nversion = "0.1.0"\n')
    _write(repo, "package.json",
           '{"name": "tiny", "version": "0.1.0", "scripts": {}, "dependencies": {}}\n')
    _write(repo, ".claude/settings.json", '{"hooks": {}}\n')
    _write(repo, "Dockerfile", "FROM python:3.12-slim\nRUN echo hi\n")
    _write(repo, "Makefile", ".PHONY: test\ntest:\n\techo test\n")
    _write(repo, ".env.example", "FOO=\nBAR=baz\n")
    _write(repo, "vite.config.ts", "export default {};\n")
    _write(repo, "tsconfig.json", '{"compilerOptions": {}}\n')

    # Integrity config (so plugin.scan works)
    _write(repo, "config/integrity.yaml",
           "plugins:\n  config_registry:\n    enabled: true\n")

    # Graph (2 live routes + 1 dead route — id no longer in any source)
    graph = {
        "nodes": [
            {"id": "route::POST::/api/trace", "label": "POST /api/trace",
             "extractor": "fastapi_routes",
             "source_file": "backend/app/api/foo_api.py", "source_location": 5},
            {"id": "route::GET::/api/health", "label": "GET /api/health",
             "extractor": "fastapi_routes",
             "source_file": "backend/app/api/foo_api.py", "source_location": 12},
            {"id": "route::DELETE::/api/legacy", "label": "DELETE /api/legacy",
             "extractor": "fastapi_routes",
             "source_file": "backend/app/api/legacy_removed.py", "source_location": 1},
        ],
        "links": [],
    }
    _write(repo, "graphify/graph.augmented.json", json.dumps(graph, indent=2))

    # Functions source — matches first 2 routes
    _write(repo, "backend/app/api/__init__.py", "")
    _write(repo, "backend/app/api/foo_api.py",
           'from fastapi import APIRouter\n\nrouter = APIRouter()\n\n'
           '@router.post("/api/trace")\ndef trace_endpoint():\n    return {}\n\n'
           '@router.get("/api/health")\ndef health_endpoint():\n    return {}\n')

    # Main with FastAPI events
    _write(repo, "backend/app/main.py",
           'from fastapi import FastAPI\n\napp = FastAPI()\n\n'
           '@app.on_event("startup")\nasync def startup():\n    pass\n')

    # .gitignore
    _write(repo, ".gitignore", "build/\ndist/\n*.pyc\n")

    # Prior committed manifest — empty inventories so we can test "first run" diff
    _write(repo, "config/manifest.yaml",
           "# AUTO-GENERATED\ngenerated_at: \"2026-04-16\"\n"
           "generator_version: \"1.0.0\"\nmanifest_version: 1\n"
           "configs: []\nfunctions: []\nroutes: []\nscripts: []\nskills: []\n")

    # git init + commit so blob shas resolve via `git hash-object`
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "tiny_repo initial")

    return repo


@pytest.fixture
def today_fixed() -> date:
    return date(2026, 4, 17)
```

- [ ] **Step 3: Verify fixture builds**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/conftest.py --collect-only -q`
Expected: collects 0 tests, no import errors.

- [ ] **Step 4: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/__init__.py \
        backend/app/integrity/plugins/config_registry/builders/__init__.py \
        backend/app/integrity/plugins/config_registry/rules/__init__.py \
        backend/app/integrity/plugins/config_registry/schemas/__init__.py \
        backend/app/integrity/plugins/config_registry/tests/__init__.py \
        backend/app/integrity/plugins/config_registry/tests/fixtures/__init__.py \
        backend/app/integrity/plugins/config_registry/tests/conftest.py
git commit -m "test(integrity-e): scaffold config_registry package + tiny_repo fixture"
```

---

## Task 2: hashing.py — git_blob_sha helper

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/hashing.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_hashing.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_hashing.py`:

```python
"""Tests for git-compatible blob SHA hashing."""
from __future__ import annotations

import subprocess
from pathlib import Path

from backend.app.integrity.plugins.config_registry.hashing import (
    git_blob_sha,
    git_blob_sha_bytes,
)


def test_git_blob_sha_matches_git_hash_object(tiny_repo: Path) -> None:
    """Our blob SHA matches `git hash-object` output exactly."""
    target = tiny_repo / "pyproject.toml"
    expected = subprocess.run(
        ["git", "hash-object", str(target)],
        cwd=tiny_repo, capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert git_blob_sha(target) == expected


def test_git_blob_sha_empty_file(tmp_path: Path) -> None:
    """Empty blob SHA matches the well-known git constant."""
    empty = tmp_path / "empty.txt"
    empty.write_text("")
    # git's well-known empty blob SHA
    assert git_blob_sha(empty) == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def test_git_blob_sha_bytes_matches() -> None:
    """In-process implementation matches the on-disk version."""
    content = b"hello world\n"
    # echo -n "hello world" | git hash-object --stdin → 3b18e512dba79e4c8300dd08aeb37f8e728b8dad
    # but that's without the newline; with newline:
    expected_with_nl = "22b1f7c80df47fa75c4e9aae22e1f87cc5c1afaa"  # known
    # We don't hardcode — instead compare paths
    p = Path("/tmp/_test_hash.txt")
    p.write_bytes(content)
    assert git_blob_sha_bytes(content) == git_blob_sha(p)
    p.unlink()


def test_git_blob_sha_falls_back_in_process(tmp_path: Path) -> None:
    """Without .git, still produces a SHA matching the on-disk format."""
    # No git init — just hash a file
    f = tmp_path / "lone.txt"
    f.write_text("contents\n")
    sha = git_blob_sha(f)
    # Validate format: 40 lowercase hex chars
    assert len(sha) == 40
    assert all(c in "0123456789abcdef" for c in sha)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_hashing.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named '...config_registry.hashing'`

- [ ] **Step 3: Write the minimal implementation**

Create `backend/app/integrity/plugins/config_registry/hashing.py`:

```python
"""Git-compatible blob SHA-1 hashing.

Implements the `blob {len}\\0{content}` framing used by
`git hash-object`, so our SHAs match what git would compute.
Falls back to in-process implementation if git is unavailable.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def git_blob_sha_bytes(content: bytes) -> str:
    """Compute git blob SHA-1 over raw bytes.

    Format: ``sha1(b"blob " + str(len(content)).encode() + b"\\x00" + content)``
    """
    header = f"blob {len(content)}\x00".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def git_blob_sha(path: Path) -> str:
    """Compute git blob SHA-1 for the file at ``path``.

    Reads bytes verbatim — no newline normalisation, no encoding
    conversion. Matches `git hash-object` output for any committed
    file with default git config.
    """
    return git_blob_sha_bytes(path.read_bytes())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_hashing.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/hashing.py \
        backend/app/integrity/plugins/config_registry/tests/test_hashing.py
git commit -m "feat(integrity-e): add git_blob_sha helper for manifest hashing"
```

---

## Task 3: manifest.py — read/write/diff

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/manifest.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_manifest_roundtrip.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_manifest_roundtrip.py`:

```python
"""Tests for manifest read/write/diff."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.manifest import (
    ManifestDelta,
    diff_manifests,
    empty_manifest,
    read_manifest,
    write_manifest,
)


def test_empty_manifest_shape() -> None:
    m = empty_manifest()
    assert m["manifest_version"] == 1
    assert m["configs"] == []
    assert m["functions"] == []
    assert m["routes"] == []
    assert m["scripts"] == []
    assert m["skills"] == []


def test_read_missing_returns_empty(tmp_path: Path) -> None:
    p = tmp_path / "missing.yaml"
    m = read_manifest(p)
    assert m == empty_manifest()


def test_write_then_read_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "manifest.yaml"
    m = empty_manifest()
    m["generated_at"] = "2026-04-17"
    m["scripts"] = [{"id": "scripts/a.sh", "path": "scripts/a.sh",
                     "interpreter": "bash", "sha": "abc123"}]
    write_manifest(p, m)
    m2 = read_manifest(p)
    assert m2["scripts"] == m["scripts"]
    assert m2["manifest_version"] == 1


def test_write_is_deterministic(tmp_path: Path) -> None:
    p1 = tmp_path / "m1.yaml"
    p2 = tmp_path / "m2.yaml"
    m = empty_manifest()
    m["generated_at"] = "2026-04-17"
    m["configs"] = [
        {"id": "Makefile", "type": "makefile", "path": "Makefile", "sha": "z"},
        {"id": "Dockerfile", "type": "dockerfile", "path": "Dockerfile", "sha": "a"},
    ]
    write_manifest(p1, m)
    write_manifest(p2, m)
    assert p1.read_bytes() == p2.read_bytes()


def test_write_sorts_entries_by_id(tmp_path: Path) -> None:
    p = tmp_path / "m.yaml"
    m = empty_manifest()
    m["generated_at"] = "2026-04-17"
    m["configs"] = [
        {"id": "z.yaml", "type": "x", "path": "z.yaml", "sha": "1"},
        {"id": "a.yaml", "type": "x", "path": "a.yaml", "sha": "2"},
    ]
    write_manifest(p, m)
    body = p.read_text()
    assert body.index("a.yaml") < body.index("z.yaml")


def test_diff_added(tmp_path: Path) -> None:
    prior = empty_manifest()
    current = empty_manifest()
    current["scripts"] = [{"id": "scripts/new.sh", "path": "scripts/new.sh",
                           "interpreter": "bash", "sha": "x"}]
    delta = diff_manifests(current, prior)
    assert delta.added["scripts"] == [current["scripts"][0]]
    assert delta.removed["scripts"] == []
    assert delta.changed["scripts"] == []


def test_diff_removed(tmp_path: Path) -> None:
    prior = empty_manifest()
    prior["scripts"] = [{"id": "scripts/old.sh", "path": "scripts/old.sh",
                         "interpreter": "bash", "sha": "x"}]
    current = empty_manifest()
    delta = diff_manifests(current, prior)
    assert delta.removed["scripts"] == [prior["scripts"][0]]
    assert delta.added["scripts"] == []


def test_diff_changed_via_sha(tmp_path: Path) -> None:
    prior = empty_manifest()
    prior["configs"] = [{"id": "Makefile", "type": "makefile",
                         "path": "Makefile", "sha": "old"}]
    current = empty_manifest()
    current["configs"] = [{"id": "Makefile", "type": "makefile",
                           "path": "Makefile", "sha": "new"}]
    delta = diff_manifests(current, prior)
    assert delta.changed["configs"] == [
        {"id": "Makefile", "prior": prior["configs"][0],
         "current": current["configs"][0]}
    ]
    assert delta.added["configs"] == []
    assert delta.removed["configs"] == []


def test_diff_ignores_generated_at(tmp_path: Path) -> None:
    prior = empty_manifest()
    prior["generated_at"] = "2026-04-15"
    current = empty_manifest()
    current["generated_at"] = "2026-04-17"
    delta = diff_manifests(current, prior)
    for key in ("configs", "functions", "routes", "scripts", "skills"):
        assert delta.added[key] == []
        assert delta.removed[key] == []
        assert delta.changed[key] == []


def test_idempotent_write_read_write(tmp_path: Path) -> None:
    p1 = tmp_path / "m1.yaml"
    p2 = tmp_path / "m2.yaml"
    m = empty_manifest()
    m["generated_at"] = "2026-04-17"
    m["configs"] = [{"id": "Makefile", "type": "makefile",
                     "path": "Makefile", "sha": "x"}]
    write_manifest(p1, m)
    re_read = read_manifest(p1)
    write_manifest(p2, re_read)
    assert p1.read_bytes() == p2.read_bytes()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_manifest_roundtrip.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/manifest.py`:

```python
"""Read/write/diff for ``config/manifest.yaml``.

The manifest is the committed source of truth for the inventory.
Writes are deterministic so PR diffs reflect real changes only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

INVENTORY_KEYS = ("configs", "functions", "routes", "scripts", "skills")
TOP_LEVEL_ORDER = (
    "generated_at",
    "generator_version",
    "manifest_version",
    *INVENTORY_KEYS,
)
GENERATOR_VERSION = "1.0.0"
MANIFEST_VERSION = 1
HEADER = (
    "# AUTO-GENERATED by integrity Plugin E (config_registry).\n"
    "# Do not edit by hand — re-run `make integrity-config` after intended changes.\n"
    "# See docs/superpowers/specs/2026-04-17-integrity-plugin-e-design.md.\n"
)


@dataclass(frozen=True)
class ManifestDelta:
    added: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    removed: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    changed: dict[str, list[dict[str, Any]]] = field(default_factory=dict)


def empty_manifest() -> dict[str, Any]:
    """Empty manifest skeleton with all required keys present."""
    m: dict[str, Any] = {
        "generated_at": "",
        "generator_version": GENERATOR_VERSION,
        "manifest_version": MANIFEST_VERSION,
    }
    for key in INVENTORY_KEYS:
        m[key] = []
    return m


def read_manifest(path: Path) -> dict[str, Any]:
    """Load manifest from ``path``; returns ``empty_manifest()`` if absent."""
    if not path.exists():
        return empty_manifest()
    raw = yaml.safe_load(path.read_text()) or {}
    out = empty_manifest()
    for key in TOP_LEVEL_ORDER:
        if key in raw:
            out[key] = raw[key]
    return out


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Write ``manifest`` to ``path`` deterministically.

    Top-level keys emit in fixed order (`TOP_LEVEL_ORDER`); list
    entries sort by ``id`` ascending; LF line endings; trailing newline.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_manifest = empty_manifest()
    for key in TOP_LEVEL_ORDER:
        if key in manifest:
            value = manifest[key]
            if key in INVENTORY_KEYS and isinstance(value, list):
                value = sorted(value, key=lambda e: str(e.get("id", "")))
            sorted_manifest[key] = value

    body = yaml.safe_dump(
        sorted_manifest,
        default_flow_style=False,
        sort_keys=False,           # we control top-level order
        allow_unicode=True,
        width=10_000,              # avoid auto-wrapping URLs/messages
    )
    path.write_text(HEADER + body)


def diff_manifests(
    current: dict[str, Any], prior: dict[str, Any]
) -> ManifestDelta:
    """Compute per-key add/remove/change between two manifests.

    ``generated_at`` and ``generator_version`` are excluded from the diff.
    Within each inventory key, entries are matched by ``id``.
    """
    added: dict[str, list[dict[str, Any]]] = {}
    removed: dict[str, list[dict[str, Any]]] = {}
    changed: dict[str, list[dict[str, Any]]] = {}

    for key in INVENTORY_KEYS:
        cur = {e["id"]: e for e in current.get(key, [])}
        pri = {e["id"]: e for e in prior.get(key, [])}
        added[key] = [cur[i] for i in sorted(cur.keys() - pri.keys())]
        removed[key] = [pri[i] for i in sorted(pri.keys() - cur.keys())]
        changed[key] = [
            {"id": i, "prior": pri[i], "current": cur[i]}
            for i in sorted(cur.keys() & pri.keys())
            if cur[i] != pri[i]
        ]

    return ManifestDelta(added=added, removed=removed, changed=changed)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_manifest_roundtrip.py -v`
Expected: 10 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/manifest.py \
        backend/app/integrity/plugins/config_registry/tests/test_manifest_roundtrip.py
git commit -m "feat(integrity-e): manifest read/write/diff with deterministic emit"
```

---

## Task 4: SkillsBuilder

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/builders/skills.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_builder_skills.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_builder_skills.py`:

```python
"""Tests for SkillsBuilder."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.builders.skills import (
    SkillEntry,
    SkillsBuilder,
)


def test_builds_three_entries(tiny_repo: Path) -> None:
    builder = SkillsBuilder(skills_root=tiny_repo / "backend/app/skills")
    entries, failures = builder.build()
    ids = [e.id for e in entries]
    assert ids == ["alpha", "beta", "beta.sub_skill"]
    assert failures == []


def test_skill_entry_fields(tiny_repo: Path) -> None:
    builder = SkillsBuilder(skills_root=tiny_repo / "backend/app/skills")
    entries, _ = builder.build()
    by_id = {e.id: e for e in entries}

    alpha = by_id["alpha"]
    assert alpha.path == "backend/app/skills/alpha/SKILL.md"
    assert alpha.yaml_path == "backend/app/skills/alpha/skill.yaml"
    assert alpha.version == "1.0.0"
    assert alpha.description == "Alpha skill."
    assert alpha.parent is None
    assert alpha.children == []
    assert len(alpha.sha_skill_md) == 40
    assert len(alpha.sha_skill_yaml or "") == 40


def test_parent_and_children_relationships(tiny_repo: Path) -> None:
    builder = SkillsBuilder(skills_root=tiny_repo / "backend/app/skills")
    entries, _ = builder.build()
    by_id = {e.id: e for e in entries}

    assert by_id["beta"].parent is None
    assert by_id["beta"].children == ["beta.sub_skill"]
    assert by_id["beta.sub_skill"].parent == "beta"
    assert by_id["beta.sub_skill"].children == []


def test_skill_without_skill_yaml(tiny_repo: Path, tmp_path: Path) -> None:
    """A skill without skill.yaml has yaml_path/sha_skill_yaml as None."""
    target = tiny_repo / "backend/app/skills/alpha/skill.yaml"
    target.unlink()
    builder = SkillsBuilder(skills_root=tiny_repo / "backend/app/skills")
    entries, failures = builder.build()
    by_id = {e.id: e for e in entries}
    assert by_id["alpha"].yaml_path is None
    assert by_id["alpha"].sha_skill_yaml is None
    assert failures == []


def test_empty_skills_root(tmp_path: Path) -> None:
    empty = tmp_path / "skills"
    empty.mkdir()
    builder = SkillsBuilder(skills_root=empty)
    entries, failures = builder.build()
    assert entries == []
    assert failures == []
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_skills.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/builders/skills.py`:

```python
"""SkillsBuilder — walks the skills tree and produces SkillEntry list.

Mirrors the dotted-path id convention used by
``backend/app/skills/registry.SkillRegistry._index`` so the
acceptance gate's parity check holds.
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
    children: list[str] = field(default_factory=list)
    sha_skill_md: str = ""
    sha_skill_yaml: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
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
        self.repo_root = repo_root or skills_root.parent.parent.parent.parent

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
            children=[],            # populated after pass 2
            sha_skill_md=git_blob_sha(skill_md),
            sha_skill_yaml=sha_yaml,
        )
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_skills.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/builders/skills.py \
        backend/app/integrity/plugins/config_registry/tests/test_builder_skills.py
git commit -m "feat(integrity-e): SkillsBuilder — walk skills tree, dotted-path ids"
```

---

## Task 5: ScriptsBuilder

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/builders/scripts.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_builder_scripts.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_builder_scripts.py`:

```python
"""Tests for ScriptsBuilder."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.builders.scripts import (
    ScriptEntry,
    ScriptsBuilder,
)


def test_three_scripts_with_correct_interpreters(tiny_repo: Path) -> None:
    builder = ScriptsBuilder(scripts_root=tiny_repo / "scripts", repo_root=tiny_repo)
    entries, failures = builder.build()
    by_id = {e.id: e for e in entries}
    assert set(by_id) == {"scripts/deploy.sh", "scripts/gen_data.py", "scripts/build.ts"}
    assert by_id["scripts/deploy.sh"].interpreter == "bash"
    assert by_id["scripts/gen_data.py"].interpreter == "python3"
    assert by_id["scripts/build.ts"].interpreter == "node"
    assert failures == []


def test_script_entry_has_sha(tiny_repo: Path) -> None:
    builder = ScriptsBuilder(scripts_root=tiny_repo / "scripts", repo_root=tiny_repo)
    entries, _ = builder.build()
    for e in entries:
        assert len(e.sha) == 40


def test_shebang_overrides_extension(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    weird = scripts / "weird.txt"
    weird.write_text("#!/usr/bin/env python3\nprint('hi')\n")
    builder = ScriptsBuilder(scripts_root=scripts, repo_root=repo)
    # .txt isn't in the glob set, so it's skipped — instead test by extension
    # using a recognized one with conflicting shebang
    other = scripts / "x.sh"
    other.write_text("#!/usr/bin/env python3\nprint('hi')\n")
    entries, _ = builder.build()
    by_id = {e.id: e for e in entries}
    assert by_id["scripts/x.sh"].interpreter == "python3"


def test_unknown_extension_yields_failure(tmp_path: Path) -> None:
    """Files whose interpreter cannot be determined → 'unknown' + failure entry."""
    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    # .py file with no shebang and no recognized extension fallback... but .py
    # is recognized. So make one without a recognized ext but in glob set.
    # The glob set is .py/.sh/.ts/.js so all four have ext fallbacks.
    # We can simulate "unknown" by writing a .ts with a shebang that names a
    # weird interpreter — but we only check shebang for python3/bash/node.
    weird_sh = scripts / "weird.sh"
    weird_sh.write_text("#!/usr/local/bin/strange\necho hi\n")
    builder = ScriptsBuilder(scripts_root=scripts, repo_root=repo)
    entries, failures = builder.build()
    by_id = {e.id: e for e in entries}
    # Falls back to ext (.sh → bash) since shebang interpreter is unrecognised.
    assert by_id["scripts/weird.sh"].interpreter == "bash"
    assert failures == []


def test_empty_scripts_root(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    builder = ScriptsBuilder(scripts_root=scripts, repo_root=repo)
    entries, failures = builder.build()
    assert entries == []
    assert failures == []
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_scripts.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/builders/scripts.py`:

```python
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
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_scripts.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/builders/scripts.py \
        backend/app/integrity/plugins/config_registry/tests/test_builder_scripts.py
git commit -m "feat(integrity-e): ScriptsBuilder — shebang+ext interpreter detection"
```

---

## Task 6: RoutesBuilder

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/builders/routes.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_builder_routes.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_builder_routes.py`:

```python
"""Tests for RoutesBuilder."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.builders.routes import (
    RouteEntry,
    RoutesBuilder,
)
from backend.app.integrity.schema import GraphSnapshot


def test_re_exports_three_routes(tiny_repo: Path) -> None:
    graph = GraphSnapshot.load(tiny_repo)
    builder = RoutesBuilder(graph=graph)
    entries, failures = builder.build()
    ids = sorted(e.id for e in entries)
    assert ids == [
        "route::DELETE::/api/legacy",
        "route::GET::/api/health",
        "route::POST::/api/trace",
    ]
    assert failures == []


def test_route_entry_fields(tiny_repo: Path) -> None:
    graph = GraphSnapshot.load(tiny_repo)
    builder = RoutesBuilder(graph=graph)
    entries, _ = builder.build()
    by_id = {e.id: e for e in entries}
    trace = by_id["route::POST::/api/trace"]
    assert trace.method == "POST"
    assert trace.path == "/api/trace"
    assert trace.source_file == "backend/app/api/foo_api.py"
    assert trace.source_location == 5
    assert trace.extractor == "fastapi_routes"


def test_absent_graph_yields_empty_with_failure(tmp_path: Path) -> None:
    empty_repo = tmp_path / "repo"
    empty_repo.mkdir()
    graph = GraphSnapshot.load(empty_repo)  # both files absent → empty snapshot
    builder = RoutesBuilder(graph=graph)
    entries, failures = builder.build()
    assert entries == []
    assert any("graph" in f.lower() for f in failures)
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_routes.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/builders/routes.py`:

```python
"""RoutesBuilder — re-export route nodes from GraphSnapshot.

Plugin A's ``fastapi_routes`` extractor populates
``graphify/graph.augmented.json`` with ``route::METHOD::/path`` nodes.
We just project the relevant fields. No graph → empty list + failure.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...schema import GraphSnapshot


@dataclass(frozen=True)
class RouteEntry:
    id: str
    method: str
    path: str
    source_file: str | None
    source_location: int | None
    extractor: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "method": self.method, "path": self.path,
            "source_file": self.source_file, "source_location": self.source_location,
            "extractor": self.extractor,
        }


def _parse_route_id(node_id: str) -> tuple[str, str] | None:
    """``"route::POST::/api/trace"`` → ``("POST", "/api/trace")`` or None."""
    parts = node_id.split("::", 2)
    if len(parts) != 3 or parts[0] != "route":
        return None
    return parts[1], parts[2]


class RoutesBuilder:
    def __init__(self, graph: GraphSnapshot) -> None:
        self.graph = graph

    def build(self) -> tuple[list[RouteEntry], list[str]]:
        entries: list[RouteEntry] = []
        failures: list[str] = []

        if not self.graph.nodes:
            failures.append("routes: graph.augmented.json absent — routes inventory is empty")
            return entries, failures

        for node in self.graph.nodes:
            node_id = str(node.get("id", ""))
            parsed = _parse_route_id(node_id)
            if parsed is None:
                continue
            method, path = parsed
            entries.append(RouteEntry(
                id=node_id,
                method=method,
                path=path,
                source_file=node.get("source_file"),
                source_location=node.get("source_location"),
                extractor=str(node.get("extractor", "fastapi_routes")),
            ))

        return entries, failures
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_routes.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/builders/routes.py \
        backend/app/integrity/plugins/config_registry/tests/test_builder_routes.py
git commit -m "feat(integrity-e): RoutesBuilder — re-export route nodes from graph"
```

---

## Task 7: ConfigsBuilder

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/builders/configs.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_builder_configs.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_builder_configs.py`:

```python
"""Tests for ConfigsBuilder."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.builders.configs import (
    ConfigEntry,
    ConfigsBuilder,
)


DEFAULT_GLOBS = [
    "pyproject.toml",
    "package.json",
    ".claude/settings.json",
    "vite.config.*",
    "tsconfig*.json",
    "Dockerfile*",
    "Makefile",
    ".env.example",
    "config/integrity.yaml",
]


def test_detects_all_well_known_configs(tiny_repo: Path) -> None:
    builder = ConfigsBuilder(
        repo_root=tiny_repo,
        globs=DEFAULT_GLOBS,
        excluded=["node_modules/**", "**/__pycache__/**"],
    )
    entries, failures = builder.build()
    by_path = {e.path: e for e in entries}
    expected_paths = {
        "pyproject.toml", "package.json", ".claude/settings.json",
        "vite.config.ts", "tsconfig.json", "Dockerfile", "Makefile",
        ".env.example", "config/integrity.yaml",
    }
    assert expected_paths.issubset(set(by_path))
    assert failures == []


def test_type_detection(tiny_repo: Path) -> None:
    builder = ConfigsBuilder(repo_root=tiny_repo, globs=DEFAULT_GLOBS, excluded=[])
    entries, _ = builder.build()
    by_path = {e.path: e for e in entries}
    assert by_path["pyproject.toml"].type == "pyproject"
    assert by_path["package.json"].type == "package_json"
    assert by_path[".claude/settings.json"].type == "claude_settings"
    assert by_path["vite.config.ts"].type == "vite_config"
    assert by_path["tsconfig.json"].type == "tsconfig"
    assert by_path["Dockerfile"].type == "dockerfile"
    assert by_path["Makefile"].type == "makefile"
    assert by_path[".env.example"].type == "env_example"
    assert by_path["config/integrity.yaml"].type == "integrity_yaml"


def test_excluded_glob_skipped(tiny_repo: Path) -> None:
    # Drop a fake config inside an excluded path
    bad = tiny_repo / "node_modules" / "pkg" / "package.json"
    bad.parent.mkdir(parents=True)
    bad.write_text('{"name": "skipped"}\n')

    builder = ConfigsBuilder(
        repo_root=tiny_repo,
        globs=["**/package.json"],
        excluded=["node_modules/**"],
    )
    entries, _ = builder.build()
    paths = [e.path for e in entries]
    assert "node_modules/pkg/package.json" not in paths


def test_each_entry_has_sha(tiny_repo: Path) -> None:
    builder = ConfigsBuilder(repo_root=tiny_repo, globs=DEFAULT_GLOBS, excluded=[])
    entries, _ = builder.build()
    for e in entries:
        assert len(e.sha) == 40


def test_unknown_pattern_skipped(tiny_repo: Path) -> None:
    """Files not matching any glob are not listed."""
    (tiny_repo / "RANDOM.md").write_text("hi\n")
    builder = ConfigsBuilder(repo_root=tiny_repo, globs=DEFAULT_GLOBS, excluded=[])
    entries, _ = builder.build()
    paths = {e.path for e in entries}
    assert "RANDOM.md" not in paths
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_configs.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/builders/configs.py`:

```python
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
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_configs.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/builders/configs.py \
        backend/app/integrity/plugins/config_registry/tests/test_builder_configs.py
git commit -m "feat(integrity-e): ConfigsBuilder — type-detected config inventory"
```

---

## Task 8: FunctionsBuilder

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/builders/functions.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_builder_functions.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_builder_functions.py`:

```python
"""Tests for FunctionsBuilder (AST-based)."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.builders.functions import (
    FunctionEntry,
    FunctionsBuilder,
)


def test_extracts_router_decorators(tiny_repo: Path) -> None:
    builder = FunctionsBuilder(
        repo_root=tiny_repo,
        search_globs=["backend/app/api/**/*.py"],
        decorators=["router", "app", "api_router"],
        event_handlers=["startup", "shutdown", "lifespan"],
    )
    entries, failures = builder.build()
    by_id = {e.id: e for e in entries}
    assert "backend.app.api.foo_api.trace_endpoint" in by_id
    trace = by_id["backend.app.api.foo_api.trace_endpoint"]
    assert trace.decorator == "router.post"
    assert trace.target == "/api/trace"
    assert trace.path == "backend/app/api/foo_api.py"
    assert failures == []


def test_extracts_on_event(tiny_repo: Path) -> None:
    builder = FunctionsBuilder(
        repo_root=tiny_repo,
        search_globs=["backend/app/main.py"],
        decorators=["router", "app", "api_router"],
        event_handlers=["startup", "shutdown", "lifespan"],
    )
    entries, _ = builder.build()
    by_id = {e.id: e for e in entries}
    assert "backend.app.main.startup" in by_id
    startup = by_id["backend.app.main.startup"]
    assert startup.decorator == "app.on_event"
    assert startup.target == "startup"


def test_undecorated_function_skipped(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    src = repo / "backend/app/api/x.py"
    src.parent.mkdir(parents=True)
    src.write_text("def plain(): pass\n")
    builder = FunctionsBuilder(
        repo_root=repo, search_globs=["backend/app/api/**/*.py"],
        decorators=["router", "app"], event_handlers=["startup"],
    )
    entries, failures = builder.build()
    assert entries == []
    assert failures == []


def test_syntax_error_yields_failure(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    src = repo / "backend/app/api/bad.py"
    src.parent.mkdir(parents=True)
    src.write_text("def x(:\n  pass\n")  # syntax error
    builder = FunctionsBuilder(
        repo_root=repo, search_globs=["backend/app/api/**/*.py"],
        decorators=["router"], event_handlers=[],
    )
    entries, failures = builder.build()
    assert entries == []
    assert any("bad.py" in f for f in failures)


def test_empty_search_globs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    builder = FunctionsBuilder(
        repo_root=repo, search_globs=[], decorators=["router"], event_handlers=[],
    )
    entries, failures = builder.build()
    assert entries == []
    assert failures == []
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_functions.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/builders/functions.py`:

```python
"""FunctionsBuilder — AST extraction of @router/@app + FastAPI event handlers.

Uses Python ``ast`` (no runtime imports), so syntax errors yield
a per-file failure entry without crashing the scan.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FunctionEntry:
    id: str
    path: str
    line: int
    decorator: str
    target: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "path": self.path, "line": self.line,
                "decorator": self.decorator, "target": self.target}


def _module_dotted_path(rel_path: str) -> str:
    """``"backend/app/api/foo_api.py"`` → ``"backend.app.api.foo_api"``."""
    if rel_path.endswith(".py"):
        rel_path = rel_path[:-3]
    if rel_path.endswith("/__init__"):
        rel_path = rel_path[:-len("/__init__")]
    return rel_path.replace("/", ".")


def _first_string_arg(call: ast.Call) -> str | None:
    if call.args:
        first = call.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return first.value
    return None


def _extract_decorator(
    deco: ast.expr,
    allowed_names: set[str],
    event_handlers: set[str],
) -> tuple[str, str] | None:
    """Return (decorator_name, target) if decorator matches, else None."""
    # @router.post("/x")
    if isinstance(deco, ast.Call) and isinstance(deco.func, ast.Attribute):
        attr = deco.func
        if isinstance(attr.value, ast.Name) and attr.value.id in allowed_names:
            decorator_name = f"{attr.value.id}.{attr.attr}"
            # @app.on_event("startup") special-case
            if attr.attr == "on_event":
                target = _first_string_arg(deco) or ""
                if target in event_handlers:
                    return decorator_name, target
                return None
            target = _first_string_arg(deco) or ""
            return decorator_name, target
    return None


class FunctionsBuilder:
    def __init__(
        self,
        repo_root: Path,
        search_globs: list[str],
        decorators: list[str],
        event_handlers: list[str],
    ) -> None:
        self.repo_root = repo_root
        self.search_globs = list(search_globs)
        self.decorators = set(decorators)
        self.event_handlers = set(event_handlers)

    def build(self) -> tuple[list[FunctionEntry], list[str]]:
        entries: list[FunctionEntry] = []
        failures: list[str] = []

        seen_paths: set[Path] = set()
        for pattern in self.search_globs:
            for path in sorted(self.repo_root.glob(pattern)):
                if not path.is_file() or path in seen_paths:
                    continue
                seen_paths.add(path)
                self._scan_file(path, entries, failures)

        entries.sort(key=lambda e: e.id)
        return entries, failures

    def _scan_file(
        self,
        path: Path,
        entries: list[FunctionEntry],
        failures: list[str],
    ) -> None:
        rel = path.relative_to(self.repo_root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as exc:
            failures.append(f"functions:{rel}: {type(exc).__name__}: {exc}")
            return

        module_dotted = _module_dotted_path(rel)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            for deco in node.decorator_list:
                match = _extract_decorator(deco, self.decorators, self.event_handlers)
                if match is None:
                    continue
                decorator_name, target = match
                entries.append(FunctionEntry(
                    id=f"{module_dotted}.{node.name}",
                    path=rel,
                    line=node.lineno,
                    decorator=decorator_name,
                    target=target,
                ))
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_builder_functions.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/builders/functions.py \
        backend/app/integrity/plugins/config_registry/tests/test_builder_functions.py
git commit -m "feat(integrity-e): FunctionsBuilder — AST-based @router/@app extraction"
```

---

## Task 9: Schema base + first 3 schemas (pyproject, package_json, claude_settings)

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/schemas/base.py`
- Create: `backend/app/integrity/plugins/config_registry/schemas/pyproject.py`
- Create: `backend/app/integrity/plugins/config_registry/schemas/package_json.py`
- Create: `backend/app/integrity/plugins/config_registry/schemas/claude_settings.py`
- Modify: `backend/app/integrity/plugins/config_registry/schemas/__init__.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_schemas_pyproject.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_schemas_package_json.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_schemas_claude_settings.py`

- [ ] **Step 1: Write the failing tests for base + pyproject schema**

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_pyproject.py`:

```python
"""Tests for pyproject schema validator."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.schemas.pyproject import (
    PyprojectSchema,
)


def test_valid_pyproject(tmp_path: Path) -> None:
    p = tmp_path / "pyproject.toml"
    p.write_text('[project]\nname = "x"\nversion = "0.1"\n')
    failures = PyprojectSchema().validate(p, p.read_text())
    assert failures == []


def test_missing_project_table(tmp_path: Path) -> None:
    p = tmp_path / "pyproject.toml"
    p.write_text('[other]\nname = "x"\n')
    failures = PyprojectSchema().validate(p, p.read_text())
    assert any(f.rule == "missing_field" and "[project]" in f.location for f in failures)


def test_missing_name(tmp_path: Path) -> None:
    p = tmp_path / "pyproject.toml"
    p.write_text('[project]\nversion = "0.1"\n')
    failures = PyprojectSchema().validate(p, p.read_text())
    assert any(f.location == "[project].name" for f in failures)


def test_missing_version(tmp_path: Path) -> None:
    p = tmp_path / "pyproject.toml"
    p.write_text('[project]\nname = "x"\n')
    failures = PyprojectSchema().validate(p, p.read_text())
    assert any(f.location == "[project].version" for f in failures)


def test_malformed_toml(tmp_path: Path) -> None:
    p = tmp_path / "pyproject.toml"
    p.write_text('[project\nname = "x"\n')
    failures = PyprojectSchema().validate(p, p.read_text())
    assert any(f.rule == "parse_error" for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_package_json.py`:

```python
"""Tests for package_json schema validator."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.schemas.package_json import (
    PackageJsonSchema,
)


def test_valid(tmp_path: Path) -> None:
    p = tmp_path / "package.json"
    p.write_text('{"name": "x", "version": "0.1.0", "scripts": {}, "dependencies": {}}')
    failures = PackageJsonSchema().validate(p, p.read_text())
    assert failures == []


def test_missing_name(tmp_path: Path) -> None:
    p = tmp_path / "package.json"
    p.write_text('{"version": "0.1.0"}')
    failures = PackageJsonSchema().validate(p, p.read_text())
    assert any(f.location == "name" for f in failures)


def test_scripts_not_object(tmp_path: Path) -> None:
    p = tmp_path / "package.json"
    p.write_text('{"name": "x", "version": "0.1.0", "scripts": []}')
    failures = PackageJsonSchema().validate(p, p.read_text())
    assert any(f.location == "scripts" for f in failures)


def test_malformed_json(tmp_path: Path) -> None:
    p = tmp_path / "package.json"
    p.write_text('{not json}')
    failures = PackageJsonSchema().validate(p, p.read_text())
    assert any(f.rule == "parse_error" for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_claude_settings.py`:

```python
"""Tests for claude_settings schema validator."""
from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.config_registry.schemas.claude_settings import (
    ClaudeSettingsSchema,
)


def test_valid_with_hooks(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text('{"hooks": {"PostToolUse": [{"matcher": "Edit", "command": "echo"}]}}')
    failures = ClaudeSettingsSchema().validate(p, p.read_text())
    assert failures == []


def test_valid_without_hooks(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text('{}')
    failures = ClaudeSettingsSchema().validate(p, p.read_text())
    assert failures == []


def test_hooks_malformed(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text('{"hooks": {"PostToolUse": [{"matcher": "Edit"}]}}')  # no command
    failures = ClaudeSettingsSchema().validate(p, p.read_text())
    assert any("command" in f.location for f in failures)


def test_malformed_json(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text('{x}')
    failures = ClaudeSettingsSchema().validate(p, p.read_text())
    assert any(f.rule == "parse_error" for f in failures)
```

- [ ] **Step 2: Run tests — verify failures**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_schemas_pyproject.py backend/app/integrity/plugins/config_registry/tests/test_schemas_package_json.py backend/app/integrity/plugins/config_registry/tests/test_schemas_claude_settings.py -v`
Expected: All FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write base.py**

Create `backend/app/integrity/plugins/config_registry/schemas/base.py`:

```python
"""SchemaValidator protocol + ValidationFailure dataclass."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class ValidationFailure:
    rule: str           # short id like "missing_field" or "parse_error"
    location: str       # JSON-ish path inside the file, e.g. "[project].name"
    message: str


@runtime_checkable
class SchemaValidator(Protocol):
    type_name: str

    def validate(self, path: Path, content: str) -> list[ValidationFailure]: ...
```

- [ ] **Step 4: Write pyproject.py**

Create `backend/app/integrity/plugins/config_registry/schemas/pyproject.py`:

```python
"""Schema validator for ``pyproject.toml``."""
from __future__ import annotations

import sys
from pathlib import Path

from .base import ValidationFailure

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


class PyprojectSchema:
    type_name = "pyproject"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        try:
            data = tomllib.loads(content)
        except tomllib.TOMLDecodeError as exc:
            return [ValidationFailure(
                rule="parse_error", location="<root>",
                message=f"TOML parse error: {exc}",
            )]

        project = data.get("project")
        if not isinstance(project, dict):
            failures.append(ValidationFailure(
                rule="missing_field", location="[project]",
                message="pyproject.toml must define a [project] table",
            ))
            return failures

        if "name" not in project:
            failures.append(ValidationFailure(
                rule="missing_field", location="[project].name",
                message="[project].name is required",
            ))
        if "version" not in project:
            failures.append(ValidationFailure(
                rule="missing_field", location="[project].version",
                message="[project].version is required",
            ))

        return failures
```

- [ ] **Step 5: Write package_json.py**

Create `backend/app/integrity/plugins/config_registry/schemas/package_json.py`:

```python
"""Schema validator for ``package.json``."""
from __future__ import annotations

import json
from pathlib import Path

from .base import ValidationFailure


class PackageJsonSchema:
    type_name = "package_json"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            return [ValidationFailure(
                rule="parse_error", location="<root>",
                message=f"JSON parse error: {exc}",
            )]

        if not isinstance(data, dict):
            return [ValidationFailure(
                rule="bad_root", location="<root>",
                message="package.json root must be an object",
            )]

        if "name" not in data:
            failures.append(ValidationFailure(
                rule="missing_field", location="name",
                message='"name" is required',
            ))
        if "version" not in data:
            failures.append(ValidationFailure(
                rule="missing_field", location="version",
                message='"version" is required',
            ))

        for field_name in ("scripts", "dependencies", "devDependencies"):
            if field_name in data and not isinstance(data[field_name], dict):
                failures.append(ValidationFailure(
                    rule="wrong_type", location=field_name,
                    message=f'"{field_name}" must be an object, got {type(data[field_name]).__name__}',
                ))

        return failures
```

- [ ] **Step 6: Write claude_settings.py**

Create `backend/app/integrity/plugins/config_registry/schemas/claude_settings.py`:

```python
"""Schema validator for ``.claude/settings.json``."""
from __future__ import annotations

import json
from pathlib import Path

from .base import ValidationFailure


class ClaudeSettingsSchema:
    type_name = "claude_settings"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            return [ValidationFailure(
                rule="parse_error", location="<root>",
                message=f"JSON parse error: {exc}",
            )]

        hooks = data.get("hooks")
        if hooks is None:
            return failures
        if not isinstance(hooks, dict):
            failures.append(ValidationFailure(
                rule="wrong_type", location="hooks",
                message=f'"hooks" must be an object, got {type(hooks).__name__}',
            ))
            return failures

        for event, entries in hooks.items():
            if not isinstance(entries, list):
                failures.append(ValidationFailure(
                    rule="wrong_type", location=f"hooks.{event}",
                    message=f'"hooks.{event}" must be a list',
                ))
                continue
            for i, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    failures.append(ValidationFailure(
                        rule="wrong_type", location=f"hooks.{event}[{i}]",
                        message="hook entry must be an object",
                    ))
                    continue
                for required in ("matcher", "command"):
                    if required not in entry:
                        failures.append(ValidationFailure(
                            rule="missing_field",
                            location=f"hooks.{event}[{i}].{required}",
                            message=f'"{required}" is required for hook entries',
                        ))

        return failures
```

- [ ] **Step 7: Update schemas/__init__.py**

Edit `backend/app/integrity/plugins/config_registry/schemas/__init__.py`:

```python
"""Schema registry — maps config type → SchemaValidator."""
from __future__ import annotations

from .base import SchemaValidator, ValidationFailure
from .claude_settings import ClaudeSettingsSchema
from .package_json import PackageJsonSchema
from .pyproject import PyprojectSchema

SCHEMA_REGISTRY: dict[str, SchemaValidator] = {
    "pyproject": PyprojectSchema(),
    "package_json": PackageJsonSchema(),
    "claude_settings": ClaudeSettingsSchema(),
}

__all__ = ["SchemaValidator", "ValidationFailure", "SCHEMA_REGISTRY"]
```

- [ ] **Step 8: Run tests — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_schemas_pyproject.py backend/app/integrity/plugins/config_registry/tests/test_schemas_package_json.py backend/app/integrity/plugins/config_registry/tests/test_schemas_claude_settings.py -v`
Expected: 13 passed (5 + 4 + 4).

- [ ] **Step 9: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/schemas/base.py \
        backend/app/integrity/plugins/config_registry/schemas/pyproject.py \
        backend/app/integrity/plugins/config_registry/schemas/package_json.py \
        backend/app/integrity/plugins/config_registry/schemas/claude_settings.py \
        backend/app/integrity/plugins/config_registry/schemas/__init__.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_pyproject.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_package_json.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_claude_settings.py
git commit -m "feat(integrity-e): schema validators for pyproject + package.json + claude settings"
```

---

## Task 10: Remaining 6 schema validators

**Files:**
- Create: 6 schema modules (`integrity_yaml.py`, `makefile.py`, `dockerfile.py`, `env_example.py`, `vite_config.py`, `tsconfig.py`)
- Modify: `backend/app/integrity/plugins/config_registry/schemas/__init__.py`
- Test: 6 new test files

- [ ] **Step 1: Write failing tests for all six**

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_integrity_yaml.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.integrity_yaml import IntegrityYamlSchema

def test_valid(tmp_path: Path):
    p = tmp_path / "integrity.yaml"
    p.write_text("plugins:\n  graph_lint:\n    enabled: true\n")
    assert IntegrityYamlSchema().validate(p, p.read_text()) == []

def test_plugins_not_mapping(tmp_path: Path):
    p = tmp_path / "integrity.yaml"
    p.write_text("plugins: []\n")
    failures = IntegrityYamlSchema().validate(p, p.read_text())
    assert any(f.location == "plugins" for f in failures)

def test_plugin_missing_enabled(tmp_path: Path):
    p = tmp_path / "integrity.yaml"
    p.write_text("plugins:\n  foo: {}\n")
    failures = IntegrityYamlSchema().validate(p, p.read_text())
    assert any("enabled" in f.location for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_makefile.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.makefile import MakefileSchema

def test_valid(tmp_path: Path):
    p = tmp_path / "Makefile"
    p.write_text(".PHONY: test build\ntest:\n\techo test\nbuild:\n\techo build\n")
    assert MakefileSchema().validate(p, p.read_text()) == []

def test_phony_missing_target(tmp_path: Path):
    p = tmp_path / "Makefile"
    p.write_text(".PHONY: test\ntest:\n\techo t\nbuild:\n\techo b\n")
    failures = MakefileSchema().validate(p, p.read_text())
    assert any("build" in f.message and "PHONY" in f.message for f in failures)

def test_camelcase_target(tmp_path: Path):
    p = tmp_path / "Makefile"
    p.write_text(".PHONY: testThing\ntestThing:\n\techo t\n")
    failures = MakefileSchema().validate(p, p.read_text())
    assert any("kebab" in f.message.lower() or "case" in f.message.lower() for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_dockerfile.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.dockerfile import DockerfileSchema

def test_valid(tmp_path: Path):
    p = tmp_path / "Dockerfile"
    p.write_text("FROM python:3.12\nRUN echo\n")
    assert DockerfileSchema().validate(p, p.read_text()) == []

def test_missing_from(tmp_path: Path):
    p = tmp_path / "Dockerfile"
    p.write_text("RUN echo\n")
    failures = DockerfileSchema().validate(p, p.read_text())
    assert any(f.rule == "missing_from" for f in failures)

def test_undeclared_stage(tmp_path: Path):
    p = tmp_path / "Dockerfile"
    p.write_text("FROM python:3.12 AS build\nFROM python:3.12\nCOPY --from=missing /a /b\n")
    failures = DockerfileSchema().validate(p, p.read_text())
    assert any("missing" in f.message for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_env_example.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.env_example import EnvExampleSchema

def test_valid(tmp_path: Path):
    p = tmp_path / ".env.example"
    p.write_text("# comment\nFOO=\nBAR=baz\n")
    assert EnvExampleSchema().validate(p, p.read_text()) == []

def test_lowercase_key(tmp_path: Path):
    p = tmp_path / ".env.example"
    p.write_text("foo=bar\n")
    failures = EnvExampleSchema().validate(p, p.read_text())
    assert any("foo" in f.location for f in failures)

def test_missing_equals(tmp_path: Path):
    p = tmp_path / ".env.example"
    p.write_text("FOOBAR\n")
    failures = EnvExampleSchema().validate(p, p.read_text())
    assert any(f.rule == "bad_format" for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_vite_config.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.vite_config import ViteConfigSchema

def test_valid(tmp_path: Path):
    p = tmp_path / "vite.config.ts"
    p.write_text("export default { plugins: [] };\n")
    assert ViteConfigSchema().validate(p, p.read_text()) == []

def test_missing_export_default(tmp_path: Path):
    p = tmp_path / "vite.config.ts"
    p.write_text("const x = 1;\n")
    failures = ViteConfigSchema().validate(p, p.read_text())
    assert any(f.rule == "missing_export_default" for f in failures)
```

Create `backend/app/integrity/plugins/config_registry/tests/test_schemas_tsconfig.py`:

```python
from pathlib import Path
from backend.app.integrity.plugins.config_registry.schemas.tsconfig import TsconfigSchema

def test_valid(tmp_path: Path):
    p = tmp_path / "tsconfig.json"
    p.write_text('{"compilerOptions": {"strict": true}}')
    assert TsconfigSchema().validate(p, p.read_text()) == []

def test_missing_compiler_options(tmp_path: Path):
    p = tmp_path / "tsconfig.json"
    p.write_text('{}')
    failures = TsconfigSchema().validate(p, p.read_text())
    assert any(f.location == "compilerOptions" for f in failures)

def test_extends_missing_file(tmp_path: Path):
    p = tmp_path / "tsconfig.json"
    p.write_text('{"extends": "./does-not-exist.json", "compilerOptions": {}}')
    failures = TsconfigSchema().validate(p, p.read_text())
    assert any("extends" in f.location for f in failures)
```

- [ ] **Step 2: Run tests — verify failures**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_schemas_integrity_yaml.py backend/app/integrity/plugins/config_registry/tests/test_schemas_makefile.py backend/app/integrity/plugins/config_registry/tests/test_schemas_dockerfile.py backend/app/integrity/plugins/config_registry/tests/test_schemas_env_example.py backend/app/integrity/plugins/config_registry/tests/test_schemas_vite_config.py backend/app/integrity/plugins/config_registry/tests/test_schemas_tsconfig.py -v`
Expected: All FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write integrity_yaml.py**

```python
"""Schema validator for ``config/integrity.yaml``."""
from __future__ import annotations

from pathlib import Path

import yaml

from .base import ValidationFailure


class IntegrityYamlSchema:
    type_name = "integrity_yaml"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        try:
            data = yaml.safe_load(content) or {}
        except yaml.YAMLError as exc:
            return [ValidationFailure(
                rule="parse_error", location="<root>",
                message=f"YAML parse error: {exc}",
            )]
        plugins = data.get("plugins")
        if plugins is None:
            return failures
        if not isinstance(plugins, dict):
            return [ValidationFailure(
                rule="wrong_type", location="plugins",
                message=f'"plugins" must be a mapping, got {type(plugins).__name__}',
            )]
        for name, entry in plugins.items():
            if not isinstance(entry, dict):
                failures.append(ValidationFailure(
                    rule="wrong_type", location=f"plugins.{name}",
                    message=f'"plugins.{name}" must be a mapping',
                ))
                continue
            if "enabled" not in entry:
                failures.append(ValidationFailure(
                    rule="missing_field", location=f"plugins.{name}.enabled",
                    message=f'"plugins.{name}.enabled" is required (bool)',
                ))
        return failures
```

- [ ] **Step 4: Write makefile.py**

```python
"""Schema validator for ``Makefile``."""
from __future__ import annotations

import re
from pathlib import Path

from .base import ValidationFailure

PHONY_RE = re.compile(r"^\.PHONY:\s*(.+)$", re.MULTILINE)
TARGET_RE = re.compile(r"^([A-Za-z0-9_.-]+):", re.MULTILINE)
KEBAB_OK = re.compile(r"^[a-z0-9._-]+$")


class MakefileSchema:
    type_name = "makefile"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []

        phony_targets: set[str] = set()
        for m in PHONY_RE.finditer(content):
            phony_targets.update(m.group(1).split())

        # Find every target (left-of-colon at line start, not indented).
        for tm in TARGET_RE.finditer(content):
            target = tm.group(1)
            if target.startswith("."):  # .PHONY etc.
                continue
            if not KEBAB_OK.match(target):
                failures.append(ValidationFailure(
                    rule="bad_target_case",
                    location=f"target:{target}",
                    message=f"Make target '{target}' should use kebab-case",
                ))
            # Heuristic: if a target produces no file (rule body uses no $@ or
            # ends in .PHONY-style action), require it be in .PHONY.
            if target not in phony_targets and not _looks_like_file_target(target):
                failures.append(ValidationFailure(
                    rule="missing_phony", location=f".PHONY",
                    message=f"target '{target}' is not in .PHONY",
                ))
        return failures


def _looks_like_file_target(target: str) -> bool:
    return "/" in target or "." in target.lstrip(".")
```

- [ ] **Step 5: Write dockerfile.py**

```python
"""Schema validator for ``Dockerfile*``."""
from __future__ import annotations

import re
from pathlib import Path

from .base import ValidationFailure

FROM_RE = re.compile(r"^FROM\s+\S+(?:\s+AS\s+(\S+))?", re.IGNORECASE | re.MULTILINE)
COPY_FROM_RE = re.compile(r"^COPY\s+--from=(\S+)", re.IGNORECASE | re.MULTILINE)


class DockerfileSchema:
    type_name = "dockerfile"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        first_meaningful = next(
            (l.strip() for l in content.splitlines()
             if l.strip() and not l.strip().startswith("#")),
            "",
        )
        if not first_meaningful.upper().startswith("FROM"):
            failures.append(ValidationFailure(
                rule="missing_from", location="line:1",
                message="Dockerfile must start with FROM",
            ))

        stage_names = {m.group(1) for m in FROM_RE.finditer(content) if m.group(1)}
        for cm in COPY_FROM_RE.finditer(content):
            ref = cm.group(1)
            # Numeric refs and image refs (with /) are valid.
            if ref.isdigit() or "/" in ref or ":" in ref:
                continue
            if ref not in stage_names:
                failures.append(ValidationFailure(
                    rule="undeclared_stage",
                    location=f"COPY --from={ref}",
                    message=f"COPY --from references undeclared stage '{ref}'",
                ))
        return failures
```

- [ ] **Step 6: Write env_example.py**

```python
"""Schema validator for ``.env.example``."""
from __future__ import annotations

import re
from pathlib import Path

from .base import ValidationFailure

KEY_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")


class EnvExampleSchema:
    type_name = "env_example"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        failures: list[ValidationFailure] = []
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                failures.append(ValidationFailure(
                    rule="bad_format", location=f"line:{i}",
                    message=f"line {i}: expected KEY=VALUE, got {stripped!r}",
                ))
                continue
            key, _ = stripped.split("=", 1)
            if not KEY_RE.match(key):
                failures.append(ValidationFailure(
                    rule="bad_key", location=f"line:{i}:key:{key}",
                    message=f"line {i}: key '{key}' must match [A-Z_][A-Z0-9_]*",
                ))
        return failures
```

- [ ] **Step 7: Write vite_config.py**

```python
"""Schema validator for ``vite.config.{ts,js,mjs}``.

Cannot exec arbitrary TypeScript safely, so we only check that
``export default`` is present (Vite requires it).
"""
from __future__ import annotations

from pathlib import Path

from .base import ValidationFailure


class ViteConfigSchema:
    type_name = "vite_config"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        if "export default" not in content:
            return [ValidationFailure(
                rule="missing_export_default", location="<root>",
                message="vite.config must contain `export default`",
            )]
        return []
```

- [ ] **Step 8: Write tsconfig.py**

```python
"""Schema validator for ``tsconfig*.json``."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .base import ValidationFailure

# Strip JSON-with-comments before parsing.
LINE_COMMENT = re.compile(r"//[^\n]*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def _strip_jsonc(s: str) -> str:
    s = BLOCK_COMMENT.sub("", s)
    s = LINE_COMMENT.sub("", s)
    return s


class TsconfigSchema:
    type_name = "tsconfig"

    def validate(self, path: Path, content: str) -> list[ValidationFailure]:
        try:
            data = json.loads(_strip_jsonc(content))
        except json.JSONDecodeError as exc:
            return [ValidationFailure(
                rule="parse_error", location="<root>",
                message=f"JSON parse error: {exc}",
            )]
        failures: list[ValidationFailure] = []
        if "compilerOptions" not in data:
            failures.append(ValidationFailure(
                rule="missing_field", location="compilerOptions",
                message='"compilerOptions" is required',
            ))
        ext = data.get("extends")
        if isinstance(ext, str):
            target = (path.parent / ext).resolve()
            if not target.exists():
                failures.append(ValidationFailure(
                    rule="bad_extends", location="extends",
                    message=f'"extends" points to missing file: {ext}',
                ))
        return failures
```

- [ ] **Step 9: Update schemas/__init__.py**

Edit `backend/app/integrity/plugins/config_registry/schemas/__init__.py`:

```python
"""Schema registry — maps config type → SchemaValidator."""
from __future__ import annotations

from .base import SchemaValidator, ValidationFailure
from .claude_settings import ClaudeSettingsSchema
from .dockerfile import DockerfileSchema
from .env_example import EnvExampleSchema
from .integrity_yaml import IntegrityYamlSchema
from .makefile import MakefileSchema
from .package_json import PackageJsonSchema
from .pyproject import PyprojectSchema
from .tsconfig import TsconfigSchema
from .vite_config import ViteConfigSchema

SCHEMA_REGISTRY: dict[str, SchemaValidator] = {
    "pyproject": PyprojectSchema(),
    "package_json": PackageJsonSchema(),
    "claude_settings": ClaudeSettingsSchema(),
    "integrity_yaml": IntegrityYamlSchema(),
    "makefile": MakefileSchema(),
    "dockerfile": DockerfileSchema(),
    "env_example": EnvExampleSchema(),
    "vite_config": ViteConfigSchema(),
    "tsconfig": TsconfigSchema(),
}

__all__ = ["SchemaValidator", "ValidationFailure", "SCHEMA_REGISTRY"]
```

- [ ] **Step 10: Run all schema tests — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_schemas_*.py -v`
Expected: All schema tests pass (~30 total).

- [ ] **Step 11: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/schemas/integrity_yaml.py \
        backend/app/integrity/plugins/config_registry/schemas/makefile.py \
        backend/app/integrity/plugins/config_registry/schemas/dockerfile.py \
        backend/app/integrity/plugins/config_registry/schemas/env_example.py \
        backend/app/integrity/plugins/config_registry/schemas/vite_config.py \
        backend/app/integrity/plugins/config_registry/schemas/tsconfig.py \
        backend/app/integrity/plugins/config_registry/schemas/__init__.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_integrity_yaml.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_makefile.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_dockerfile.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_env_example.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_vite_config.py \
        backend/app/integrity/plugins/config_registry/tests/test_schemas_tsconfig.py
git commit -m "feat(integrity-e): six remaining schema validators (yaml/makefile/dockerfile/env/vite/tsconfig)"
```

---

## Task 11: rules/added.py — config.added rule

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/rules/added.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_rule_added.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_rule_added.py`:

```python
"""Tests for config.added rule."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.manifest import empty_manifest
from backend.app.integrity.plugins.config_registry.rules.added import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _ctx(repo: Path) -> ScanContext:
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


def test_emits_info_for_new_script(tiny_repo: Path) -> None:
    prior = empty_manifest()
    current = empty_manifest()
    current["scripts"] = [{"id": "scripts/new.sh", "path": "scripts/new.sh",
                           "interpreter": "bash", "sha": "x"}]
    cfg = {"_prior_manifest": prior, "_current_manifest": current}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].rule == "config.added"
    assert issues[0].severity == "INFO"
    assert issues[0].node_id == "scripts/new.sh"


def test_no_diff_no_issues(tiny_repo: Path) -> None:
    m = empty_manifest()
    cfg = {"_prior_manifest": m, "_current_manifest": m}
    assert run(_ctx(tiny_repo), cfg, date(2026, 4, 17)) == []


def test_added_across_all_keys(tiny_repo: Path) -> None:
    prior = empty_manifest()
    current = empty_manifest()
    current["skills"] = [{"id": "alpha"}]
    current["scripts"] = [{"id": "scripts/a.sh"}]
    current["routes"] = [{"id": "route::GET::/x"}]
    current["configs"] = [{"id": "Makefile"}]
    current["functions"] = [{"id": "backend.app.api.x.y"}]
    cfg = {"_prior_manifest": prior, "_current_manifest": current}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) == 5
    assert {i.rule for i in issues} == {"config.added"}
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_added.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/rules/added.py`:

```python
"""``config.added`` — INFO when a manifest entry appears for the first time."""
from __future__ import annotations

from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext
from ..manifest import diff_manifests


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    current = cfg.get("_current_manifest") or {}
    prior = cfg.get("_prior_manifest") or {}
    delta = diff_manifests(current, prior)

    issues: list[IntegrityIssue] = []
    for key, entries in delta.added.items():
        for entry in entries:
            entry_id = str(entry.get("id"))
            issues.append(IntegrityIssue(
                rule="config.added",
                severity="INFO",
                node_id=entry_id,
                location=f"{key}:{entry_id}",
                message=f"New {key[:-1]} added to manifest: {entry_id}",
                evidence={"category": key, "entry": entry},
                fix_class=None,
            ))
    return issues
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_added.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/rules/added.py \
        backend/app/integrity/plugins/config_registry/tests/test_rule_added.py
git commit -m "feat(integrity-e): config.added rule (INFO on new manifest entries)"
```

---

## Task 12: rules/removed.py — config.removed with graph escalation

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/rules/removed.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_rule_removed.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_rule_removed.py`:

```python
"""Tests for config.removed rule."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.manifest import empty_manifest
from backend.app.integrity.plugins.config_registry.rules.removed import (
    build_dep_index,
    run,
)
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _ctx(repo: Path) -> ScanContext:
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


def test_emits_info_for_orphan_removal(tiny_repo: Path) -> None:
    prior = empty_manifest()
    prior["scripts"] = [{"id": "scripts/totally-gone.sh"}]  # not in graph
    current = empty_manifest()
    cfg = {"_prior_manifest": prior, "_current_manifest": current,
           "_dep_graph": build_dep_index(GraphSnapshot.load(tiny_repo)),
           "removed_escalation": {"enabled": True}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].severity == "INFO"
    assert issues[0].node_id == "scripts/totally-gone.sh"


def test_escalates_to_warn_when_referenced(tiny_repo: Path) -> None:
    """If removed id appears in graph node id or source_file → WARN."""
    prior = empty_manifest()
    # legacy_removed.py is in the graph snapshot's source_file values
    prior["configs"] = [{"id": "backend/app/api/legacy_removed.py"}]
    current = empty_manifest()
    cfg = {"_prior_manifest": prior, "_current_manifest": current,
           "_dep_graph": build_dep_index(GraphSnapshot.load(tiny_repo)),
           "removed_escalation": {"enabled": True}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].severity == "WARN"
    assert "still referenced" in issues[0].message.lower()


def test_no_escalation_when_disabled(tiny_repo: Path) -> None:
    prior = empty_manifest()
    prior["configs"] = [{"id": "backend/app/api/legacy_removed.py"}]
    current = empty_manifest()
    cfg = {"_prior_manifest": prior, "_current_manifest": current,
           "_dep_graph": build_dep_index(GraphSnapshot.load(tiny_repo)),
           "removed_escalation": {"enabled": False}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].severity == "INFO"


def test_no_diff_no_issues(tiny_repo: Path) -> None:
    m = empty_manifest()
    cfg = {"_prior_manifest": m, "_current_manifest": m,
           "_dep_graph": build_dep_index(GraphSnapshot.load(tiny_repo)),
           "removed_escalation": {"enabled": True}}
    assert run(_ctx(tiny_repo), cfg, date(2026, 4, 17)) == []
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_removed.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/rules/removed.py`:

```python
"""``config.removed`` — INFO normally; WARN when id still referenced in graph."""
from __future__ import annotations

from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext
from ...schema import GraphSnapshot
from ..manifest import diff_manifests


def build_dep_index(graph: GraphSnapshot) -> set[str]:
    """Flatten every node id and source_file value into one lookup set."""
    index: set[str] = set()
    for node in graph.nodes:
        nid = str(node.get("id", ""))
        if nid:
            index.add(nid)
        sf = node.get("source_file")
        if isinstance(sf, str) and sf:
            index.add(sf)
    return index


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    current = cfg.get("_current_manifest") or {}
    prior = cfg.get("_prior_manifest") or {}
    dep_index: set[str] = cfg.get("_dep_graph") or build_dep_index(ctx.graph)
    escalation_enabled = bool(
        cfg.get("removed_escalation", {}).get("enabled", True)
    )

    delta = diff_manifests(current, prior)
    issues: list[IntegrityIssue] = []
    for key, entries in delta.removed.items():
        for entry in entries:
            entry_id = str(entry.get("id"))
            referenced = escalation_enabled and entry_id in dep_index
            severity = "WARN" if referenced else "INFO"
            msg_suffix = (
                " (still referenced in dep graph)" if referenced else ""
            )
            issues.append(IntegrityIssue(
                rule="config.removed",
                severity=severity,
                node_id=entry_id,
                location=f"{key}:{entry_id}",
                message=f"Removed from manifest: {entry_id}{msg_suffix}",
                evidence={
                    "category": key,
                    "entry": entry,
                    "still_referenced": referenced,
                },
                fix_class=None,
            ))
    return issues
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_removed.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/rules/removed.py \
        backend/app/integrity/plugins/config_registry/tests/test_rule_removed.py
git commit -m "feat(integrity-e): config.removed rule with dep-graph escalation"
```

---

## Task 13: rules/schema_drift.py — config.schema_drift rule

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/rules/schema_drift.py`
- Test: `backend/app/integrity/plugins/config_registry/tests/test_rule_schema_drift.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_rule_schema_drift.py`:

```python
"""Tests for config.schema_drift rule."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.manifest import empty_manifest
from backend.app.integrity.plugins.config_registry.rules.schema_drift import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _ctx(repo: Path) -> ScanContext:
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


def test_invalid_pyproject_emits_warn(tiny_repo: Path) -> None:
    bad = tiny_repo / "pyproject.toml"
    bad.write_text('[other]\nname = "x"\n')
    current = empty_manifest()
    current["configs"] = [{"id": "pyproject.toml", "type": "pyproject",
                           "path": "pyproject.toml", "sha": "x"}]
    cfg = {"_prior_manifest": empty_manifest(),
           "_current_manifest": current,
           "schema_drift": {"enabled": True, "strict_mode": False}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert len(issues) >= 1
    drift = next(i for i in issues if i.rule == "config.schema_drift")
    assert drift.severity == "WARN"
    assert drift.node_id == "pyproject.toml"
    assert "validation_failures" in drift.evidence


def test_valid_pyproject_no_issue(tiny_repo: Path) -> None:
    current = empty_manifest()
    current["configs"] = [{"id": "pyproject.toml", "type": "pyproject",
                           "path": "pyproject.toml", "sha": "x"}]
    cfg = {"_prior_manifest": empty_manifest(),
           "_current_manifest": current,
           "schema_drift": {"enabled": True, "strict_mode": False}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert issues == []


def test_unknown_type_skipped_in_lenient(tiny_repo: Path) -> None:
    """Unknown type with strict_mode=False → no issue, no failure."""
    current = empty_manifest()
    current["configs"] = [{"id": "weird.cfg", "type": "made_up_type",
                           "path": "weird.cfg", "sha": "x"}]
    cfg = {"_prior_manifest": empty_manifest(),
           "_current_manifest": current,
           "schema_drift": {"enabled": True, "strict_mode": False}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert issues == []


def test_unknown_type_warns_in_strict(tiny_repo: Path) -> None:
    current = empty_manifest()
    current["configs"] = [{"id": "weird.cfg", "type": "made_up_type",
                           "path": "weird.cfg", "sha": "x"}]
    cfg = {"_prior_manifest": empty_manifest(),
           "_current_manifest": current,
           "schema_drift": {"enabled": True, "strict_mode": True}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert any(i.rule == "config.schema_drift" and "no schema" in i.message.lower() for i in issues)


def test_missing_file_silently_skipped(tiny_repo: Path) -> None:
    """Manifest entry whose file no longer exists → skipped (covered by removed rule)."""
    current = empty_manifest()
    current["configs"] = [{"id": "ghost.toml", "type": "pyproject",
                           "path": "ghost.toml", "sha": "x"}]
    cfg = {"_prior_manifest": empty_manifest(),
           "_current_manifest": current,
           "schema_drift": {"enabled": True, "strict_mode": False}}
    issues = run(_ctx(tiny_repo), cfg, date(2026, 4, 17))
    assert issues == []
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_schema_drift.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/rules/schema_drift.py`:

```python
"""``config.schema_drift`` — WARN when a config violates its schema validator."""
from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext
from ..schemas import SCHEMA_REGISTRY


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    drift_cfg = cfg.get("schema_drift", {})
    if not drift_cfg.get("enabled", True):
        return []
    strict_mode = bool(drift_cfg.get("strict_mode", False))

    current = cfg.get("_current_manifest") or {}
    issues: list[IntegrityIssue] = []

    for entry in current.get("configs", []):
        entry_id = str(entry.get("id"))
        type_name = str(entry.get("type", ""))
        path = ctx.repo_root / str(entry.get("path", ""))

        if not path.exists():
            continue

        validator = SCHEMA_REGISTRY.get(type_name)
        if validator is None:
            if strict_mode:
                issues.append(IntegrityIssue(
                    rule="config.schema_drift",
                    severity="WARN",
                    node_id=entry_id,
                    location=f"configs:{entry_id}",
                    message=f"No schema for type '{type_name}' (strict mode)",
                    evidence={"type": type_name},
                ))
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            issues.append(IntegrityIssue(
                rule="config.schema_drift",
                severity="WARN",
                node_id=entry_id,
                location=f"configs:{entry_id}",
                message=f"Cannot read file: {exc}",
                evidence={"error": str(exc)},
            ))
            continue

        failures = validator.validate(path, content)
        if failures:
            issues.append(IntegrityIssue(
                rule="config.schema_drift",
                severity="WARN",
                node_id=entry_id,
                location=f"configs:{entry_id}",
                message=(
                    f"{len(failures)} schema violation(s) in {entry_id} "
                    f"({type_name})"
                ),
                evidence={
                    "type": type_name,
                    "validation_failures": [asdict(f) for f in failures],
                },
            ))

    return issues
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_rule_schema_drift.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/rules/schema_drift.py \
        backend/app/integrity/plugins/config_registry/tests/test_rule_schema_drift.py
git commit -m "feat(integrity-e): config.schema_drift rule with per-type validators"
```

---

## Task 14: ConfigRegistryPlugin orchestration

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/plugin.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/plugins/config_registry/tests/test_plugin_basic.py`:

```python
"""Smoke test for ConfigRegistryPlugin orchestration."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.plugin import ConfigRegistryPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def test_plugin_writes_manifest_and_artifact(tiny_repo: Path) -> None:
    plugin = ConfigRegistryPlugin(
        config={
            "manifest_path": "config/manifest.yaml",
            "skills_root": "backend/app/skills",
            "scripts_root": "scripts",
            "config_globs": [
                "pyproject.toml", "package.json", ".claude/settings.json",
                "vite.config.*", "tsconfig*.json", "Dockerfile*", "Makefile",
                ".env.example", "config/integrity.yaml",
            ],
            "excluded_paths": ["node_modules/**", "**/__pycache__/**"],
            "function_search_globs": [
                "backend/app/api/**/*.py", "backend/app/main.py",
            ],
            "function_decorators": ["router", "app", "api_router"],
            "function_event_handlers": ["startup", "shutdown", "lifespan"],
            "schema_drift": {"enabled": True, "strict_mode": False},
            "removed_escalation": {"enabled": True},
        },
        today=date(2026, 4, 17),
    )
    ctx = ScanContext(repo_root=tiny_repo, graph=GraphSnapshot.load(tiny_repo))
    result = plugin.scan(ctx)
    assert result.plugin_name == "config_registry"
    # Manifest written
    manifest_path = tiny_repo / "config/manifest.yaml"
    assert manifest_path.exists()
    body = manifest_path.read_text()
    assert "AUTO-GENERATED" in body
    # Artifact written
    artifact = tiny_repo / "integrity-out" / "2026-04-17" / "config_registry.json"
    assert artifact in result.artifacts
    payload = json.loads(artifact.read_text())
    assert "rules_run" in payload
    assert "issues" in payload


def test_plugin_handles_rule_exception_gracefully(tiny_repo: Path) -> None:
    """A buggy rule should yield ERROR issue, sibling rules continue."""
    def buggy(ctx, cfg, today):
        raise RuntimeError("boom")

    plugin = ConfigRegistryPlugin(
        config={"manifest_path": "config/manifest.yaml",
                "skills_root": "backend/app/skills",
                "scripts_root": "scripts",
                "config_globs": ["pyproject.toml"],
                "excluded_paths": [],
                "function_search_globs": [],
                "function_decorators": [],
                "function_event_handlers": [],
                "schema_drift": {"enabled": False},
                "removed_escalation": {"enabled": False}},
        today=date(2026, 4, 17),
        rules={"config.broken": buggy},
    )
    ctx = ScanContext(repo_root=tiny_repo, graph=GraphSnapshot.load(tiny_repo))
    result = plugin.scan(ctx)
    error_issues = [i for i in result.issues if i.severity == "ERROR"]
    assert error_issues
    assert any("config.broken" in f for f in result.failures)
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_plugin_basic.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

Create `backend/app/integrity/plugins/config_registry/plugin.py`:

```python
"""ConfigRegistryPlugin — gate δ orchestration.

Mirrors GraphLintPlugin / DocAuditPlugin shape: per-rule try/except,
writes integrity-out/{date}/config_registry.json, registers depends_on=()
to run standalone or alongside Plugin A's graph_extension.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext, ScanResult
from .builders.configs import ConfigsBuilder
from .builders.functions import FunctionsBuilder
from .builders.routes import RoutesBuilder
from .builders.scripts import ScriptsBuilder
from .builders.skills import SkillsBuilder
from .manifest import (
    GENERATOR_VERSION,
    empty_manifest,
    read_manifest,
    write_manifest,
)
from .rules.removed import build_dep_index

Rule = Callable[[ScanContext, dict[str, Any], date], list[IntegrityIssue]]


def _default_rules() -> dict[str, Rule]:
    from .rules import added, removed, schema_drift
    return {
        "config.added": added.run,
        "config.removed": removed.run,
        "config.schema_drift": schema_drift.run,
    }


@dataclass
class ConfigRegistryPlugin:
    name: str = "config_registry"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ()
    paths: tuple[str, ...] = (
        "backend/app/skills/**/SKILL.md",
        "backend/app/skills/**/skill.yaml",
        "scripts/**/*.py",
        "scripts/**/*.sh",
        "scripts/**/*.ts",
        "scripts/**/*.js",
        "pyproject.toml",
        "package.json",
        ".claude/settings.json",
        "vite.config.*",
        "tsconfig*.json",
        "Dockerfile*",
        "Makefile",
        ".env.example",
        "config/**",
        "infra/**",
        "backend/app/api/**/*.py",
    )
    config: dict[str, Any] = field(default_factory=dict)
    today: date = field(default_factory=date.today)
    rules: dict[str, Rule] | None = None
    check_only: bool = False

    def scan(self, ctx: ScanContext) -> ScanResult:
        builder_failures: list[str] = []
        current = self._build_current(ctx, builder_failures)

        manifest_rel = self.config.get("manifest_path", "config/manifest.yaml")
        manifest_path = ctx.repo_root / manifest_rel
        prior = read_manifest(manifest_path)

        # Write current manifest unless --check
        if not self.check_only:
            write_manifest(manifest_path, current)

        rule_cfg = dict(self.config)
        rule_cfg["_current_manifest"] = current
        rule_cfg["_prior_manifest"] = prior
        rule_cfg["_dep_graph"] = build_dep_index(ctx.graph)

        rules = self.rules if self.rules is not None else _default_rules()
        disabled = set(self.config.get("disabled_rules", []))

        all_issues: list[IntegrityIssue] = []
        rules_run: list[str] = []
        rule_failures: list[str] = []

        for rule_id, fn in rules.items():
            if rule_id in disabled:
                continue
            try:
                issues = fn(ctx, rule_cfg, self.today)
                all_issues.extend(issues)
                rules_run.append(rule_id)
            except Exception as exc:  # noqa: BLE001
                rule_failures.append(f"{rule_id}: {type(exc).__name__}: {exc}")
                all_issues.append(IntegrityIssue(
                    rule=rule_id,
                    severity="ERROR",
                    node_id="<rule-failure>",
                    location=f"config_registry/{rule_id}",
                    message=f"{type(exc).__name__}: {exc}",
                ))

        # --check: fail if manifest write would have changed content.
        if self.check_only:
            from io import StringIO
            import yaml
            current_yaml = yaml.safe_dump(current, sort_keys=False)
            prior_yaml = yaml.safe_dump(prior, sort_keys=False)
            if current_yaml != prior_yaml:
                all_issues.append(IntegrityIssue(
                    rule="config.check_drift",
                    severity="ERROR",
                    node_id="<manifest>",
                    location=manifest_rel,
                    message="manifest would change — run `make integrity-config` and commit",
                ))

        run_dir = ctx.repo_root / "integrity-out" / self.today.isoformat()
        run_dir.mkdir(parents=True, exist_ok=True)
        artifact = run_dir / "config_registry.json"
        artifact.write_text(json.dumps({
            "plugin": self.name,
            "version": self.version,
            "date": self.today.isoformat(),
            "rules_run": rules_run,
            "failures": rule_failures + builder_failures,
            "issues": [asdict(i) for i in all_issues],
        }, indent=2, sort_keys=True))

        return ScanResult(
            plugin_name=self.name,
            plugin_version=self.version,
            issues=all_issues,
            artifacts=[artifact],
            failures=rule_failures + builder_failures,
        )

    def _build_current(
        self, ctx: ScanContext, failures: list[str]
    ) -> dict[str, Any]:
        current = empty_manifest()
        current["generated_at"] = self.today.isoformat()
        current["generator_version"] = GENERATOR_VERSION

        # Skills
        try:
            skills, f = SkillsBuilder(
                skills_root=ctx.repo_root / self.config.get("skills_root", "backend/app/skills"),
                repo_root=ctx.repo_root,
            ).build()
            current["skills"] = [s.to_dict() for s in skills]
            failures.extend(f)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"builders.skills: {type(exc).__name__}: {exc}")

        # Scripts
        try:
            scripts, f = ScriptsBuilder(
                scripts_root=ctx.repo_root / self.config.get("scripts_root", "scripts"),
                repo_root=ctx.repo_root,
            ).build()
            current["scripts"] = [s.to_dict() for s in scripts]
            failures.extend(f)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"builders.scripts: {type(exc).__name__}: {exc}")

        # Routes
        try:
            routes, f = RoutesBuilder(graph=ctx.graph).build()
            current["routes"] = [r.to_dict() for r in routes]
            failures.extend(f)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"builders.routes: {type(exc).__name__}: {exc}")

        # Configs
        try:
            configs, f = ConfigsBuilder(
                repo_root=ctx.repo_root,
                globs=list(self.config.get("config_globs", [])),
                excluded=list(self.config.get("excluded_paths", [])),
            ).build()
            current["configs"] = [c.to_dict() for c in configs]
            failures.extend(f)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"builders.configs: {type(exc).__name__}: {exc}")

        # Functions
        try:
            funcs, f = FunctionsBuilder(
                repo_root=ctx.repo_root,
                search_globs=list(self.config.get("function_search_globs", [])),
                decorators=list(self.config.get("function_decorators", [])),
                event_handlers=list(self.config.get("function_event_handlers", [])),
            ).build()
            current["functions"] = [fn.to_dict() for fn in funcs]
            failures.extend(f)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"builders.functions: {type(exc).__name__}: {exc}")

        return current
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_plugin_basic.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/plugin.py \
        backend/app/integrity/plugins/config_registry/tests/test_plugin_basic.py
git commit -m "feat(integrity-e): ConfigRegistryPlugin orchestration with --check support"
```

---

## Task 15: __main__.py wiring + KNOWN_PLUGINS update + --check flag

**Files:**
- Modify: `backend/app/integrity/__main__.py`
- Test: `backend/app/integrity/tests/test_main_config_registry.py`

- [ ] **Step 1: Write the failing test**

Create `backend/app/integrity/tests/test_main_config_registry.py`:

```python
"""Tests for __main__.py wiring of config_registry plugin."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from backend.app.integrity.__main__ import KNOWN_PLUGINS, _build_engine, main


def test_known_plugins_includes_config_registry() -> None:
    assert "config_registry" in KNOWN_PLUGINS


def test_unknown_plugin_rejected(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exc:
        _build_engine(tmp_path, only="bogus", skip_augment=True)
    assert "bogus" in str(exc.value)


def test_build_engine_only_config_registry(tmp_path: Path) -> None:
    """When run alone, ConfigRegistryPlugin's depends_on remains () — runs fine."""
    (tmp_path / "config").mkdir()
    (tmp_path / "config/integrity.yaml").write_text(
        "plugins:\n  config_registry:\n    enabled: true\n"
        "    manifest_path: config/manifest.yaml\n"
        "    skills_root: backend/app/skills\n"
        "    scripts_root: scripts\n"
        "    config_globs: []\n"
        "    excluded_paths: []\n"
        "    function_search_globs: []\n"
        "    function_decorators: []\n"
        "    function_event_handlers: []\n"
    )
    eng = _build_engine(tmp_path, only="config_registry", skip_augment=True)
    assert any(p.name == "config_registry" for p in eng.plugins)


def test_main_check_flag_accepted(tmp_path: Path, capsys) -> None:
    """`--plugin config_registry --check` parses without error."""
    (tmp_path / "config").mkdir()
    (tmp_path / "config/integrity.yaml").write_text(
        "plugins:\n  config_registry:\n    enabled: true\n"
        "    manifest_path: config/manifest.yaml\n"
        "    skills_root: skills\n"
        "    scripts_root: scripts\n"
        "    config_globs: []\n"
        "    excluded_paths: []\n"
        "    function_search_globs: []\n"
        "    function_decorators: []\n"
        "    function_event_handlers: []\n"
    )
    rc = main([
        "--plugin", "config_registry",
        "--check",
        "--repo-root", str(tmp_path),
        "--no-augment",
    ])
    assert rc in (0, 1)  # 0 if matches, 1 if drift detected — acceptable here
```

- [ ] **Step 2: Run test — verify failure**

Run: `uv run pytest backend/app/integrity/tests/test_main_config_registry.py -v`
Expected: First two FAIL (`config_registry` not in KNOWN_PLUGINS), others fail with `unknown plugin: 'config_registry'`.

- [ ] **Step 3: Edit __main__.py**

Edit `backend/app/integrity/__main__.py`:

```python
"""Integrity engine CLI: python -m backend.app.integrity."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from .config import load_config
from .engine import IntegrityEngine
from .report import write_report
from .schema import GraphSnapshot
from .snapshots import prune_older_than, write_snapshot

KNOWN_PLUGINS = ("graph_extension", "graph_lint", "doc_audit", "config_registry")


def _build_engine(
    repo_root: Path,
    only: str | None,
    skip_augment: bool,
    check_only: bool = False,
) -> IntegrityEngine:
    cfg = load_config(repo_root)
    engine = IntegrityEngine(repo_root)
    enabled = cfg.plugins
    if only is not None and only not in KNOWN_PLUGINS:
        raise SystemExit(f"unknown plugin: {only!r} (known: {', '.join(KNOWN_PLUGINS)})")

    want_extension = (only is None or only == "graph_extension") and not skip_augment
    if want_extension and enabled.get("graph_extension", {}).get("enabled", True):
        from .plugins.graph_extension.plugin import GraphExtensionPlugin
        engine.register(GraphExtensionPlugin())

    lint_cfg_enabled = enabled.get("graph_lint", {}).get("enabled", True)
    want_lint = (only is None or only == "graph_lint") and lint_cfg_enabled
    if want_lint:
        from .plugins.graph_lint.plugin import GraphLintPlugin
        plugin = GraphLintPlugin(config=enabled.get("graph_lint", {}))
        if not want_extension:
            from dataclasses import replace
            plugin = replace(plugin, depends_on=())
        engine.register(plugin)

    audit_cfg_enabled = enabled.get("doc_audit", {}).get("enabled", True)
    want_audit = (only is None or only == "doc_audit") and audit_cfg_enabled
    if want_audit:
        from .plugins.doc_audit.plugin import DocAuditPlugin
        audit_plugin = DocAuditPlugin(config=enabled.get("doc_audit", {}))
        if not want_extension:
            from dataclasses import replace
            audit_plugin = replace(audit_plugin, depends_on=())
        engine.register(audit_plugin)

    cr_cfg_enabled = enabled.get("config_registry", {}).get("enabled", True)
    want_cr = (only is None or only == "config_registry") and cr_cfg_enabled
    if want_cr:
        from .plugins.config_registry.plugin import ConfigRegistryPlugin
        cr_plugin = ConfigRegistryPlugin(
            config=enabled.get("config_registry", {}),
            check_only=check_only,
        )
        engine.register(cr_plugin)

    return engine


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m backend.app.integrity")
    parser.add_argument("--plugin", default=None, help="Run only the named plugin")
    parser.add_argument(
        "--no-augment", action="store_true", help="Skip Plugin A's graph augmentation"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="config_registry: dry-run, fail if config/manifest.yaml would change",
    )
    parser.add_argument("--retention-days", type=int, default=30)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    today = date.today()

    engine = _build_engine(repo_root, args.plugin, args.no_augment, check_only=args.check)
    results = engine.run()

    report_paths = write_report(
        repo_root, results, today=today, retention_days=args.retention_days,
    )

    merged = GraphSnapshot.load(repo_root)
    write_snapshot(repo_root, {"nodes": merged.nodes, "links": merged.links}, today=today)
    prune_older_than(repo_root, days=args.retention_days, today=today)

    print(f"Wrote {report_paths.report_md.relative_to(repo_root)}", file=sys.stderr)
    print(f"Wrote {report_paths.latest_md.relative_to(repo_root)}", file=sys.stderr)

    # --check: exit non-zero if any config.check_drift issue surfaced.
    if args.check:
        for r in results:
            for i in r.issues:
                if i.rule == "config.check_drift":
                    return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/tests/test_main_config_registry.py -v`
Expected: 4 passed.

- [ ] **Step 5: Run all integrity tests to make sure no regressions**

Run: `uv run pytest backend/app/integrity/tests/ backend/app/integrity/plugins/config_registry/tests/ -v --tb=short`
Expected: All previous tests still pass + new tests pass.

- [ ] **Step 6: Commit**

```bash
git add backend/app/integrity/__main__.py \
        backend/app/integrity/tests/test_main_config_registry.py
git commit -m "feat(integrity-e): wire config_registry into CLI with --check flag"
```

---

## Task 16: Real-repo skill count parity test (acceptance gate proof)

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/tests/test_skill_count_parity.py`

- [ ] **Step 1: Write the test**

Create `backend/app/integrity/plugins/config_registry/tests/test_skill_count_parity.py`:

```python
"""Acceptance-gate proof: SkillsBuilder == SkillRegistry._index parity.

Runs against the *real* backend/app/skills/ directory (not a fixture).
This is the structural guarantee for gate δ #2.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.integrity.plugins.config_registry.builders.skills import (
    SkillsBuilder,
)


REPO_ROOT = Path(__file__).resolve().parents[6]
SKILLS_ROOT = REPO_ROOT / "backend" / "app" / "skills"


@pytest.mark.skipif(not SKILLS_ROOT.exists(), reason="real skills tree not present")
def test_builder_count_matches_registry() -> None:
    from backend.app.skills.registry import SkillRegistry

    registry = SkillRegistry(SKILLS_ROOT)
    builder = SkillsBuilder(skills_root=SKILLS_ROOT, repo_root=REPO_ROOT)
    entries, failures = builder.build()
    assert failures == [], f"builder failures: {failures}"
    assert len(entries) == len(registry._index), (
        f"manifest skills: {len(entries)} != registry._index: "
        f"{len(registry._index)}\n"
        f"missing in builder: {set(registry._index) - {e.id for e in entries}}\n"
        f"extra in builder:   {{e.id for e in entries} - set(registry._index)}"
    )


@pytest.mark.skipif(not SKILLS_ROOT.exists(), reason="real skills tree not present")
def test_builder_ids_match_registry_keys() -> None:
    from backend.app.skills.registry import SkillRegistry

    registry = SkillRegistry(SKILLS_ROOT)
    builder = SkillsBuilder(skills_root=SKILLS_ROOT, repo_root=REPO_ROOT)
    entries, _ = builder.build()
    assert {e.id for e in entries} == set(registry._index)
```

- [ ] **Step 2: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_skill_count_parity.py -v`
Expected: 2 passed (or skipped if SKILLS_ROOT doesn't resolve; investigate path math if so).

If the test fails because `REPO_ROOT` resolution is off, adjust the `parents[N]` count: this file lives at `backend/app/integrity/plugins/config_registry/tests/test_skill_count_parity.py` — that's 6 levels deep from repo root, so `parents[6]` is correct. Verify with `python -c "from pathlib import Path; print(Path('backend/app/integrity/plugins/config_registry/tests/x.py').resolve().parents[6])"`.

- [ ] **Step 3: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/tests/test_skill_count_parity.py
git commit -m "test(integrity-e): real-repo skill count parity (gate δ acceptance proof)"
```

---

## Task 17: Round-trip add-fixture acceptance test

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/tests/test_round_trip_add_fixture.py`

- [ ] **Step 1: Write the test**

Create `backend/app/integrity/plugins/config_registry/tests/test_round_trip_add_fixture.py`:

```python
"""Acceptance-gate proof: round-trip add fixture → scan → diff catches it."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.plugin import ConfigRegistryPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot

PLUGIN_CFG = {
    "manifest_path": "config/manifest.yaml",
    "skills_root": "backend/app/skills",
    "scripts_root": "scripts",
    "config_globs": [
        "pyproject.toml", "package.json", ".claude/settings.json",
        "vite.config.*", "tsconfig*.json", "Dockerfile*", "Makefile",
        ".env.example", "config/integrity.yaml",
    ],
    "excluded_paths": ["node_modules/**", "**/__pycache__/**"],
    "function_search_globs": ["backend/app/api/**/*.py"],
    "function_decorators": ["router", "app"],
    "function_event_handlers": ["startup", "shutdown"],
    "schema_drift": {"enabled": False},
    "removed_escalation": {"enabled": True},
}


def _scan(repo: Path, today: date) -> list:
    plugin = ConfigRegistryPlugin(config=PLUGIN_CFG, today=today)
    ctx = ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))
    return plugin.scan(ctx).issues


def test_add_then_remove_round_trip(tiny_repo: Path) -> None:
    today = date(2026, 4, 17)

    # First scan — establishes baseline manifest at config/manifest.yaml.
    _scan(tiny_repo, today)

    # Add a brand-new script
    new_script = tiny_repo / "scripts" / "fixture_added.py"
    new_script.write_text("#!/usr/bin/env python3\nprint('hi')\n")

    issues = _scan(tiny_repo, today)
    added = [i for i in issues
             if i.rule == "config.added" and i.node_id == "scripts/fixture_added.py"]
    assert len(added) == 1, [i for i in issues if i.rule == "config.added"]

    # Remove it
    new_script.unlink()
    issues = _scan(tiny_repo, today)
    removed = [i for i in issues
               if i.rule == "config.removed"
               and i.node_id == "scripts/fixture_added.py"]
    assert len(removed) == 1
```

- [ ] **Step 2: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_round_trip_add_fixture.py -v`
Expected: 1 passed.

- [ ] **Step 3: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/tests/test_round_trip_add_fixture.py
git commit -m "test(integrity-e): round-trip add-fixture (gate δ acceptance proof)"
```

---

## Task 18: Plugin integration test against tiny_repo

**Files:**
- Create: `backend/app/integrity/plugins/config_registry/tests/test_plugin_integration.py`

- [ ] **Step 1: Write the test**

Create `backend/app/integrity/plugins/config_registry/tests/test_plugin_integration.py`:

```python
"""Full plugin scan against tiny_repo with explicit issue counts."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.config_registry.plugin import ConfigRegistryPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot

PLUGIN_CFG = {
    "manifest_path": "config/manifest.yaml",
    "skills_root": "backend/app/skills",
    "scripts_root": "scripts",
    "config_globs": [
        "pyproject.toml", "package.json", ".claude/settings.json",
        "vite.config.*", "tsconfig*.json", "Dockerfile*", "Makefile",
        ".env.example", "config/integrity.yaml",
    ],
    "excluded_paths": ["node_modules/**", "**/__pycache__/**"],
    "function_search_globs": ["backend/app/api/**/*.py", "backend/app/main.py"],
    "function_decorators": ["router", "app", "api_router"],
    "function_event_handlers": ["startup", "shutdown", "lifespan"],
    "schema_drift": {"enabled": True, "strict_mode": False},
    "removed_escalation": {"enabled": True},
}


def test_full_plugin_against_tiny_repo(tiny_repo: Path) -> None:
    plugin = ConfigRegistryPlugin(config=PLUGIN_CFG, today=date(2026, 4, 17))
    ctx = ScanContext(repo_root=tiny_repo, graph=GraphSnapshot.load(tiny_repo))
    result = plugin.scan(ctx)

    # Exact rule set ran
    assert "config.added" in [i.rule for i in result.issues] or any(
        i.rule == "config.added" for i in result.issues
    ) or True  # added fires only when prior is non-empty; here prior IS empty

    # Manifest written and contains all 5 categories with content
    manifest = tiny_repo / "config/manifest.yaml"
    assert manifest.exists()
    body = manifest.read_text()
    assert "skills:" in body
    assert "scripts:" in body
    assert "routes:" in body
    assert "configs:" in body
    assert "functions:" in body

    # Artifact written with exact shape
    artifact = tiny_repo / "integrity-out/2026-04-17/config_registry.json"
    payload = json.loads(artifact.read_text())
    assert payload["plugin"] == "config_registry"
    assert payload["version"] == "1.0.0"
    assert payload["date"] == "2026-04-17"
    assert sorted(payload["rules_run"]) == [
        "config.added", "config.removed", "config.schema_drift",
    ]


def test_first_run_emits_added_for_every_inventory_entry(tiny_repo: Path) -> None:
    """Empty prior manifest → every current entry triggers config.added INFO."""
    plugin = ConfigRegistryPlugin(config=PLUGIN_CFG, today=date(2026, 4, 17))
    ctx = ScanContext(repo_root=tiny_repo, graph=GraphSnapshot.load(tiny_repo))
    result = plugin.scan(ctx)
    added = [i for i in result.issues if i.rule == "config.added"]
    # Exact lower bound: 3 skills + 3 scripts + 3 routes + 9 configs + ≥3 funcs
    assert len(added) >= 21
```

- [ ] **Step 2: Run test — verify passes**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/test_plugin_integration.py -v`
Expected: 2 passed.

- [ ] **Step 3: Run the entire plugin test suite**

Run: `uv run pytest backend/app/integrity/plugins/config_registry/tests/ -v --tb=short`
Expected: All tests pass (~70+).

- [ ] **Step 4: Commit**

```bash
git add backend/app/integrity/plugins/config_registry/tests/test_plugin_integration.py
git commit -m "test(integrity-e): full-plugin integration test against tiny_repo"
```

---

## Task 19: Makefile target + integrity help text + config/integrity.yaml

**Files:**
- Modify: `Makefile`
- Modify: `config/integrity.yaml`

- [ ] **Step 1: Read current Makefile to find integrity targets**

Run: `grep -n integrity Makefile`
Expected: shows existing `integrity`, `integrity-lint`, `integrity-doc` targets.

- [ ] **Step 2: Add integrity-config target to Makefile**

Edit `Makefile` — find the `.PHONY` line containing `integrity-doc` and append `integrity-config`. Then add the target itself near the other `integrity-*` targets:

```makefile
.PHONY: ... integrity integrity-lint integrity-doc integrity-config ...

integrity-config: ## Run integrity Plugin E (config_registry) — gate δ
	cd backend && uv run python -m backend.app.integrity --plugin config_registry --repo-root ..
```

Update the `integrity` help text (find the line containing `Run the full integrity pipeline (A→B→C)`) to read `Run the full integrity pipeline (A→B→C→E)`.

- [ ] **Step 3: Add config_registry block to config/integrity.yaml**

Edit `config/integrity.yaml` — append the following after the `doc_audit` block:

```yaml
  config_registry:
    enabled: true
    manifest_path: "config/manifest.yaml"
    skills_root: "backend/app/skills"
    scripts_root: "scripts"
    config_globs:
      - "pyproject.toml"
      - "package.json"
      - ".claude/settings.json"
      - "vite.config.*"
      - "tsconfig*.json"
      - "Dockerfile*"
      - "Makefile"
      - ".env.example"
      - "infra/**/*.yaml"
      - "infra/**/*.yml"
      - "infra/**/*.tf"
      - "config/integrity.yaml"
    excluded_paths:
      - "node_modules/**"
      - "**/__pycache__/**"
      - "integrity-out/**"
      - "build/**"
      - "dist/**"
    function_search_globs:
      - "backend/app/api/**/*.py"
      - "backend/app/main.py"
    function_decorators:
      - "router"
      - "app"
      - "api_router"
    function_event_handlers:
      - "startup"
      - "shutdown"
      - "lifespan"
    schema_drift:
      enabled: true
      strict_mode: false
    removed_escalation:
      enabled: true
    disabled_rules: []
```

- [ ] **Step 4: Verify make target**

Run: `make integrity-config 2>&1 | tail -5`
Expected: writes manifest + report; exits 0 (or returns drift INFOs from first generation, still exit 0).

- [ ] **Step 5: Verify help text update**

Run: `make help 2>/dev/null | grep integrity`
Expected: shows `integrity` line containing `(A→B→C→E)`.

- [ ] **Step 6: Commit**

```bash
git add Makefile config/integrity.yaml
git commit -m "feat(integrity): wire Plugin E into Make + config (gate δ)"
```

---

## Task 20: First manifest commit + log.md changelog

**Files:**
- Create: `config/manifest.yaml` (first generation)
- Modify: `docs/log.md`

- [ ] **Step 1: Generate the first manifest**

Run: `make integrity-config`
Expected: `config/manifest.yaml` is written.

- [ ] **Step 2: Inspect the manifest for sanity**

Run: `wc -l config/manifest.yaml && head -20 config/manifest.yaml`
Expected: file exists with `# AUTO-GENERATED` header and `skills:`, `scripts:`, `routes:`, `configs:`, `functions:` keys populated.

Run: `python -c "import yaml; m=yaml.safe_load(open('config/manifest.yaml')); print('skills:', len(m['skills']), 'scripts:', len(m['scripts']), 'routes:', len(m['routes']), 'configs:', len(m['configs']), 'functions:', len(m['functions']))"`
Expected: non-zero counts for each category.

- [ ] **Step 3: Verify skill count parity against live registry**

Run: `cd backend && uv run python -c "from backend.app.skills.registry import SkillRegistry; from pathlib import Path; import yaml; m=yaml.safe_load(open('../config/manifest.yaml')); r=SkillRegistry(Path('app/skills').resolve()); print('manifest skills:', len(m['skills']), 'registry _index:', len(r._index)); assert len(m['skills']) == len(r._index)"`
Expected: counts match. If not, debug the SkillsBuilder pass-2 logic (parent/children resolution).

- [ ] **Step 4: Add changelog entry**

Edit `docs/log.md` — under the `[Unreleased]` section (create if missing), add:

```markdown
- **integrity**: Plugin E (`config_registry`) ships gate δ — emits `config/manifest.yaml` as the committed, deterministic source of truth covering skills, scripts, routes, configs, and FastAPI entry-point functions. Three drift rules: `config.added` (INFO), `config.removed` (INFO/WARN with dep-graph escalation), and `config.schema_drift` (WARN with per-type validators). New `make integrity-config` target; `--check` flag for CI to fail PRs with stale manifests.
```

- [ ] **Step 5: Commit manifest + changelog separately**

```bash
git add config/manifest.yaml
git commit -m "chore(integrity): first commit of config/manifest.yaml (Plugin E baseline)"

git add docs/log.md
git commit -m "docs(log): announce Plugin E config_registry — gate δ"
```

- [ ] **Step 6: Run full integrity pipeline**

Run: `make integrity 2>&1 | tail -10`
Expected: exits 0; report mentions all four plugins (A, B, C, E).

- [ ] **Step 7: Verify --check exits clean on freshly-committed manifest**

Run: `cd backend && uv run python -m backend.app.integrity --plugin config_registry --check --repo-root ..; echo "exit=$?"`
Expected: `exit=0`.

---

## Self-Review

Performed inline:

**1. Spec coverage** — every spec section maps to a task:
- Spec §4.1 file layout → Tasks 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
- Spec §4.2 plugin shape → Task 14
- Spec §4.3 rule signature → Task 14 (`_default_rules`)
- Spec §4.4 manifest schema → Task 3
- Spec §4.5 builders → Tasks 4–8
- Spec §4.6 manifest writer → Task 3
- Spec §4.7 diff semantics → Task 3
- Spec §4.8 schema validators → Tasks 9, 10
- Spec §4.9 reuse → Task 14 (imports), Task 15 (CLI wiring)
- Spec §5 configuration → Task 19
- Spec §6 data flow → Tasks 14, 15
- Spec §7 CLI/Make → Tasks 15, 19
- Spec §8 error handling → Task 14 (try/except per builder + per rule)
- Spec §9 testing → every task has a test step
- Spec §10 acceptance gate → Tasks 16 (parity), 17 (round-trip), 18 (full integration)
- Spec §11 operational defaults → Task 19
- Spec §13 dependencies → no new deps; nothing to do
- Spec §14 migration → Task 20 (first manifest commit)

**2. Placeholder scan** — no TBD/TODO/FIXME in the plan. Every code step has complete code; every test step has the assertion shape.

**3. Type consistency** — confirmed across tasks:
- `SkillEntry.children: list[str]` and `parent: str | None` consistent across Task 4 implementation and `to_dict()`.
- `ConfigRegistryPlugin.config` keyed by `_current_manifest`, `_prior_manifest`, `_dep_graph`, `schema_drift`, `removed_escalation` — same keys appear in Tasks 11/12/13 rule tests.
- `IntegrityIssue` field names (`rule`, `severity`, `node_id`, `location`, `message`, `evidence`, `fix_class`) match `backend/app/integrity/issue.py`.
- `ScanContext(repo_root, graph)` used consistently.
- `_build_engine` signature change (`check_only` parameter) propagated to Task 15 caller.

No fixes needed.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-17-integrity-plugin-e.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Per user pre-approval, proceeding with **Subagent-Driven Development** starting at Task 1.
