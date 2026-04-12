"""Load ladder YAML files into LadderDefinition objects."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from app.sop.types import LadderDefinition

LADDERS_DIR = Path(__file__).parent / "ladders"

_BUCKET_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def _validate_bucket(bucket: str) -> None:
    """Raise ValueError if *bucket* contains characters that could cause path traversal."""
    if not _BUCKET_RE.match(bucket):
        raise ValueError(
            f"Invalid bucket name {bucket!r}: must match ^[a-z][a-z0-9_]*$"
        )


def load_ladder(bucket: str) -> LadderDefinition:
    """Load one ladder by bucket name (e.g. 'context', 'evaluation_bias')."""
    _validate_bucket(bucket)
    slug = bucket.replace("_", "-")
    for path in LADDERS_DIR.glob(f"[0-9][0-9]-{slug}.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            raise ValueError(f"Ladder YAML is empty: {path}")
        return LadderDefinition.model_validate(data)
    raise FileNotFoundError(f"No ladder YAML for bucket {bucket!r} in {LADDERS_DIR}")


def load_all_ladders() -> list[LadderDefinition]:
    """Load every ladder YAML in order of filename (which is cost of triage)."""
    ladders = []
    for path in sorted(LADDERS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            raise ValueError(f"Ladder YAML is empty: {path}")
        ladders.append(LadderDefinition.model_validate(data))
    return ladders
