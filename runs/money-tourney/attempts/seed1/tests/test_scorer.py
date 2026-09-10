import json
import subprocess
import sys

import scorer


def test_score_math():
    opp = {"name": "x", "demand_growth": 0.9, "supply_inelasticity": 0.85}
    assert scorer.score(opp) == 0.9 * 0.85
    assert scorer.score({"name": "y", "demand_growth": 0.5, "supply_inelasticity": 0.6}) == 0.3


def test_ranking_order():
    r = scorer.ranked()
    assert len(r) == 5
    scores = [d["score"] for d in r]
    assert scores == sorted(scores, reverse=True)
    assert r[0]["name"] == "eicr-hmo-validation"


def test_json_shape_stdout():
    p = subprocess.run([sys.executable, "scorer.py"], capture_output=True, text=True, cwd=".")
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert isinstance(data, list) and len(data) == 5
    for d in data:
        assert set(d.keys()) == {"name", "score"}
        assert isinstance(d["name"], str) and isinstance(d["score"], float)


def test_scores_match_inputs():
    r = {d["name"]: d["score"] for d in scorer.ranked()}
    assert abs(r["ev-charger-commissioning"] - 0.56) < 1e-9
    assert abs(r["smart-meter-install"] - 0.20) < 1e-9
