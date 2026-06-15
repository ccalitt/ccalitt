#!/usr/bin/env python3
"""plot-scout dry-run CLI (§11).

Runs the full deterministic pipeline on ONE locality, offline, against fixtures.
No schedules, no channels — those are wired only after the owner approves.

Usage:
    python run.py --locality patia
    python run.py --locality patia --db /tmp/scratch.db
"""

from __future__ import annotations

import argparse
import json

from services.pipeline import run_dry_run


def main() -> None:
    ap = argparse.ArgumentParser(description="plot-scout dry run (one locality)")
    ap.add_argument("--locality", default="patia", help="locality to dry-run on")
    ap.add_argument("--db", default=None, help="SQLite path (default: data/plot_scout.db)")
    ap.add_argument("--json", action="store_true", help="print full JSON result")
    args = ap.parse_args()

    result = run_dry_run(args.locality, db_path=args.db)

    print("=" * 70)
    print(f"DRY RUN — {args.locality}  (run_id={result['run_id']})")
    print("=" * 70)
    print(f"sourced={result['raw_count']}  in-locality={result['target_count']}  "
          f"kept={result['kept']}  dropped={result['dropped']}  "
          f"canonical_plots={result['canonical_plots']}")
    cov = result["coverage"]
    print(f"baseline coverage: {cov['coverage_pct']}% "
          f"({cov['cells_meeting_gate']}/{cov['cells']} cells >= {cov['min_comparables']} comps)")
    ev = result["evaluation"]
    print(f"evaluation: {ev['status']}  spearman={ev['spearman']}  "
          f"kendall={ev['kendall']}  trusted={ev['trusted']}")
    if result["dropped_records"]:
        print("\nDropped (pre-extraction gate):")
        for d in result["dropped_records"]:
            print(f"  - {d['locality']}: {d['reason']}")

    print("\n--- sample scored record (top candidate) ---")
    if result["scored"]:
        top = result["scored"][0]
        contract = {k: top.get(k) for k in (
            "value_band", "commercial_band", "confidence", "missing_fields",
            "red_flags", "zoning_status", "est_price", "required_loan", "comfort_tier",
            "price_per_sqft", "n_comparables",
        )}
        print(json.dumps(contract, indent=2, default=str))

    print("\n--- telegram digest preview ---")
    print(result["digest"])

    if args.json:
        print("\n--- full JSON ---")
        print(json.dumps({k: v for k, v in result.items() if k != "scored"},
                         indent=2, default=str))


if __name__ == "__main__":
    main()
