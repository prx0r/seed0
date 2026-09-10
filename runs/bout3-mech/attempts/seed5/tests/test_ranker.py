import os
import tempfile

from ranker import load, rank, save, score


def test_order_descending():
    items = [
        {"x": 0, "y": 0, "z": 0},
        {"x": 1, "y": 1, "z": 0},
        {"x": 0, "y": 0, "z": 10},
    ]
    ranked = rank(items)
    scores = [score(d) for d in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0] == {"x": 1, "y": 1, "z": 0}
    # generic dicts handled gracefully
    assert score({}) == 0.0
    assert score({"foo": "bar"}) == 0.0


def test_formula_spot_check():
    # formula: 2*x + 3*y - z
    assert score({"x": 1, "y": 2, "z": 3}) == 2.0 * 1 + 3.0 * 2 - 3
    assert score({"x": 2, "y": 0, "z": 0}) == 4.0
    assert score({}) == 0.0


def test_round_trip_preserves_order():
    items = rank([{"x": 1}, {"x": 5}, {"x": 3}])
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "items.json")
        save(p, items)
        back = load(p)
    assert back == items
