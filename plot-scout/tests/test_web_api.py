import tempfile
from pathlib import Path

from services.pipeline import run_scan
from lib import state_store
from web import api


def _populated_conn(tmp):
    db = str(Path(tmp) / "ui.db")
    run_scan(db_path=db)
    conn = state_store.connect(db)
    state_store.init_db(conn)
    return conn


def test_list_plots_ranked_and_flagged_sink():
    with tempfile.TemporaryDirectory() as tmp:
        conn = _populated_conn(tmp)
        plots = api.list_plots(conn)
        assert len(plots) > 10
        # ranks are 1..n, contiguous
        assert [p["rank"] for p in plots] == list(range(1, len(plots) + 1))
        # top-tier-blocking flags (fraud, agri) must not appear in the top 5
        blockers = {"price_too_good_fraud_risk", "agri_kissam_no_conversion"}
        for p in plots[:5]:
            assert not (blockers & set(p["red_flags"]))
        conn.close()


def test_get_plot_detail_shape():
    with tempfile.TemporaryDirectory() as tmp:
        conn = _populated_conn(tmp)
        first = api.list_plots(conn)[0]
        detail = api.get_plot(conn, first["id"])
        for key in ("distances_km", "comparables", "sources",
                    "diligence_checklist", "financeability", "rank"):
            assert key in detail
        assert "nh16" in detail["distances_km"]
        assert detail["sources"]  # at least one source candidate linked
        conn.close()


def test_summary_reports_gold_pending():
    with tempfile.TemporaryDirectory() as tmp:
        conn = _populated_conn(tmp)
        s = api.get_summary(conn)
        assert s["canonical_plots"] == len(api.list_plots(conn))
        assert s["evaluation"]["status"] == "gold set pending"
        assert s["budget"]["ceiling"] == 15000000
        reports = api.get_reports(conn)
        assert "plot-scout" in reports["digest"]
        conn.close()
