"""budget_filter — apply the ₹1.5 Cr ceiling + locality whitelist BEFORE
extraction/scoring, and compute required_loan + comfort tier (§5, §7).

No lower bound: a cheaper-but-viable plot is preferred by the value score.
"""

from __future__ import annotations

from typing import Any, Optional

from config import settings
from lib.geocoder import is_whitelisted


def required_loan(est_price: Optional[float], equity: float = settings.EQUITY_MAX) -> Optional[float]:
    """Implied loan = price − equity (using the upper equity bound by default)."""
    if est_price is None:
        return None
    return round(max(0.0, est_price - equity), 2)


def comfort_tier(loan: Optional[float]) -> str:
    if loan is None:
        return "unknown"
    for label, ceiling in settings.COMFORT_TIERS:
        if loan <= ceiling:
            return label
    return "stretch"


def financeability_flag(est_price: Optional[float], loan: Optional[float]) -> Optional[str]:
    """Surface (don't block) when the implied loan exceeds typical raw-land LTV."""
    if est_price is None or loan is None or est_price <= 0:
        return None
    if loan / est_price > settings.RAW_LAND_MAX_LTV:
        return "verify financeability"
    return None


def assess(record: dict[str, Any]) -> dict[str, Any]:
    """Annotate a record with budget fields. Does not drop; see passes_filter."""
    price = record.get("price_inr")
    loan = required_loan(price)
    record["required_loan"] = loan
    record["comfort_tier"] = comfort_tier(loan)
    flag = financeability_flag(price, loan)
    if flag:
        record.setdefault("red_flags", [])
        if flag not in record["red_flags"]:
            record["red_flags"].append(flag)
    return record


def passes_filter(record: dict[str, Any]) -> tuple[bool, str]:
    """Gate run BEFORE extraction/scoring. Returns (keep, reason_if_dropped)."""
    if not is_whitelisted(record.get("locality")):
        return False, f"locality not in whitelist: {record.get('locality')!r}"
    price = record.get("price_inr")
    # Unknown price is kept (extraction may recover it); only a known
    # over-ceiling price is dropped.
    if price is not None and price > settings.BUDGET_CEILING:
        return False, f"price ₹{price:,.0f} exceeds ceiling ₹{settings.BUDGET_CEILING:,.0f}"
    return True, ""


def filter_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    kept, dropped = [], []
    for rec in records:
        ok, reason = passes_filter(rec)
        if ok:
            kept.append(assess(rec))
        else:
            rec["_dropped_reason"] = reason
            dropped.append(rec)
    return kept, dropped
