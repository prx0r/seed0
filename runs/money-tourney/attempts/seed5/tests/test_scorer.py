import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scorer import OPPORTUNITIES, ranked, score_opp


def test_ranking_order():
    r = ranked()
    scores = [d["score"] for d in r]
    assert scores == sorted(scores, reverse=True)
    assert r[0]["name"] == "landlord-eicr-remedials-manchester"


def test_score_math():
    for o in OPPORTUNITIES:
        assert score_opp(o) == o["demand_growth"] * o["supply_inelasticity"]
    assert len(OPPORTUNITIES) == 5


def test_json_shape_stdout():
    p = subprocess.run([sys.executable, "scorer.py"], capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent.parent))
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert isinstance(data, list) and len(data) == 5
    for d in data:
        assert set(d.keys()) == {"name", "score"}
        assert isinstance(d["name"], str) and isinstance(d["score"], float)
