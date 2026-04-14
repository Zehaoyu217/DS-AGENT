"""REST endpoints for the slash-command registry.

For now the registry is a static hardcoded list and execution returns a stub
response for known ids. Real actions wire up in later phases (P4–P9).
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/slash", tags=["slash"])


class SlashCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    description: str


class SlashExecuteRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    command_id: str
    args: dict[str, object] = Field(default_factory=dict)
    conversation_id: str | None = None


class SlashExecuteResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    ok: bool
    message: str


SLASH_COMMANDS: list[SlashCommand] = [
    SlashCommand(id="help", label="/help", description="Show slash command reference"),
    SlashCommand(id="clear", label="/clear", description="Clear current conversation view"),
    SlashCommand(id="new", label="/new", description="Start a new conversation"),
    SlashCommand(id="settings", label="/settings", description="Open settings"),
]

_KNOWN_IDS = frozenset(cmd.id for cmd in SLASH_COMMANDS)


@router.get("")
def list_slash_commands() -> list[SlashCommand]:
    return SLASH_COMMANDS


@router.post("/execute")
def execute_slash_command(payload: SlashExecuteRequest) -> SlashExecuteResponse:
    if payload.command_id not in _KNOWN_IDS:
        raise HTTPException(status_code=404, detail="unknown slash command")
    return SlashExecuteResponse(ok=True, message=f"Executed {payload.command_id}")
