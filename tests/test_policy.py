"""policy.py tests: cold heuristic ordering, learning direction, regret, persistence."""
from policy import CheckinPolicy


def test_cold_heuristic_orders_risk(tmp_path):
    pol = CheckinPolicy(str(tmp_path / "p.json"))
    risky = pol.decide({"action_class": "push:main", "diff_lines": 500,
                        "files": 12, "security": 1})
    trivial = pol.decide({"action_class": "docs:typo", "diff_lines": 2,
                          "files": 1, "security": 0})
    assert risky["verdict"] == "checkin" and risky["learned"] is False
    assert trivial["verdict"] == "proceed"
    assert risky["p_checkin"] > trivial["p_checkin"]


def test_learning_moves_with_evidence(tmp_path):
    pol = CheckinPolicy(str(tmp_path / "p.json"))
    act = {"action_class": "push:branch", "diff_lines": 40, "files": 3}
    p0 = pol.predict(act)
    for _ in range(12):
        pol.observe(dict(act), approved=False)
    assert pol.samples == 12
    p_denied = pol.predict(act)
    assert p_denied > p0, (p0, p_denied)
    assert pol.decide(act)["learned"] is True
    pol2 = CheckinPolicy(str(tmp_path / "p.json"))
    for _ in range(12):
        pol2.observe(dict(act), approved=True)
    assert pol2.predict(act) < p_denied  # approvals pull the other way


def test_regret_counts_as_denial_and_persists(tmp_path):
    p = str(tmp_path / "p.json")
    pol = CheckinPolicy(p)
    pol.observe({"action_class": "x"}, approved=True, regret=True)
    assert pol.history["x"] == {"approved": 0, "denied": 1}
    pol2 = CheckinPolicy(p)  # reload from disk
    assert pol2.history["x"]["denied"] == 1 and pol2.samples == 1
