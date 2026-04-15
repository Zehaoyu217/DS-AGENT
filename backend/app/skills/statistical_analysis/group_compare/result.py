from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CompareResult:
    effect_size: float
    effect_ci_low: float
    effect_ci_high: float
    effect_name: str
    p_value: float
    method_used: str
    n_per_group: tuple[int, ...]
    group_labels: tuple[str, ...]
    assumption_report: dict
    paired: bool
    artifact_id: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["n_per_group"] = list(self.n_per_group)
        d["group_labels"] = list(self.group_labels)
        return d
