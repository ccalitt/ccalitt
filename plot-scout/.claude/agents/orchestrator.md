---
name: orchestrator
description: Coordination notes for the main session (Opus). Not a delegatable subagent — documents how the main session drives the pipeline and when it (and only it) uses Opus-level judgment.
model: opus
---

> This file documents the **main session's** role (§2). The main session is the
> orchestrator; it is the only place — together with ambiguous red-flag
> adjudication — that uses Opus.

## Coordination
Drive the daily flow by invoking subagents **explicitly by name** (auto-routing
is unreliable):

```
auction-scout + inbox-scout + portal-scout   (sources; Haiku)
  -> budget_filter + geocoder                (/lib, deterministic, pre-extraction)
  -> extractor (Haiku) + extractor_helpers   (/lib)
  -> resolver (Sonnet, ambiguous only) + dedup_matcher (/lib)
  -> baseline-keeper (Sonnet) + comparables_aggregator (/lib)
  -> scorer (Sonnet, ambiguous only) + lib/scoring.py
  -> zoning-checker (Haiku) + bhulekh_lookup (/lib)
  -> diligence-writer (Haiku) + report_renderer (/lib)
  -> push top-5 digest to Telegram
```

## Token discipline (§7)
- Bulk read-only work on Haiku; resolve/score/eval on Sonnet; Opus only here.
- Subagents return structured records only — never raw HTML into this session.
- Delta-source against `state_store`; never re-extract/re-score unchanged plots.
- `budget_filter` + locality whitelist run before extraction; batch-score.

## Guardrails
- Do not enable schedules or widen scope until the dry-run gate (§11) passes and
  the owner gives go-ahead.
- Reserve Opus for genuine judgment: ambiguous red-flag adjudication and
  coordination. Everything rule-based is `/lib` code.
