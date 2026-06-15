# ADR 0002 — Deterministic reference scorer alongside the LLM scorer

**Status:** accepted · **Date:** 2026-06-16

## Context
§2 assigns scoring to a Sonnet `scorer` subagent. §0/§7 demand that repeatable,
rule-based work be code, not tokens, and that capabilities graduate to `/lib`.
Pure-LLM scoring of every plot is expensive and non-reproducible, which also
breaks the evaluation spine (§4) that needs a stable ranking to compare.

## Decision
Build a deterministic reference scorer in `lib/scoring.py` that produces the
full §3 output contract from `/lib` outputs (baseline, distances, budget, red
flags, zoning). The Sonnet `scorer` subagent adjudicates only the ambiguous
residue (unclear commercial potential, borderline red flags) and may override
bands — but it inherits the contract and may never relax a hard gate.

## Consequences
- The dry run and `evaluator` run with zero token cost and reproducible output.
- Hard gates (comparables, zoning, fraud) are enforced once, in code.
- As the LLM's judgment stabilises on a sub-problem, that logic graduates into
  `scoring.py` / `red_flag_rules.py`, lowering per-run tokens over time.
