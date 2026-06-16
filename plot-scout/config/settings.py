"""Single source of truth for plot-scout constants.

Everything repeatable and rule-based lives here or in /lib (deterministic code),
never in per-run LLM tokens. Edit values here; modules import them.

All monetary values are in INR (rupees). All distances are in kilometres.
"""

from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = Path(os.environ.get("PLOT_SCOUT_DB", DATA_DIR / "plot_scout.db"))
SCHEMA_PATH = DATA_DIR / "schema.sql"
FIXTURES_DIR = PROJECT_ROOT / "fixtures"

# --------------------------------------------------------------------------
# Budget (§5) — CONFIRMED
# --------------------------------------------------------------------------
# Deployable savings / equity the owner can put in.
EQUITY_MIN = 30_00_000      # ₹30 L
EQUITY_MAX = 50_00_000      # ₹50 L
# Hard ceiling = 3 × capability, computed on the upper bound.
BUDGET_CEILING = 3 * EQUITY_MAX   # ₹1.5 Cr
# No lower bound — a cheaper-but-viable plot is preferred by the value score.

# Raw / commercial land typically gets lower LTV from lenders.
RAW_LAND_MAX_LTV = 0.70     # ~60–75%; we use 0.70 as the financeability trip-wire.

# Comfort tiers by implied loan size (required_loan = est_price − EQUITY_MAX).
COMFORT_TIERS = (
    # (label, max_loan_inclusive)
    ("low", 50_00_000),         # loan <= ₹50 L
    ("moderate", 1_00_00_000),  # ₹50 L < loan <= ₹1 Cr
    ("stretch", float("inf")),  # > ₹1 Cr (still under ceiling)
)

# --------------------------------------------------------------------------
# Sprint timeline (§6) — CONFIRMED
# --------------------------------------------------------------------------
SPRINT_WEEKS = 4
SPRINT_START = os.environ.get("PLOT_SCOUT_SPRINT_START", "2026-06-16")
# end_date is derived in services if needed: SPRINT_START + SPRINT_WEEKS.

# --------------------------------------------------------------------------
# Comparables gate (§3 VALUE) — no value score without enough comparables.
# --------------------------------------------------------------------------
MIN_COMPARABLES = 3   # N — value score is refused below this.

# Per-sqft area bands for the price baseline distribution.
SQFT_BANDS = (
    ("micro", 0, 1000),
    ("small", 1000, 2000),
    ("mid", 2000, 5000),
    ("large", 5000, 20000),
    ("xlarge", 20000, float("inf")),
)

# --------------------------------------------------------------------------
# Geography — Bhubaneswar landmarks (lat, lng).
# Coordinates are approximate and documented as such; refine in /docs if needed.
# --------------------------------------------------------------------------
LANDMARKS = {
    "airport": (20.2526, 85.8179),          # Biju Patnaik Intl Airport (BBI)
    "infocity": (20.3499, 85.8197),          # Infocity / IT corridor, Patia
    "kiit": (20.3558, 85.8166),              # KIIT University
    "soa": (20.2535, 85.7700),               # SOA / ITER, Ghatikia
    "railway_station": (20.2647, 85.8341),   # Bhubaneswar Railway Station
}

# NH-16 modelled as a polyline through the Bhubaneswar stretch (approximate).
# distance_engine computes the nearest point on these segments.
NH16_POLYLINE = (
    (20.3400, 85.8050),
    (20.2980, 85.8240),
    (20.2700, 85.8400),
    (20.2300, 85.8200),
    (20.1900, 85.7900),
)

# Locality whitelist with cached centroids — feeds budget_filter + geocoder.
# Anything outside the whitelist is dropped before extraction (§7).
LOCALITY_WHITELIST = {
    "patia": (20.3499, 85.8197),
    "chandrasekharpur": (20.3289, 85.8155),
    "infocity": (20.3499, 85.8197),
    "patrapada": (20.2444, 85.7783),
    "khandagiri": (20.2585, 85.7796),
    "tomando": (20.2520, 85.7700),
    "sundarpada": (20.2200, 85.8300),
    "pahala": (20.3550, 85.8600),
    "raghunathpur": (20.3700, 85.8300),
    "hanspal": (20.3100, 85.8900),
    "balianta": (20.2700, 85.9100),
    "andharua": (20.3380, 85.7900),
    "jatni": (20.1700, 85.7000),
    "kiit square": (20.3550, 85.8170),
    "nandankanan road": (20.3650, 85.8200),
    "gothapatna": (20.2700, 85.7600),
    "dumduma": (20.2600, 85.7800),
    "aiginia": (20.2450, 85.7950),
}

# --------------------------------------------------------------------------
# Red-flag rules (§3 HARD GATES, §9 red_flag_rules)
# --------------------------------------------------------------------------
# A price below this fraction of the locality/band median ₹/sqft is a fraud flag.
FRAUD_PRICE_FRACTION = 0.40

# Keyword triggers (case-insensitive substring match on listing text).
LITIGATION_KEYWORDS = (
    "dispute", "disputed", "litigation", "court case", "stay order",
    "encroach", "mortgage", "lien", "under litigation", "legal notice",
    "partition suit", "ga land", "government land",
)
# Agricultural Kissam terms — block top tier unless conversion is evidenced.
AGRI_KISSAM_KEYWORDS = (
    "agricultural", "agri land", "krushi", "kisam", "kissam",
    "patita", "danga", "farm land", "farmland", "paddy",
)
# Affirmative evidence that agricultural land has been converted. NOTE: a bare
# "conversion" is deliberately excluded — it matches negations like "no
# conversion done yet" and would wrongly clear the gate.
CONVERSION_EVIDENCE_KEYWORDS = (
    "converted", "non-agricultural", "na converted", "na order",
    "conversion order", "conversion done", "land use change", "clu",
    "commercial use approved",
)
# Phrases that explicitly mean NOT converted — these keep the agri gate on even
# if an affirmative keyword substring also appears.
NEGATED_CONVERSION_KEYWORDS = (
    "not converted", "no conversion", "without conversion",
    "yet to be converted", "conversion pending", "unconverted", "un-converted",
)

# --------------------------------------------------------------------------
# Rubric band thresholds — deterministic reference scorer (lib/scoring.py).
# The `scorer` subagent (Sonnet) only adjudicates ambiguous residue; the
# common case is scored here, in code, for zero tokens.
# --------------------------------------------------------------------------
# VALUE band by discount vs locality median ₹/sqft (negative = cheaper = better).
VALUE_BANDS = (
    # (band, max_premium_fraction)  premium = (price - median) / median
    ("A", -0.15),   # >=15% below median
    ("B", 0.00),    # at/below median
    ("C", 0.15),    # up to 15% above median
    ("D", float("inf")),  # more than 15% above median
)

# COMMERCIAL band needs commercial/mixed zoning to reach top tier (hard gate).
ZONING_TOP_TIER_OK = ("commercial", "mixed", "mixed-use")

CONFIDENCE_LEVELS = ("high", "medium", "low")
