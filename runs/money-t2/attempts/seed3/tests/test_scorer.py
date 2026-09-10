import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scorer import OPPORTUNITIES, ranked, score


def test_ranking_order_descending():
    rows = ranked()
    scores = [r["score"] for r in rows]
    assert scores == sorted(scores, reverse=True)
    assert rows[0]["name"] == "ev-panel-brokerage"


def test_score_math_is_product():
    opp = {"name": "x", "demand_growth": 0.8, "supply_inelasticity": 0.5}
    assert score(opp) == 0.8 * 0.5
    assert len(OPPORTUNITIES) == 5


def test_json_shape_ranked_stdout():
    r = subprocess.run([sys.executable, "scorer.py"],
                       cwd=Path(__file__).resolve().parent.parent,
                       capture_output=True, text=True, timeout=60)
    rows = json.loads(r.stdout)
    assert isinstance(rows, list) and len(rows) == 5
    assert all(set(x) == {"name", "score"} for x in rows)
    assert all(isinstance(x["score"], float) for x in rows)
