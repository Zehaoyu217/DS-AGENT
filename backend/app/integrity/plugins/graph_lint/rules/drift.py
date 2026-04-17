from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext


def run_added(ctx: ScanContext, config: dict[str, Any], today: date) -> list[IntegrityIssue]:
    return []


def run_removed(ctx: ScanContext, config: dict[str, Any], today: date) -> list[IntegrityIssue]:
    return []
