from demand import weekly_demand, rank, AREAS


def test_unknown_postcode_returns_zero():
    assert weekly_demand("ZZ99") == 0.0
    assert weekly_demand("") == 0.0


def test_rank_descending_order():
    postcodes = list(AREAS.keys())
    ranked = rank(postcodes)
    demands = [weekly_demand(p) for p in ranked]
    assert demands == sorted(demands, reverse=True)
    # top should be B4 (80000*0.65/52 = 1000.0), bottom B3
    assert ranked[0] == "B4"
    assert ranked[-1] == "B3"


def test_math_spot_check():
    # B4: 80000 * 0.65 / 52 = 1000.0
    assert weekly_demand("B4") == 80000 * 0.65 / 52.0
    assert weekly_demand("B4") == 1000.0
    # B1: 45000 * 0.55 / 52
    assert abs(weekly_demand("B1") - (45000 * 0.55 / 52.0)) < 1e-9


def test_rank_unknown_last():
    ranked = rank(["ZZ99", "B4", "B3"])
    assert ranked[-1] == "ZZ99"
