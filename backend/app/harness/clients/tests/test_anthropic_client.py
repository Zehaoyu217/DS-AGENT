from __future__ import annotations

from unittest.mock import MagicMock

from app.harness.clients.anthropic_client import AnthropicClient
from app.harness.clients.base import CompletionRequest, Message, ToolSchema
from app.harness.config import ModelProfile


def test_anthropic_client_maps_request_to_api(monkeypatch) -> None:
    fake_anthropic = MagicMock()
    fake_response = MagicMock()
    fake_response.content = [
        MagicMock(type="text", text="answer"),
    ]
    fake_response.stop_reason = "end_turn"
    fake_response.usage = MagicMock(input_tokens=10, output_tokens=5)
    fake_anthropic.messages.create.return_value = fake_response

    profile = ModelProfile(
        name="claude_sonnet", provider="anthropic",
        model_id="claude-sonnet-4-6", tier="observatory",
        thinking_budget=8000,
    )
    client = AnthropicClient(profile=profile, api_client=fake_anthropic)

    request = CompletionRequest(
        system="be thoughtful",
        messages=(Message(role="user", content="hi"),),
        tools=(ToolSchema(name="skill", description="load skill",
                          input_schema={"type": "object"}),),
        max_tokens=1024,
    )
    resp = client.complete(request)
    assert resp.text == "answer"
    assert resp.stop_reason == "end_turn"
    assert resp.usage == {"input_tokens": 10, "output_tokens": 5}

    kwargs = fake_anthropic.messages.create.call_args.kwargs
    assert kwargs["model"] == "claude-sonnet-4-6"
    assert kwargs["system"] == "be thoughtful"
    assert kwargs["max_tokens"] == 1024
    assert len(kwargs["messages"]) == 1
    assert len(kwargs["tools"]) == 1
