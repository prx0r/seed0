"""metrics.py tests: the ruler is tested before it measures anything."""
from metrics import footrule, rank_distance, storm_counts


def test_footrule_known_values():
    assert footrule(["A", "B"], ["A", "B"]) == 0
    assert footrule(["B", "A"], ["A", "B"]) == 2
    assert footrule(["A", "B", "C"], ["C", "B", "A"]) == 4


def test_rank_distance_adds_orders():
    assert rank_distance([["A", "B"], ["A", "B"]], ["A", "B"]) == 0
    assert rank_distance([["B", "A"], ["A", "B"]], ["A", "B"]) == 2


def test_storm_counts_dict_shape():
    n, u = storm_counts(lambda s, k: {"id": k}, "x", "k1", n=5)
    assert (n, u) == (5, 1)
