"""scoring — deterministic reference scorer producing the §3 output contract.

This is the "graduate to code" half of scoring: the common, rule-based case is
scored here for zero tokens. The Sonnet `scorer` subagent only adjudicates the
ambiguous residue (unclear commercial potential, borderline red flags) and may
override bands, but it inherits this contract shape and these hard gates.

Output contract (§3):
  { value_band, commercial_band, confidence, missing_fields[], red_flags[],
    zoning_status, est_price, required_loan }
Plus surfaced extras: comfort_tier, distances, price_per_sqft, n_comparables.

Confident-wrong is the enemy (§0):
  - no value_band without >= MIN_COMPARABLES comparables;
  - no top-tier commercial band when zoning is unknown/verify;
  - every score carries a confidence band + missing_fields list.
"""

from __future__ import annotations

from typing import Any, Optional

from config import settings
from lib import budget_filter, red_flag_rules
from lib.distance_engine import distances_for_plot

# Fields we expect for a confident score; absence lowers confidence + is listed.
# zoning_status is handled separately (it arrives as an argument, and 'verify'/
# 'unknown' counts as missing).
EXPECTED_FIELDS = (
    "price_inr", "area_sqft", "locality", "lat", "lng",
    "road_width_ft", "plot_no",
)
UNRESOLVED_ZONING = ("verify", "unknown")


def value_band(
    price_per_sqft: Optional[float],
    baseline: Optional[dict[str, Any]],
) -> tuple[Optional[str], Optional[str]]:
    """Return (band, gate_reason). band is None when the comparables gate fails."""
    if baseline is None or baseline.get("n_comparables", 0) < settings.MIN_COMPARABLES:
        n = baseline.get("n_comparables", 0) if baseline else 0
        return None, f"value gate: only {n} comparables (need {settings.MIN_COMPARABLES})"
    if not price_per_sqft:
        return None, "value gate: price/sqft unknown"

    median = baseline["median_price_per_sqft"]
    premium = (price_per_sqft - median) / median if median else 0.0
    for band, max_premium in settings.VALUE_BANDS:
        if premium <= max_premium:
            return band, None
    return "D", None


def commercial_band(
    zoning_status: str,
    distances: dict[str, float],
    road_width_ft: Optional[float],
) -> tuple[str, list[str]]:
    """Coarse commercial-potential band. Top tier (A) gated on zoning (§3)."""
    notes: list[str] = []
    # Proximity signal: closer to arterial (NH-16) + catchment (campus/IT) is better.
    score = 0
    if distances.get("nh16", 99) <= 1.0:
        score += 2
    elif distances.get("nh16", 99) <= 3.0:
        score += 1
    if distances.get("kiit_soa", 99) <= 2.0 or distances.get("infocity", 99) <= 2.0:
        score += 2
    elif distances.get("kiit_soa", 99) <= 5.0 or distances.get("infocity", 99) <= 5.0:
        score += 1
    if road_width_ft and road_width_ft >= 40:
        score += 1
    elif road_width_ft is None:
        notes.append("road_width unknown")

    if score >= 4:
        raw_band = "A"
    elif score >= 2:
        raw_band = "B"
    else:
        raw_band = "C"

    # Hard gate: cannot reach top tier without commercial/mixed zoning.
    if raw_band == "A" and zoning_status not in settings.ZONING_TOP_TIER_OK:
        notes.append("top-tier blocked: zoning not commercial/mixed")
        raw_band = "B"
    return raw_band, notes


def confidence_level(missing_fields: list[str], red_flags: list[str]) -> str:
    if len(missing_fields) >= 4 or red_flags:
        return "low"
    if len(missing_fields) >= 2:
        return "medium"
    return "high"


def score_plot(
    record: dict[str, Any],
    baseline: Optional[dict[str, Any]],
    zoning_status: str = "verify",
) -> dict[str, Any]:
    """Score a single resolved plot into the output contract."""
    missing = [f for f in EXPECTED_FIELDS if record.get(f) in (None, "")]
    if zoning_status in UNRESOLVED_ZONING:
        missing.append("zoning_status")

    lat, lng = record.get("lat"), record.get("lng")
    distances = distances_for_plot(lat, lng) if lat is not None and lng is not None else {}

    baseline_median = baseline.get("median_price_per_sqft") if baseline else None
    flags = red_flag_rules.evaluate(record, baseline_median)

    vband, vgate = value_band(record.get("price_per_sqft"), baseline)
    if vgate:
        missing.append(vgate)

    cband, cnotes = commercial_band(zoning_status, distances, record.get("road_width_ft"))

    est_price = record.get("price_inr")
    loan = budget_filter.required_loan(est_price)
    tier = budget_filter.comfort_tier(loan)

    # Top-tier blockers downgrade commercial band defensively.
    if red_flag_rules.blocks_top_tier(flags) and cband == "A":
        cband = "B"
        cnotes.append("top-tier blocked: red flag")

    return {
        "value_band": vband,
        "commercial_band": cband,
        "confidence": confidence_level(missing, flags),
        "missing_fields": missing,
        "red_flags": flags,
        "zoning_status": zoning_status,
        "est_price": est_price,
        "required_loan": loan,
        "comfort_tier": tier,
        # surfaced extras (not part of the strict contract but persisted)
        "price_per_sqft": record.get("price_per_sqft"),
        "n_comparables": baseline.get("n_comparables", 0) if baseline else 0,
        "distances_km": distances,
        "commercial_notes": cnotes,
    }


# Composite ordinal used only for ranking/eval (not part of the contract).
_VALUE_RANK = {"A": 4, "B": 3, "C": 2, "D": 1, None: 0}
_COMM_RANK = {"A": 3, "B": 2, "C": 1, None: 0}


def rank_key(scored: dict[str, Any]) -> tuple:
    """Sort key: best plots first. Blockers sink to the bottom."""
    blocked = red_flag_rules.blocks_top_tier(scored.get("red_flags", []))
    return (
        0 if blocked else 1,
        _VALUE_RANK.get(scored.get("value_band"), 0) + _COMM_RANK.get(scored.get("commercial_band"), 0),
        -(scored.get("required_loan") or 0),
    )
