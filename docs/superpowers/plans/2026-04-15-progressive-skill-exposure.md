# Progressive Skill Exposure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the skill system from a flat catalog to a progressive, hierarchical exposure model where the agent discovers sub-skills by loading parent skills — reducing per-turn token cost by ~65% and making the skill space navigable.

**Architecture:** The registry builds a `SkillNode` tree from nested directories at startup. The system prompt shows only Level 1 skills with `[N sub-skills]` annotations on hubs. Loading a skill auto-appends its sub-skill catalog (system-generated). The sandbox bootstrap is generated dynamically from the tree. `references/` directories are removed — reference material becomes Level 3 SKILL.md files.

**Tech Stack:** Python 3.12+, pytest, dataclasses, pathlib, PyYAML

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Modify | `backend/app/skills/base.py` | Remove `level` from `SkillMetadata`; add `SkillNode` dataclass |
| Modify | `backend/app/skills/registry.py` | Recursive discovery; `SkillNode` tree; new API methods |
| Modify | `backend/app/harness/skill_tools.py` | New response format (sub-skill catalog, breadcrumb); remove `references` |
| Modify | `backend/app/harness/injector.py` | Level-1-only catalog; `[N sub-skills]` annotation; update Protocol |
| Modify | `backend/app/harness/sandbox_bootstrap.py` | Dynamic bootstrap via registry |
| Modify | `backend/tests/unit/test_skill_registry_frontmatter.py` | Update for new registry API |
| Modify | `backend/tests/unit/test_skill_tool.py` | Remove `level`/`references` assertions; add hub/breadcrumb tests |
| Create | `backend/app/skills/statistical_analysis/SKILL.md` | Hub guidance for stat skills |
| Create | `backend/app/skills/charting/SKILL.md` | Hub guidance for chart skills |
| Create | `backend/app/skills/reporting/SKILL.md` | Hub guidance for reporting skills |
| git mv | `correlation/` → `statistical_analysis/correlation/` | Hierarchy migration |
| git mv | `distribution_fit/` → `statistical_analysis/distribution_fit/` | Hierarchy migration |
| git mv | `group_compare/` → `statistical_analysis/group_compare/` | Hierarchy migration |
| git mv | `stat_validate/` → `statistical_analysis/stat_validate/` | Hierarchy migration |
| git mv | `time_series/` → `statistical_analysis/time_series/` | Hierarchy migration |
| git mv | `altair_charts/` → `charting/altair_charts/` | Hierarchy migration |
| git mv | `report_builder/` → `reporting/report_builder/` | Hierarchy migration |
| git mv | `dashboard_builder/` → `reporting/dashboard_builder/` | Hierarchy migration |
| git mv | `html_tables/` → `reporting/html_tables/` | Hierarchy migration |
| Modify | `backend/app/harness/skill_tools.py` | Update import paths after git mv |
| Modify | `Makefile` | Update `skill-new` target |
| Modify | `docs/skill-creation.md` | Full rewrite for hierarchical model |
| Create | `docs/progressive-skill-exposure.md` | Mental model documentation |
| Modify | `prompts/data_scientist.md` | Update skill menu section |
| Modify | `CLAUDE.md` | Update architecture section |

---

### Task 1: Update SkillMetadata and add SkillNode to base.py

**Files:**
- Modify: `backend/app/skills/base.py`
- Modify: `backend/tests/unit/test_skill_registry_frontmatter.py` (remove `level` assertion)
- Modify: `backend/tests/unit/test_skill_base.py` (add SkillNode test)

- [ ] **Step 1: Write the failing tests**

Add to `backend/tests/unit/test_skill_base.py`:

```python
from app.skills.base import SkillError, SkillResult, SkillMetadata, SkillNode
from pathlib import Path


def test_skill_metadata_has_no_level_field() -> None:
    meta = SkillMetadata(name="foo", version="0.1", description="bar")
    assert not hasattr(meta, "level")


def test_skill_node_constructs_correctly() -> None:
    meta = SkillMetadata(name="foo", version="0.1", description="bar")
    node = SkillNode(
        metadata=meta,
        instructions="# Foo\n\nDo foo.",
        package_path=Path("/skills/foo/pkg"),
        depth=1,
        parent=None,
    )
    assert node.metadata.name == "foo"
    assert node.depth == 1
    assert node.parent is None
    assert node.children == []


def test_skill_node_child_relationship() -> None:
    parent_meta = SkillMetadata(name="hub", version="0.1", description="hub")
    child_meta = SkillMetadata(name="leaf", version="0.1", description="leaf")
    parent = SkillNode(
        metadata=parent_meta, instructions="", package_path=None, depth=1, parent=None
    )
    child = SkillNode(
        metadata=child_meta, instructions="", package_path=None, depth=2, parent=parent
    )
    parent.children.append(child)
    assert len(parent.children) == 1
    assert parent.children[0].metadata.name == "leaf"
    assert child.parent is parent
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_base.py -v 2>&1 | tail -20
```

Expected: ImportError or AttributeError — `SkillNode` not defined, `level` still present.

- [ ] **Step 3: Update base.py**

Replace `backend/app/skills/base.py` entirely:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class SkillError(Exception):
    """Actionable error with template-based formatting."""

    def __init__(
        self,
        code: str,
        context: dict[str, Any],
        templates: dict[str, dict[str, str]] | None = None,
    ) -> None:
        self.code = code
        self.context = context
        self.templates = templates or {}
        super().__init__(self.format())

    def format(self) -> str:
        template = self.templates.get(self.code)
        if template is None:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.code}: {context_str}"
        parts: list[str] = []
        for key in ("message", "guidance", "recovery"):
            raw = template.get(key, "")
            if raw:
                try:
                    parts.append(raw.format(**self.context))
                except KeyError:
                    parts.append(raw)
        return "\n".join(parts)


@dataclass(frozen=True)
class SkillResult:
    """Return type for all skill function executions."""

    data: Any = None
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class SkillMetadata:
    """Parsed metadata from SKILL.md frontmatter and skill.yaml.

    ``level`` has been removed — depth is computed from directory position
    by SkillRegistry and stored on SkillNode, never authored in frontmatter.
    """

    name: str
    version: str
    description: str
    dependencies_requires: list[str] = field(default_factory=list)
    dependencies_used_by: list[str] = field(default_factory=list)
    dependencies_packages: list[str] = field(default_factory=list)
    error_templates: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class SkillNode:
    """A node in the skill hierarchy tree.

    Built by SkillRegistry.discover(). Not frozen — children list is
    populated incrementally during recursive discovery.

    depth: 1 = Level 1 (root), 2 = Level 2 (sub-skill), etc.
    parent: None for Level 1 skills.
    children: empty list for leaf skills.
    package_path: path to pkg/ directory, or None if the skill has no Python package.
    """

    metadata: SkillMetadata
    instructions: str
    package_path: Path | None
    depth: int
    parent: SkillNode | None
    children: list[SkillNode] = field(default_factory=list)
```

- [ ] **Step 4: Remove `level` assertion from the registry frontmatter test**

In `backend/tests/unit/test_skill_registry_frontmatter.py`, find and remove the line:
```python
assert loaded.metadata.level == 2
```

Also remove `level: 2` from the SKILL.md content written in the fixture (the `"level: 2\n"` line in `test_registry_reads_metadata_from_skill_md_frontmatter`).

The fixture SKILL.md becomes:
```python
(skill_dir / "SKILL.md").write_text(
    "---\n"
    "name: demo\n"
    "description: Minimal demo skill.\n"
    "version: '0.3'\n"
    "---\n"
    "# Demo\n\nBody text.\n"
)
```

- [ ] **Step 5: Run all tests to verify they pass**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_base.py tests/unit/test_skill_registry_frontmatter.py -v 2>&1 | tail -30
```

