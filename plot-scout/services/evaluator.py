"""evaluator — run the scorer's ranking against the gold set (§4).

Reports rank correlation (Spearman rho + Kendall tau) and drift. Must reproduce
the owner's best->worst ranking within tolerance before the engine is trusted;
re-run on every rubric.md change.

Gracefully reports "gold set pending" when the owner has not yet supplied it.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Optional

from config import settings
from lib.geocoder import _normalize

# Default trust threshold for Spearman correlation.
TRUST_THRESHOLD = 0.70


def _spearman(rank_a: list[float], rank_b: list[float]) -> Optional[float]:
    n = len(rank_a)
    if n < 2:
        return None
    d2 = sum((a - b) ** 2 for a, b in zip(rank_a, rank_b))
    return round(1 - (6 * d2) / (n * (n * n - 1)), 4)


def _kendall(rank_a: list[float], rank_b: list[float]) -> Optional[float]:
    n = len(rank_a)
    if n < 2:
        return None
    concordant = discordant = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (rank_a[i] - rank_a[j]) * (rank_b[i] - rank_b[j])
            if s > 0:
                concordant += 1
            elif s < 0:
                discordant += 1
    denom = n * (n - 1) / 2
    return round((concordant - discordant) / denom, 4) if denom else None


def _match_gold_to_scored(
    gold: list[dict[str, Any]], scored: list[dict[str, Any]]
) -> list[tuple[float, float]]:
    """Pair gold-set rank with the engine's rank, matched by locality + area.

    Returns list of (gold_rank, engine_rank) for matched plots only.
    """
    # engine rank: 1 = best (scored already ordered best->worst by caller)
    engine_rank = {}
    for i, s in enumerate(scored, 1):
        key = (_normalize(s.get("locality", "")), round((s.get("area_sqft") or 0) / 100))
        engine_rank[key] = i

    pairs: list[tuple[float, float]] = []
    for g in gold:
        key = (_normalize(g.get("locality", "")), round((g.get("area_sqft") or 0) / 100))
        if key in engine_rank:
            pairs.append((float(g["rank"]), float(engine_rank[key])))
    return pairs


def evaluate(
    conn: sqlite3.Connection,
    scored_ranked: list[dict[str, Any]],
    threshold: float = TRUST_THRESHOLD,
) -> dict[str, Any]:
    """Compare the engine's ranking to the gold set.

    ``scored_ranked`` must already be ordered best->worst by the caller.
    """
    gold = [dict(r) for r in conn.execute(
        "SELECT plot_label, locality, rank, area_sqft FROM gold_set ORDER BY rank"
    ).fetchall()]

    if not gold:
        return {
            "status": "gold set pending",
            "spearman": None,
            "kendall": None,
            "matched": 0,
            "gold_size": 0,
            "trusted": False,
            "note": "Owner to supply 15-20 ranked Bhubaneswar plots (§4).",
        }

    pairs = _match_gold_to_scored(gold, scored_ranked)
    if len(pairs) < 2:
        return {
            "status": "insufficient overlap",
            "spearman": None,
            "kendall": None,
            "matched": len(pairs),
            "gold_size": len(gold),
            "trusted": False,
            "note": "Engine output did not overlap enough gold-set plots to score.",
        }

    gold_ranks = [p[0] for p in pairs]
    engine_ranks = [p[1] for p in pairs]
    rho = _spearman(gold_ranks, engine_ranks)
    tau = _kendall(gold_ranks, engine_ranks)
    trusted = rho is not None and rho >= threshold

    return {
        "status": "ok",
        "spearman": rho,
        "kendall": tau,
        "matched": len(pairs),
        "gold_size": len(gold),
        "threshold": threshold,
        "trusted": trusted,
        "note": "Trusted" if trusted else f"Below trust threshold {threshold}; do not widen scope.",
    }
