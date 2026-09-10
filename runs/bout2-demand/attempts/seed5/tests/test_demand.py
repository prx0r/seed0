import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from demand import AREAS, weekly_demand, rank


def test_unknown_postcode_returns_zero():
    assert weekly_demand("ZZ9") == 0.0
    assert weekly_demand("UNKNOWN") == 0.0


def test_rank_orders_descending_demand():
    postcodes = list(AREAS.keys())
    ranked = rank(postcodes)
    demands = [weekly_demand(p) for p in ranked]
    assert demands == sorted(demands, reverse=True)
    # full ordering check against explicit sort
    assert ranked == sorted(postcodes, key=weekly_demand, reverse=True)
    # top of rank is the max-demand area
    assert ranked[0] == max(postcodes, key=weekly_demand)


def test_math_spot_check():
    # LE1: 12000 * 0.60 / 52
    assert weekly_demand("LE1") == 12000 * 0.60 / 52.0
    # LE3: 9000 * 0.70 / 52
    assert abs(weekly_demand("LE3") - (9000 * 0.70 / 52.0)) < 1e-9
