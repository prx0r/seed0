"""Registry tests: lifecycle, M-lock, unlock graph, browser poll."""
import pytest
from ham_registry import Registry
def reg(tmp_path):
    return Registry(tmp_path / "ham.jsonl")
def test_a_close_needs_passing_evidence(tmp_path):
    r = reg(tmp_path)
    t = r.add("A", "demo", validation={"validator": "nonempty"})
    with pytest.raises(ValueError):
        r.close_a(t["id"], "", lambda e: bool(e))
    assert r.get(t["id"])["status"] == "open"
    r.close_a(t["id"], "evidence-log-line", lambda e: bool(e))
    assert r.get(t["id"])["status"] == "done"
def test_retire_archives_but_retains(tmp_path):
    r = reg(tmp_path)
    t = r.add("A", "demo")
    r.retire_criteria(t["id"], "superseded")
    g = r.get(t["id"])
    assert g["status"] == "archived" and g["validation"]["retired"]
def test_h_self_approve_refused(tmp_path):
    r = reg(tmp_path)
    t = r.add("H", "need human")
    with pytest.raises(PermissionError):
        r.approve_h(t["id"], "agent:me")
    r.approve_h(t["id"], "human:owner", "yes")
    assert r.get(t["id"])["status"] == "approved"
def test_m_spend_without_grant_refused(tmp_path):
    r = reg(tmp_path)
    t = r.add("M", "buy thing", cap=10)
    with pytest.raises(PermissionError):
        r.spend_m(t["id"], "nope", 5, "thing")
def test_m_grant_spend_double_spend_overcap_scope(tmp_path):
    r = reg(tmp_path)
    t = r.add("M", "buy thing", cap=10)
    _, tok = r.approve_m(t["id"], "human:owner", 8, "thing")
    with pytest.raises(PermissionError):
        r.spend_m(t["id"], tok, 9, "thing")  # over grant
    with pytest.raises(PermissionError):
        r.spend_m(t["id"], tok, 5, "other")  # purpose mismatch
    r.spend_m(t["id"], tok, 5, "thing")
    assert r.get(t["id"])["status"] == "spent"
    with pytest.raises(PermissionError):
        r.spend_m(t["id"], tok, 1, "thing")  # single-use
def test_m_grant_respects_cap(tmp_path):
    r = reg(tmp_path)
    t = r.add("M", "buy thing", cap=10)
    with pytest.raises(AssertionError):
        r.approve_m(t["id"], "human:owner", 50, "thing")
def test_revoke_kills_grant(tmp_path):
    r = reg(tmp_path)
    t = r.add("M", "buy thing", cap=10)
    _, tok = r.approve_m(t["id"], "human:owner", 8, "thing")
    r.revoke(t["id"], "human:owner", "changed-mind")
    with pytest.raises(PermissionError):
        r.spend_m(t["id"], tok, 5, "thing")
def test_unlock_graph_and_priority(tmp_path):
    r = reg(tmp_path)
    h = r.add("H", "approve funnel")
    a = r.add("A", "run funnel", blocked_by=[h["id"]])
    assert r.runnable_a() == []
    assert r.human_priority()[0]["id"] == h["id"]
    r.approve_h(h["id"], "human:owner")
    assert [t["id"] for t in r.runnable_a()] == [a["id"]]
def test_browser_poll_picks_up_external_approval(tmp_path):
    r = reg(tmp_path)
    t = r.add("H", "need human")
    r2 = Registry(r.path)  # browser-side handle appends
    r2.approve_h(t["id"], "human:owner", "via-ui")
    changed = r.poll()
    assert changed[t["id"]] == "approved"
