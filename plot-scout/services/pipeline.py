"""pipeline — deterministic orchestration spine for the dry-run gate (§11).

Runs the full flow on ONE locality with NO schedules and NO live network:
  scouts -> budget_filter -> extractor_helpers -> resolver(dedup) ->
  baseline-keeper -> scorer(deterministic) -> zoning-checker -> diligence ->
  report_renderer + evaluator vs gold set.

This is the deterministic backbone. In production the Sonnet `resolver`/`scorer`
subagents adjudicate only the ambiguous residue this leaves behind; everything
here costs zero tokens. Schedules/channels (§8) are wired ONLY after the owner
approves the dry-run output.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Optional

from config import settings
from lib import (
    budget_filter,
    comparables_aggregator,
    dedup_matcher,
    extractor_helpers,
    bhulekh_lookup,
    report_renderer,
    scoring,
    state_store,
)
from lib.geocoder import _normalize, geocode
from lib.source_adapters import REGISTRY
from services import evaluator


def _collect(sources: Optional[list[str]] = None) -> list[dict[str, Any]]:
    """Run the configured scouts and return normalized records."""
    sources = sources or list(REGISTRY)
    records: list[dict[str, Any]] = []
    for name in sources:
        adapter = REGISTRY[name]()
        records.extend(adapter.collect())
    return records


def _persist_candidate(conn: sqlite3.Connection, rec: dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO candidates(source, source_id, url, price_inr, area_sqft, area_raw, "
        "locality, lat, lng, phone, text, photos, plot_no, khata_no, content_hash, "
        "fetched_at, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(source, source_id) DO UPDATE SET "
        "price_inr=excluded.price_inr, area_sqft=excluded.area_sqft, text=excluded.text, "
        "content_hash=excluded.content_hash, fetched_at=excluded.fetched_at",
        (
            rec["source"], rec["source_id"], rec.get("url"), rec.get("price_inr"),
            rec.get("area_sqft"), rec.get("area_raw"), rec.get("locality"),
            rec.get("lat"), rec.get("lng"), rec.get("phone"), rec.get("text"),
            json.dumps(rec.get("photos", [])), rec.get("plot_no"), rec.get("khata_no"),
            rec.get("content_hash"), rec.get("fetched_at"), state_store.now_iso(),
        ),
    )


def _persist_canonical(conn: sqlite3.Connection, plot: dict[str, Any]) -> None:
    ts = state_store.now_iso()
    conn.execute(
        "INSERT INTO canonical_plots(canonical_key, locality, lat, lng, area_sqft, "
        "price_inr, phone, plot_no, khata_no, value_band, commercial_band, confidence, "
        "missing_fields, red_flags, zoning_status, est_price, required_loan, comfort_tier, "
        "n_sources, first_seen, last_seen, updated_at) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(canonical_key) DO UPDATE SET "
        "value_band=excluded.value_band, commercial_band=excluded.commercial_band, "
        "confidence=excluded.confidence, missing_fields=excluded.missing_fields, "
        "red_flags=excluded.red_flags, zoning_status=excluded.zoning_status, "
        "est_price=excluded.est_price, required_loan=excluded.required_loan, "
        "comfort_tier=excluded.comfort_tier, n_sources=excluded.n_sources, "
        "last_seen=excluded.last_seen, updated_at=excluded.updated_at",
        (
            plot["canonical_key"], plot.get("locality"), plot.get("lat"), plot.get("lng"),
            plot.get("area_sqft"), plot.get("price_inr"), plot.get("phone"),
            plot.get("plot_no"), plot.get("khata_no"), plot.get("value_band"),
            plot.get("commercial_band"), plot.get("confidence"),
            json.dumps(plot.get("missing_fields", [])), json.dumps(plot.get("red_flags", [])),
            plot.get("zoning_status"), plot.get("est_price"), plot.get("required_loan"),
            plot.get("comfort_tier"), plot.get("n_sources", 1), ts, ts, ts,
        ),
    )


def run_dry_run(
    locality: str,
    db_path: Optional[str] = None,
    sources: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Full deterministic pipeline on ONE locality. Returns a result summary."""
    target = _normalize(locality)
    with state_store.session(db_path) as conn:
        run_id = state_store.new_run_id()

        # 1. Scouts -> normalized records
        raw_records = _collect(sources)
        state_store.log_stage(conn, run_id, "scout", records_out=len(raw_records))

        # Restrict to the target locality for the dry run.
        records = [r for r in raw_records if _normalize(r.get("locality", "")) == target
                   or target in _normalize(r.get("locality", ""))]

        # 2. Delta sourcing — skip unchanged
        new_changed, unchanged = state_store.diff_records(conn, records)
        state_store.log_stage(conn, run_id, "delta", records_in=len(records),
                              records_out=len(new_changed),
                              notes=f"{len(unchanged)} unchanged skipped")

        # 3. Geocode (fills lat/lng from whitelist) + budget filter BEFORE extraction
        for r in new_changed:
            if r.get("lat") is None or r.get("lng") is None:
                coord = geocode(conn, r.get("locality", ""))
                if coord:
                    r["lat"], r["lng"] = coord
        kept, dropped = budget_filter.filter_records(new_changed)
        state_store.log_stage(conn, run_id, "budget_filter", records_in=len(new_changed),
                              records_out=len(kept),
                              notes=f"{len(dropped)} dropped (ceiling/whitelist)")

        # 4. Deterministic extraction
        for r in kept:
            extractor_helpers.enrich(r)
            _persist_candidate(conn, r)
        conn.commit()
        state_store.log_stage(conn, run_id, "extract", records_out=len(kept))

        # 5. Baseline (comparables) — rebuild from all candidates seen so far
        cells = comparables_aggregator.rebuild_baseline(conn)
        state_store.log_stage(conn, run_id, "baseline", records_out=cells)

        # 6. Resolver — dedup into canonical plots
        clusters = dedup_matcher.cluster(kept)
        state_store.log_stage(conn, run_id, "resolve", records_in=len(kept),
                              records_out=len(clusters))

        # 7. Zoning + 8. Score each canonical plot
        scored_plots: list[dict[str, Any]] = []
        for grp in clusters:
            rep = _representative(grp)
            zoning = bhulekh_lookup.lookup(rep.get("plot_no"), rep.get("khata_no"),
                                           rep.get("locality"))
            baseline = comparables_aggregator.get_baseline(conn, rep.get("locality", ""),
                                                           rep.get("area_sqft"))
            result = scoring.score_plot(rep, baseline, zoning["zoning_status"])
            plot = {**rep, **result, "canonical_key": dedup_matcher.canonical_key(grp),
                    "n_sources": len(grp)}
            _persist_canonical(conn, plot)
            scored_plots.append(plot)
        conn.commit()
        state_store.log_stage(conn, run_id, "score", records_out=len(scored_plots))

        # Rank best -> worst
        scored_plots.sort(key=scoring.rank_key, reverse=True)

        # 9. Evaluate vs gold set
        eval_summary = evaluator.evaluate(conn, scored_plots)
        state_store.log_stage(conn, run_id, "evaluate", status="ok",
                              notes=eval_summary.get("status", ""))

        coverage = comparables_aggregator.coverage(conn)
        digest = report_renderer.render_digest(scored_plots, title=f"dry run · {locality}")

        return {
            "run_id": run_id,
            "locality": locality,
            "raw_count": len(raw_records),
            "target_count": len(records),
            "kept": len(kept),
            "dropped": len(dropped),
            "canonical_plots": len(scored_plots),
            "coverage": coverage,
            "evaluation": eval_summary,
            "scored": scored_plots,
            "digest": digest,
            "dropped_records": [
                {"locality": d.get("locality"), "reason": d.get("_dropped_reason")}
                for d in dropped
            ],
        }


def _representative(group: list[dict[str, Any]]) -> dict[str, Any]:
    """Pick the most complete record in a cluster as the canonical representative."""
    def completeness(r: dict[str, Any]) -> int:
        return sum(1 for k in ("price_inr", "area_sqft", "lat", "lng", "plot_no", "khata_no")
                   if r.get(k) not in (None, ""))
    best = max(group, key=completeness)
    # Prefer the lowest known price across the cluster (value-favouring).
    prices = [r["price_inr"] for r in group if r.get("price_inr")]
    rep = dict(best)
    if prices:
        rep["price_inr"] = min(prices)
        rep["price_per_sqft"] = extractor_helpers.price_per_sqft(rep["price_inr"], rep.get("area_sqft"))
    return rep
