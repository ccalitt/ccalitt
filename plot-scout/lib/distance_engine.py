"""distance_engine — distances from a plot to Bhubaneswar landmarks.

Pure math, zero tokens (§9). Distances in kilometres. NH-16 is modelled as a
polyline and we return the distance to the nearest point on it.
"""

from __future__ import annotations

import math
from typing import Iterable

from config import settings

EARTH_RADIUS_KM = 6371.0088


def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Great-circle distance between two (lat, lng) points, in km."""
    lat1, lng1 = map(math.radians, a)
    lat2, lng2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(h))


def _point_to_segment_km(
    p: tuple[float, float], a: tuple[float, float], b: tuple[float, float]
) -> float:
    """Distance from point p to segment a-b, using a local equirectangular
    projection (accurate at city scale)."""
    lat0 = math.radians((a[0] + b[0]) / 2)

    def to_xy(pt: tuple[float, float]) -> tuple[float, float]:
        x = math.radians(pt[1]) * math.cos(lat0) * EARTH_RADIUS_KM
        y = math.radians(pt[0]) * EARTH_RADIUS_KM
        return x, y

    px, py = to_xy(p)
    ax, ay = to_xy(a)
    bx, by = to_xy(b)
    dx, dy = bx - ax, by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg_len_sq))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def distance_to_polyline_km(
    p: tuple[float, float], polyline: Iterable[tuple[float, float]]
) -> float:
    pts = list(polyline)
    return min(
        _point_to_segment_km(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1)
    )


def distances_for_plot(lat: float, lng: float) -> dict[str, float]:
    """All rubric-relevant distances (km) for a plot, rounded to 2 dp."""
    p = (lat, lng)
    out = {name: round(haversine_km(p, coord), 2) for name, coord in settings.LANDMARKS.items()}
    out["nh16"] = round(distance_to_polyline_km(p, settings.NH16_POLYLINE), 2)
    # Convenience composite used by the rubric (nearest of the two campuses).
    out["kiit_soa"] = round(min(out["kiit"], out["soa"]), 2)
    return out