Expected: All tests pass. (Registry tests may fail since registry still parses `level` — that's fine, fixed in Task 2.)

- [ ] **Step 6: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/skills/base.py backend/tests/unit/test_skill_base.py backend/tests/unit/test_skill_registry_frontmatter.py
git commit -m "refactor: remove level from SkillMetadata, add SkillNode dataclass"
```

---

### Task 2: Rewrite SkillRegistry with recursive discovery

**Files:**
- Modify: `backend/app/skills/registry.py`
- Modify: `backend/tests/unit/test_skill_registry_frontmatter.py`

- [ ] **Step 1: Write the failing tests**

Replace the contents of `backend/tests/unit/test_skill_registry_frontmatter.py` with:

```python
from __future__ import annotations

from pathlib import Path

import pytest

from app.skills.registry import SkillRegistry


def _write_skill(
    root: Path,
    name: str,
    *,
    description: str = "A skill.",
    version: str = "0.1",
    has_pkg: bool = False,
) -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\nversion: '{version}'\n---\n# {name}\n\nBody.\n"
    )
    (skill_dir / "skill.yaml").write_text(
        "dependencies:\n  requires: []\n  used_by: []\n  packages: []\nerrors: {}\n"
    )
    if has_pkg:
        pkg = skill_dir / "pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
    return skill_dir


# ── Flat discovery (backward compat) ─────────────────────────────────────────

def test_registry_discovers_flat_skill(tmp_path: Path) -> None:
    _write_skill(tmp_path, "alpha")
    registry = SkillRegistry(tmp_path)
    registry.discover()
    assert registry.get_skill("alpha") is not None


def test_registry_reads_frontmatter(tmp_path: Path) -> None:
    _write_skill(tmp_path, "demo", description="Minimal demo skill.", version="0.3")
    (tmp_path / "demo" / "skill.yaml").write_text(
        "dependencies:\n"
        "  requires: [theme_config]\n"
        "  used_by: []\n"
        "  packages: [pandas]\n"
        "errors:\n"
        "  BAD_INPUT:\n"
        "    message: bad input {field}\n"
        "    guidance: provide {field}\n"
        "    recovery: supply the value and rerun\n"
    )
    registry = SkillRegistry(tmp_path)
    registry.discover()

    node = registry.get_skill("demo")
    assert node is not None
    assert node.metadata.name == "demo"
    assert node.metadata.description == "Minimal demo skill."
    assert node.metadata.version == "0.3"
    assert node.metadata.dependencies_requires == ["theme_config"]
    assert node.metadata.dependencies_packages == ["pandas"]
    assert "BAD_INPUT" in node.metadata.error_templates
    assert not hasattr(node.metadata, "level")


def test_registry_body_excludes_frontmatter(tmp_path: Path) -> None:
    _write_skill(tmp_path, "demo")
    registry = SkillRegistry(tmp_path)
    registry.discover()
    node = registry.get_skill("demo")
    assert node.instructions.startswith("# demo")
    assert "---" not in node.instructions.splitlines()[0]


def test_registry_ignores_dir_without_skill_md(tmp_path: Path) -> None:
    (tmp_path / "nope").mkdir()
    registry = SkillRegistry(tmp_path)
    registry.discover()
    assert registry.list_top_level() == []


def test_registry_skips_skill_with_invalid_yaml(tmp_path: Path) -> None:
    broken = tmp_path / "broken"
    broken.mkdir()
    (broken / "SKILL.md").write_text(
        "---\nname: broken\ndescription: bad\n  indent: wrong\n---\nbody\n"
    )
    _write_skill(tmp_path, "good")
    registry = SkillRegistry(tmp_path)
    registry.discover()
    assert registry.get_skill("broken") is None
    assert registry.get_skill("good") is not None


# ── Hierarchy ─────────────────────────────────────────────────────────────────

def _make_hierarchy(tmp_path: Path) -> SkillRegistry:
    """
    hub/
      SKILL.md
      child_a/
        SKILL.md
        grandchild/
          SKILL.md
      child_b/
        SKILL.md
    standalone/
      SKILL.md
    """
    _write_skill(tmp_path, "hub", description="Hub skill.")
    _write_skill(tmp_path / "hub", "child_a", description="Child A.")
    _write_skill(tmp_path / "hub" / "child_a", "grandchild", description="Grandchild.")
    _write_skill(tmp_path / "hub", "child_b", description="Child B.")
    _write_skill(tmp_path, "standalone", description="Standalone.")
    registry = SkillRegistry(tmp_path)
    registry.discover()
    return registry


