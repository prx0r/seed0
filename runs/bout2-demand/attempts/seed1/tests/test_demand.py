import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from demand import AREAS, weekly_demand, rank


def test_unknown_postcode_returns_zero():
    assert weekly_demand("ZZ99") == 0.0
    assert weekly_demand("") == 0.0
    assert weekly_demand("  ") == 0.0


def test_rank_orders_descending_demand():
    pcs = list(AREAS.keys())
    ranked = rank(pcs)
    demands = [weekly_demand(p) for p in ranked]
    assert demands == sorted(demands, reverse=True)
    # Highest must be OX4 (18400*0.75/52=265.38), lowest SW1A
    assert ranked[0] == "OX4"
    assert ranked[-1] == "SW1A"
    # Unknown postcode sorts last
    assert rank(["ZZ99", "OX4"])[0] == "OX4"


def test_math_spot_check():
    # OX1: 12500 * 0.82 / 52 = 197.115384...
    assert abs(weekly_demand("OX1") - (12500 * 0.82 / 52)) < 1e-9
    # OX33: 6300 * 0.88 / 52 = 106.615384...
    assert abs(weekly_demand("OX33") - (6300 * 0.88 / 52)) < 1e-9
