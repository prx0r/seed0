import json
import subprocess
import sys

from scorer import OPPORTUNITIES, score_opps


def test_ranking_order():
    ranked = score_opps()
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0]["name"] == "eicr_remedials_rentals"


def test_score_math():
    ranked = {r["name"]: r["score"] for r in score_opps()}
    assert abs(ranked["eicr_remedials_rentals"] - 0.90 * 0.85) < 1e-9
    assert abs(ranked["smart_home_retrofit"] - 0.60 * 0.40) < 1e-9
    assert len(OPPORTUNITIES) == 5


def test_json_shape():
    ranked = score_opps()
    assert isinstance(ranked, list) and len(ranked) == 5
    for row in ranked:
        assert set(row.keys()) == {"name", "score"}
        assert isinstance(row["name"], str)
        assert isinstance(row["score"], float)


def test_stdout_ranked_json():
    p = subprocess.run([sys.executable, "scorer.py"], capture_output=True, text=True)
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert [r["name"] for r in data] == [r["name"] for r in score_opps()]
