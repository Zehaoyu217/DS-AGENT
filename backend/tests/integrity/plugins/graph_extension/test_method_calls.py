from __future__ import annotations
from pathlib import Path

from backend.app.integrity.plugins.graph_extension.extractors import method_calls
from backend.app.integrity.schema import GraphSnapshot

EMPTY = GraphSnapshot(nodes=[], links=[])


def _write(repo: Path, rel: str, body: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_annotation_resolves_method_call(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "backend/app/context/manager.py",
        "class ContextManager:\n    def add_layer(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/api/chat_api.py",
        "from ..context.manager import ContextManager\n"
        "def post_chat(manager: ContextManager) -> None:\n"
        "    manager.add_layer()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("chat_api_post_chat", "manager_contextmanager_add_layer", "calls") in triples


def test_constructor_assignment_resolves_method(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "backend/app/wiki/engine.py",
        "class WikiEngine:\n    def append_log(self, msg): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/harness/wiring.py",
        "from ..wiki.engine import WikiEngine\n"
        "def wire():\n"
        "    eng = WikiEngine()\n"
        "    eng.append_log('hi')\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("wiring_wire", "engine_wikiengine_append_log", "calls") in triples


def test_dunder_method_strips_underscores_in_id(tmp_path: Path) -> None:
    """``__init__`` lands as ``..._init`` (graphify strips leading+trailing ``_``)."""
    _write(
        tmp_path,
        "backend/app/context/manager.py",
        "class ContextManager:\n    def __init__(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/api/chat_api.py",
        "from ..context.manager import ContextManager\n"
        "def boot():\n"
        "    m = ContextManager()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("chat_api_boot", "manager_contextmanager_init", "calls") in triples


def test_unique_method_name_fallback_emits_edge(tmp_path: Path) -> None:
    """Type unknown but method name is unique in registry → emit anyway."""
    _write(
        tmp_path,
        "backend/app/harness/loop.py",
        "class AgentLoop:\n    def run_stream(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/api/chat_api.py",
        "def stream(loop):\n"
        "    loop.run_stream()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("chat_api_stream", "loop_agentloop_run_stream", "calls") in triples


def test_ambiguous_method_skipped_when_no_type(tmp_path: Path) -> None:
    """Method name on >1 class with unknown type → skip (avoid pollution)."""
    _write(
        tmp_path,
        "backend/app/a.py",
        "class A:\n    def shared(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/b.py",
        "class B:\n    def shared(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/caller.py",
        "def use(x):\n    x.shared()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert not any(t == "calls" and ".shared" in tgt for _, tgt, t in triples)
    assert not any(s == "caller_use" for s, _, _ in triples)


def test_self_method_call_skipped(tmp_path: Path) -> None:
    """``self.method()`` is intra-file's job; method_calls should not double-emit."""
    _write(
        tmp_path,
        "backend/app/foo.py",
        "class Foo:\n"
        "    def helper(self): ...\n"
        "    def caller(self):\n"
        "        self.helper()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert not any(s == "foo_caller" and "_helper" in t for s, t, _ in triples)


def test_optional_annotation_resolves(tmp_path: Path) -> None:
    """``x: Optional[Foo]`` should still bind ``x`` to ``Foo``."""
    _write(
        tmp_path,
        "backend/app/store.py",
        "class ArtifactStore:\n    def add_artifact(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/caller.py",
        "from typing import Optional\n"
        "from .store import ArtifactStore\n"
        "def go(store: Optional[ArtifactStore]) -> None:\n"
        "    store.add_artifact()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("caller_go", "store_artifactstore_add_artifact", "calls") in triples


def test_module_qualified_constructor(tmp_path: Path) -> None:
    """``x = mod.ClassName()`` should bind ``x`` to ``ClassName``."""
    _write(
        tmp_path,
        "backend/app/scheduler/engine.py",
        "class CronEngine:\n    def start(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/main.py",
        "from .scheduler import engine\n"
        "def boot():\n"
        "    e = engine.CronEngine()\n"
        "    e.start()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("main_boot", "engine_cronengine_start", "calls") in triples


def test_string_annotation_pep563(tmp_path: Path) -> None:
    """``def f(x: 'Foo')`` (stringified annotation) should still resolve."""
    _write(
        tmp_path,
        "backend/app/harness/dispatcher.py",
        "class ToolDispatcher:\n    def get_handler(self): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/harness/a2a.py",
        "def call(d: 'ToolDispatcher') -> None:\n"
        "    d.get_handler()\n",
    )
    result = method_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("a2a_call", "dispatcher_tooldispatcher_get_handler", "calls") in triples


def test_no_backend_dir_returns_empty(tmp_path: Path) -> None:
    result = method_calls.extract(tmp_path, EMPTY)
    assert result.edges == []
    assert result.failures == []


def test_syntax_error_recorded(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/broken.py", "class Foo:\n    def bad(\n")
    result = method_calls.extract(tmp_path, EMPTY)
    assert any("broken.py" in f for f in result.failures)
