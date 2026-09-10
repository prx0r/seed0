import json
import sys

from budgets import Budget, BudgetExceeded
from telemetry import Meter, cost_usd, file_version


def test_budget_trips_and_callbacks():
    seen = []
    b = Budget(max_usd=0.01, on_spend=[seen.append])
    b.record(tokens=10, cost=0.005, label="a")
    assert seen and seen[0]["spent_usd"] == 0.005
    try:
        b.record(tokens=10, cost=0.006, label="b")
        assert False, "should have raised"
    except BudgetExceeded as e:
        assert "exhausted" in str(e)


def test_unknown_model_costs_null_but_counts_tokens():
    assert cost_usd("nope-9", 100, 50) is None
    assert cost_usd("mimo-v2.5", 1000000, 0) == 0.14


def test_zero_budget_stops_pyeval_run(tmp_path, monkeypatch):
    import urllib.request
    from pyeval import run
    from budgets import Budget

    class FakeResp:
        def __init__(self, p): self._b = json.dumps(p).encode()
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return self._b

    def fake_open(req, timeout=None):
        return FakeResp({"choices": [{"message": {"content": "hi"}}]})

    monkeypatch.setattr(urllib.request, "urlopen", fake_open)
    ds = tmp_path / "d.json"
    ds.write_text(json.dumps({"cases": [
        {"id": "c1", "input": "q", "expect": {"contains": ["hi"]}, "weight": 1},
        {"id": "c2", "input": "q", "expect": {"contains": ["hi"]}, "weight": 1}]}))
    rep = run(str(ds), "m", "http://x", "k", budget=Budget(max_tokens=0))
    assert [r["why"] for r in rep["results"]] == [
        "budget exhausted — run stopped, not failed"] * 2
    assert rep["pass"] is False  # stopped, honestly not passed


def test_meter_versions_and_funnel_env(tmp_path):
    f = tmp_path / "idea.md"
    f.write_text("idea text")
    m = Meter(model="mimo-v2.5", idea=str(f), criteria="")
    assert m.block()["idea_version"] == file_version(str(f))
    assert file_version("/nonexistent-xyz") == "missing"
    import subprocess
    probe = tmp_path / "probe.sh"
    probe.write_text('#!/bin/sh\necho "USD=$SEED_BUDGET_USD TOK=$SEED_BUDGET_TOKENS"\n')
    probe.chmod(0o755)
    import os
    env = dict(os.environ)
    from budgets import from_env
    os.environ["SEED_BUDGET_USD"] = "0.5"
    try:
        b = from_env()
        env.update(b.advertise())
        r = subprocess.run([str(probe)], capture_output=True, text=True, env=env)
        assert "USD=0.5" in r.stdout
    finally:
        del os.environ["SEED_BUDGET_USD"]


def test_pre_call_refusal_fires_before_transport():
    from budgets import Budget, BudgetExceeded
    b = Budget(max_tokens=0)
    with __import__("pytest").raises(BudgetExceeded):
        b.check("case-1")
    b2 = Budget(max_tokens=10)
    b2.check("case-1")  # no raise when headroom


def test_pyeval_zero_budget_makes_no_calls(tmp_path, monkeypatch):
    import urllib.request as _url
    from pyeval import run
    from budgets import Budget
    called = []
    monkeypatch.setattr(_url, "urlopen", lambda *a, **k: called.append(1) or 1 / 0)
    ds = tmp_path / "d.json"
    ds.write_text(__import__("json").dumps(
        {"cases": [{"id": "c1", "input": "hi",
                    "expect": {"contains": ["x"]}, "weight": 1}]}))
    rep = run(str(ds), "m", "http://x", "k", budget=Budget(max_tokens=0))
    assert called == [] and rep["score"] == 0
    assert "budget" in rep["results"][0]["why"]


def test_max_usd_trips_and_precheck_refuses():
    from budgets import Budget, BudgetExceeded
    import pytest as _pt
    b = Budget(max_usd=0.01)
    b.record(tokens=5, cost=0.004, label="t1")
    assert b.exhausted() is False
    with _pt.raises(BudgetExceeded):
        b.record(tokens=5, cost=0.008, label="t2")  # crosses $0.01
    b2 = Budget(max_usd=0.005)
    b2.record(tokens=1, cost=0.004, label="t1")
    b2.check("still-room")  # under cap: passes
    with _pt.raises(BudgetExceeded):
        b2.record(tokens=1, cost=0.002, label="t2")  # crosses the line
    with _pt.raises(BudgetExceeded):
        b2.check("next-call")  # pre-call refusal, no transport touched
