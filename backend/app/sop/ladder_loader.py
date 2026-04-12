"""Load ladder YAML files into LadderDefinition objects."""
from __future__ import annotations

from pathlib import Path

import yaml

from app.sop.types import LadderDefinition

LADDERS_DIR = Path(__file__).parent / "ladders"


def load_ladder(bucket: str) -> LadderDefinition:
    """Load one ladder by bucket name (e.g. 'context', 'evaluation_bias')."""
    slug = bucket.replace("_", "-")
    for path in LADDERS_DIR.glob(f"*{slug}.yaml"):
        data = yaml.safe_load(path.read_text())
        return LadderDefinition.model_validate(data)
    raise FileNotFoundError(f"No ladder YAML for bucket {bucket!r} in {LADDERS_DIR}")


def load_all_ladders() -> list[LadderDefinition]:
    """Load every ladder YAML in order of filename (which is cost of triage)."""
    ladders = []
    for path in sorted(LADDERS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        ladders.append(LadderDefinition.model_validate(data))
    return ladders
