"""Second-Brain tool handlers. Each function returns a JSON-serializable dict.

When the Second-Brain KB is disabled (directory missing), every handler
returns a structured error rather than raising, so the agent loop keeps
working without the KB.
"""
from __future__ import annotations

from typing import Any

from app import config


def _disabled(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"ok": False, "error": "second_brain_disabled"}
    if extra:
        out.update(extra)
    return out


def _cfg():  # noqa: ANN202
    from second_brain.config import Config
    return Config.load()


def sb_search(args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled({"hits": []})
    from second_brain.index.retriever import BM25Retriever

    query = str(args.get("query", ""))
    if not query:
        return {"ok": False, "error": "missing query", "hits": []}
    k = int(args.get("k", 5))
    scope = str(args.get("scope", "both"))
    taxonomy = args.get("taxonomy")
    with_neighbors = bool(args.get("with_neighbors", False))

    cfg = _cfg()
    if not cfg.fts_path.exists():
        return {"ok": False, "error": "no_index", "hits": []}

    retriever = BM25Retriever(cfg)
    hits = retriever.search(
        query,
        k=k,
        scope=scope,  # type: ignore[arg-type]
        taxonomy=taxonomy,
        with_neighbors=with_neighbors,
    )
    return {
        "ok": True,
        "hits": [
            {
                "id": h.id,
                "kind": h.kind,
                "score": h.score,
                "matched_field": h.matched_field,
                "snippet": h.snippet,
                "neighbors": h.neighbors,
            }
            for h in hits
        ],
    }


def sb_load(args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled()
    from second_brain.load import LoadError, load_node

    node_id = str(args.get("node_id", ""))
    if not node_id:
        return {"ok": False, "error": "missing node_id"}
    depth = int(args.get("depth", 0))
    relations = args.get("relations") or None
    if isinstance(relations, str):
        relations = [r.strip() for r in relations.split(",") if r.strip()]

    cfg = _cfg()
    try:
        result = load_node(cfg, node_id, depth=depth, relations=relations)
    except LoadError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001 — KB may be uninitialised; surface as structured error
        return {"ok": False, "error": f"load_failed: {exc}"}
    return {
        "ok": True,
        "root": result.root,
        "neighbors": result.neighbors,
        "edges": result.edges,
    }


def sb_reason(args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled({"paths": []})
    from second_brain.reason import GraphPattern
    from second_brain.reason import sb_reason as _run

    start_id = str(args.get("start_id", ""))
    walk = str(args.get("walk", ""))
    if not start_id or not walk:
        return {"ok": False, "error": "start_id and walk required", "paths": []}
    direction = str(args.get("direction", "outbound"))
    max_depth = int(args.get("max_depth", 3))
    terminator = args.get("terminator")

    cfg = _cfg()
    paths = _run(
        cfg,
        start_id=start_id,
        pattern=GraphPattern(
            walk=walk,
            direction=direction,  # type: ignore[arg-type]
            max_depth=max_depth,
            terminator=terminator,
        ),
    )
    return {"ok": True, "paths": paths}


def sb_ingest(args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled()
    from pathlib import Path as _Path

    from second_brain.ingest.base import IngestInput
    from second_brain.ingest.orchestrator import IngestError, ingest

    path_or_url = str(args.get("path", ""))
    if not path_or_url:
        return {"ok": False, "error": "missing path"}

    cfg = _cfg()
    try:
        if path_or_url.startswith(("http://", "https://", "gh:", "file://")):
            # URL and repo converters accept origin strings via IngestInput.from_origin;
            # fall back to a path if the URL/repo shorthand isn't supported here.
            inp = (
                IngestInput.from_path(_Path(path_or_url))
                if _Path(path_or_url).exists()
                else None
            )
            if inp is None:
                # Future: add IngestInput.from_origin for URLs/repos.
                return {
                    "ok": False,
                    "error": "url/repo ingest via tool not yet supported",
                }
        else:
            inp = IngestInput.from_path(_Path(path_or_url))
        folder = ingest(inp, cfg=cfg)
    except IngestError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "source_id": folder.root.name, "folder": str(folder.root)}


def sb_promote_claim(args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled()
    # v1: claude-code-agent wiki findings don't yet carry ids that second-brain
    # can resolve. Return a structured not-implemented so the agent can continue.
    return {"ok": False, "error": "sb_promote_claim not wired in v1 bridge"}
