"""geocoder — locality/address -> (lat, lng), cached in geocode_cache.

Resolution order:
  1. geocode_cache (already resolved before).
  2. LOCALITY_WHITELIST centroid (free, deterministic).
  3. External provider hook (left as an injectable callable; not wired in the
     dry run so the pipeline runs offline). Results are written back to cache.

Replaces re-geocoding the same localities every run (§9).
"""

from __future__ import annotations

import sqlite3
from typing import Callable, Optional

from config import settings
from lib.state_store import now_iso

ProviderFn = Callable[[str], Optional[tuple[float, float]]]


def _normalize(query: str) -> str:
    return " ".join(query.strip().lower().split())


def geocode(
    conn: sqlite3.Connection,
    query: str,
    provider: ProviderFn | None = None,
) -> Optional[tuple[float, float]]:
    if not query:
        return None
    key = _normalize(query)

    row = conn.execute(
        "SELECT lat, lng FROM geocode_cache WHERE query=?", (key,)
    ).fetchone()
    if row and row["lat"] is not None:
        return (row["lat"], row["lng"])

    coord: Optional[tuple[float, float]] = None
    source = None

    if key in settings.LOCALITY_WHITELIST:
        coord = settings.LOCALITY_WHITELIST[key]
        source = "whitelist"
    else:
        # Match on whitelist substring (e.g. "plot near patia, bbsr").
        for name, c in settings.LOCALITY_WHITELIST.items():
            if name in key:
                coord, source = c, "whitelist"
                break

    if coord is None and provider is not None:
        coord = provider(query)
        source = "provider"

    if coord is not None:
        conn.execute(
            "INSERT OR REPLACE INTO geocode_cache(query, lat, lng, source, cached_at) "
            "VALUES (?,?,?,?,?)",
            (key, coord[0], coord[1], source, now_iso()),
        )
        conn.commit()

    return coord


def is_whitelisted(locality: str | None) -> bool:
    if not locality:
        return False
    key = _normalize(locality)
    if key in settings.LOCALITY_WHITELIST:
        return True
    return any(name in key for name in settings.LOCALITY_WHITELIST)
