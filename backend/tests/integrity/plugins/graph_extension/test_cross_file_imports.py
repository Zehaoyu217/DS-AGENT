from __future__ import annotations
from pathlib import Path

from backend.app.integrity.plugins.graph_extension.extractors import cross_file_imports
from backend.app.integrity.schema import GraphSnapshot


EMPTY = GraphSnapshot(nodes=[], links=[])


def _write(repo: Path, rel: str, body: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_relative_from_import_emits_edges(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/trace/events.py", "class SessionEndEvent: ...\n")
    _write(
        tmp_path,
        "backend/app/trace/publishers.py",
        "from .events import SessionEndEvent\n",
    )
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    # Symbol target (Y is a class)
    assert ("publishers", "events_sessionendevent", "imports_from") in triples
    # Module-fallback target (Y could be a module)
    assert ("publishers", "sessionendevent", "imports_from") in triples


def test_module_only_import_emits_module_edge(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/skills/effect_size.py", "x = 1\n")
    _write(
        tmp_path,
        "backend/app/skills/compare.py",
        "from . import effect_size\n",
    )
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("compare", "effect_size", "imports_from") in triples


def test_plain_import_emits_module_edge(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/utils.py", "x = 1\n")
    _write(tmp_path, "backend/app/api/foo.py", "import backend.app.utils\n")
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("foo", "utils", "imports_from") in triples


def test_walks_backend_scripts_too(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/evals/judge.py", "class FallbackJudge: ...\n")
    _write(
        tmp_path,
        "backend/scripts/run_eval.py",
        "from backend.app.evals.judge import FallbackJudge\n",
    )
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("run_eval", "judge_fallbackjudge", "imports_from") in triples


def test_aliased_import_uses_original_name(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/core/home.py", "def traces_path(): ...\n")
    _write(
        tmp_path,
        "backend/app/api/chat_api.py",
        "from ..core.home import traces_path as tp\n",
    )
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("chat_api", "home_traces_path", "imports_from") in triples


def test_absolute_import_resolves_to_leaf_module(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/skills/analysis_plan/pkg/steps.py", "def pick_steps(): ...\n")
    _write(
        tmp_path,
        "backend/app/skills/analysis_plan/pkg/plan.py",
        "from backend.app.skills.analysis_plan.pkg.steps import pick_steps\n",
    )
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("plan", "steps_pick_steps", "imports_from") in triples


def test_star_import_skipped(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/utils.py", "x = 1\n")
    _write(tmp_path, "backend/app/main.py", "from .utils import *\n")
    result = cross_file_imports.extract(tmp_path, EMPTY)
    assert result.edges == []


def test_identical_src_tgt_skipped(tmp_path: Path) -> None:
    """from . import events inside events.py would self-loop; that one is skipped."""
    _write(tmp_path, "backend/app/trace/events.py", "from . import events\n")
    result = cross_file_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("events", "events", "imports_from") not in triples


def test_no_backend_dir_returns_empty(tmp_path: Path) -> None:
    result = cross_file_imports.extract(tmp_path, EMPTY)
    assert result.edges == []
    assert result.failures == []


def test_syntax_error_recorded(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/broken.py", "from .bad import (\n")
    result = cross_file_imports.extract(tmp_path, EMPTY)
    assert any("broken.py" in f for f in result.failures)
