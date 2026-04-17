#!/usr/bin/env python3
"""Seed all sample data for a fresh dev environment.

Runs three things in order:
  1. ``app.data.db_init.initialize_db()`` — load any bank-macro / bank-revenue
     CSVs into the shared analytical DuckDB.
  2. ``scripts.seed_eval_data`` — generate deterministic eval data into
     ``data/duckdb/eval.db``.
  3. Print a one-line summary of what's loaded.

Run: ``python -m scripts.seed_data``
Or:  ``make seed-data``
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import duckdb

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("seed_data")


def _summarize_db(path: Path, label: str) -> None:
    if not path.exists():
        log.info("%s db: %s — does not exist (skipped)", label, path)
        return
    try:
        conn = duckdb.connect(str(path), read_only=True)
        try:
            tables = conn.execute("SHOW TABLES").fetchall()
            if not tables:
                log.info("%s db: %s — 0 tables", label, path)
                return
            counts: list[str] = []
            for (tbl,) in tables:
                row = conn.execute(f'SELECT COUNT(*) FROM "{tbl}"').fetchone()
                n = row[0] if row else 0
                counts.append(f'{tbl}({n:,})')
            log.info("%s db: %s — %s", label, path, ", ".join(counts))
        finally:
            conn.close()
    except duckdb.Error as exc:
        log.warning("%s db: %s — could not summarize: %s", label, path, exc)


def main(argv: list[str] | None = None) -> int:
    log.info("=== seed_data: initializing analytical DB (db_init) ===")
    try:
        from app.data.db_init import initialize_db

        initialize_db()
    except Exception as exc:  # noqa: BLE001  pragma: no cover
        log.error("db_init failed: %s", exc)
        return 1

    log.info("=== seed_data: generating eval dataset (seed_eval_data) ===")
    try:
        from scripts.seed_eval_data import DB_PATH, seed_all

        counts = seed_all(DB_PATH)
        for table, count in counts.items():
            log.info("  %s: %d rows", table, count)
    except Exception as exc:  # noqa: BLE001
        log.error("seed_eval_data failed: %s", exc)
        return 1

    log.info("=== seed_data: summary ===")
    backend = Path(__file__).resolve().parent.parent
    _summarize_db(backend / "data" / "duckdb" / "analytical.db", "analytical")
    _summarize_db(backend / "data" / "duckdb" / "eval.db", "eval")

    log.info("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
