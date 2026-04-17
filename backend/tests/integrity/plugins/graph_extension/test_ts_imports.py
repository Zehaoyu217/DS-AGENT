from __future__ import annotations
from pathlib import Path

from backend.app.integrity.plugins.graph_extension.extractors import ts_imports
from backend.app.integrity.schema import GraphSnapshot

EMPTY = GraphSnapshot(nodes=[], links=[])


def _write(repo: Path, rel: str, body: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_named_import_emits_dual_edges(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/lib/tokens.ts", "export const formatTokens = () => 0;\n")
    _write(
        tmp_path,
        "frontend/src/sections/ChatSection.tsx",
        "import { formatTokens } from '../lib/tokens';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("chatsection", "tokens_formattokens", "imports_from") in triples
    assert ("chatsection", "formattokens", "imports_from") in triples


def test_default_import_uses_local_name(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/lib/highlight.ts", "export default function highlightCode(){}\n")
    _write(
        tmp_path,
        "frontend/src/components/Code.tsx",
        "import highlightCode from '../lib/highlight';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("code", "highlight_highlightcode", "imports_from") in triples


def test_aliased_named_import_uses_source_name(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/hooks/useRegistry.ts", "export const useCommandRegistry = ()=>0;\n")
    _write(
        tmp_path,
        "frontend/src/components/Cmd.tsx",
        "import { useCommandRegistry as reg } from '../hooks/useRegistry';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("cmd", "useregistry_usecommandregistry", "imports_from") in triples


def test_namespace_import_emits_module_edge(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/lib/api.ts", "export const listSessions = ()=>0;\n")
    _write(
        tmp_path,
        "frontend/src/hooks/useSessions.ts",
        "import * as api from '../lib/api';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("usesessions", "api_api", "imports_from") in triples or (
        "usesessions",
        "api",
        "imports_from",
    ) in triples


def test_index_path_resolves_to_parent_segment(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/components/index.ts", "export const Hello = ()=>0;\n")
    _write(
        tmp_path,
        "frontend/src/App.tsx",
        "import { Hello } from './components';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("app", "components_hello", "imports_from") in triples


def test_explicit_index_segment_resolves_to_parent(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/components/index.ts", "export const Goodbye = ()=>0;\n")
    _write(
        tmp_path,
        "frontend/src/App.tsx",
        "import { Goodbye } from './components/index';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("app", "components_goodbye", "imports_from") in triples


def test_bare_specifier_skipped(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/App.tsx", "import { useState } from 'react';\n")
    result = ts_imports.extract(tmp_path, EMPTY)
    assert result.edges == []


def test_type_only_import_emits_edge(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/lib/types.ts", "export type Token = string;\n")
    _write(
        tmp_path,
        "frontend/src/App.tsx",
        "import type { Token } from './lib/types';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("app", "types_token", "imports_from") in triples


def test_no_frontend_dir_returns_empty(tmp_path: Path) -> None:
    result = ts_imports.extract(tmp_path, EMPTY)
    assert result.edges == []
    assert result.failures == []


def test_hyphenated_filename_normalized_to_underscore(tmp_path: Path) -> None:
    """Graphify ids for ``api-agents.ts`` are ``api_agents_*``; the extractor must match."""
    _write(tmp_path, "frontend/src/lib/api-agents.ts", "export const listAgentGroups = ()=>0;\n")
    _write(
        tmp_path,
        "frontend/src/components/sidebar/AgentsTab.tsx",
        "import { listAgentGroups } from '../../lib/api-agents';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("agentstab", "api_agents_listagentgroups", "imports_from") in triples


def test_inline_type_keyword_stripped(tmp_path: Path) -> None:
    """``import { type Foo }`` should bind ``Foo``, not ``type Foo``."""
    _write(tmp_path, "frontend/src/lib/api-backend.ts", "export type BrandingConfig = {};\n")
    _write(
        tmp_path,
        "frontend/src/hooks/useBranding.ts",
        "import { backend, type BrandingConfig } from '../lib/api-backend';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("usebranding", "api_backend_brandingconfig", "imports_from") in triples
    assert all("type " not in t for _, t, _ in triples)


def test_alias_path_emits_edge(tmp_path: Path) -> None:
    _write(tmp_path, "frontend/src/components/Inner.tsx", "export const Inner = ()=>null;\n")
    _write(
        tmp_path,
        "frontend/src/App.tsx",
        "import { Inner } from '@/components/Inner';\n",
    )
    result = ts_imports.extract(tmp_path, EMPTY)
    triples = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("app", "inner_inner", "imports_from") in triples
