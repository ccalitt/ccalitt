"""report_renderer — deterministic Telegram digest + weekly ranked report.

Zero-token templating from the DB (§9). No LLM involved: given scored canonical
plots and baseline coverage, render the strings the channels push out (§8).
"""

from __future__ import annotations

from typing import Any


def _inr(value: Any) -> str:
    if value is None:
        return "—"
    return f"₹{float(value):,.0f}"


def _band(value: Any) -> str:
    return value if value else "gated"


def render_plot_line(plot: dict[str, Any], idx: int) -> str:
    flags = plot.get("red_flags") or []
    flag_str = f"  ⚠️ {', '.join(flags)}" if flags else ""
    return (
        f"{idx}. {plot.get('locality', '?').title()} · {_inr(plot.get('est_price'))} · "
        f"{plot.get('area_sqft', '?')} sqft\n"
        f"   value={_band(plot.get('value_band'))} commercial={_band(plot.get('commercial_band'))} "
        f"conf={plot.get('confidence', '?')} zoning={plot.get('zoning_status', '?')}\n"
        f"   loan={_inr(plot.get('required_loan'))} ({plot.get('comfort_tier', '?')})"
        f"{flag_str}"
    )


def render_digest(plots: list[dict[str, Any]], top_n: int = 5, title: str = "plot-scout digest") -> str:
    """Top-N daily Telegram digest."""
    lines = [f"🏗️ {title}", ""]
    if not plots:
        lines.append("No qualifying candidates this run.")
        return "\n".join(lines)
    for i, plot in enumerate(plots[:top_n], 1):
        lines.append(render_plot_line(plot, i))
        lines.append("")
    return "\n".join(lines).rstrip()


def render_weekly_report(
    plots: list[dict[str, Any]],
    coverage: dict[str, Any],
    eval_summary: dict[str, Any] | None = None,
    top_n: int = 10,
) -> str:
    """Monday weekly review (§6): top candidates + baseline coverage + eval drift."""
    lines = ["📊 plot-scout — weekly review", ""]
    lines.append(
        f"Baseline coverage: {coverage.get('coverage_pct', 0)}% "
        f"({coverage.get('cells_meeting_gate', 0)}/{coverage.get('cells', 0)} cells "
        f">= {coverage.get('min_comparables', '?')} comparables)"
    )
    if eval_summary:
        lines.append(
            f"Eval vs gold set: spearman={eval_summary.get('spearman', 'n/a')} "
            f"kendall={eval_summary.get('kendall', 'n/a')} "
            f"({eval_summary.get('status', '')})"
        )
    lines.append("")
    lines.append(f"Top {min(top_n, len(plots))} candidates:")
    lines.append("")
    for i, plot in enumerate(plots[:top_n], 1):
        lines.append(render_plot_line(plot, i))
        lines.append("")
    return "\n".join(lines).rstrip()


def render_diligence_checklist(plot: dict[str, Any]) -> str:
    """Per-plot human checklist (mirrors diligence-writer output shape)."""
    items = [
        f"Verify title & encumbrance certificate (khata {plot.get('khata_no') or 'unknown'})",
        f"Confirm CDP zoning at site (status: {plot.get('zoning_status', 'verify')})",
        "Check BDA approval + ORERA registration",
        "Confirm Kissam / land classification (rule out agricultural without conversion)",
        f"Verify facing-road width (recorded: {plot.get('road_width_ft') or 'unknown'} ft)",
        f"Confirm financeability — implied loan {_inr(plot.get('required_loan'))} "
        f"({plot.get('comfort_tier', '?')})",
        "Physical site visit + neighbour/broker cross-check",
    ]
    flags = plot.get("red_flags") or []
    lines = [f"Diligence checklist — {plot.get('locality', '?').title()} ({_inr(plot.get('est_price'))})", ""]
    if flags:
        lines.append(f"⚠️ Red flags to clear first: {', '.join(flags)}")
        lines.append("")
    lines += [f"[ ] {it}" for it in items]
    return "\n".join(lines)
