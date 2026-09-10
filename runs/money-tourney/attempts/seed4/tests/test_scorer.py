import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scorer import OPPORTUNITIES, ranked, score


def test_ranking_order():
    r = ranked()
    assert [d["name"] for d in r] == [
        "eicr-remedial-slots",
        "ev-charger-installs",
        "heat-pump-commissioning",
        "solar-rooftop-retrofit",
        "smart-meter-swaps",
    ]
    scores = [d["score"] for d in r]
    assert scores == sorted(scores, reverse=True)


def test_score_math():
    for o in OPPORTUNITIES:
        assert score(o) == o["demand_growth"] * o["supply_inelasticity"]
    assert abs(score(OPPORTUNITIES[0]) - 0.765) < 1e-9
    assert len(OPPORTUNITIES) == 5


def test_json_shape_stdout():
    root = Path(__file__).resolve().parent.parent
    out = subprocess.run(
        [sys.executable, str(root / "scorer.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert out.returncode == 0
    data = json.loads(out.stdout)
    assert isinstance(data, list) and len(data) == 5
    for d in data:
        assert set(d.keys()) == {"name", "score"}
        assert isinstance(d["name"], str)
        assert isinstance(d["score"], float)


def test_top_is_chosen_wedge():
    r = ranked()
    assert r[0]["name"] == "eicr-remedial-slots"
