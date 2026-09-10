"""agentrun tests: external timing, timeout kill, usage parsing, honesty labels."""
import json
import time

from agentrun import run_agent, read_usage_file


def test_external_timing_measures_real_time(tmp_path):
    r = run_agent("sleeper", ["python3", "-c", "import time; time.sleep(0.4)"],
                  model="", timeout_s=30, cwd=str(tmp_path))
    assert r["returncode"] == 0 and r["timed_out"] is False
    assert 0.35 <= r["elapsed_s"] <= 10.0  # harness clock, not agent claim
    assert r["usage_source"] == "no-inference" and r["cost_usd"] == 0.0


def test_timeout_kills_and_records(tmp_path):
    t0 = time.monotonic()
    r = run_agent("hang", ["python3", "-c", "import time; time.sleep(60)"],
                  timeout_s=2, cwd=str(tmp_path))
    wall = time.monotonic() - t0
    assert r["timed_out"] is True and r["returncode"] == -1
    assert r["elapsed_s"] < 20 and wall < 20  # killed, not waited out


def test_usage_file_shapes_parsed(tmp_path):
    f = tmp_path / "u.json"
    f.write_text(json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 25}}))
    assert read_usage_file(str(f)) == {"input_tokens": 100, "output_tokens": 25}
    f.write_text(json.dumps({"input_tokens": 5, "output_tokens": 2}))
    assert read_usage_file(str(f)) == {"input_tokens": 5, "output_tokens": 2}
    assert read_usage_file(str(tmp_path / "nope.json")) == {}
    f.write_text("not json{{")
    assert read_usage_file(str(f)) == {}


def test_failure_recorded_not_raised(tmp_path):
    r = run_agent("failer", ["python3", "-c", "import sys; sys.exit(3)"],
                  cwd=str(tmp_path))
    assert r["returncode"] == 3 and "elapsed_s" in r
