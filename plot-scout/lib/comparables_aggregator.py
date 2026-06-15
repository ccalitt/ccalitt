"""comparables_aggregator — per-locality, per-sqft-band ₹/sqft distribution.

Computes median + p25/p75 + n_comparables deterministically and persists to
price_baseline. This IS the value-score gate: the scorer refuses a value band
when n_comparables < MIN_COMPARABLES (§3, §9).
"""

from __future__ import annotations

import sqlite3
import statistics
from typing import Any, Optional

from config import settings
from lib.geocoder import _normalize
from lib.state_store import now_iso


def sqft_band(area_sqft: Optional[float]) -> str:
    if area_sqft is None:
        return "unknown"
    for name, lo, hi in settings.SQFT_BANDS:
        if lo <= area_sqft < hi:
            return name
    return "unknown"


def rebuild_baseline(conn: sqlite3.Connection) -> int:
    """Recompute price_baseline from all candidates with a known ₹/sqft.

    Returns the number of (locality, band) cells written.
    """
    rows = conn.execute(
        "SELECT locality, area_sqft, price_inr FROM candidates "
        "WHERE price_inr IS NOT NULL AND area_sqft IS NOT NULL AND area_sqft > 0"
    ).fetchall()

    cells: dict[tuple[str, str], list[float]] = {}
    for r in rows:
        loc = _normalize(r["locality"] or "")
        if not loc:
            continue
        band = sqft_band(r["area_sqft"])
        ppsf = r["price_inr"] / r["area_sqft"]
        cells.setdefault((loc, band), []).append(ppsf)

    ts = now_iso()
    written = 0
    for (loc, band), vals in cells.items():
        vals.sort()
        median = round(statistics.median(vals), 2)
        p25 = round(_percentile(vals, 25), 2)
        p75 = round(_percentile(vals, 75), 2)
        conn.execute(
            "INSERT INTO price_baseline(locality, sqft_band, median_price_per_sqft, "
            "p25_price_per_sqft, p75_price_per_sqft, n_comparables, updated_at) "
            "VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(locality, sqft_band) DO UPDATE SET "
            "median_price_per_sqft=excluded.median_price_per_sqft, "
            "p25_price_per_sqft=excluded.p25_price_per_sqft, "
            "p75_price_per_sqft=excluded.p75_price_per_sqft, "
            "n_comparables=excluded.n_comparables, updated_at=excluded.updated_at",
            (loc, band, median, p25, p75, len(vals), ts),
        )
        written += 1
    conn.commit()
    return written


def get_baseline(
    conn: sqlite3.Connection, locality: str, area_sqft: Optional[float]
) -> Optional[dict[str, Any]]:
    band = sqft_band(area_sqft)
    row = conn.execute(
        "SELECT * FROM price_baseline WHERE locality=? AND sqft_band=?",
        (_normalize(locality or ""), band),
    ).fetchone()
    if row is None:
        return None
    return dict(row)


def coverage(conn: sqlite3.Connection) -> dict[str, Any]:
    """Baseline coverage stats for the weekly digest (§6)."""
    total = conn.execute("SELECT COUNT(*) AS c FROM price_baseline").fetchone()["c"]
    gated = conn.execute(
        "SELECT COUNT(*) AS c FROM price_baseline WHERE n_comparables >= ?",
        (settings.MIN_COMPARABLES,),
    ).fetchone()["c"]
    return {
        "cells": total,
        "cells_meeting_gate": gated,
        "min_comparables": settings.MIN_COMPARABLES,
        "coverage_pct": round(100 * gated / total, 1) if total else 0.0,
    }


def _percentile(sorted_vals: list[float], pct: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * pct / 100.0
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)
