"""RealAgentAdapter — drives the real /api/chat/stream endpoint for eval runs.

Usage in eval tests:
    from tests.evals.real_agent import RealAgentAdapter

    adapter = RealAgentAdapter(base_url="http://localhost:8000", traces_dir="traces")
    trace = await adapter.run(
        prompt="Which customer segment has the highest default rate?",
        db_path="/path/to/eval.db",
    )

The adapter:
1. POSTs to /api/chat/stream with the eval prompt and db_path.
2. Streams SSE events, capturing tool calls and the final response.
3. After the stream ends, loads the trace YAML to extract full tool call data
   (requires EVAL-2: publish_tool_call wired in loop.py).
4. Returns an AgentTrace suitable for the eval runner.

Prerequisites:
- Backend running at base_url
- eval.db seeded (make seed-eval)
- Trace YAML write enabled (TRACE_DIR env var or default ./traces/)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import httpx
import yaml

from app.evals.types import AgentTrace

_DEFAULT_BASE_URL = os.environ.get("CCAGENT_EVAL_BASE_URL", "http://localhost:8000")
_DEFAULT_TRACES_DIR = os.environ.get("TRACE_DIR", "traces")


class BackendNotReachableError(RuntimeError):
    """Raised when the backend is not reachable at the configured base_url."""


class RealAgentAdapter:
    """Connects the eval framework to the running backend via /api/chat/stream.

    Args:
        base_url: Base URL of the running backend (default: http://localhost:8000).
        traces_dir: Directory where trace YAMLs are written (default: traces/).
        timeout: HTTP timeout for the full SSE stream (seconds).
    """

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        traces_dir: str | Path = _DEFAULT_TRACES_DIR,
        timeout: float = 300.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._traces_dir = Path(traces_dir)
        self._timeout = timeout

    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        """Run the real agent against the given prompt and database.

        Args:
            prompt: The eval question / instruction to send.
            db_path: Absolute path to the DuckDB file (eval.db).

        Returns:
            AgentTrace with queries, final_output, errors, and timing.
        """
        import secrets
        session_id = f"eval-{secrets.token_hex(6)}"
        started = time.monotonic()

        errors: list[str] = []
        final_output = ""
        tool_call_previews: list[dict[str, Any]] = []

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream(
                "POST",
                f"{self._base_url}/api/chat/stream",
                json={
                    "message": prompt,
                    "dataset_path": db_path,
                    "session_id": session_id,
                },
                headers={"Accept": "text/event-stream"},
            ) as resp:
                if resp.status_code != 200:
                    raise BackendNotReachableError(
                        f"Backend returned HTTP {resp.status_code} for /api/chat/stream"
                    )
                async for raw_line in resp.aiter_lines():
                    line = raw_line.strip()
                    if not line or not line.startswith("data: "):
                        continue
                    try:
                        event = json.loads(line[6:])
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("type", "")
                    payload: dict[str, Any] = event.get("payload", {})

                    if event_type == "tool_call":
                        tool_call_previews.append({
                            "name": payload.get("name", ""),
                            "input_preview": payload.get("input_preview", ""),
                        })

                    elif event_type == "tool_result":
                        if payload.get("status") == "error":
                            errors.append(
                                f"{payload.get('name', 'tool')}: "
                                f"{payload.get('preview', '')[:200]}"
                            )

                    elif event_type == "turn_end":
                        final_output = payload.get("final_text", "") or ""

        duration_ms = int((time.monotonic() - started) * 1000)

        # ── Load full trace YAML for accurate query data ──────────────────────
        # After EVAL-2 (loop.py publish_tool_call), the YAML has ToolCallEvents
        # with full tool_input. We prefer those over truncated SSE previews.
        queries = self._extract_queries_from_trace(session_id)

        # Fall back to SSE previews if trace not yet written / no ToolCallEvents
        if not queries:
            queries = [
                tc["input_preview"]
                for tc in tool_call_previews
                if tc["name"] == "execute_python" and tc["input_preview"]
            ]

        # Extract intermediate artifacts from trace
        intermediate = self._extract_intermediate_from_trace(session_id)

        # Token count from trace summary (0 if trace not available)
        token_count = self._extract_token_count_from_trace(session_id)

        return AgentTrace(
            queries=queries,
            intermediate=intermediate,
            final_output=final_output,
            token_count=token_count,
            duration_ms=duration_ms,
            errors=errors,
        )

    # ── Trace YAML helpers ────────────────────────────────────────────────────

    def _load_trace_yaml(self, session_id: str) -> dict[str, Any] | None:
        path = self._traces_dir / f"{session_id}.yaml"
        if not path.exists():
            return None
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))  # type: ignore[return-value]
        except yaml.YAMLError:
            return None

    def _extract_queries_from_trace(self, session_id: str) -> list[str]:
        trace = self._load_trace_yaml(session_id)
        if trace is None:
            return []
        queries: list[str] = []
        for ev in trace.get("events", []):
            if ev.get("kind") == "tool_call" and ev.get("tool_name") == "execute_python":
                code = ev.get("tool_input", {}).get("code", "")
                if code:
                    queries.append(str(code))
        return queries

    def _extract_intermediate_from_trace(self, session_id: str) -> list[Any]:
        trace = self._load_trace_yaml(session_id)
        if trace is None:
            return []
        intermediate: list[Any] = []
        for ev in trace.get("events", []):
            if ev.get("kind") == "tool_call":
                output = ev.get("tool_output", "")
                if output and ev.get("tool_name") != "execute_python":
                    intermediate.append({
                        "tool": ev.get("tool_name"),
                        "output_preview": str(output)[:200],
                    })
        return intermediate

    def _extract_token_count_from_trace(self, session_id: str) -> int:
        trace = self._load_trace_yaml(session_id)
        if trace is None:
            return 0
        summary = trace.get("summary", {})
        return int(
            summary.get("total_input_tokens", 0)
            + summary.get("total_output_tokens", 0)
        )

    # ── Health check ──────────────────────────────────────────────────────────

    async def health_check(self) -> bool:
        """Return True if the backend is reachable."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self._base_url}/api/health")
                return resp.status_code == 200
        except (httpx.HTTPError, OSError):
            return False
