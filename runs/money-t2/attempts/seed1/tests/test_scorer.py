"""Tests for scorer.py: ranking order, score math, JSON shape."""
import json
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scorer import OPPORTUNITIES, ranked, score_opportunity


def test_score_math():
    assert score_opportunity(0.9, 0.85) == abs(0.9 * 0.85)
    assert abs(score_opportunity(0.9, 0.85) - 0.765) < 1e-9
    assert abs(score_opportunity(0.95, 0.2) - 0.19) < 1e-9


def test_ranking_order():
    result = ranked()
    assert len(result) == 5
    scores = [r["score"] for r in result]
    assert scores == sorted(scores, reverse=True)
    assert result[0]["name"] == "pre-listing inspection wedge"
    assert result[-1]["name"] == "ai-staging software"


def test_json_shape_stdout():
    proc = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scorer.py")],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert isinstance(data, list) and len(data) == 5
    for item in data:
        assert set(item.keys()) == {"name", "score"}
        assert isinstance(item["name"], str)
        assert isinstance(item["score"], float)


def test_scores_match_formula():
    expected = {o["name"]: o["demand_growth"] * o["supply_inelasticity"] for o in OPPORTUNITIES}
    for row in ranked():
        assert abs(row["score"] - expected[row["name"]]) < 1e-9
