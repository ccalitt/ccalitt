from lib import dedup_matcher as dm
from lib import red_flag_rules as rf


def test_fraud_price_flag():
    assert rf.fraud_price_flag(1250, 6000) == "price_too_good_fraud_risk"
    assert rf.fraud_price_flag(5500, 6000) is None
    assert rf.fraud_price_flag(None, 6000) is None


def test_litigation_keywords():
    flags = rf.litigation_flags("Plot under litigation, court case pending")
    assert any("litigation" in f for f in flags)
    assert rf.litigation_flags("clean title, BDA approved") == []


def test_agri_kissam_gate():
    assert rf.agri_kissam_flag("agricultural paddy land") == "agri_kissam_no_conversion"
    # conversion evidence clears it
    assert rf.agri_kissam_flag("agricultural land, NA converted for commercial use") is None
    assert rf.agri_kissam_flag("commercial plot, BDA approved") is None
    # "no conversion done yet" must NOT be read as conversion evidence
    assert rf.agri_kissam_flag("agricultural paddy land, no conversion done yet") == "agri_kissam_no_conversion"
    assert rf.agri_kissam_flag("agri land, not converted") == "agri_kissam_no_conversion"


def test_blocks_top_tier():
    assert rf.blocks_top_tier(["agri_kissam_no_conversion"]) is True
    assert rf.blocks_top_tier(["litigation_keyword:dispute"]) is False


def test_dedup_same_phone():
    r1 = {"phone": "+91-9000000001", "area_sqft": 1500, "price_inr": 9000000,
          "lat": 20.3499, "lng": 85.8197}
    r2 = {"phone": "9000000001", "area_sqft": 1490, "price_inr": 9200000,
          "lat": 20.3501, "lng": 85.8199}
    assert dm.same_plot(r1, r2) is True


def test_dedup_distinct_plots():
    r1 = {"phone": "+91-1111111111", "area_sqft": 1200, "price_inr": 7800000,
          "lat": 20.3470, "lng": 85.8160}
    r2 = {"phone": "+91-2222222222", "area_sqft": 1800, "price_inr": 9900000,
          "lat": 20.3520, "lng": 85.8230}
    assert dm.same_plot(r1, r2) is False


def test_cluster_merges_duplicates():
    recs = [
        {"phone": "+91-9000000001", "area_sqft": 1500, "price_inr": 9000000,
         "lat": 20.3499, "lng": 85.8197},
        {"phone": "+91-9000000001", "area_sqft": 1500, "price_inr": 9200000,
         "lat": 20.3501, "lng": 85.8199},
        {"phone": "+91-3333333333", "area_sqft": 1200, "price_inr": 7800000,
         "lat": 20.3470, "lng": 85.8160},
    ]
    clusters = dm.cluster(recs)
    assert len(clusters) == 2
