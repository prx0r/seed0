import json
import os
import tempfile

from ranker import load, rank, save, score


def test_order_descending():
    items = [
        {"a": 1, "b": 0, "c": 0},  # 2
        {"a": 0, "b": 5, "c": 0},  # 5
        {"a": 0, "b": 0, "c": 1},  # -1
    ]
    ranked = rank(items)
    assert [score(x) for x in ranked] == [5.0, 2.0, -1.0]
    assert ranked[0]["b"] == 5


def test_formula_spot_check():
    assert score({"a": 2, "b": 3, "c": 1}) == 2 * 2 + 3 - 1
    assert score({}) == 0.0
    assert score({"a": "bad", "b": None, "c": [1]}) == 0.0
    assert score("not-a-dict") == 0.0


def test_round_trip_preserves_order():
    items = rank([{"a": 1}, {"a": 3}, {"a": 2}])
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "items.json")
        save(p, items)
        back = load(p)
    assert back == items
    assert [x["a"] for x in back] == [3, 2, 1]
