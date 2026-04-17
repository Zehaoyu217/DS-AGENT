from __future__ import annotations

from pathlib import Path

from backend.app.integrity.plugins.graph_extension.extractors import module_qualified_calls
from backend.app.integrity.schema import GraphSnapshot

EMPTY = GraphSnapshot(nodes=[], links=[])


def _write(repo: Path, rel: str, body: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_from_x_import_module_then_method(tmp_path: Path) -> None:
    """`from app.trace import bus` + `bus.publish(...)` → calls bus_publish."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(event): ...\n")
    _write(
        tmp_path,
        "backend/app/trace/publishers.py",
        "from app.trace import bus\n"
        "def emit(e):\n"
        "    bus.publish(e)\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("publishers_emit", "bus_publish", "calls") in triples


def test_relative_import_from_dot_module(tmp_path: Path) -> None:
    """`from ..trace import bus` (relative) resolves to absolute `app.trace.bus`."""
    _write(tmp_path, "backend/app/trace/bus.py", "def subscribe(event): ...\n")
    _write(
        tmp_path,
        "backend/app/api/x.py",
        "from ..trace import bus\n"
        "def hook():\n"
        "    bus.subscribe('e')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("x_hook", "bus_subscribe", "calls") in triples


def test_from_dot_import_module_in_package(tmp_path: Path) -> None:
    """`from . import bus` inside `app/trace/__init__.py` binds bus to app.trace.bus."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/trace/dispatcher.py",
        "from . import bus\n"
        "def fire(e):\n"
        "    bus.publish(e)\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("dispatcher_fire", "bus_publish", "calls") in triples


def test_import_with_alias(tmp_path: Path) -> None:
    """`import a.b.bus as bus` + `bus.publish(...)` → calls bus_publish."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/main.py",
        "import app.trace.bus as bus\n"
        "def boot():\n"
        "    bus.publish('hi')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("main_boot", "bus_publish", "calls") in triples


def test_import_dotted_then_full_chain(tmp_path: Path) -> None:
    """`import app.trace.bus` + `app.trace.bus.publish()` resolves via direct chain lookup."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/main.py",
        "import app.trace.bus\n"
        "def boot():\n"
        "    app.trace.bus.publish('hi')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("main_boot", "bus_publish", "calls") in triples


def test_skip_when_target_module_missing(tmp_path: Path) -> None:
    """Imports of modules outside the repo do not emit edges."""
    _write(
        tmp_path,
        "backend/app/main.py",
        "from third_party import lib\n"
        "def boot():\n"
        "    lib.do_thing()\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    assert result.edges == []


def test_skip_when_function_not_in_module(tmp_path: Path) -> None:
    """Module exists but doesn't define the called function → no emit."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/main.py",
        "from app.trace import bus\n"
        "def boot():\n"
        "    bus.unknown_fn()\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    assert result.edges == []


def test_local_shadow_blocks_resolution(tmp_path: Path) -> None:
    """Local `bus = something()` shadows the import; no edge emitted."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/main.py",
        "from app.trace import bus\n"
        "def boot():\n"
        "    bus = create_bus()\n"
        "    bus.publish('x')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("main_boot", "bus_publish", "calls") not in triples


def test_class_symbol_not_misidentified_as_module(tmp_path: Path) -> None:
    """`from app.trace import EventBus` (a class re-exported from __init__) → no module edge."""
    _write(
        tmp_path,
        "backend/app/trace/__init__.py",
        "class EventBus:\n    @staticmethod\n    def publish(e): ...\n",
    )
    _write(
        tmp_path,
        "backend/app/main.py",
        "from app.trace import EventBus\n"
        "def boot():\n"
        "    EventBus.publish('x')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert not any(s == "main_boot" and t == "eventbus_publish" for s, t, _ in triples)


def test_async_caller_and_callee(tmp_path: Path) -> None:
    """Async functions are valid as both callers and callees."""
    _write(tmp_path, "backend/app/trace/bus.py", "async def aemit(e): ...\n")
    _write(
        tmp_path,
        "backend/app/api/handler.py",
        "from app.trace import bus\n"
        "async def handle():\n"
        "    await bus.aemit('e')\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("handler_handle", "bus_aemit", "calls") in triples


def test_class_method_caller(tmp_path: Path) -> None:
    """Class methods are valid callers; caller_id uses just stem + method name."""
    _write(tmp_path, "backend/app/trace/bus.py", "def publish(e): ...\n")
    _write(
        tmp_path,
        "backend/app/services/svc.py",
        "from app.trace import bus\n"
        "class Service:\n"
        "    def emit(self, e):\n"
        "        bus.publish(e)\n",
    )
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("svc_emit", "bus_publish", "calls") in triples


def test_no_backend_dir_returns_empty(tmp_path: Path) -> None:
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    assert result.edges == []
    assert result.failures == []


def test_syntax_error_recorded(tmp_path: Path) -> None:
    _write(tmp_path, "backend/app/broken.py", "def bad(\n")
    result = module_qualified_calls.extract(tmp_path, EMPTY)
    assert any("broken.py" in f for f in result.failures)
