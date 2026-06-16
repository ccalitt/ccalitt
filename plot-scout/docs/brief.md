# plot-scout — Master Build Brief

**Autonomous Bhubaneswar commercial-plot sourcing & scoring engine**

Source-of-record for this project. Implementation status is tracked in
`run-log.md`; the authoritative scoring spec is `rubric.md`.

## Context & references
- **Owner:** Lalit (ccalitt@gmail.com, +91-9437507735)
- **Host:** M2 Mac mini · Claude Code · Telegram bridge
- **Date:** 16 June 2026
- **Source planning session:** *(paste the claude.ai chat URL here for traceability)*

## 0. Operating principles
- **Confident-wrong is the enemy.** No score without a confidence band +
  missing-fields list. No value score without ≥ N comparables. No top-tier
  shortlist entry with zoning = unknown.
- **Deterministic code over tokens.** Repeatable, rule-based work is `/lib`
  code, not LLM work. The model is reserved for genuine judgment. Per-run token
  cost must fall as capabilities graduate to code.
- **Delegate explicitly.** Invoke subagents by name; don't rely on auto-routing;
  don't delegate trivial single-file work.
- **Bounded runs.** Nothing runs indefinitely (§6).

## 1. Scaffold
- `/lib` reusable versioned capabilities · `/docs` ADRs/rubric/schema/run-log ·
  `/data` SQLite (`candidates`, `canonical_plots`, `price_baseline`, `gold_set`,
  `run_log`) · `.claude/agents` subagent definitions.

## 2. Subagents (scoped tools + model tier)
auction-scout (Haiku, read/fetch) · inbox-scout (Haiku, gmail read) ·
portal-scout (Haiku, read/fetch) · resolver (Sonnet, db) · extractor (Haiku,
read) · baseline-keeper (Sonnet, db) · scorer (Sonnet, db read) · zoning-checker
(Haiku, read/fetch) · diligence-writer (Haiku, db) · evaluator (Sonnet, db) ·
docs-keeper (Haiku, write /docs) · builder (Sonnet, write /lib) · orchestrator
(main session, Opus).

## 3. Rubric spec
See `rubric.md` (single source of truth). VALUE (gated on ≥ N comparables),
COMMERCIAL (zoning gate to top tier), HARD GATES (agri-Kissam, unknown zoning,
price-too-good), and the output contract.

## 4. Evaluation spine (build BEFORE going wide)
Owner supplies 15–20 real Bhubaneswar plots ranked best→worst → `gold_set`.
`evaluator` must reproduce the ranking within tolerance before the engine is
trusted. Re-run on every `rubric.md` change. *(Gold set pending.)*

## 5. Budget cap — CONFIRMED
Equity ₹30–50 L; hard ceiling = 3 × upper = ₹1.5 Cr (drop above ceiling before
extraction). No lower bound. `required_loan = est_price − equity`; surface
financeability flag for large implied loans (raw-land LTV ~60–75%). Comfort
tiering low/moderate/stretch.

## 6. Bounded timeline — CONFIRMED
4-week sourcing sprint with `end_date`. Weekly Monday Telegram digest (top
candidates + baseline coverage % + eval drift). Hard stop → final ranked report
+ renew/stop decision.

## 7. Token efficiency
Model tiers as §2; subagents return structured records only; delta sourcing via
`state_store`; prompt-cache rubric/schema/system prompts; `budget_filter` +
whitelist before extraction; batch-score.

## 8. Scheduling & channels (wire AFTER dry run)
Daily sourcing → cloud task (scouts → resolver → extractor → baseline → scorer →
zoning → diligence → top-5 Telegram digest), `end_date` = sprint end.
Price/status watch → `/loop every 12h` over top-20 (alert on >5% drop or
"sold"). Telegram = alerts out + human-feed in (forwarded listing → same
pipeline).

## 9. /lib capabilities (build order)
`state_store` → `source_adapters/` (auction first) → `geocoder` →
`distance_engine` → `dedup_matcher` → `comparables_aggregator` →
`budget_filter` → `extractor_helpers` → `red_flag_rules` → `bhulekh_lookup` →
`report_renderer`. See `lib-registry.md`.

## 10. Self-extending services
Documentation service (`docs-keeper` + `/docs`) and coding service (`builder` +
`/lib`): detect gap → build once → document → register → reuse.

## 11. Dry-run gate (do FIRST)
Run the full pipeline on one locality, no schedules. Show canonical plots, a
sample extracted record with confidences, a sample score with missing-fields +
`required_loan`, and `evaluator` correlation vs gold set. **Wait for owner
go-ahead** before enabling schedules or widening scope.

## 12. Kickoff sequence
1. Scaffold + `state_store`. 2. Subagents + `rubric.md`. 3. `/lib` in order via
builder + docs-keeper. 4. Request gold set; build `evaluator`. 5. Dry run on one
locality → review. 6. On go-ahead: wire schedules + channels for the sprint.
