from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    id: str
    title: str
    body: str
    evidence: list[str] = field(default_factory=list)
    stat_validate_pass: bool = False


@dataclass(frozen=True)
class Hypothesis:
    id: str
    title: str
    body: str


@dataclass(frozen=True)
class Entity:
    name: str
    body: str
