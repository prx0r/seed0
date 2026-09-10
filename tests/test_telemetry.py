

def test_metered_run_validates_both_paths(tmp_path, monkeypatch):
    import sys as _sys
    from telemetry import metered_run, PRICES
    r = metered_run("mimo-v2.5", 1000, 500, 1.25)
    assert r["cost_usd"] == round(1000 / 1e6 * 0.14 + 500 / 1e6 * 0.28, 6)
    assert r["usage_source"] == "reported"
    r2 = metered_run("unknown-model", 10, 5, 0.5)
    assert r2["cost_usd"] is None  # unpriced: recorded, never guessed
    import pytest as _pt
    with _pt.raises((ValueError, Exception)):
        metered_run("mimo-v2.5", -1, 0, 0.5)
    # fallback path: pydantic hidden -> identical stdlib contract
    monkeypatch.setitem(_sys.modules, "pydantic", None)
    import importlib as _il
    import telemetry as _tm
    _il.reload(_tm)
    try:
        rf = _tm.metered_run("mimo-v2.5", 1000, 500, 1.25)
        assert rf["cost_usd"] == r["cost_usd"]
        with _pt.raises(ValueError):
            _tm.metered_run("mimo-v2.5", 0, 0, -2.0)
    finally:
        _il.reload(_tm)


def test_stopwatch_monotonic_and_external_timing():
    import time as _t
    from telemetry import Stopwatch, timed_subprocess
    sw = Stopwatch()
    _t.sleep(0.05)
    e1 = sw.elapsed()
    assert 0.04 <= e1 <= 2.0
    sw.reset()
    assert sw.elapsed() < e1
    r = timed_subprocess(["python3", "-c", "print('hi')"])
    assert r["returncode"] == 0 and r["stdout_tail"] == "hi"
    assert r["elapsed_s"] >= 0
    r = timed_subprocess(["python3", "-c", "import time; time.sleep(0.2)"])
    assert 0.15 <= r["elapsed_s"] <= 5.0  # external clock sees real time
    r = timed_subprocess(["python3", "-c", "import sys; sys.exit(3)"])
    assert r["returncode"] == 3


def test_validate_usage_tripwires():
    from telemetry import validate_usage
    req = "x" * 1000
    resp = "y" * 500
    assert validate_usage(req, resp, {"input_tokens": 250, "output_tokens": 120}) == []
    assert validate_usage(req, resp, {"input_tokens": -1, "output_tokens": 0}) != []
    assert validate_usage(req, resp, {"input_tokens": 5000, "output_tokens": 5}) != []  # more tokens than chars
    assert validate_usage("", resp, {"input_tokens": 10, "output_tokens": 5}) != []
    assert validate_usage(req, "", {"input_tokens": 5, "output_tokens": 9}) != []
    assert validate_usage(req, resp, {"input_tokens": "lots", "output_tokens": 5}) != []
