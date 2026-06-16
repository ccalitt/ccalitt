# ADR 0001 — Architecture & operating principles

**Status:** accepted · **Date:** 2026-06-16

## Context
Autonomous Bhubaneswar commercial-plot sourcing & scoring engine, run on an M2
Mac mini via Claude Code with a Telegram bridge. See the master build brief.

## Decisions
1. **Confident-wrong is the enemy.** Every score carries a confidence band +
   missing-fields list. Hard gates (comparables, zoning, fraud) are enforced in
   code and cannot be relaxed by the LLM layer.
2. **Deterministic code over tokens.** Repeatable, rule-based work lives in
   `/lib`; the model is reserved for genuine judgment. Per-run token cost should
   fall as capabilities graduate to code.
3. **Explicit delegation.** Subagents are invoked by name (no auto-routing);
   trivial single-file work stays in the main session.
4. **Bounded runs.** Nothing runs indefinitely; the sprint carries an
   `end_date` (§6).
5. **Python + SQLite, stdlib-only runtime.** No runtime third-party deps;
   `pytest` is dev-only. Keeps the engine portable on the mini and in cloud
   tasks.

## Consequences
- The dry-run pipeline runs fully offline against fixtures, so the gate (§11)
  can be demonstrated without live network or token spend.
- LLM subagents return structured records only — never raw HTML into the
  orchestrator (§7).
