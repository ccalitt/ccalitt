from config import settings
from lib import budget_filter as bf
from lib import distance_engine as de


def test_haversine_known_distance():
    # Airport to railway station ~ a few km; just assert it's sane and symmetric.
    a = settings.LANDMARKS["airport"]
    b = settings.LANDMARKS["railway_station"]
    d = de.haversine_km(a, b)
    assert 0 < d < 10
    assert abs(de.haversine_km(a, b) - de.haversine_km(b, a)) < 1e-9


def test_distances_for_plot_keys():
    d = de.distances_for_plot(20.3499, 85.8197)
    for key in ("airport", "infocity", "kiit", "soa", "railway_station", "nh16", "kiit_soa"):
        assert key in d
    assert d["kiit_soa"] == min(d["kiit"], d["soa"])


def test_required_loan_and_tier():
    assert bf.required_loan(90_00_000) == 90_00_000 - settings.EQUITY_MAX
    assert bf.required_loan(40_00_000) == 0.0  # below equity -> no loan
    assert bf.comfort_tier(40_00_000) == "low"
    assert bf.comfort_tier(80_00_000) == "moderate"
    assert bf.comfort_tier(1_20_00_000) == "stretch"


def test_budget_ceiling_drop():
    over = {"locality": "Patia", "price_inr": settings.BUDGET_CEILING + 1}
    ok, reason = bf.passes_filter(over)
    assert ok is False and "ceiling" in reason


def test_whitelist_gate():
    ok, reason = bf.passes_filter({"locality": "Some Random Village", "price_inr": 50_00_000})
    assert ok is False and "whitelist" in reason
    ok2, _ = bf.passes_filter({"locality": "Patia", "price_inr": 50_00_000})
    assert ok2 is True


def test_financeability_flag():
    # loan/price > 0.70 trips the flag.
    price = 2_00_00_000  # over ceiling in practice, but tests the math
    loan = bf.required_loan(price)
    assert bf.financeability_flag(price, loan) == "verify financeability"
    # small loan relative to price -> no flag
    assert bf.financeability_flag(60_00_000, 10_00_000) is None
