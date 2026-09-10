"""grants.py tests: ceiling enforcement, purpose/expiry lock, receipts, treasury."""
import pytest

from grants import (GrantDenied, new_grant, activate, state, check_spend,
                    record_receipt, verify_receipt, Treasury, select_tier,
                    metered_call, log_spend)


def live_grant(tmp_path, cents=100, purpose="eval-run"):
    p = str(tmp_path / "m.jsonl")
    g = new_grant(cents, purpose, "https://x402.egoic.ai/v1/work", path=p)
    activate(g["id"], path=p)
    return g["id"], p


def test_grant_lifecycle_exact_amount(tmp_path):
    gid, p = live_grant(tmp_path)
    check_spend(gid, 100, "eval-run", path=p)
    record_receipt(gid, {"tx": "abc123xyz789", "amount_cents": 60,
                         "endpoint": "https://x402.egoic.ai/v1/work",
                         "ts": 1.0}, path=p)
    st = state(gid, p)
    assert (st["status"], st["spent_cents"], st["remaining_cents"]) == ("active", 60, 40)
    with pytest.raises(GrantDenied):
        check_spend(gid, 41, "eval-run", path=p)  # over remaining ceiling
    record_receipt(gid, {"tx": "def456uvw012", "amount_cents": 40,
                         "endpoint": "https://x402.egoic.ai/v1/work",
                         "ts": 2.0}, path=p)
    assert state(gid, p)["status"] == "spent"


def test_purpose_expiry_status_locks(tmp_path):
    p = str(tmp_path / "m.jsonl")
    g = new_grant(50, "eval-run", "ep", path=p)
    with pytest.raises(GrantDenied):
        check_spend(g["id"], 10, "eval-run", path=p)  # proposed, not active
    activate(g["id"], path=p)
    with pytest.raises(GrantDenied):
        check_spend(g["id"], 10, "other-purpose", path=p)
    with pytest.raises(GrantDenied):
        new_grant(0, "x", "ep", path=p)
    with pytest.raises(GrantDenied):
        new_grant(10.5, "x", "ep", path=p)  # integer cents only
    assert state(g["id"], p, now=1e12)["status"] == "expired"


def test_receipt_shape_gate(tmp_path):
    gid, p = live_grant(tmp_path)
    assert verify_receipt({"tx": "abc123xyz789", "amount_cents": 5,
                           "endpoint": "e", "ts": 1.0}) is True
    for bad in [{"tx": "short", "amount_cents": 5, "endpoint": "e", "ts": 1.0},
                {"tx": "abc123xyz789", "amount_cents": -1, "endpoint": "e", "ts": 1.0},
                {"tx": "abc123xyz789", "amount_cents": 5, "ts": 1.0}]:
        assert verify_receipt(bad) is False
        with pytest.raises(GrantDenied):
            record_receipt(gid, bad, path=p)


def test_treasury_fail_closed():
    t = Treasury()
    t.register_bucket("cf-neurons", "neurons", 1000)
    t.fund(0.05)
    t.charge("cf-neurons", 100)
    assert t.buckets["cf-neurons"]["remaining"] == 900
    with pytest.raises(GrantDenied):
        t.charge("cf-neurons", 10000)
    with pytest.raises(GrantDenied):
        t.charge("nope", 1)
    with pytest.raises(GrantDenied):
        t.charge("cf-neurons", 1, money_usd=99.0)
    assert select_tier(0.0)["tier"] == "free"
    assert select_tier(1.0, uncertainty=0.9)["tier"] == "strong"


def test_metered_call_accumulates_and_logs(tmp_path):
    acc = {}
    out = metered_call(lambda: ("tok", 1000, 500), acc, model="mimo-v2.5")
    assert out == "tok"
    assert acc["input_tokens"] == 1000 and acc["output_tokens"] == 500
    assert acc["cost_usd"] == round(1000 / 1e6 * 0.14 + 500 / 1e6 * 0.28, 6)
    sp = str(tmp_path / "spend.jsonl")
    log_spend(sp, {"model": "mimo-v2.5", "in": 1, "out": 2})
    assert len(open(sp).read().splitlines()) == 1


def test_escalate_tier_policy():
    from grants import escalate_tier
    assert escalate_tier("free", False)["tier"] == "free"
    assert escalate_tier("free", True)["tier"] == "cheap"
    assert escalate_tier("cheap", True)["tier"] == "strong"
    top = escalate_tier("strong", True)
    assert top["tier"] == "strong" and top["escalate_human"] is True
    assert escalate_tier("???", True)["tier"] == "free"
