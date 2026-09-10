import json
import subprocess
import sys

from scorer import OPPORTUNITIES, score


def test_ranking_order():
    ranked = score()
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0]["name"] == "eicr_landlord_rush"


def test_score_math():
    ranked = {r["name"]: r["score"] for r in score()}
    assert abs(ranked["eicr_landlord_rush"] - 0.9 * 0.85) < 1e-9
    assert abs(ranked["ev_charger_install"] - 0.8 * 0.6) < 1e-9
    assert len(ranked) == 5


def test_json_shape():
    out = subprocess.run(
        [sys.executable, "scorer.py"], capture_output=True, text=True, check=True
    ).stdout
    data = json.loads(out)
    assert isinstance(data, list) and len(data) == 5
    for row in data:
        assert set(row.keys()) == {"name", "score"}
        assert isinstance(row["name"], str)
        assert isinstance(row["score"], float)


def test_custom_input_scores():
    custom = [
        {"name": "a", "demand_growth": 0.5, "supply_inelasticity": 0.5},
        {"name": "b", "demand_growth": 1.0, "supply_inelasticity": 0.1},
    ]
    ranked = score(custom)
    assert ranked[0] == {"name": "a", "score": 0.25}
    assert ranked[1] == {"name": "b", "score": 0.1}
