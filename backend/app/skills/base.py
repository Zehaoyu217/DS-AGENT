from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SkillError(Exception):
    """Actionable error with template-based formatting.

    Every error code maps to a template in skill.yaml with message,
    guidance, and recovery fields. Context values fill the placeholders.
    """

    def __init__(
        self,
        code: str,
        context: dict[str, Any],
        templates: dict[str, dict[str, str]] | None = None,
    ) -> None:
        self.code = code
        self.context = context
        self.templates = templates or {}
        super().__init__(self.format())

    def format(self) -> str:
        template = self.templates.get(self.code)
        if template is None:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.code}: {context_str}"
        parts: list[str] = []
        for key in ("message", "guidance", "recovery"):
            raw = template.get(key, "")
            if raw:
                try:
                    parts.append(raw.format(**self.context))
                except KeyError:
                    parts.append(raw)
        return "\n".join(parts)


@dataclass(frozen=True)
class SkillResult:
    """Return type for all skill function executions."""

    data: Any = None
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class SkillMetadata:
    """Parsed metadata from skill.yaml."""

    name: str
    version: str
    description: str
    level: int
    dependencies_requires: list[str] = field(default_factory=list)
    dependencies_used_by: list[str] = field(default_factory=list)
    dependencies_packages: list[str] = field(default_factory=list)
    error_templates: dict[str, dict[str, str]] = field(default_factory=dict)
