import json
import subprocess
import sys

import scorer


def test_score_math():
    opp = {"name": "x", "demand_growth": 0.9, "supply_inelasticity": 0.85}
    assert scorer.score_opp(opp) == 0.9 * 0.85
    assert scorer.score_opp(scorer.OPPORTUNITIES[0]) == 0.90 * 0.85


def test_ranking_order():
    ranked = scorer.ranked()
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0]["name"] == "p2p_gold_xrf_verification"
    assert len(ranked) == 5


def test_json_shape_stdout():
    proc = subprocess.run(
        [sys.executable, "scorer.py"], capture_output=True, text=True, cwd="."
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert isinstance(data, list) and len(data) == 5
    for item in data:
        assert set(item.keys()) == {"name", "score"}
        assert isinstance(item["name"], str)
        assert isinstance(item["score"], float)