def test_list_top_level_returns_only_roots(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    names = [n.metadata.name for n in registry.list_top_level()]
    assert set(names) == {"hub", "standalone"}


def test_get_children_returns_direct_children(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    children = registry.get_children("hub")
    names = {n.metadata.name for n in children}
    assert names == {"child_a", "child_b"}


def test_get_children_returns_empty_for_leaf(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    assert registry.get_children("standalone") == []
    assert registry.get_children("child_b") == []


def test_depth_is_computed_from_nesting(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    assert registry.get_skill("hub").depth == 1
    assert registry.get_skill("child_a").depth == 2
    assert registry.get_skill("grandchild").depth == 3
    assert registry.get_skill("standalone").depth == 1


def test_get_breadcrumb_root(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    assert registry.get_breadcrumb("hub") == ["hub"]


def test_get_breadcrumb_nested(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    assert registry.get_breadcrumb("grandchild") == ["hub", "child_a", "grandchild"]


def test_get_skill_permissive_access(tmp_path: Path) -> None:
    """Any skill at any depth is accessible by name directly."""
    registry = _make_hierarchy(tmp_path)
    assert registry.get_skill("grandchild") is not None
    assert registry.get_skill("child_a") is not None


def test_parent_references_set_correctly(tmp_path: Path) -> None:
    registry = _make_hierarchy(tmp_path)
    grandchild = registry.get_skill("grandchild")
    assert grandchild.parent.metadata.name == "child_a"
    assert grandchild.parent.parent.metadata.name == "hub"
    assert grandchild.parent.parent.parent is None


def test_pkg_excluded_from_discovery(tmp_path: Path) -> None:
    """pkg/ directory must never be discovered as a child skill."""
    _write_skill(tmp_path, "alpha", has_pkg=True)
    registry = SkillRegistry(tmp_path)
    registry.discover()
    alpha = registry.get_skill("alpha")
    assert alpha is not None
    assert alpha.children == []


def test_generate_bootstrap_imports_includes_pkg_skills(tmp_path: Path) -> None:
    _write_skill(tmp_path, "hub")
    _write_skill(tmp_path / "hub", "leaf_with_pkg", has_pkg=True)
    _write_skill(tmp_path / "hub", "leaf_no_pkg", has_pkg=False)
    registry = SkillRegistry(tmp_path)
    registry.discover()
    imports = registry.generate_bootstrap_imports()
    combined = "\n".join(imports)
    assert "leaf_with_pkg" in combined
    assert "leaf_no_pkg" not in combined
```

- [ ] **Step 2: Run to verify the new tests fail**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_registry_frontmatter.py -v 2>&1 | tail -30
```

Expected: Multiple failures — `list_top_level`, `get_children`, `get_breadcrumb` not defined.

- [ ] **Step 3: Rewrite registry.py**

Replace `backend/app/skills/registry.py` entirely:

```python
from __future__ import annotations

from pathlib import Path

import yaml

from app.skills.base import SkillMetadata, SkillNode


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a SKILL.md file into (frontmatter_dict, body)."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(
            i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        return {}, text
    raw = "".join(lines[1:end])
    body = "".join(lines[end + 1 :]).lstrip("\n")
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {}, text
    if not isinstance(parsed, dict):
        return {}, body
    return parsed, body


# Directories inside a skill dir that are never child skills.
_SKIP_DIRS = frozenset({"pkg", "tests", "evals", "__pycache__", ".git"})


class SkillRegistry:
    """Discovers and loads skills from a nested directory tree.

    Parent-child relationships are encoded purely by filesystem nesting:
    a directory with a SKILL.md that contains other directories with
    SKILL.md files is a hub skill. Depth is computed from position in
    the tree (Level 1 = root, Level 2 = one nesting, etc.).

    Two structures are maintained simultaneously:
    - _roots: list of Level-1 SkillNodes (for catalog generation)
    - _index: flat dict[name → SkillNode] (for permissive direct access)
    """

    def __init__(self, skills_root: Path) -> None:
        self._root = skills_root
        self._roots: list[SkillNode] = []
        self._index: dict[str, SkillNode] = {}

    def discover(self) -> None:
        """Walk the skills directory recursively and build the tree."""
        self._roots.clear()
        self._index.clear()
        if not self._root.exists():
            return
        for skill_dir in sorted(self._root.iterdir()):
            if skill_dir.is_dir() and skill_dir.name not in _SKIP_DIRS:
                self._discover_recursive(skill_dir, parent=None, depth=1)

    def _discover_recursive(
        self, dir: Path, parent: SkillNode | None, depth: int
    ) -> None:
        skill_md = dir / "SKILL.md"
        if not skill_md.exists():
            return

        fm, body = _split_frontmatter(skill_md.read_text())
        name = fm.get("name")
        if not name:
            return

        skill_yaml = dir / "skill.yaml"
        deps: dict = {}
        errors: dict = {}
        if skill_yaml.exists():
            raw = yaml.safe_load(skill_yaml.read_text()) or {}
            deps = raw.get("dependencies", {}) or {}
            errors = raw.get("errors", {}) or {}

        metadata = SkillMetadata(
            name=name,
            version=str(fm.get("version", "0.0")),
            description=fm.get("description", ""),
            dependencies_requires=deps.get("requires", []),
            dependencies_used_by=deps.get("used_by", []),
            dependencies_packages=deps.get("packages", []),
            error_templates=errors,
        )

        pkg_path = dir / "pkg"
        node = SkillNode(
            metadata=metadata,
            instructions=body,
            package_path=pkg_path if pkg_path.exists() else None,
            depth=depth,
            parent=parent,
        )

        self._index[name] = node
        if parent is None:
            self._roots.append(node)
        else:
            parent.children.append(node)

        for subdir in sorted(dir.iterdir()):
            if subdir.is_dir() and subdir.name not in _SKIP_DIRS:
                self._discover_recursive(subdir, parent=node, depth=depth + 1)

    # ── Public API ────────────────────────────────────────────────────────────

    def list_top_level(self) -> list[SkillNode]:
        """Return Level-1 (root) skills only — used to build the system prompt catalog."""
        return list(self._roots)

    def get_skill(self, name: str) -> SkillNode | None:
        """Flat lookup by name — works for any skill at any depth."""
        return self._index.get(name)

    def get_children(self, name: str) -> list[SkillNode]:
        """Return direct children of a skill. Empty list for leaf skills."""
        node = self._index.get(name)
        return list(node.children) if node else []

    def get_breadcrumb(self, name: str) -> list[str]:
        """Return path from root to skill: ['statistical_analysis', 'correlation']."""
        node = self._index.get(name)
        if node is None:
            return []
        parts: list[str] = []
        current: SkillNode | None = node
        while current is not None:
            parts.append(current.metadata.name)
            current = current.parent
        return list(reversed(parts))

    def generate_bootstrap_imports(self) -> list[str]:
        """Auto-generate Python import lines for all skills that have a pkg/ directory.

        Each line is ``from <module_path> import *`` where module_path is
        computed from the skill directory's position relative to the backend root.
        The skill's pkg/__init__.py must define __all__ for selective exports.

        Example: skills/statistical_analysis/correlation/pkg →
                 from app.skills.statistical_analysis.correlation.pkg import *
        """
        backend_root = self._root.parent.parent  # backend/app/skills → backend/
        lines: list[str] = []
        for node in self._iter_all():
            if node.package_path is None:
                continue
            if not any(node.package_path.iterdir()):
                continue  # empty pkg/
            try:
                rel = node.package_path.relative_to(backend_root)
            except ValueError:
                continue
            module_path = ".".join(rel.parts)
            lines.append(f"from {module_path} import *  # {node.metadata.name}")
        return lines

    def _iter_all(self) -> list[SkillNode]:
        """BFS over all nodes in the tree."""
        result: list[SkillNode] = []
        queue = list(self._roots)
        while queue:
            node = queue.pop(0)
            result.append(node)
            queue.extend(node.children)
        return result

    # ── Backward-compat shims (used by manifest.py) ───────────────────────────

    def list_skills(self) -> list[str]:
        """Return all skill names at all depths. Used by manifest.py."""
        return list(self._index.keys())

    def get_instructions(self, name: str) -> str | None:
        node = self._index.get(name)
        return node.instructions if node else None

    def get_dependency_graph(self) -> dict[str, list[str]]:
        return {
            name: node.metadata.dependencies_requires
            for name, node in self._index.items()
        }
```

- [ ] **Step 4: Run the full registry test suite**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_registry_frontmatter.py -v 2>&1 | tail -40
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/skills/registry.py backend/tests/unit/test_skill_registry_frontmatter.py
git commit -m "refactor: rewrite SkillRegistry with recursive discovery and SkillNode tree"
```

---

### Task 3: Update skill_tools.py — new response format

The `_load_skill_body` handler gains: breadcrumb header, auto-appended sub-skill catalog, removed `level` and `references` from response.

**Files:**
- Modify: `backend/app/harness/skill_tools.py`
- Modify: `backend/tests/unit/test_skill_tool.py`

- [ ] **Step 1: Write the failing tests**

Replace `backend/tests/unit/test_skill_tool.py` with:

```python
"""Tests for the skill-loading tool with progressive exposure."""
from __future__ import annotations

from pathlib import Path

import pytest

from app.artifacts.store import ArtifactStore
from app.harness.dispatcher import ToolDispatcher, ToolCall
from app.harness.sandbox import SandboxExecutor
from app.harness.skill_tools import _closest_skill_names, register_core_tools
from app.skills.registry import SkillRegistry
from app.wiki.engine import WikiEngine


def _write_skill(
    root: Path,
    name: str,
    *,
    description: str = "A test skill.",
    body: str = "# Body\n\nContent.",
    has_pkg: bool = False,
) -> None:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\nversion: 1.2\ndescription: {description}\n---\n{body}"
    )
    (skill_dir / "skill.yaml").write_text(
        "dependencies:\n  requires: [foo]\n  packages: [pandas]\n"
        "errors:\n  BadInput:\n    hint: 'check your input'\n"
    )
    if has_pkg:
        pkg = skill_dir / "pkg"
        pkg.mkdir(exist_ok=True)
        (pkg / "__init__.py").write_text("")


def _build_dispatcher(tmp_path: Path) -> tuple[ToolDispatcher, SkillRegistry]:
    skills_root = tmp_path / "skills"
    skills_root.mkdir()

    # Hub: stat_hub with two children, one of which has a reference grandchild
    _write_skill(skills_root, "stat_hub", description="Statistical analysis hub.")
    _write_skill(
        skills_root / "stat_hub",
        "correlation",
        description="Runs correlation analysis.",
        has_pkg=True,
    )
    _write_skill(
        skills_root / "stat_hub" / "correlation",
        "corr_reference",
        description="[Reference] Mathematical details. Load only for algorithmic depth.",
    )
    _write_skill(
        skills_root / "stat_hub",
        "distribution",
        description="Fits distributions.",
    )
    # Standalone leaf
    _write_skill(skills_root, "sql_builder", description="Writes SQL queries.")

    registry = SkillRegistry(skills_root)
    registry.discover()

    wiki = WikiEngine(root=tmp_path / "wiki")
    (tmp_path / "wiki").mkdir(exist_ok=True)
    artifact_store = ArtifactStore(
        db_path=tmp_path / "artifacts.db",
        disk_root=tmp_path / "artifacts",
    )
    sandbox = SandboxExecutor(python_executable="/usr/bin/env python3")

    dispatcher = ToolDispatcher()
    register_core_tools(
        dispatcher=dispatcher,
        artifact_store=artifact_store,
        wiki=wiki,
        sandbox=sandbox,
        session_id="t-1",
        registry=registry,
    )
    return dispatcher, registry


def _call_skill(dispatcher: ToolDispatcher, name: str) -> dict:
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={"name": name}))
    assert result.ok, f"skill({name!r}) failed: {result.error_message}"
    return result.payload


# ── Response format ───────────────────────────────────────────────────────────

def test_hub_skill_body_and_metadata_returned(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "stat_hub")
    assert "Body" in payload["body"] or "stat_hub" in payload["body"]
    meta = payload["metadata"]
    assert meta["name"] == "stat_hub"
    assert meta["version"] == "1.2"
    assert meta["description"] == "Statistical analysis hub."
    assert "level" not in meta
    assert "references" not in payload


def test_hub_skill_appends_sub_skill_catalog(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "stat_hub")
    body = payload["body"]
    assert "## Sub-skills" in body
    assert "`correlation`" in body
    assert "Runs correlation analysis." in body
    assert "`distribution`" in body
    assert "Fits distributions." in body


def test_reference_skill_description_preserved_in_catalog(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "correlation")
    body = payload["body"]
    assert "## Sub-skills" in body
    assert "[Reference]" in body
    assert "`corr_reference`" in body


def test_nested_skill_shows_breadcrumb(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "correlation")
    body = payload["body"]
    assert "stat_hub" in body
    assert "›" in body  # breadcrumb separator


def test_leaf_skill_has_no_sub_skills_section(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "sql_builder")
    assert "## Sub-skills" not in payload["body"]


def test_level_1_skill_has_no_breadcrumb(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "sql_builder")
    assert "›" not in payload["body"]


def test_direct_access_to_level3_skill(tmp_path: Path) -> None:
    """Permissive access — agent can load any skill by name directly."""
    dispatcher, _ = _build_dispatcher(tmp_path)
    payload = _call_skill(dispatcher, "corr_reference")
    assert payload["metadata"]["name"] == "corr_reference"


def test_skill_unknown_suggests_close_match(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(
        ToolCall(id="c1", name="skill", arguments={"name": "correlat"}),
    )
    assert result.ok is False
    err_text = (result.error_message or "") + str(result.payload or "")
    assert "correlation" in err_text


def test_skill_rejects_missing_name(tmp_path: Path) -> None:
    dispatcher, _ = _build_dispatcher(tmp_path)
    result = dispatcher.dispatch(ToolCall(id="c1", name="skill", arguments={}))
    assert result.ok is False
    assert "required" in (result.error_message or "").lower()


def test_closest_skill_names_handles_typos() -> None:
    names = ["correlation", "time_series", "distribution_fit", "group_compare"]
    assert "correlation" in _closest_skill_names("correl", names)
    assert "time_series" in _closest_skill_names("timeseries", names)
    assert _closest_skill_names("", names) == []
    assert _closest_skill_names("xxxxxxxx", names) == []
```

- [ ] **Step 2: Run to verify the tests fail**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_tool.py -v 2>&1 | tail -30
```

Expected: Multiple failures about missing breadcrumb, missing Sub-skills section, `level` present.

- [ ] **Step 3: Update `_load_skill_body` in skill_tools.py**

Find the `_load_skill_body` nested function in `register_core_tools` (starting around line 58) and replace it entirely:

```python
    def _load_skill_body(args: dict[str, Any]) -> dict:
        """Return the SKILL.md body with breadcrumb header and sub-skill catalog.

        Progressive exposure: loading a skill automatically appends the catalog
        of its direct children (system-generated from the registry tree).
        The agent calls skill() on any child name to go deeper.
        """
        name = args.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("skill: 'name' (string) required")
        if registry is None:
            raise RuntimeError("skill registry not wired")

        node = registry.get_skill(name)
        if node is None:
            available = registry.list_skills()
            suggestions = _closest_skill_names(name, available)
            raise KeyError(
                f"skill: '{name}' not found. "
                f"{len(available)} skills available. "
                f"Suggestions: {suggestions}"
            )

        meta = node.metadata
        breadcrumb = registry.get_breadcrumb(name)
        children = registry.get_children(name)

        # Build the body: optional breadcrumb header + instructions + optional sub-skill catalog
        parts: list[str] = []

        # Breadcrumb header (only for skills below Level 1)
        if node.depth > 1:
            crumb = " › ".join(breadcrumb)
            parts.append(f"# {crumb}\n")
        else:
            parts.append(f"# {name}\n")

        parts.append(node.instructions)

        # Auto-appended sub-skill catalog (system-generated, never authored)
        if children:
            catalog_lines = ["---", "## Sub-skills", ""]
            for child in children:
                child_desc = child.metadata.description.strip()
                catalog_lines.append(f"- `{child.metadata.name}` — {child_desc}")
            parts.append("\n".join(catalog_lines))

        full_body = "\n\n".join(p.strip() for p in parts if p.strip())

        has_package = node.package_path is not None and any(node.package_path.iterdir())

        return {
            "name": meta.name,
            "body": full_body,
            "metadata": {
                "name": meta.name,
                "version": meta.version,
                "description": meta.description,
                "requires": list(meta.dependencies_requires),
                "used_by": list(meta.dependencies_used_by),
                "packages": list(meta.dependencies_packages),
                "error_templates": dict(meta.error_templates),
            },
            "has_python_package": has_package,
            "depth": node.depth,
            "breadcrumb": breadcrumb,
            "child_count": len(children),
        }
```

- [ ] **Step 4: Run the skill tool tests**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/test_skill_tool.py -v 2>&1 | tail -40
```

Expected: All tests pass.

- [ ] **Step 5: Run the full test suite to check for regressions**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/ -v 2>&1 | tail -30
```

- [ ] **Step 6: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/harness/skill_tools.py backend/tests/unit/test_skill_tool.py
git commit -m "feat: progressive skill tool response — breadcrumb + sub-skill catalog"
```

---

### Task 4: Update PreTurnInjector — Level-1-only catalog

**Files:**
- Modify: `backend/app/harness/injector.py`

No new test file — the injector is tested via integration. Update the Protocol and `_skill_menu()` method.

- [ ] **Step 1: Update the `_SkillRegistry` Protocol**

In `injector.py`, replace:

```python
class _SkillRegistry(Protocol):
    def list_skills(self) -> list[dict]: ...
```

with:

```python
from app.skills.base import SkillNode

class _SkillRegistry(Protocol):
    def list_top_level(self) -> list[SkillNode]: ...
```

(Add the import at the top of the file near the other imports.)

- [ ] **Step 2: Rewrite `_skill_menu()`**

Replace the `_skill_menu` method:

```python
    def _skill_menu(self) -> str:
        roots = self._skills.list_top_level()
        if not roots:
            return ""
        preamble = (
            "Use the `skill` tool to load any skill before using it. "
            "Hub skills expand into sub-skills when loaded — read the "
            "sub-skill catalog before deciding which to use."
        )
        lines: list[str] = []
        for node in roots:
            desc = node.metadata.description.strip()
            child_count = len(node.children)
            annotation = f" [{child_count} sub-skills]" if child_count > 0 else ""
            lines.append(f"- `{node.metadata.name}` — {desc}{annotation}")
        return "\n\n## Skills\n\n" + preamble + "\n\n" + "\n".join(lines)
```

- [ ] **Step 3: Verify the backend starts without import errors**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "from app.harness.injector import PreTurnInjector; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/harness/injector.py
git commit -m "feat: system prompt shows Level-1 skills only with sub-skill count annotations"
```

---

### Task 5: Make sandbox bootstrap dynamic

**Files:**
- Modify: `backend/app/harness/sandbox_bootstrap.py`

- [ ] **Step 1: Update `sandbox_bootstrap.py` to accept registry**

Replace the `_SKILL_IMPORTS` list and update `build_duckdb_globals` to accept an optional registry parameter. When the registry is provided, its `generate_bootstrap_imports()` output replaces the static skill import lines.

In `backend/app/harness/sandbox_bootstrap.py`, find `_SKILL_IMPORTS` and add this function right after it:

```python
def _build_skill_import_lines(registry=None) -> list[str]:
    """Return skill import lines.

    When a SkillRegistry is provided, generates imports dynamically from the
    tree (correct paths regardless of nesting depth). Falls back to the
    static _SKILL_IMPORTS list for backward compatibility during migration.

    # Auto-generated by SkillRegistry.generate_bootstrap_imports(). Do not edit
    # the generated portion manually — add skills via 'make skill-new' instead.
    """
    if registry is not None:
        return registry.generate_bootstrap_imports()
    # Static fallback — used only when no registry is wired (tests, legacy paths)
    return [line for line in _SKILL_IMPORTS if line.startswith("from app.skills")]
```

Then update the signature of `build_duckdb_globals`:

```python
def build_duckdb_globals(
    session_id: str,
    dataset_path: str | Path | None = None,
    db_path: str = _MAIN_DB_PATH,
    registry=None,  # SkillRegistry | None — injected by chat_api
) -> str:
```

And inside `build_duckdb_globals`, replace the line:
```python
    parts: list[str] = list(_SKILL_IMPORTS) + [
```
with:
```python
    skill_lines = _build_skill_import_lines(registry)
    _base_imports = [
        line for line in _SKILL_IMPORTS
        if not line.startswith("from app.skills")
    ]
    parts: list[str] = _base_imports + skill_lines + [
```

- [ ] **Step 2: Verify the bootstrap builds without errors**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "
from app.harness.sandbox_bootstrap import build_duckdb_globals
result = build_duckdb_globals('test-session', registry=None)
print('OK — first 200 chars:', result[:200])
"
```

Expected: `OK` with the bootstrap preamble printed.

- [ ] **Step 3: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/harness/sandbox_bootstrap.py
git commit -m "refactor: sandbox bootstrap accepts registry for dynamic skill imports"
```

---

### Task 6: Create hub skill SKILL.md files

Hub skills are guidance docs. Their SKILL.md explains what domain they cover and how to choose among sub-skills. No `pkg/` needed.

**Files:**
- Create: `backend/app/skills/statistical_analysis/SKILL.md`
- Create: `backend/app/skills/charting/SKILL.md`
- Create: `backend/app/skills/reporting/SKILL.md`

- [ ] **Step 1: Create `statistical_analysis/SKILL.md`**

```bash
mkdir -p /Users/jay/Developer/claude-code-agent/backend/app/skills/statistical_analysis
```

Write `backend/app/skills/statistical_analysis/SKILL.md`:

```markdown
---
name: statistical_analysis
description: "Statistical tests and analysis: correlation, distribution fitting, group
  comparison, assumption validation, and time-series. Load sub-skills to proceed."
version: "0.1"
---

# Statistical Analysis

Hub for statistical analysis capabilities. Load the appropriate sub-skill for your task.

## Choosing a sub-skill

| Task | Sub-skill |
|------|-----------|
| Measure relationship between two variables | `correlation` |
| Fit a parametric distribution to a variable | `distribution_fit` |
| Compare means/medians across groups | `group_compare` |
| Validate statistical assumptions before analysis | `stat_validate` |
| Decompose, forecast, or detect anomalies in time-series | `time_series` |

## Workflow

Always validate assumptions (`stat_validate`) before drawing conclusions.
`stat_validate` should run after `correlation`, `group_compare`, or `distribution_fit`
to confirm the test's preconditions were met.
```

- [ ] **Step 2: Create `charting/SKILL.md`**

```bash
mkdir -p /Users/jay/Developer/claude-code-agent/backend/app/skills/charting
```

Write `backend/app/skills/charting/SKILL.md`:

```markdown
---
name: charting
description: "Visualization capabilities using Altair: bar, line, scatter, histogram,
  heatmap, and more. Load sub-skills for chart-specific guidance."
version: "0.1"
---

# Charting

Hub for all chart types. The `altair_charts` sub-skill provides the chart generation
functions available in the sandbox.

## When to load this hub

Load `charting` first when you need to produce any chart. Then load `altair_charts`
to see the specific chart functions, their parameters, and expected data shapes.

## Altair theme

All charts use the project theme. Call `ensure_registered()` and `use_variant("dark")`
(or `"light"`) before generating charts. This is pre-run in the sandbox bootstrap.
```

- [ ] **Step 3: Create `reporting/SKILL.md`**

```bash
mkdir -p /Users/jay/Developer/claude-code-agent/backend/app/skills/reporting
```

Write `backend/app/skills/reporting/SKILL.md`:

```markdown
---
name: reporting
description: "Build HTML reports, dashboards, and formatted tables from findings.
  Sub-skills: report_builder, dashboard_builder, html_tables."
version: "0.1"
---

# Reporting

Hub for output assembly. Use these sub-skills to produce structured deliverables from
analysis results.

## Choosing a sub-skill

| Task | Sub-skill |
|------|-----------|
| Assemble a multi-section HTML report with narrative | `report_builder` |
| Build an interactive dashboard from artifact IDs | `dashboard_builder` |
| Render a DataFrame or dict as a styled HTML table | `html_tables` |

## Workflow

Typically: analyze → promote findings → call `report_builder` or `dashboard_builder`
to assemble the output. `html_tables` is used inside report content, not standalone.
```

- [ ] **Step 4: Verify the registry discovers hubs (flat, pre-migration)**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "
from pathlib import Path
from app.skills.registry import SkillRegistry
r = SkillRegistry(Path('app/skills'))
r.discover()
roots = [n.metadata.name for n in r.list_top_level()]
print('Top-level skills:', roots)
"
```

Expected: `statistical_analysis`, `charting`, `reporting` appear in the list alongside the existing flat skills.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/skills/statistical_analysis/ backend/app/skills/charting/ backend/app/skills/reporting/
git commit -m "feat: add hub SKILL.md files for statistical_analysis, charting, reporting"
```

---

### Task 7: Migrate existing skills into hierarchy (git mv)

This is the big filesystem reorganization. `git mv` preserves history. After this task, the directory structure matches the design spec.

**Prerequisite check:** Ensure Tasks 1-6 are committed and tests pass before starting this task.

- [ ] **Step 1: Add `__init__.py` to hub directories**

Hub directories need `__init__.py` so Python can traverse them to reach nested `pkg/` packages.

```bash
cd /Users/jay/Developer/claude-code-agent
touch backend/app/skills/statistical_analysis/__init__.py
touch backend/app/skills/charting/__init__.py
touch backend/app/skills/reporting/__init__.py
```

- [ ] **Step 2: Move statistical_analysis sub-skills**

```bash
cd /Users/jay/Developer/claude-code-agent/backend/app/skills
git mv correlation statistical_analysis/correlation
git mv distribution_fit statistical_analysis/distribution_fit
git mv group_compare statistical_analysis/group_compare
git mv stat_validate statistical_analysis/stat_validate
git mv time_series statistical_analysis/time_series
```

- [ ] **Step 3: Move charting sub-skills**

```bash
cd /Users/jay/Developer/claude-code-agent/backend/app/skills
git mv altair_charts charting/altair_charts
```

- [ ] **Step 4: Move reporting sub-skills**

```bash
cd /Users/jay/Developer/claude-code-agent/backend/app/skills
git mv report_builder reporting/report_builder
git mv dashboard_builder reporting/dashboard_builder
git mv html_tables reporting/html_tables
```

- [ ] **Step 5: Add `__init__.py` to nested skill parents that contain pkg/ descendants**

After moving, any parent that contains children with `pkg/` directories needs `__init__.py`:

```bash
cd /Users/jay/Developer/claude-code-agent/backend/app/skills

# statistical_analysis children with pkg/
touch statistical_analysis/correlation/__init__.py    # correlation has pkg/
touch statistical_analysis/time_series/__init__.py   # time_series has pkg/ (if any)

# charting
touch charting/altair_charts/__init__.py             # altair_charts has pkg/
```

Note: Only needed for skill directories that are parents of skills with `pkg/`. Leaf skills already have their own `__init__.py` if they have a `pkg/`.

- [ ] **Step 6: Verify the registry discovers the new hierarchy**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "
from pathlib import Path
from app.skills.registry import SkillRegistry
r = SkillRegistry(Path('app/skills'))
r.discover()
print('Top-level:', [n.metadata.name for n in r.list_top_level()])
print('stat_analysis children:', [n.metadata.name for n in r.get_children('statistical_analysis')])
print('charting children:', [n.metadata.name for n in r.get_children('charting')])
print('reporting children:', [n.metadata.name for n in r.get_children('reporting')])
print('correlation breadcrumb:', r.get_breadcrumb('correlation'))
print('All bootstrap imports:')
for line in r.generate_bootstrap_imports():
    print(' ', line)
"
```

Expected output (approximate):
```
Top-level: ['analysis_plan', 'charting', 'data_profiler', 'reporting', 'sql_builder', 'statistical_analysis']
stat_analysis children: ['correlation', 'distribution_fit', 'group_compare', 'stat_validate', 'time_series']
charting children: ['altair_charts']
reporting children: ['dashboard_builder', 'html_tables', 'report_builder']
correlation breadcrumb: ['statistical_analysis', 'correlation']
All bootstrap imports:
  from app.skills.statistical_analysis.correlation.pkg import *  # correlation
  ...
```

- [ ] **Step 7: Commit the migration**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/skills/
git commit -m "refactor: migrate skills into hierarchical directory structure"
```

---

### Task 8: Update import paths in skill_tools.py after migration

The `git mv` broke the static imports in `skill_tools.py` and the static `_SKILL_IMPORTS` list in `sandbox_bootstrap.py`. Fix them now.

**Files:**
- Modify: `backend/app/harness/skill_tools.py`
- Modify: `backend/app/harness/sandbox_bootstrap.py`

- [ ] **Step 1: Update the module-level imports in skill_tools.py**

Find the import block (lines ~17-35) and update all skill imports:

```python
# OLD
from app.skills.correlation import correlate
from app.skills.group_compare import compare
from app.skills.distribution_fit import fit as dist_fit
from app.skills.data_profiler import profile
from app.skills.stat_validate import validate
from app.skills.time_series import (
    characterize,
    decompose,
    find_anomalies,
    find_changepoints,
    lag_correlate,
)

# NEW
from app.skills.statistical_analysis.correlation import correlate
from app.skills.statistical_analysis.group_compare import compare
from app.skills.statistical_analysis.distribution_fit import fit as dist_fit
from app.skills.data_profiler import profile
from app.skills.statistical_analysis.stat_validate import validate
from app.skills.statistical_analysis.time_series import (
    characterize,
    decompose,
    find_anomalies,
    find_changepoints,
    lag_correlate,
)
```

Also find the late imports near the bottom of `register_core_tools` and update:

```python
# OLD
from app.skills.report_builder.pkg.build import build as _report_build
from app.skills.analysis_plan.pkg.plan import plan as _analysis_plan
from app.skills.dashboard_builder.pkg.build import build as _dashboard_build

# NEW
from app.skills.reporting.report_builder.pkg.build import build as _report_build
from app.skills.analysis_plan.pkg.plan import plan as _analysis_plan
from app.skills.reporting.dashboard_builder.pkg.build import build as _dashboard_build
```

- [ ] **Step 2: Update `_SKILL_IMPORTS` in sandbox_bootstrap.py**

Find the static `_SKILL_IMPORTS` list and update all `app.skills.*` paths:

```python
_SKILL_IMPORTS: list[str] = [
    "import sys",
    "import os",
    f"if {_BACKEND_DIR!r} not in sys.path:",
    f"    sys.path.insert(0, {_BACKEND_DIR!r})",
    "import json",
    "import numpy as np",
    "import pandas as pd",
    "import altair as alt",
    "import duckdb",
    "",
    "from config.themes.altair_theme import register_all as ensure_registered, use_variant",
    "ensure_registered()",
    "",
    # Statistical analysis skills (now nested)
    "from app.skills.statistical_analysis.correlation import correlate",
    "from app.skills.statistical_analysis.group_compare import compare",
    "from app.skills.statistical_analysis.stat_validate import validate",
    "from app.skills.statistical_analysis.time_series import (",
    "    characterize, decompose, find_anomalies,",
    "    find_changepoints, lag_correlate,",
    ")",
    "from app.skills.statistical_analysis.distribution_fit import fit",
    # Data skills (unchanged — still at root level)
    "from app.skills.data_profiler import profile",
    # Charting skills (now nested)
    "from app.skills.charting.altair_charts.pkg import (",
    "    bar, multi_line, histogram,",
    "    scatter_trend, boxplot, correlation_heatmap,",
    ")",
    # Reporting skills (now nested)
    "from app.skills.reporting.report_builder.pkg.build import build as report_build",
    "from app.skills.reporting.dashboard_builder.pkg.build import build as dashboard_build",
    # Standalone skills (unchanged)
    "from app.skills.analysis_plan.pkg.plan import plan as analysis_plan",
]
```

- [ ] **Step 3: Verify the backend imports without errors**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "
from app.harness.skill_tools import register_core_tools
print('skill_tools import OK')
from app.harness.sandbox_bootstrap import build_duckdb_globals
print('sandbox_bootstrap import OK')
"
```

Expected: Both `OK` lines print.

- [ ] **Step 4: Run the full test suite**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/pytest tests/unit/ -v 2>&1 | tail -40
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/harness/skill_tools.py backend/app/harness/sandbox_bootstrap.py
git commit -m "fix: update import paths after skill hierarchy migration"
```

---

### Task 9: Strip `level` field from all SKILL.md files

Every existing SKILL.md still has `level: N` in frontmatter. The registry ignores it now (never reads it), but it's dead weight and `make skill-check` should flag it. Remove it.

**Files:**
- All `SKILL.md` files under `backend/app/skills/`

- [ ] **Step 1: Remove `level:` lines with a Python script**

```bash
cd /Users/jay/Developer/claude-code-agent
python3 -c "
import re
from pathlib import Path

skill_files = list(Path('backend/app/skills').rglob('SKILL.md'))
removed = 0
for path in skill_files:
    text = path.read_text()
    new_text = re.sub(r'^level:.*\n', '', text, flags=re.MULTILINE)
    if new_text != text:
        path.write_text(new_text)
        removed += 1
        print(f'  Stripped level from {path}')
print(f'Done — stripped {removed} files.')
"
```

- [ ] **Step 2: Verify no `level:` lines remain**

```bash
grep -r "^level:" /Users/jay/Developer/claude-code-agent/backend/app/skills/
```

Expected: No output (no matches).

- [ ] **Step 3: Run registry discovery to confirm nothing broke**

```bash
cd /Users/jay/Developer/claude-code-agent/backend
.venv/bin/python -c "
from pathlib import Path
from app.skills.registry import SkillRegistry
r = SkillRegistry(Path('app/skills'))
r.discover()
all_skills = r.list_skills()
print(f'Discovered {len(all_skills)} skills:', all_skills)
"
```

Expected: All skills still discovered correctly.

- [ ] **Step 4: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add backend/app/skills/
git commit -m "chore: strip level field from all SKILL.md frontmatter (computed from directory depth)"
```

---

### Task 10: Update Makefile `skill-new` target

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Replace the `skill-new` target**

Find and replace the existing `skill-new` target in the Makefile:

```makefile
skill-new:
ifndef name
	$(error Usage: make skill-new name=<skill_name> [parent=<parent_skill>] [type=reference])
endif
ifdef parent
	$(eval SKILL_DIR := backend/app/skills/$(parent)/$(name))
else
	$(eval SKILL_DIR := backend/app/skills/$(name))
endif
ifdef parent
	@# Ensure parent hub has __init__.py for Python import traversal
	@touch backend/app/skills/$(parent)/__init__.py
endif
	@mkdir -p $(SKILL_DIR)
ifdef type
	@# Reference skill: no pkg/, description prefixed with [Reference]
	@printf -- "---\nname: $(name)\ndescription: '[Reference] Describe what this documents and when to load it.'\nversion: '0.1'\n---\n# $(name)\n\nReference documentation.\n\n## Contents\n\n...\n" > $(SKILL_DIR)/SKILL.md
else
	@mkdir -p $(SKILL_DIR)/pkg
	@mkdir -p $(SKILL_DIR)/tests
	@touch $(SKILL_DIR)/pkg/__init__.py
	@printf -- "---\nname: $(name)\ndescription: 'One-line description of what this skill does.'\nversion: '0.1'\n---\n# $(name)\n\nOne-paragraph overview.\n\n## When to use\n\n...\n\n## Contract\n\n...\n" > $(SKILL_DIR)/SKILL.md
endif
	@printf "dependencies:\n  requires: []\n  used_by: []\n  packages: []\nerrors: {}\n" > $(SKILL_DIR)/skill.yaml
	@echo "Skill scaffolded at $(SKILL_DIR)/"
ifdef parent
	@echo "Hub: backend/app/skills/$(parent)/ — $(name) is now a sub-skill."
endif
```

- [ ] **Step 2: Test the new target**

```bash
cd /Users/jay/Developer/claude-code-agent

# Test Level 1 standalone
make skill-new name=test_standalone_skill
ls backend/app/skills/test_standalone_skill/

# Test Level 2 sub-skill
make skill-new name=test_sub_skill parent=statistical_analysis
ls backend/app/skills/statistical_analysis/test_sub_skill/

# Test reference skill
make skill-new name=test_ref parent=statistical_analysis type=reference
cat backend/app/skills/statistical_analysis/test_ref/SKILL.md | head -5
```

Expected: `[Reference]` prefix in the reference skill description.

- [ ] **Step 3: Clean up test skills**

```bash
cd /Users/jay/Developer/claude-code-agent
rm -rf backend/app/skills/test_standalone_skill
rm -rf backend/app/skills/statistical_analysis/test_sub_skill
rm -rf backend/app/skills/statistical_analysis/test_ref
```

- [ ] **Step 4: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent
git add Makefile
git commit -m "feat: update skill-new to support parent and type=reference options"
```

---

### Task 11: Update documentation

**Files:**
- Modify: `docs/skill-creation.md`
- Create: `docs/progressive-skill-exposure.md`
- Modify: `prompts/data_scientist.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Rewrite `docs/skill-creation.md`**

Replace the entire file with:

```markdown
# Skill Creation Guide

Skills are organized in a tree. The agent sees top-level (Level 1) skills in the system
prompt. Loading a skill reveals its children. This is progressive exposure — the agent
loads only what the current task needs.

## Skill Levels

| Level | Description | Example |
|-------|-------------|---------|
| 1 | Hub or standalone skill; always visible to agent | `statistical_analysis`, `sql_builder` |
| 2 | Sub-skill; visible after loading its parent | `correlation`, `altair_charts` |
| 3 | Reference/deep-doc; visible after loading its parent | `correlation_methodology` |

**Hub rule:** Only create a hub (a skill with children) when it has 2+ children.
A hub with one child is just indirection — make the child a Level 1 standalone instead.

## File Structure

```
backend/app/skills/
  my_hub/                    ← Level 1 hub
    SKILL.md                 ← hub guidance doc
    __init__.py              ← required for Python import traversal
    child_skill/             ← Level 2
      SKILL.md
      pkg/
        __init__.py
      skill.yaml
      tests/
      deep_reference/        ← Level 3 (reference)
        SKILL.md
        skill.yaml

  standalone_skill/          ← Level 1 standalone (no hub)
    SKILL.md
    pkg/
    skill.yaml
    tests/
```

**`__init__.py` rule:** Any skill directory that has children (is a hub at any depth)
must have `__init__.py`. This lets Python traverse the module path to reach nested
`pkg/` packages. The `make skill-new parent=X` command handles this automatically.

## Scaffolding Commands

```bash
# Level 1 standalone skill
make skill-new name=my_skill

# Level 2 sub-skill under an existing hub
make skill-new name=my_skill parent=my_hub

# Level 3 reference skill (no pkg/, [Reference] description template)
make skill-new name=my_ref parent=my_hub type=reference
```

## SKILL.md Format

**Operational skill (Level 1 or 2):**

```yaml
---
name: my_skill
description: One-line description of what this skill does.
version: "0.1"
---
```

Body: what it does, when to use it, contract (inputs/outputs), usage examples.
Max 200 lines. Put implementation in `pkg/`.

**Hub skill (Level 1, has children):**

```yaml
---
name: my_hub
description: "Domain description. Sub-skills: child_a, child_b."
version: "0.1"
---
```

Body: decision table for choosing sub-skills, workflow guidance. No code examples.
Typically 30-60 lines.

**Reference skill (Level 3):**

```yaml
---
name: my_reference
description: "[Reference] What this documents and when to load it. Be specific —
  the agent uses this one-liner to decide whether to load the reference."
version: "0.1"
---
```

Body: deep technical documentation, methodology, limitations, edge cases.
No length limit. Never advertised in the always-on catalog — only visible after
the parent is loaded.

**Rules:**
- Never add a `level:` field — depth is computed from directory position.
- `[Reference]` prefix belongs in the `description` field, not a separate field.
- Description must be one line (or two short lines) — it appears in the sub-skill catalog.

## skill.yaml

```yaml
dependencies:
  requires: []         # skill names this skill depends on at runtime
  used_by: []          # skills that depend on this
  packages: []         # Python packages needed in the sandbox
errors:
  MY_ERROR:
    message: "Description with {placeholder}"
    guidance: "What the agent should do."
    recovery: "Concrete recovery step."
```

## Hub SKILL.md Guidelines

Hub skills are navigation aids, not instruction documents. Their body should contain:
- A decision table: "task X → use sub-skill Y"
- Workflow notes: what order to load sub-skills, when to combine them
- No code examples (code lives in leaf skills)

The sub-skill catalog is auto-appended by the system — do not write it yourself.

## Validation

```bash
make skill-check    # validates dependency graph, __init__.py presence, [Reference] rules
```
```

- [ ] **Step 2: Create `docs/progressive-skill-exposure.md`**

```markdown
# Progressive Skill Exposure

## Mental Model

The agent always sees the top of the skill tree (Level 1 skills). Loading a skill
reveals its children. Loading a child reveals its children. The agent traverses as
deeply as the task requires — no deeper.

```
System prompt (every turn) — Level 1 only:
  statistical_analysis  [5 sub-skills]
  charting              [1 sub-skill]
  reporting             [3 sub-skills]
  data_profiler
  sql_builder
  analysis_plan

Agent loads statistical_analysis → sees body + sub-skill catalog:
  correlation
  distribution_fit
  group_compare
  stat_validate
  time_series

Agent loads correlation → sees body + sub-skill catalog:
  correlation_methodology  [Reference] — load only for algorithmic depth
```

## Why This Exists

The original system injected all ~18 skill descriptions into every turn of the
conversation. The new system injects 6 Level-1 descriptions. Sub-skill catalogs
only appear after an explicit `skill()` call. Estimated token reduction: ~65% per turn.

Beyond tokens: the flat catalog gave the agent no information about skill relationships.
The progressive model makes the domain structure explicit and navigable.

## What the Agent Sees

**System prompt (always-on):**
```
## Skills

Use the `skill` tool to load any skill before using it. Hub skills expand into sub-skills
when loaded — read the sub-skill catalog before deciding which to use.

- `statistical_analysis` — Statistical tests and analysis. [5 sub-skills]
- `charting` — Visualization capabilities using Altair. [1 sub-skill]
- `reporting` — Build HTML reports, dashboards, and tables. [3 sub-skills]
- `data_profiler` — Full-dataset profile: schema, types, nulls, distributions.
- `sql_builder` — Write and execute SQL queries against loaded datasets.
- `analysis_plan` — Generate a structured analysis plan before diving into data.
```

**After `skill("statistical_analysis")`:**
```
# statistical_analysis

[hub body]

---
## Sub-skills

- `correlation` — Selects and runs the right correlation method.
- `distribution_fit` — Fits parametric distributions to a column.
- `group_compare` — Compares means/medians across groups.
- `stat_validate` — Validates statistical assumptions before analysis.
- `time_series` — Decomposes and forecasts time-series data.
```

**After `skill("correlation")`:**
```
# statistical_analysis › correlation

[correlation body]

---
## Sub-skills

- `correlation_methodology` — [Reference] Mathematical assumptions and numeric limits.
  Load only when debugging unexpected results or needing algorithmic depth.
```

## Access Rules

- Discovery is progressive — the agent navigates via hub→sub-skill.
- Access is permissive — `skill("correlation")` works even without loading `statistical_analysis` first.
  This supports power-users who name a skill explicitly in their prompt.
- Reference skills signal themselves via `[Reference]` in their description.
  The agent self-selects — the system never forces a reference skill load.

## Implementation

- **Registry:** `SkillRegistry.list_top_level()` → Level 1 only (for system prompt).
  `SkillRegistry.get_children(name)` → direct children (for sub-skill catalog).
  Both structures maintained in a single recursive `discover()` pass.
- **Skill tool:** `_load_skill_body()` auto-appends the sub-skill catalog when
  `get_children()` returns results. Never shown for leaf skills.
- **Injector:** `PreTurnInjector._skill_menu()` calls `list_top_level()`, annotates
  hubs with `[N sub-skills]`.
- **Hierarchy:** Filesystem nesting IS the hierarchy. No metadata field for level.
  Depth is computed from directory position during discovery.
```

- [ ] **Step 3: Update skill section in `prompts/data_scientist.md`**

Find the `## Skill Menu` section in `prompts/data_scientist.md` and update the description of how skills work. Replace whatever is there with:

```markdown
## Skills

Skills are organized hierarchically. The catalog (shown in context) lists only
**Level 1 skills**. Hub skills expand into sub-skills when loaded.

**Workflow:**
1. Identify which Level 1 skill covers your task.
2. Call `skill("name")` to load it.
3. If it's a hub, read the sub-skill catalog and call `skill("child_name")`.
4. Load reference skills (`[Reference]` prefix) only when you need algorithmic
   depth or are debugging unexpected results.

Never guess a skill name. Only call skills listed in the catalog or sub-skill catalogs
you have already seen this session.
```

- [ ] **Step 4: Update `CLAUDE.md` architecture section**

Find the Skills line in the Architecture section of `CLAUDE.md` and add:

```markdown
## Skills System

Skills are organized in a tree (nested directories). `SkillRegistry` discovers the
tree recursively at startup and maintains two structures:
- `_roots`: Level-1 skills (for the system prompt catalog)
- `_index`: flat name→SkillNode lookup (for permissive direct access)

The system prompt shows only Level-1 skills. Loading a skill auto-appends the catalog
of its children. Reference skills (Level 3, `[Reference]` prefix in description) are
only visible after their parent is loaded.

Sandbox bootstrap imports are generated dynamically from the registry tree via
`SkillRegistry.generate_bootstrap_imports()`.
```

Also update the `make skill-new name=X` line in the Commands section to:
```
make skill-new name=X [parent=Y] [type=reference]  # Scaffold new skill
```

- [ ] **Step 5: Commit all documentation**

```bash
cd /Users/jay/Developer/claude-code-agent
git add docs/skill-creation.md docs/progressive-skill-exposure.md prompts/data_scientist.md CLAUDE.md
git commit -m "docs: update skill system docs for progressive exposure model"
```

---

## Self-Review

**Spec coverage check:**

| Spec Requirement | Task |
|-----------------|------|
| Nested dirs as hierarchy | Tasks 6, 7 |
| Remove `level` from SkillMetadata | Task 1 |
| Add `SkillNode` with depth, parent, children | Task 1 |
| `SkillRegistry` recursive discovery | Task 2 |
| `list_top_level()`, `get_children()`, `get_breadcrumb()` | Task 2 |
| `generate_bootstrap_imports()` | Task 2, 5 |
| Skill tool: breadcrumb header | Task 3 |
| Skill tool: auto-appended sub-skill catalog | Task 3 |
| Skill tool: no sub-skills section for leaf skills | Task 3 |
| Permissive direct access by name | Task 3 (get_skill works at any depth) |
| Remove `level` and `references` from tool response | Task 3 |
| System prompt Level-1 only | Task 4 |
| `[N sub-skills]` annotation on hubs | Task 4 |
| Protocol update in injector | Task 4 |
| Dynamic sandbox bootstrap | Task 5 |
| Hub SKILL.md files created | Task 6 |
| Filesystem migration (git mv) | Task 7 |
| `__init__.py` at hub levels | Task 7 |
| Import paths updated after migration | Task 8 |
| `level` stripped from all frontmatter | Task 9 |
| `make skill-new parent=Y type=reference` | Task 10 |
| `docs/skill-creation.md` rewrite | Task 11 |
| `docs/progressive-skill-exposure.md` new | Task 11 |
| `prompts/data_scientist.md` update | Task 11 |
| `CLAUDE.md` update | Task 11 |
| `references/` removal | No action needed (none exist in codebase) |

All spec requirements covered. No placeholders. No TBDs.
