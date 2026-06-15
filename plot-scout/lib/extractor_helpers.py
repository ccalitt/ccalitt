"""extractor_helpers — deterministic field extraction (regex/rule).

Handles the easy fields so the LLM extractor only sees genuinely ambiguous text
(§9): area-unit normalization, ₹/sqft, corner/facing/road-width flags, price
parsing for Indian formats (lakh/crore, comma grouping).
"""

from __future__ import annotations

import re
from typing import Optional

# --------------------------------------------------------------------------
# Area units -> square feet
# --------------------------------------------------------------------------
SQFT_PER_UNIT = {
    "sqft": 1.0,
    "sft": 1.0,
    "sq ft": 1.0,
    "square feet": 1.0,
    "sqyd": 9.0,
    "sq yd": 9.0,
    "square yard": 9.0,
    "gaj": 9.0,
    "sqm": 10.7639,
    "sq m": 10.7639,
    "square meter": 10.7639,
    "square metre": 10.7639,
    "acre": 43560.0,
    "decimal": 435.6,       # Odisha decimal = 1/100 acre
    "cent": 435.6,
    "guntha": 1089.0,
    "katha": 720.0,         # Odisha katha (approx; varies — documented assumption)
    "kattha": 720.0,
    "bigha": 14400.0,       # regional approx; documented assumption
    "ground": 2400.0,
}

_AREA_RE = re.compile(
    r"(?P<value>\d[\d,]*\.?\d*)\s*(?P<unit>sq\s?ft|sft|sq\s?yd|sqyd|gaj|sq\s?m|sqm|"
    r"square\s+(?:feet|yard|meter|metre)|acre|decimal|cent|guntha|kat?tha|bigha|ground)",
    re.IGNORECASE,
)


def normalize_area_to_sqft(text: str) -> Optional[tuple[float, str]]:
    """Return (area_sqft, matched_raw) for the first area mention, else None."""
    m = _AREA_RE.search(text or "")
    if not m:
        return None
    value = float(m.group("value").replace(",", ""))
    unit = re.sub(r"\s+", " ", m.group("unit").strip().lower())
    factor = SQFT_PER_UNIT.get(unit)
    if factor is None:
        # collapse e.g. "square feet" already handled; fall back to sqft
        factor = SQFT_PER_UNIT.get(unit.replace(" ", ""), 1.0)
    return round(value * factor, 2), m.group(0).strip()


# --------------------------------------------------------------------------
# Price parsing (Indian conventions)
# --------------------------------------------------------------------------
_PRICE_RE = re.compile(
    r"(?:₹|rs\.?|inr)?\s*(?P<value>\d[\d,]*\.?\d*)\s*(?P<unit>cr|crore|crores|"
    r"l|lac|lakh|lakhs|k|thousand)?",
    re.IGNORECASE,
)
_PRICE_MULT = {
    "cr": 1_00_00_000, "crore": 1_00_00_000, "crores": 1_00_00_000,
    "l": 1_00_000, "lac": 1_00_000, "lakh": 1_00_000, "lakhs": 1_00_000,
    "k": 1_000, "thousand": 1_000,
}


def parse_price_inr(text: str) -> Optional[float]:
    """Parse a price like '₹1.2 Cr', 'Rs 85 lakh', '95,00,000' -> float INR."""
    if not text:
        return None
    m = _PRICE_RE.search(text)
    if not m or not m.group("value"):
        return None
    value = float(m.group("value").replace(",", ""))
    unit = (m.group("unit") or "").lower()
    return round(value * _PRICE_MULT.get(unit, 1.0), 2)


def price_per_sqft(price_inr: Optional[float], area_sqft: Optional[float]) -> Optional[float]:
    if not price_inr or not area_sqft:
        return None
    return round(price_inr / area_sqft, 2)


# --------------------------------------------------------------------------
# Boolean / categorical flags
# --------------------------------------------------------------------------
def is_corner_plot(text: str) -> bool:
    return bool(re.search(r"\bcorner\b", text or "", re.IGNORECASE))


_FACING_RE = re.compile(
    r"\b(north[\s-]?east|north[\s-]?west|south[\s-]?east|south[\s-]?west|"
    r"north|south|east|west)\b[\s-]*(?:facing|face)?",
    re.IGNORECASE,
)


def facing(text: str) -> Optional[str]:
    m = re.search(r"\b(north|south|east|west)(?:[\s-]?(east|west))?\b[\s-]*facing",
                  text or "", re.IGNORECASE)
    if not m:
        return None
    return m.group(0).lower().replace("facing", "").strip(" -")


_ROAD_RE = re.compile(
    r"(?P<value>\d{1,3}(?:\.\d+)?)\s*(?P<unit>ft|feet|foot|m|meter|metre)\b[\s-]*(?:wide\s*)?road",
    re.IGNORECASE,
)


def road_width_ft(text: str) -> Optional[float]:
    """Extract facing-road width in feet (converts metres if stated)."""
    m = _ROAD_RE.search(text or "")
    if not m:
        return None
    value = float(m.group("value"))
    unit = m.group("unit").lower()
    if unit in ("m", "meter", "metre"):
        value *= 3.28084
    return round(value, 1)


def extract_plot_khata(text: str) -> dict[str, Optional[str]]:
    """Best-effort plot no / khata no extraction (used to gate bhulekh_lookup)."""
    plot = re.search(r"(?:plot\s*(?:no\.?|number)?|p\.?\s*no\.?)\s*[:#-]?\s*([0-9]+[a-z0-9/-]*)",
                     text or "", re.IGNORECASE)
    khata = re.search(r"(?:khata\s*(?:no\.?|number)?)\s*[:#-]?\s*([0-9]+[a-z0-9/-]*)",
                      text or "", re.IGNORECASE)
    return {
        "plot_no": plot.group(1) if plot else None,
        "khata_no": khata.group(1) if khata else None,
    }


def enrich(record: dict) -> dict:
    """Apply all deterministic extractors to a normalized record in place."""
    text = record.get("text", "") or ""

    if not record.get("area_sqft"):
        area = normalize_area_to_sqft(text)
        if area:
            record["area_sqft"], record["area_raw"] = area
    if not record.get("price_inr"):
        record["price_inr"] = parse_price_inr(text)

    record["price_per_sqft"] = price_per_sqft(record.get("price_inr"), record.get("area_sqft"))
    record["corner"] = is_corner_plot(text)
    record["facing"] = facing(text)
    record["road_width_ft"] = road_width_ft(text)

    ids = extract_plot_khata(text)
    if not record.get("plot_no"):
        record["plot_no"] = ids["plot_no"]
    if not record.get("khata_no"):
        record["khata_no"] = ids["khata_no"]
    return record
