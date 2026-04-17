"""Fixer registry for Plugin F.

Each fixer module exports `propose(artifacts, repo_root, config) -> list[Diff]`.
The registry maps fix-class names to their propose callables.
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from ..diff import Diff
from ..loader import SiblingArtifacts

Fixer = Callable[[SiblingArtifacts, Path, dict[str, Any]], list[Diff]]


def _registry() -> dict[str, Fixer]:
    from .claude_md_link import propose as claude_md_link
    from .dead_directive_cleanup import propose as dead_directive_cleanup
    from .doc_link_renamed import propose as doc_link_renamed
    from .health_dashboard_refresh import propose as health_dashboard_refresh
    from .manifest_regen import propose as manifest_regen
    return {
        "claude_md_link": claude_md_link,
        "doc_link_renamed": doc_link_renamed,
        "manifest_regen": manifest_regen,
        "dead_directive_cleanup": dead_directive_cleanup,
        "health_dashboard_refresh": health_dashboard_refresh,
    }


FIXER_REGISTRY: dict[str, Fixer] = {}


def get_registry() -> dict[str, Fixer]:
    """Lazy-init to avoid circular imports during module load."""
    global FIXER_REGISTRY
    if not FIXER_REGISTRY:
        FIXER_REGISTRY = _registry()
    return FIXER_REGISTRY
