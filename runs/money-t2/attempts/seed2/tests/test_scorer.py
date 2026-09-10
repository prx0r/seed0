import json
import subprocess
import sys

sys.path.insert(0, ".")
from scorer import OPPORTUNITIES, ranked, score_opp


def test_ranking_order_descending():
    rows = ranked()
    scores = [r["score"] for r in rows]
    assert scores == sorted(scores, reverse=True)
    assert rows[0]["name"] == "dc_backup_witness_test"


def test_score_math():
    for o in OPPORTUNITIES:
        assert score_opp(o) == o["demand_growth"] * o["supply_inelasticity"]
    assert len(OPPORTUNITIES) == 5


def test_json_shape_stdout():
    p = subprocess.run([sys.executable, "scorer.py"], capture_output=True, text=True)
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert isinstance(data, list) and len(data) == 5
    for row in data:
        assert set(row.keys()) == {"name", "score"}
        assert isinstance(row["name"], str)
        assert isinstance(row["score"], float)
