"""User-configurable hook system (P23).

Reads backend/config/hooks.json (or $CCAGENT_HOOKS_PATH) and runs shell
commands in response to PreToolUse, PostToolUse, and Stop events.

Design constraints:
- Never raises — hook failures are logged, never propagated.
- Uses fnmatch for matcher patterns (supports *, ?, [seq]).
- Subprocess timeout: 10 seconds per hook command.
- Env vars available to commands: TOOL_NAME, TOOL_INPUT, TOOL_OUTPUT,
  SESSION_ID (PostToolUse only for TOOL_OUTPUT).
"""
from __future__ import annotations

import fnmatch
import json
import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "hooks.json"


class HookRunner:
    """Load hook config and run matching commands for each hook event."""

    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path or Path(
            os.environ.get("CCAGENT_HOOKS_PATH", str(_DEFAULT_CONFIG))
        )
        self._config: dict[str, list[dict]] | None = None

    def _load(self) -> dict[str, list[dict]]:
        if self._config is not None:
            return self._config
        path = self._config_path
        if not path.exists():
            self._config = {}
            return self._config
        try:
            self._config = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("hooks: failed to load config %s: %s", path, exc)
            self._config = {}
        return self._config

    def _match(self, matcher: str, tool_name: str) -> bool:
        """Return True if matcher pattern matches tool_name."""
        return fnmatch.fnmatch(tool_name, matcher)

    def _run(
        self,
        command: str,
        extra_env: dict[str, str],
        description: str,
    ) -> None:
        env = {**os.environ, **extra_env}
        try:
            result = subprocess.run(
                command,
                shell=True,
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.warning(
                    "hooks: command failed (exit %d) — %s: %s",
                    result.returncode,
                    description,
                    result.stderr[:200],
                )
        except subprocess.TimeoutExpired:
            logger.warning("hooks: command timed out — %s", description)
        except Exception as exc:
            logger.warning("hooks: command error — %s: %s", description, exc)

    def run_pre(
        self,
        tool_name: str,
        arguments: dict,
        session_id: str = "",
    ) -> None:
        """Run all matching PreToolUse hooks."""
        hooks = self._load().get("PreToolUse", [])
        env = {
            "TOOL_NAME": tool_name,
            "TOOL_INPUT": json.dumps(arguments),
            "SESSION_ID": session_id,
        }
        for hook in hooks:
            if self._match(hook.get("matcher", ""), tool_name):
                self._run(hook["command"], env, hook.get("description", ""))

    def run_post(
        self,
        tool_name: str,
        result: dict,
        session_id: str = "",
    ) -> None:
        """Run all matching PostToolUse hooks."""
        hooks = self._load().get("PostToolUse", [])
        env = {
            "TOOL_NAME": tool_name,
            "TOOL_OUTPUT": json.dumps(result),
            "SESSION_ID": session_id,
        }
        for hook in hooks:
            if self._match(hook.get("matcher", ""), tool_name):
                self._run(hook["command"], env, hook.get("description", ""))

    def run_stop(self, session_id: str = "") -> None:
        """Run all Stop hooks (called at end of session)."""
        hooks = self._load().get("Stop", [])
        env = {"SESSION_ID": session_id}
        for hook in hooks:
            self._run(hook.get("command", ""), env, hook.get("description", ""))
