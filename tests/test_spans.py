"""spans.py tests: nesting, schema, rollup math, OTLP adapter shape."""
from spans import Tracer, to_otlp


def test_nesting_and_parentage(tmp_path):
    t = Tracer(str(tmp_path / "s.jsonl"), service="t")
    with t.span("root", a=1) as r:
        r.event("mid", {"k": "v"})
        with t.span("child") as c:
            c.attr("gen_ai.usage.prompt_tokens", 10)
            c.attr("gen_ai.usage.completion_tokens", 5)
            c.attr("llm.estimated_cost_usd", 0.001)
    assert len(t.finished) == 2
    by_name = {s["name"]: s for s in t.finished}
    assert by_name["child"]["parent_id"] == by_name["root"]["span_id"]
    assert by_name["root"]["parent_id"] is None
    assert len(by_name["root"]["trace_id"]) == 32
    assert by_name["root"]["events"][0]["name"] == "mid"
    assert by_name["child"]["elapsed_s"] >= 0
    assert by_name["child"]["status"] == "OK"


def test_error_status_and_rollup(tmp_path):
    import pytest as _pt
    t = Tracer(str(tmp_path / "s.jsonl"))
    with _pt.raises(ValueError):
        with t.span("boom") as s:
            s.attr("gen_ai.usage.prompt_tokens", 4)
            raise ValueError("x")
    assert len(t.finished) == 1  # emitted despite exception
    assert t.finished[0]["status"].startswith("ERROR")
    rep = t.rollup()
    assert rep == {"trace_id": t.trace_id, "spans": 1, "input_tokens": 4,
                   "output_tokens": 0, "cost_usd": 0.0,
                   "elapsed_s": t.finished[0]["elapsed_s"]}


def test_otlp_shape():
    t = Tracer()
    with t.span("n", **{"gen_ai.response.model": "m"}) as s:
        pass
    o = to_otlp(t.finished[0])
    assert o["name"] == "n" and o["traceId"] == t.trace_id
    assert any(a["key"] == "gen_ai.response.model" for a in o["attributes"])
