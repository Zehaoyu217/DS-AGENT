from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class InjectorInputs:
    active_profile_summary: str | None = None
    extras: dict[str, str] = field(default_factory=dict)


class _SkillRegistry(Protocol):
    def list_skills(self) -> list[dict]: ...


class _Wiki(Protocol):
    def working_digest(self) -> str: ...
    def index_digest(self) -> str: ...


class _GotchaIndex(Protocol):
    def as_injection(self) -> str: ...


class PreTurnInjector:
    def __init__(
        self,
        prompt_path: str | Path,
        wiki: _Wiki,
        skill_registry: _SkillRegistry,
        gotcha_index: _GotchaIndex,
    ) -> None:
        self._prompt_path = Path(prompt_path)
        self._wiki = wiki
        self._skills = skill_registry
        self._gotchas = gotcha_index

    def _static(self) -> str:
        return self._prompt_path.read_text(encoding="utf-8").rstrip()

    def _operational_state(self) -> str:
        working = self._wiki.working_digest()
        idx = self._wiki.index_digest()
        body = []
        if working:
            body.append("### working.md\n\n" + working)
        if idx:
            body.append("### index.md\n\n" + idx)
        if not body:
            return ""
        return "\n\n## Operational State\n\n" + "\n\n".join(body)

    def _skill_menu(self) -> str:
        entries = self._skills.list_skills()
        if not entries:
            return ""
        lines = [
            f"- `{e['name']}` — {e.get('description', '').strip()}"
            for e in entries
        ]
        return "\n\n## Skill Menu\n\n" + "\n".join(lines)

    def _gotchas_section(self) -> str:
        body = self._gotchas.as_injection().strip()
        if not body:
            return ""
        return "\n\n## Statistical Gotchas\n\n" + body

    def _profile_section(self, summary: str | None) -> str:
        if not summary:
            return ""
        return "\n\n## Active Dataset Profile\n\n" + summary.strip()

    def build(self, inputs: InjectorInputs) -> str:
        parts = [
            self._static(),
            self._operational_state(),
            self._skill_menu(),
            self._gotchas_section(),
            self._profile_section(inputs.active_profile_summary),
        ]
        for key, value in inputs.extras.items():
            parts.append(f"\n\n## {key}\n\n{value.strip()}")
        return "".join(parts)
