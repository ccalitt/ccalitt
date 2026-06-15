"""red_flag_rules — deterministic red-flag detection (§3 HARD GATES, §9).

Catches the rule-based residue (fraud price, litigation keywords, agri-Kissam)
so the LLM only adjudicates genuinely ambiguous cases. Each rule returns a
machine-readable flag string; the scorer turns these into gate decisions.
"""

from __future__ import annotations

from typing import Any, Optional

from config import settings


def fraud_price_flag(
    price_per_sqft: Optional[float], baseline_median: Optional[float]
) -> Optional[str]:
    """Price-too-good-to-be-true vs locality/band median (§3)."""
    if not price_per_sqft or not baseline_median:
        return None
    if price_per_sqft < settings.FRAUD_PRICE_FRACTION * baseline_median:
        return "price_too_good_fraud_risk"
    return None


def litigation_flags(text: str) -> list[str]:
    text_l = (text or "").lower()
    hits = [kw for kw in settings.LITIGATION_KEYWORDS if kw in text_l]
    return [f"litigation_keyword:{kw}" for kw in hits]


def agri_kissam_flag(text: str) -> Optional[str]:
    """Agricultural Kissam without conversion evidence = block top tier."""
    text_l = (text or "").lower()
    is_agri = any(kw in text_l for kw in settings.AGRI_KISSAM_KEYWORDS)
    if not is_agri:
        return None
    has_conversion = any(kw in text_l for kw in settings.CONVERSION_EVIDENCE_KEYWORDS)
    if has_conversion:
        return None
    return "agri_kissam_no_conversion"


# Flags that block the top tier of the shortlist (§3 HARD GATES).
TOP_TIER_BLOCKERS = {"agri_kissam_no_conversion", "price_too_good_fraud_risk"}


def evaluate(record: dict[str, Any], baseline_median: Optional[float] = None) -> list[str]:
    """Run all rules; return a deduped list of red-flag strings."""
    flags: list[str] = list(record.get("red_flags", []))
    text = record.get("text", "")

    fraud = fraud_price_flag(record.get("price_per_sqft"), baseline_median)
    if fraud:
        flags.append(fraud)
    flags.extend(litigation_flags(text))
    agri = agri_kissam_flag(text)
    if agri:
        flags.append(agri)

    # dedupe, preserve order
    seen: set[str] = set()
    out: list[str] = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def blocks_top_tier(flags: list[str]) -> bool:
    return any(f in TOP_TIER_BLOCKERS for f in flags)
