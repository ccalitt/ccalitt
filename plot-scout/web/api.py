"""Read-side API for the browse UI.

Pure functions that turn the SQLite DB into JSON-able dicts. Distances and the
diligence checklist are recomputed on the fly (cheap, deterministic) rather than
denormalized into the DB.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import date, timedelta
from typing import Any, Optional

from config import settings
from lib import budget_filter, comparables_aggregator, report_renderer, scoring
from lib.distance_engine import distances_for_plot
from services import evaluator


def _row_to_plot(row: sqlite3.Row) -> dict[str, Any]:
    plot = dict(row)
    plot["red_flags"] = json.loads(plot.get("red_flags") or "[]")
    plot["missing_fields"] = json.loads(plot.get("missing_fields") or "[]")
    area = plot.get("area_sqft")
    price = plot.get("est_price")
    plot["price_per_sqft"] = round(price / area, 2) if price and area else None
    return plot


def _ranked(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM canonical_plots").fetchall()
    plots = [_row_to_plot(r) for r in rows]
    plots.sort(key=scoring.rank_key, reverse=True)
    for i, p in enumerate(plots, 1):
        p["rank"] = i
    return plots


def list_plots(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _ranked(conn)


def get_plot(conn: sqlite3.Connection, plot_id: int) -> Optional[dict[str, Any]]:
    row = conn.execute("SELECT * FROM canonical_plots WHERE id=?", (plot_id,)).fetchone()
    if row is None:
        return None
    plot = _row_to_plot(row)

    # rank within the full ranking
    for p in _ranked(conn):
        if p["id"] == plot_id:
            plot["rank"] = p["rank"]
            break

    lat, lng = plot.get("lat"), plot.get("lng")
    plot["distances_km"] = distances_for_plot(lat, lng) if lat is not None and lng is not None else {}

    plot["comparables"] = comparables_aggregator.get_baseline(
        conn, plot.get("locality", ""), plot.get("area_sqft")
    )

    members = conn.execute(
        "SELECT source, source_id, url, price_inr, area_sqft, phone, fetched_at "
        "FROM candidates WHERE canonical_id=?", (plot_id,)
    ).fetchall()
    plot["sources"] = [dict(m) for m in members]

    plot["financeability"] = budget_filter.financeability_flag(
        plot.get("est_price"), plot.get("required_loan")
    )
    plot["diligence_checklist"] = report_renderer.render_diligence_checklist(plot)
    return plot


def get_landmarks() -> dict[str, Any]:
    return {
        "landmarks": {k: {"lat": v[0], "lng": v[1]} for k, v in settings.LANDMARKS.items()},
        "nh16": [{"lat": p[0], "lng": p[1]} for p in settings.NH16_POLYLINE],
        "whitelist": {k: {"lat": v[0], "lng": v[1]} for k, v in settings.LOCALITY_WHITELIST.items()},
    }


def get_localities(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    counts = {
        r["locality"]: r["c"]
        for r in conn.execute(
            "SELECT locality, COUNT(*) c FROM canonical_plots GROUP BY locality"
        ).fetchall()
    }
    out = []
    for name in settings.LOCALITY_WHITELIST:
        out.append({"key": name, "label": name.title(),
                    "plots": counts.get(name.title(), counts.get(name, 0))})
    return out


def _sprint_days_left() -> int:
    try:
        start = date.fromisoformat(settings.SPRINT_START)
    except ValueError:
        return settings.SPRINT_WEEKS * 7
    end = start + timedelta(weeks=settings.SPRINT_WEEKS)
    return (end - date.today()).days


def get_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    plots = _ranked(conn)
    candidates = conn.execute("SELECT COUNT(*) c FROM candidates").fetchone()["c"]
    localities = conn.execute(
        "SELECT COUNT(DISTINCT locality) c FROM canonical_plots"
    ).fetchone()["c"]
    gold_size = conn.execute("SELECT COUNT(*) c FROM gold_set").fetchone()["c"]
    flagged = sum(1 for p in plots if p["red_flags"])
    gated = sum(1 for p in plots if p["value_band"] is None)

    return {
        "candidates": candidates,
        "canonical_plots": len(plots),
        "localities_with_data": localities,
        "flagged_plots": flagged,
        "value_gated_plots": gated,
        "coverage": comparables_aggregator.coverage(conn),
        "evaluation": evaluator.evaluate(conn, plots),
        "gold_set_size": gold_size,
        "budget": {
            "ceiling": settings.BUDGET_CEILING,
            "equity_min": settings.EQUITY_MIN,
            "equity_max": settings.EQUITY_MAX,
        },
        "sprint": {
            "start": settings.SPRINT_START,
            "weeks": settings.SPRINT_WEEKS,
            "days_left": _sprint_days_left(),
        },
    }


def get_reports(conn: sqlite3.Connection) -> dict[str, Any]:
    plots = _ranked(conn)
    coverage = comparables_aggregator.coverage(conn)
    eval_summary = evaluator.evaluate(conn, plots)
    return {
        "digest": report_renderer.render_digest(plots, top_n=5, title="plot-scout — top 5"),
        "weekly": report_renderer.render_weekly_report(plots, coverage, eval_summary, top_n=10),
    }
