import json
from pathlib import Path

import pytest
from backend.app.integrity.schema import GraphSnapshot


@pytest.fixture
def repo_with_graphs(tmp_path: Path) -> Path:
    (tmp_path / "graphify").mkdir()
    base = {
        "nodes": [
            {"id": "a", "label": "a", "kind": "function", "source_file": "x.py"},
            {"id": "b", "label": "b", "kind": "function", "source_file": "x.py"},
        ],
        "links": [
            {"source": "a", "target": "b", "relation": "calls", "confidence": "EXTRACTED"},
        ],
    }
    (tmp_path / "graphify" / "graph.json").write_text(json.dumps(base))
    return tmp_path


def test_loads_base_when_no_augmented(repo_with_graphs: Path):
    g = GraphSnapshot.load(repo_with_graphs)
    assert {n["id"] for n in g.nodes} == {"a", "b"}
    assert len(g.links) == 1


def test_merges_augmented_nodes(repo_with_graphs: Path):
    aug = {
        "nodes": [{"id": "c", "label": "c", "kind": "function", "source_file": "y.py"}],
        "links": [{"source": "a", "target": "c", "relation": "calls", "confidence": "EXTRACTED"}],
    }
    (repo_with_graphs / "graphify" / "graph.augmented.json").write_text(json.dumps(aug))
    g = GraphSnapshot.load(repo_with_graphs)
    assert {n["id"] for n in g.nodes} == {"a", "b", "c"}
    assert len(g.links) == 2


def test_augmented_node_wins_on_duplicate_id(repo_with_graphs: Path):
    aug = {
        "nodes": [{"id": "a", "label": "A_AUGMENTED", "kind": "function", "source_file": "x.py"}],
        "links": [],
    }
    (repo_with_graphs / "graphify" / "graph.augmented.json").write_text(json.dumps(aug))
    g = GraphSnapshot.load(repo_with_graphs)
    a_node = next(n for n in g.nodes if n["id"] == "a")
    assert a_node["label"] == "A_AUGMENTED"


def test_link_dedupe_on_source_target_relation(repo_with_graphs: Path):
    aug = {
        "nodes": [],
        "links": [
            {"source": "a", "target": "b", "relation": "calls", "confidence": "EXTRACTED"},  # dup
            # not dup — different relation
            {"source": "a", "target": "b", "relation": "imports_from", "confidence": "EXTRACTED"},
        ],
    }
    (repo_with_graphs / "graphify" / "graph.augmented.json").write_text(json.dumps(aug))
    g = GraphSnapshot.load(repo_with_graphs)
    assert len(g.links) == 2
    relations = sorted(link["relation"] for link in g.links)
    assert relations == ["calls", "imports_from"]
