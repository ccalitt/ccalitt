"""state_store — SQLite connection, schema bootstrap, delta sourcing, run-log.

Delta sourcing (§7): we hash each listing's salient fields and only treat it as
new/changed work when the hash differs from what we last saw. This is what keeps
the orchestrator from re-extracting or re-scoring unchanged plots.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

from config import settings


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def content_hash(record: dict[str, Any]) -> str:
    """Stable hash over the fields that matter for change detection."""
    salient = {
        "price_inr": record.get("price_inr"),
        "area_sqft": record.get("area_sqft"),
        "locality": (record.get("locality") or "").strip().lower(),
        "text": (record.get("text") or "").strip(),
        "phone": record.get("phone"),
    }
    blob = json.dumps(salient, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else settings.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection, schema_path: Path | None = None) -> None:
    schema = Path(schema_path) if schema_path else settings.SCHEMA_PATH
    conn.executescript(schema.read_text())
    conn.commit()


@contextmanager
def session(db_path: Path | str | None = None) -> Iterator[sqlite3.Connection]:
    """Open a connection with the schema guaranteed to exist."""
    conn = connect(db_path)
    try:
        init_db(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


# --------------------------------------------------------------------------
# Delta sourcing
# --------------------------------------------------------------------------
def diff_records(
    conn: sqlite3.Connection, records: Iterable[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split incoming records into (new_or_changed, unchanged).

    Updates state_store as a side effect. Each record must carry ``source`` and
    ``source_id``; ``content_hash`` is computed if absent.
    """
    new_or_changed: list[dict[str, Any]] = []
    unchanged: list[dict[str, Any]] = []
    ts = now_iso()

    for rec in records:
        h = rec.get("content_hash") or content_hash(rec)
        rec["content_hash"] = h
        row = conn.execute(
            "SELECT content_hash FROM state_store WHERE source=? AND source_id=?",
            (rec["source"], str(rec["source_id"])),
        ).fetchone()

        if row is None:
            conn.execute(
                "INSERT INTO state_store(source, source_id, content_hash, status, "
                "first_seen, last_seen) VALUES (?,?,?,?,?,?)",
                (rec["source"], str(rec["source_id"]), h, "seen", ts, ts),
            )
            new_or_changed.append(rec)
        elif row["content_hash"] != h:
            conn.execute(
                "UPDATE state_store SET content_hash=?, status='changed', last_seen=? "
                "WHERE source=? AND source_id=?",
                (h, ts, rec["source"], str(rec["source_id"])),
            )
            new_or_changed.append(rec)
        else:
            conn.execute(
                "UPDATE state_store SET last_seen=? WHERE source=? AND source_id=?",
                (ts, rec["source"], str(rec["source_id"])),
            )
            unchanged.append(rec)

    conn.commit()
    return new_or_changed, unchanged


# --------------------------------------------------------------------------
# Run log
# --------------------------------------------------------------------------
def new_run_id() -> str:
    return f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:6]}"


def log_stage(
    conn: sqlite3.Connection,
    run_id: str,
    stage: str,
    status: str = "ok",
    records_in: int | None = None,
    records_out: int | None = None,
    tokens_estimate: int = 0,
    notes: str = "",
    started_at: str | None = None,
    ended_at: str | None = None,
) -> None:
    conn.execute(
        "INSERT INTO run_log(run_id, stage, status, records_in, records_out, "
        "tokens_estimate, notes, started_at, ended_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (
            run_id, stage, status, records_in, records_out, tokens_estimate,
            notes, started_at or now_iso(), ended_at or now_iso(),
        ),
    )
    conn.commit()
