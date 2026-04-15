from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True, slots=True)
class CorrelationResult:
    coefficient: float
    ci_low: float
    ci_high: float
    p_value: float
    method_used: str
    nonlinear_warning: bool
    n_effective: int
    na_dropped: int
    x: str
    y: str
    partial_on: tuple[str, ...] = field(default_factory=tuple)
    detrend: str | None = None
    bootstrap_n: int = 1000
    artifact_id: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["partial_on"] = list(self.partial_on)
        return d
