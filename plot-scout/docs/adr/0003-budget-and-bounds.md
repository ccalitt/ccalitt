# ADR 0003 — Budget ceiling, financeability, and bounded runs

**Status:** accepted · **Date:** 2026-06-16

## Context
§5 confirms equity capability ₹30–50 L and a hard ceiling of 3× the upper bound
(₹1.5 Cr). §6 confirms a 4-week sourcing sprint with a hard stop.

## Decisions
1. **Ceiling = 3 × EQUITY_MAX = ₹1.5 Cr**, applied by `budget_filter` *before*
   extraction/scoring. No lower bound — cheaper-but-viable wins on value.
2. **required_loan = est_price − EQUITY_MAX**, with comfort tiers low (≤ ₹50 L)
   / moderate (≤ ₹1 Cr) / stretch (> ₹1 Cr). Surfaced, not blocked, so the
   shortlist isn't all ceiling-priced.
3. **Financeability flag** (surface, don't block): raw/commercial land gets
   ~60–75% LTV; when implied loan / price > 0.70 we add `verify financeability`.
4. **Bounded sprint:** `SPRINT_WEEKS = 4` from `SPRINT_START`; cloud task and
   `/loop` carry the derived `end_date`. Hard stop → final ranked report +
   explicit renew/stop decision.

## Consequences
- Unknown-price listings are *kept* through the filter (extraction may recover
  the price); only a *known* over-ceiling price is dropped.
- All monetary thresholds live in `config/settings.py` (single source of truth).
