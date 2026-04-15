from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.harness.clients.base import ToolCall
from app.harness.dispatcher import ToolDispatcher, ToolResult


def test_dispatcher_routes_to_registered_handler() -> None:
    handler = MagicMock(return_value={"ok": True})
    disp = ToolDispatcher()
    disp.register("skill", handler)
    result = disp.dispatch(ToolCall(id="t1", name="skill", arguments={"name": "foo"}))
    assert isinstance(result, ToolResult)
    assert result.tool_use_id == "t1"
    assert result.ok is True
    assert result.payload == {"ok": True}
    handler.assert_called_once_with({"name": "foo"})


def test_dispatcher_captures_exception_and_wraps_error() -> None:
    def boom(_args):
        raise RuntimeError("nope")
    disp = ToolDispatcher()
    disp.register("boom", boom)
    result = disp.dispatch(ToolCall(id="t2", name="boom", arguments={}))
    assert result.ok is False
    assert "nope" in result.error_message


def test_dispatcher_unknown_tool_is_error() -> None:
    disp = ToolDispatcher()
    result = disp.dispatch(ToolCall(id="t3", name="ghost", arguments={}))
    assert result.ok is False
    assert "unknown tool" in result.error_message


def test_dispatcher_register_twice_raises() -> None:
    disp = ToolDispatcher()
    disp.register("x", lambda a: None)
    with pytest.raises(ValueError, match="already registered"):
        disp.register("x", lambda a: None)
