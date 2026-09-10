import sys

sys.path.insert(0, ".")
from tasks import Feed, new_task


def test_predict_unblocks_and_reconcile_reverifies(tmp_path):
    f = Feed(tmp_path / "t.jsonl")
    creds = f.add(new_task("human", "Telnyx API key", needed_from="owner",
                           options=["paste key", "skip voice"]))
    build = f.add(new_task("agent", "Wire SIP dispatch",
                           blocked_by=[creds["id"]]))
    assert f.agent_tasks() == []  # blocked: no prediction yet
    f.predict(creds["id"], {"TELNYX_API_KEY": "MOCK"}, note="shape only")
    assert [t["id"] for t in f.agent_tasks()] == [build["id"]]  # unblocked on mock
    build["status"] = "done"
    f._save(build)
    f.deliver(creds["id"], {"TELNYX_API_KEY": "REAL"}, receipt="owner pasted")
    affected = f.reconcile(creds["id"])
    assert [t["id"] for t in affected] == [build["id"]]  # must re-verify on real data
    assert f.tasks[build["id"]]["status"] == "open"


def test_expire_reescalates_never_approves(tmp_path):
    f = Feed(tmp_path / "t.jsonl")
    t = new_task("human", "Approve spend", ttl_s=-1)
    f.add(t)
    out = f.expire()
    assert [x["id"] for x in out] == [t["id"]]
    assert f.tasks[t["id"]]["status"] == "open"  # re-escalated, NOT approved


def test_feeds_separate(tmp_path):
    f = Feed(tmp_path / "t.jsonl")
    h = f.add(new_task("human", "Decide name"))
    a = f.add(new_task("agent", "Scaffold repo"))
    assert [t["id"] for t in f.human_tasks()] == [h["id"]]
    assert [t["id"] for t in f.agent_tasks()] == [a["id"]]
