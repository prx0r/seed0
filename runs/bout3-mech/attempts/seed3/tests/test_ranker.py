import os
import tempfile

from ranker import load, rank, save, score


def test_order_descending():
    items = [
        {"alpha": 1, "beta": 0, "gamma": 0},
        {"alpha": 3, "beta": 0, "gamma": 0},
        {"alpha": 2, "beta": 0, "gamma": 0},
    ]
    ranked = rank(items)
    assert [score(x) for x in ranked] == sorted([score(x) for x in items], reverse=True)
    assert ranked[0]["alpha"] == 3 and ranked[-1]["alpha"] == 1


def test_formula_spot_check():
    # 2.0*3 + 1.0*4 - 1.0*1 = 9.0
    assert score({"alpha": 3, "beta": 4, "gamma": 1}) == 9.0
    assert score({}) == 0.0
    assert score({"alpha": "bad", "beta": None, "gamma": [1]}) == 0.0


def test_round_trip_preserves_order():
    items = rank([
        {"alpha": 1, "beta": 2, "gamma": 0},
        {"alpha": 5, "beta": 0, "gamma": 1},
    ])
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "items.json")
        save(p, items)
        back = load(p)
    assert back == items


def test_generic_dicts_graceful():
    assert isinstance(score({"other": 99}), float)
    assert rank([]) == []
    assert rank([{"x": 1}, {}])[0] is not None
