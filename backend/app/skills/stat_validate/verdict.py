from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Violation:
    code: str
    severity: str  # "WARN" | "FAIL"
    message: str
    gotcha_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Check:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Validation:
    status: str  # "PASS" | "WARN" | "FAIL" — for serialization convenience
    failures: tuple[Violation, ...]
    warnings: tuple[Violation, ...]
    passes: tuple[Check, ...]

    def rollup_status(self) -> str:
        if self.failures:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"

    def gotcha_refs(self) -> tuple[str, ...]:
        seen: list[str] = []
        for v in (*self.failures, *self.warnings):
            for ref in v.gotcha_refs:
                if ref not in seen:
                    seen.append(ref)
        return tuple(seen)

    def to_dict(self) -> dict:
        return {
            "status": self.rollup_status(),
            "failures": [
                {"code": v.code, "severity": v.severity, "message": v.message,
                 "gotcha_refs": list(v.gotcha_refs)}
                for v in self.failures
            ],
            "warnings": [
                {"code": v.code, "severity": v.severity, "message": v.message,
                 "gotcha_refs": list(v.gotcha_refs)}
                for v in self.warnings
            ],
            "passes": [{"code": c.code, "message": c.message} for c in self.passes],
            "gotcha_refs": list(self.gotcha_refs()),
        }
