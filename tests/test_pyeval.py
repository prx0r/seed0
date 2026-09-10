import io
import json
import sys
import urllib.request

from pyeval import run, grade_rule


class FakeResp:
    def __init__(self, payload):
        self._b = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._b


def _stub(monkeypatch, answers):
    calls = {"n": 0}

    def fake_open(req, timeout=None):
        body = json.loads(req.data.decode())
        text = answers[min(calls["n"], len(answers) - 1)]
        calls["n"] += 1
        msg = body["messages"][-1]["content"]
        assert "sk-" not in msg and "OPENCODE_GO" not in msg  # key never in body
        return FakeResp({"choices": [{"message": {"content": text}}]})

    monkeypatch.setattr(urllib.request, "urlopen", fake_open)
    return calls


def test_rule_and_judge_paths(tmp_path, monkeypatch):
    ds = tmp_path / "d.json"
    ds.write_text(json.dumps({"cases": [
        {"id": "r1", "input": "q", "expect": {"contains": ["hello"]},
         "evaluator": "rule", "weight": 1},
        {"id": "j1", "input": "q", "evaluator": "judge", "rubric": "R",
         "weight": 2}]}))
    _stub(monkeypatch, ["hello there", "VERDICT: PASS. Reason: fine"])
    rep = run(str(ds), "m", "http://x", "k")
    assert rep["pass"] is True and rep["score"] == 3.0


def test_judge_fail_and_transport_error(tmp_path, monkeypatch):
    ds = tmp_path / "d.json"
    ds.write_text(json.dumps({"cases": [
        {"id": "j1", "input": "q", "evaluator": "judge", "rubric": "R",
         "weight": 1}]}))
    _stub(monkeypatch, ["blah", "VERDICT: FAIL. Reason: bad"])
    rep = run(str(ds), "m", "http://x", "k")
    assert rep["pass"] is False

    def boom(req, timeout=None):
        raise ConnectionError("down")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    rep2 = run(str(ds), "m", "http://x", "k")
    assert rep2["results"][0]["pass"] is False
    assert "transport" in rep2["results"][0]["why"]


def test_grade_rule_contract():
    ok, _ = grade_rule("Costs £950-£1400 depending on scope",
                       {"contains": ["£"], "absent": ["guaranteed"]})
    assert ok is True
    ok, why = grade_rule("Guaranteed £950 total", {"absent": ["guaranteed"]})
    assert ok is False and "forbidden" in why


def test_spend_log_hook_no_network(tmp_path, monkeypatch):
    import json as _json
    import urllib.request as _url
    from pyeval import complete
    from telemetry import Meter

    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self):
            return _json.dumps({"usage": {"input_tokens": 10, "output_tokens": 4},
                                "choices": [{"message": {"content": "hi"}}]}).encode()

    monkeypatch.setattr(_url, "urlopen", lambda *a, **k: FakeResp())
    sp = str(tmp_path / "spend.jsonl")
    monkeypatch.setenv("SPEND_LOG", sp)
    m = Meter(model="mimo-v2.5")
    assert complete("http://x", "k", "mimo-v2.5", [], meter=m) == "hi"
    assert (m.input_tokens, m.output_tokens) == (10, 4)
    lines = open(sp).read().splitlines()
    assert len(lines) == 1 and _json.loads(lines[0])["out"] == 4



def test_resolve_model_auto_no_network():
    from pyeval import resolve_model
    from budgets import Budget
    m, why = resolve_model({"--model": "mimo-v2.5"}, None)
    assert (m, why) == ("mimo-v2.5", "explicit")
    m, why = resolve_model({"--model": "auto"}, Budget(max_usd=0.0005))
    assert m == "mimo-v2.5" and "free" in why  # thin budget -> free tier
    m, why = resolve_model({"--model": "auto", "--uncertainty": "0.9"},
                           Budget(max_usd=5.0))
    assert m == "muse-spark-1.3-contributor" and "strong" in why


def test_per_case_telemetry_present_no_network(tmp_path, monkeypatch):
    import json as _json
    import urllib.request as _url
    from pyeval import run
    from budgets import Budget

    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self):
            return _json.dumps({"usage": {"input_tokens": 20, "output_tokens": 8},
                                "choices": [{"message": {"content": "needle here"}}]}).encode()

    monkeypatch.setattr(_url, "urlopen", lambda *a, **k: FakeResp())
    ds = tmp_path / "d.json"
    ds.write_text(_json.dumps(
        {"cases": [{"id": "c1", "input": "find needle",
                    "expect": {"contains": ["needle"]}, "weight": 1}]}))
    rep = run(str(ds), "mimo-v2.5", "http://x", "k", budget=Budget(max_usd=1.0))
    r = rep["results"][0]
    assert r["pass"] is True
    assert (r["input_tokens"], r["output_tokens"]) == (20, 8)
    assert r["elapsed_s"] >= 0 and r["cost_usd"] > 0
    assert rep["telemetry"]["input_tokens"] == 20
