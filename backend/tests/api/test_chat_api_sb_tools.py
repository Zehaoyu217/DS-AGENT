"""Tests that the sb_* ToolSchemas are registered in chat_api._CHAT_TOOLS."""
from __future__ import annotations

from app.api.chat_api import _CHAT_TOOLS


def test_sb_tool_schemas_present():
    names = {t.name for t in _CHAT_TOOLS}
    assert {
        "sb_search",
        "sb_load",
        "sb_reason",
        "sb_ingest",
        "sb_promote_claim",
    } <= names


def test_sb_search_schema_requires_query():
    schema = next(t for t in _CHAT_TOOLS if t.name == "sb_search").input_schema
    assert "query" in schema["required"]


def test_sb_load_schema_has_node_id_and_depth():
    schema = next(t for t in _CHAT_TOOLS if t.name == "sb_load").input_schema
    assert "node_id" in schema["required"]
    assert "depth" in schema["properties"]
