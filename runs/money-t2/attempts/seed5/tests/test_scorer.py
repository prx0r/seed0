import json
import subprocess
import sys

import scorer


def test_score_math():
    opp = {"name": "x", "demand_growth": 0.85, "supply_inelasticity": 0.90}
    assert scorer.score_opp(opp) == 0.85 * 0.90


def test_ranking_order():
    ranked = scorer.ranked()
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0]["name"] == "datacenter-loadbank-testing"


def test_json_shape():
    out = subprocess.run(
        [sys.executable, "scorer.py"], capture_output=True, text=True, cwd="."
    )
    data = json.loads(out.stdout)
    assert isinstance(data, list) and len(data) == 5
    for item in data:
        assert set(item.keys()) == {"name", "score"}
        assert isinstance(item["name"], str)
        assert isinstance(item["score"], float)
