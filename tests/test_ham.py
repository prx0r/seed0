"""ham.py tests: prohibited screen, digest-bound approvals, standing ratchet."""
from pathlib import Path

from ham import (check_prohibited, approve, approval_valid, log_decision,
                 record_outcome, standing)

SK_LIT = "sk-" + "abc123XYZ4567890"  # split so this file stays scanner-clean


def test_prohibited_catches_all_five():
    bad = ["git commit -a -m x .env",
           "git push --force origin main",
           "rm -rf / --no-preserve-root",
           "echo " + SK_LIT,
           "run eval on gpt-oss-120b"]
    for action in bad:
        assert check_prohibited(action) != [], action
    ids = {h["id"] for a in bad for h in check_prohibited(a)}
    assert len(ids) == 5, ids


def test_clean_actions_pass():
    for action in ["python3 -m pytest tests/ -q", "git status --short",
                   "git push origin sparky-vertical", "cat .env.example"]:
        assert check_prohibited(action) == [], action


def test_ham_source_is_self_clean():
    from seed0 import SECRET_RES
    src = Path(__file__).resolve().parent.parent / "ham.py"
    text = src.read_text()
    assert check_prohibited(text) == []
    assert not any(rx.search(text) for rx in SECRET_RES)


def test_approval_bound_to_digest_then_void(tmp_path):
    target = tmp_path / "plan.md"
    target.write_text("v1")
    log = str(tmp_path / "decisions.jsonl")
    rec = approve("H-test", str(target), by="owner", log_path=log)
    assert approval_valid(rec, str(target)) is True
    target.write_text("v1 edited")
    assert approval_valid(rec, str(target)) is False
    assert approval_valid({"kind": "A", "target_digest": "x"}, str(target)) is False


def test_decision_ids_content_addressed(tmp_path):
    log = str(tmp_path / "d.jsonl")
    a = log_decision("M", "eval run", cost_usd=0.001, log_path=log)
    b = log_decision("M", "eval run", cost_usd=0.001, log_path=log)
    assert a["id"] == b["id"]  # ts excluded from id


def test_standing_ratchet_and_denial_blocks(tmp_path):
    pol = str(tmp_path / "ham_policy.json")
    assert standing("push:branch", pol) == "ask"
    record_outcome("push:branch", True, pol)
    record_outcome("push:branch", True, pol)
    assert standing("push:branch", pol) == "ask"
    record_outcome("push:branch", True, pol)
    assert standing("push:branch", pol) == "allow"
    record_outcome("never:thing", False, pol)
    for _ in range(5):
        record_outcome("never:thing", True, pol)
    assert standing("never:thing", pol) == "ask"
