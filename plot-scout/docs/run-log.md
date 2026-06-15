# Run Log (build + change history, owned by docs-keeper, §10)

Per-run **stage** telemetry is written to the `run_log` DB table. This file is
the human-readable build/change narrative.

## 2026-06-16 — Initial scaffold + /lib + dry run
- Built scaffold (§1): `/lib`, `/docs`, `/data` (SQLite schema), `.claude/agents`.
- Built `state_store` (delta sourcing + run-log) and the full `/lib` chain in
  the §9 build order, plus a deterministic reference scorer (`lib/scoring.py`).
- Created 13 subagent definitions (§2) with scoped tools + model tiers.
- Wrote `rubric.md` (§3 single source of truth), `schema.md`, `lib-registry.md`.
- Built `evaluator` (§4); gold set **pending** from owner.
- **Dry run (§11)** on one locality (`patia`), offline against fixtures:
  - 7 sourced → 1 dropped at ₹1.5 Cr ceiling → 6 kept → 5 canonical plots
    (one duplicate merged across portal + inbox by phone + geo).
  - Baseline coverage 100% (small band, 6 comparables ≥ gate of 3).
  - Fraud (`price_too_good_fraud_risk`) and agri (`agri_kissam_no_conversion`)
    flags fired and sank those plots; zoning held at `verify` (never claimed).
  - Evaluator correctly reported **gold set pending** (no crash).
  - 21 unit/integration tests pass.
- **Schedules + channels (§8) NOT wired** — gated on owner go-ahead at the
  dry-run gate.

### Next (awaiting owner)
1. Owner supplies 15–20 ranked Bhubaneswar plots → load into `gold_set`.
2. Re-run `evaluator`; confirm Spearman ≥ trust threshold.
3. On go-ahead: wire live source fetchers, Bhulekh fetcher, geocoder provider,
   then daily cloud task + `/loop` price watch + Telegram channel (§8), bounded
   to the 4-week sprint `end_date`.
