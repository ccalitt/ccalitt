# Rubric Spec — single source of truth (§3)

This document defines how plots are scored. **It is authoritative.** When it
changes, the `evaluator` must be re-run against the gold set (§4) before the
engine is trusted again. Thresholds live in `config/settings.py`; this file
explains intent, the code enforces it.

> **Confident-wrong is the enemy (§0).** No score is emitted without a
> confidence band + missing-fields list. No value score without ≥ N
> comparables. No top-tier shortlist entry with zoning = unknown.

## Output contract

Every scored canonical plot emits exactly this shape (`lib/scoring.py`):

```json
{
  "value_band":      "A | B | C | D | null (gated)",
  "commercial_band": "A | B | C",
  "confidence":      "high | medium | low",
  "missing_fields":  ["..."],
  "red_flags":       ["..."],
  "zoning_status":   "commercial | mixed | residential | agricultural | unknown | verify",
  "est_price":       0,
  "required_loan":   0
}
```

Surfaced extras (persisted, not part of the strict contract): `comfort_tier`,
`price_per_sqft`, `n_comparables`, `distances_km`, `commercial_notes`.

## VALUE (gated on ≥ N comparables)

`N = MIN_COMPARABLES` (default **3**). If the locality + sqft-band cell has
fewer comparables, **no value band is emitted** — `value_band = null` and the
gate reason is added to `missing_fields`.

Band by premium vs locality/band **median ₹/sqft** (`price − median) / median`):

| Band | Meaning |
|------|---------|
| A | ≥ 15% below median |
| B | at / below median |
| C | up to 15% above median |
| D | more than 15% above median |

Additional value signals (informational, surfaced via distances/flags): road
width facing plot, frontage:depth, corner, distance to NH-16 / airport / IT
corridor / KIIT–SOA / station, BDA-approved + ORERA-registered, micro-market
appreciation.

## COMMERCIAL

Coarse band from arterial proximity (NH-16), catchment (KIIT–SOA / Infocity),
and facing-road width. **HARD GATE:** a plot cannot reach top tier (band A)
unless CDP zoning is `commercial` or `mixed`. Also considered: visibility,
competing supply, permitted FAR / ground coverage.

## HARD GATES (§3)

1. **Agricultural Kissam without conversion** → `agri_kissam_no_conversion`
   flag + blocked from top tier.
2. **Zoning unknown / unverified** → blocked from top tier (commercial band
   cannot be A while `zoning_status ∈ {verify, unknown}`).
3. **Price-too-good** (< `FRAUD_PRICE_FRACTION` × median ₹/sqft, default 40%)
   → `price_too_good_fraud_risk` fraud flag + blocked from top tier.

Top-tier blockers (`red_flag_rules.TOP_TIER_BLOCKERS`) also sink the plot to the
bottom of the ranking (`scoring.rank_key`).

## Confidence

- `high` — ≤ 1 missing field, no red flags.
- `medium` — 2–3 missing fields, no red flags.
- `low` — ≥ 4 missing fields, or any red flag present.

## Division of labour (deterministic vs LLM)

The common case is scored in **code** (`lib/scoring.py`) for zero tokens. The
Sonnet `scorer` subagent adjudicates only the ambiguous residue (unclear
commercial potential, borderline red flags) and may override bands — but it
inherits this contract and these gates and may never relax a hard gate.
