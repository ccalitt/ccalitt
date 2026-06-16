from lib import extractor_helpers as eh


def test_area_units_to_sqft():
    assert eh.normalize_area_to_sqft("plot of 1200 sqft")[0] == 1200
    assert eh.normalize_area_to_sqft("200 sq yd corner")[0] == 1800  # 200 * 9
    assert round(eh.normalize_area_to_sqft("0.5 acre")[0]) == 21780
    assert eh.normalize_area_to_sqft("10 decimal plot")[0] == 4356
    assert eh.normalize_area_to_sqft("no area here") is None


def test_price_parsing_indian():
    assert eh.parse_price_inr("₹1.2 Cr") == 1_20_00_000
    assert eh.parse_price_inr("Rs 85 lakh") == 85_00_000
    assert eh.parse_price_inr("95,00,000") == 95_00_000
    assert eh.parse_price_inr("price 90 L only") == 90_00_000


def test_price_per_sqft():
    assert eh.price_per_sqft(9000000, 1500) == 6000.0
    assert eh.price_per_sqft(None, 1500) is None
    assert eh.price_per_sqft(9000000, None) is None


def test_flags_and_road_width():
    assert eh.is_corner_plot("nice corner plot") is True
    assert eh.facing("north facing plot") == "north"
    assert eh.road_width_ft("40 ft wide road") == 40.0
    # metre conversion
    assert eh.road_width_ft("12 m wide road") == round(12 * 3.28084, 1)


def test_plot_khata_extraction():
    ids = eh.extract_plot_khata("Plot No 221, Khata No 145, BDA approved")
    assert ids["plot_no"] == "221"
    assert ids["khata_no"] == "145"


def test_enrich_does_not_clobber_existing():
    rec = {"text": "Plot No 305", "area_sqft": 1800, "price_inr": 9900000}
    eh.enrich(rec)
    assert rec["plot_no"] == "305"
    assert rec["price_per_sqft"] == 5500.0
