import tempfile
from pathlib import Path

from services.pipeline import run_dry_run


def test_dry_run_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        db = str(Path(tmp) / "t.db")
        result = run_dry_run("patia", db_path=db)

        # ceiling drop happened
        assert result["dropped"] == 1
        # duplicate (portal + inbox, same phone) merged: 6 kept -> 5 canonical
        assert result["kept"] == 6
        assert result["canonical_plots"] == 5

        # comparables gate satisfied for this locality/band
        assert result["coverage"]["coverage_pct"] == 100.0

        # gold set not supplied yet -> evaluator reports pending, not a crash
        assert result["evaluation"]["status"] == "gold set pending"
        assert result["evaluation"]["trusted"] is False

        scored = result["scored"]
        flags = {f for p in scored for f in p["red_flags"]}
        assert "price_too_good_fraud_risk" in flags
        assert "agri_kissam_no_conversion" in flags

        # flagged plots must NOT be the top candidate (blockers sink)
        assert not any(f in scored[0]["red_flags"]
                       for f in ("price_too_good_fraud_risk", "agri_kissam_no_conversion"))

        # every scored plot carries the full output contract
        for p in scored:
            for key in ("value_band", "commercial_band", "confidence",
                        "missing_fields", "red_flags", "zoning_status",
                        "est_price", "required_loan"):
                assert key in p
            # no top-tier commercial band while zoning unverified
            if p["zoning_status"] in ("verify", "unknown"):
                assert p["commercial_band"] != "A"


def test_delta_sourcing_skips_unchanged():
    with tempfile.TemporaryDirectory() as tmp:
        db = str(Path(tmp) / "t.db")
        run_dry_run("patia", db_path=db)
        second = run_dry_run("patia", db_path=db)
        # nothing changed between runs -> no new/changed records to extract
        assert second["kept"] == 0
