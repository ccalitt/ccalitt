# plot-scout

**Autonomous Bhubaneswar commercial-plot sourcing & scoring engine.**

Sources plots (BDA + Odisha e-auction first, plus saved-search email alerts and
rate-limited portals), resolves them to canonical plots, scores them against a
versioned rubric with confidence bands and hard gates, and pushes a ranked
shortlist — without emitting confident-wrong scores.

> Status: **scaffold + `/lib` + dry-run gate complete.** Schedules and live
> channels (§8) are intentionally **not** wired — they unlock only after the
> owner approves the dry-run output (§11). See `docs/run-log.md`.

## Operating principles (§0)
- **Confident-wrong is the enemy.** No score without a confidence band +
  missing-fields list; no value score without ≥ N comparables; no top-tier plot
  with unknown zoning.
- **Deterministic code over tokens.** Repeatable work lives in `/lib`; the LLM
  is reserved for genuine judgment. Capabilities graduate from tokens to code.
- **Explicit delegation, bounded runs.** Subagents invoked by name; the sourcing
  sprint carries a hard `end_date`.

## Layout
```
config/        single source of truth (settings.py)
lib/           deterministic, reusable capabilities (§9)
  source_adapters/   BDA + Odisha auction, inbox, portal
services/      evaluator (§4) + dry-run pipeline (§11)
docs/          rubric (source of truth), schema, ADRs, lib-registry, run-log
data/          schema.sql (+ runtime SQLite, gitignored)
fixtures/      offline sample listings for the dry run
tests/         unit + integration tests
.claude/agents 13 subagent definitions (§2)
```

## Quick start
```bash
# Dry run on one locality, fully offline against fixtures (no tokens, no network)
python run.py --locality patia

# Tests (dev dependency only)
pip install -r requirements-dev.txt
python -m pytest -q
```

The runtime is **standard-library only**.

## Pipeline (dry-run path)
```
scouts -> delta-source -> geocode + budget_filter (pre-extraction)
       -> extractor_helpers -> resolver(dedup) -> baseline (comparables)
       -> zoning(bhulekh) -> scorer(rubric) -> rank -> evaluator(vs gold set)
       -> report_renderer (Telegram digest / weekly report / diligence checklist)
```

## What's gated until owner go-ahead (§8, §11)
- Live source fetchers, Bhulekh/BhuNaksha lookup, geocoder provider.
- Daily cloud sourcing task, `/loop` price/status watch, Telegram channel.
- Gold set (§4): owner to supply 15–20 ranked plots; `evaluator` must clear the
  trust threshold before scope widens.

## Output contract (§3)
```json
{ "value_band", "commercial_band", "confidence", "missing_fields": [],
  "red_flags": [], "zoning_status", "est_price", "required_loan" }
```
Full rubric: `docs/rubric.md`. Full brief: `docs/brief.md`.
