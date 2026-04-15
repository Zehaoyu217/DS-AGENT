from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Severity(Enum):
    WARN = auto()
    FAIL = auto()

    def blocks_strict(self) -> bool:
        return self is Severity.FAIL

    def warns(self) -> bool:
        return self in (Severity.WARN, Severity.FAIL)


class GuardrailOutcome(Enum):
    PASS = auto()
    WARN = auto()
    BLOCK = auto()
    OBSERVE = auto()


@dataclass(frozen=True, slots=True)
class GuardrailFinding:
    code: str
    severity: Severity
    message: str
    metadata: dict | None = None
