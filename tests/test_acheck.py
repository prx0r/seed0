"""acheck: self-audit for A-task nativeness."""
import json
import time

import acheck as A


def _q(tmp_path, recs):
    q = tmp_path / "tasks.jsonl"
    q.write_text("\n".join(json.dumps(r, sort_keys=True) for r in recs) + "\n")
    (tmp_path / "a-logs").mkdir(exist_ok=True)
    (tmp_path / "reports").mkdir(exist_ok=True)
    return q


def _good(done=True):
    return [
        {"id": "a-1", "tier": "A", "summary": "w", "status": "DONE",
         "blocked_by": [], "validation_ref": "r-1.json",
         "report_ref": "reports/a-1.md"},
        {"id": "a-2", "tier": "A", "summary": "w2", "status": "JUSTIFIED",
         "blocked_by": ["a-1"]},
    ]


def test_clean_queue_passes(tmp_path):
    q = _q(tmp_path, _good())
    (tmp_path / "r-1.json").write_text("{}")
    (tmp_path / "reports" / "a-1.md").write_text("# done\n")
    assert A.check(q, tmp_path / "a-logs", tmp_path / "reports") == []


def test_done_without_proof_fails(tmp_path):
    recs = _good()
    del recs[0]["validation_ref"]
    q = _q(tmp_path, recs)
    f = A.check(q, tmp_path / "a-logs", tmp_path / "reports")
    assert any("DONE without validation_ref" in x for x in f)


def test_unresolvable_receipt_fails(tmp_path):
    q = _q(tmp_path, _good())  # r-1.json NOT created
    f = A.check(q, tmp_path / "a-logs", tmp_path / "reports")
    assert any("validation_ref unresolvable" in x for x in f)


def test_sha256_uri_resolves_like_loop(tmp_path):
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs" / "sha256_abc123.json").write_text("{}")
    recs = _good()
    recs[0]["validation_ref"] = "sha256:abc123"
    q = _q(tmp_path, recs)
    (tmp_path / "reports" / "a-1.md").write_text("# done\n")
    assert A.check(q, tmp_path / "a-logs", tmp_path / "reports") == []
    recs[0]["validation_ref"] = "sha256:ghost000"
    q = _q(tmp_path, recs)
    f = A.check(q, tmp_path / "a-logs", tmp_path / "reports")
    assert any("validation_ref unresolvable" in x for x in f)


def test_dangling_blocker_and_bad_status(tmp_path):
    q = _q(tmp_path, [
        {"id": "a-x", "tier": "A", "summary": "w", "status": "YOLO",
         "blocked_by": ["a-ghost"]}])
    f = A.check(q, tmp_path / "a-logs", tmp_path / "reports")
    assert any("dangling blocked_by 'a-ghost'" in x for x in f)
    assert any("bad status 'YOLO'" in x for x in f)


def test_executing_needs_fresh_alog(tmp_path):
    q = _q(tmp_path, [
        {"id": "a-e", "tier": "A", "summary": "w", "status": "EXECUTING",
         "blocked_by": []}])
    al = tmp_path / "a-logs"
    f = A.check(q, al, tmp_path / "reports")
    assert any("EXECUTING with no a-log" in x for x in f)
    (al / "a-e.jsonl").write_text('{"action":"started"}\n')
    assert A.check(q, al, tmp_path / "reports") == []
    old = time.time() - 100000
    import os
    os.utime(al / "a-e.jsonl", (old, old))
    f = A.check(q, al, tmp_path / "reports", stale_hours=24)
    assert any("STALE" in x for x in f)


def test_missing_queue_is_a_finding(tmp_path):
    f = A.check(tmp_path / "nope.jsonl", tmp_path, tmp_path)
    assert f == [f"queue missing: {tmp_path / 'nope.jsonl'}"]
