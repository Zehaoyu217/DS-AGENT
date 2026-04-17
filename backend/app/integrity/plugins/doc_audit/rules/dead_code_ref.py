from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex
from ..parser.code_refs import extract_code_refs


def _graph_indices(ctx: ScanContext) -> tuple[set[str], set[str]]:
    paths: set[str] = set()
    symbols: set[str] = set()
    for node in ctx.graph.nodes:
        sf = node.get("source_file")
        if isinstance(sf, str) and sf:
            paths.add(sf)
        nid = node.get("id")
        if isinstance(nid, str):
            symbols.add(nid.lower())
        label = node.get("label")
        if isinstance(label, str):
            symbols.add(label.lower())
    return paths, symbols


def _is_adr(rel: str) -> bool:
    return rel.startswith("knowledge/adr/")


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    graph_paths, graph_symbols = _graph_indices(ctx)
    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        if _is_adr(rel):
            continue  # handled by adr_status_drift
        parsed = idx.docs[rel]
        refs = extract_code_refs(parsed.raw_text)
        for ref in refs:
            if ref.kind in ("path", "path_line"):
                target = ref.path or ""
                if not target:
                    continue
                if target in graph_paths:
                    continue
                if (ctx.repo_root / target).exists():
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.dead_code_ref",
                        severity="WARN",
                        node_id=f"{rel}->{target}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Dead code reference: {target}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
            elif ref.kind == "symbol":
                if not ref.symbol or "." not in ref.symbol:
                    continue
                if ref.symbol.lower() in graph_symbols:
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.dead_code_ref",
                        severity="WARN",
                        node_id=f"{rel}->{ref.symbol}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Dead symbol reference: {ref.symbol}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
    return issues
