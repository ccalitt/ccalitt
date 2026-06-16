"""dedup_matcher — deterministic entity resolution scaffold.

Blocking + similarity on geo + area + price + phone produces a canonical key,
so the LLM never has to reason "is this the same plot?" for the common case
(§9). The Sonnet `resolver` subagent is reserved only for genuinely ambiguous
clusters this leaves behind.
"""

from __future__ import annotations

import math
import re
from typing import Any, Optional

from lib.distance_engine import haversine_km

# Two listings are candidate-same if within this geo radius AND areas/prices are
# close. Tuned conservative — better to leave a hard case for the resolver than
# to merge two different plots.
GEO_RADIUS_KM = 0.15          # ~150 m
AREA_TOLERANCE = 0.10         # ±10%
PRICE_TOLERANCE = 0.10        # ±10%


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    return digits[-10:] if len(digits) >= 10 else None


def blocking_key(record: dict[str, Any]) -> str:
    """Coarse key to bucket potential duplicates cheaply before pairwise compare.

    Rounds geo to ~1 km grid and buckets area; phone is a strong secondary key.
    """
    lat, lng = record.get("lat"), record.get("lng")
    geo = f"{round(lat, 2)},{round(lng, 2)}" if lat is not None and lng is not None else "nogeo"
    area = record.get("area_sqft")
    area_bucket = int(area // 500) if area else -1
    return f"{geo}|{area_bucket}"


def _close(a: Optional[float], b: Optional[float], tol: float) -> bool:
    if a is None or b is None:
        return False
    if a == 0 or b == 0:
        return a == b
    return abs(a - b) / max(a, b) <= tol


def same_plot(r1: dict[str, Any], r2: dict[str, Any]) -> bool:
    """Deterministic same-physical-plot decision."""
    p1, p2 = normalize_phone(r1.get("phone")), normalize_phone(r2.get("phone"))
    phone_match = p1 is not None and p1 == p2

    geo_match = False
    if all(r1.get(k) is not None for k in ("lat", "lng")) and all(
        r2.get(k) is not None for k in ("lat", "lng")
    ):
        d = haversine_km((r1["lat"], r1["lng"]), (r2["lat"], r2["lng"]))
        geo_match = d <= GEO_RADIUS_KM

    area_match = _close(r1.get("area_sqft"), r2.get("area_sqft"), AREA_TOLERANCE)
    price_match = _close(r1.get("price_inr"), r2.get("price_inr"), PRICE_TOLERANCE)

    # Same plot if: same phone + similar area, OR co-located + similar area + price.
    if phone_match and area_match:
        return True
    if geo_match and area_match and price_match:
        return True
    return False


def cluster(records: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group records into canonical clusters via blocking then pairwise union."""
    buckets: dict[str, list[dict[str, Any]]] = {}
    for rec in records:
        buckets.setdefault(blocking_key(rec), []).append(rec)

    clusters: list[list[dict[str, Any]]] = []
    for bucket in buckets.values():
        local: list[list[dict[str, Any]]] = []
        for rec in bucket:
            placed = False
            for grp in local:
                if any(same_plot(rec, other) for other in grp):
                    grp.append(rec)
                    placed = True
                    break
            if not placed:
                local.append([rec])
        clusters.extend(local)
    return clusters


def canonical_key(group: list[dict[str, Any]]) -> str:
    """Stable key for a resolved plot cluster (geo + area signature)."""
    lats = [r["lat"] for r in group if r.get("lat") is not None]
    lngs = [r["lng"] for r in group if r.get("lng") is not None]
    areas = [r["area_sqft"] for r in group if r.get("area_sqft") is not None]
    lat = round(sum(lats) / len(lats), 4) if lats else 0.0
    lng = round(sum(lngs) / len(lngs), 4) if lngs else 0.0
    area = round(sum(areas) / len(areas)) if areas else 0
    return f"{lat},{lng}|{area}"
