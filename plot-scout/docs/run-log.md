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

## 2026-06-16 — Local browse UI + fixes (ADR 0004)
- Added a stdlib-only browse UI under `web/`: JSON API (`web/api.py`) + a
  vanilla single-page app (`web/static/`) with a dashboard, sortable/filterable
  table, Leaflet map (plots + landmarks + NH-16), per-plot detail drawer
  (contract, distances, comparables, sources, diligence), reports tab, and
  Run/Scan controls. Launch: `python web/server.py --scan --open`.
- Engine changes: populate `candidates.canonical_id` (was unused); add
  `pipeline.run_scan()` to scan all whitelist localities into one DB.
- Enriched fixtures to ~17 listings across 7 localities (Patia,
  Chandrasekharpur, Patrapada, Khandagiri, Tomando, Sundarpada, Gothapatna) so
  the UI has a realistic spread of bands, comfort tiers, flags, gated value
  scores, and a ceiling drop. Scan → 24 candidates → 2 dropped → 23 canonical.
- **Bug fix:** `agri_kissam_flag` mis-read "no conversion done yet" as
  conversion evidence (bare "conversion" substring), wrongly clearing the
  agricultural gate. Now requires affirmative evidence + negation guard. The
  Khandagiri agri plot is correctly flagged and sinks in the ranking.
- 24 tests pass (added `tests/test_web_api.py`).
- Project relocated to its **own private repo** `ccalitt/plot-scout-engine`
  (moved out of the `ccalitt/ccalitt` profile repo).

### Next (awaiting owner)
1. Owner supplies 15–20 ranked Bhubaneswar plots → load into `gold_set`.
2. Re-run `evaluator`; confirm Spearman ≥ trust threshold.
3. On go-ahead: wire live source fetchers, Bhulekh fetcher, geocoder provider,
   then daily cloud task + `/loop` price watch + Telegram channel (§8), bounded
   to the 4-week sprint `end_date`.
