"""instrument dispatch: every key against real machinery on tmp roots."""
import json
import time

import instrument as I


def _root(tmp_path):
    now = time.time()
    loop = tmp_path / "loop"
    loop.mkdir()
    (loop / "tasks.jsonl").write_text("\n".join([
        json.dumps({"id": "a-1", "tier": "A", "summary": "done work",
                    "status": "DONE", "blocked_by": []}),
        json.dumps({"id": "a-2", "tier": "A", "summary": "ready work",
                    "status": "JUSTIFIED", "blocked_by": []}),
        json.dumps({"id": "a-3", "tier": "A", "summary": "blocked work",
                    "status": "JUSTIFIED", "blocked_by": ["a-9"]}),
    ]) + "\n")
    (loop / "registry_h.jsonl").write_text("\n".join([
        json.dumps({"id": "h-a1", "kind": "request", "h_kind": "approval",
                    "summary": "approve plan", "status": "open", "ts": now,
                    "unlocks": ["a-2"], "options": []}),
        json.dumps({"id": "h-c1", "kind": "request", "h_kind": "input",
                    "summary": "pick lane", "status": "open", "ts": now,
                    "unlocks": [], "options": ["fast", "safe"]}),
    ]) + "\n")
    (loop / "heuristics.md").write_text("# H\n- retry with evidence\n")
    return str(tmp_path)


def test_zoom_and_dig_readonly(tmp_path):
    r = _root(tmp_path)
    p = I.run("2", session="t", root=r)
    assert p["results"][0]["ok"]
    assert "achieved 1 / missing 2" in p["close"]
    p = I.run("3", session="t", root=r)
    assert "retry with evidence" in p["results"][0]["detail"]["heuristics"]


def test_go_orders_ready_not_blocked(tmp_path):
    r = _root(tmp_path)
    p = I.run("1", session="t", root=r)
    assert p["results"][0]["detail"]["ready"] == ["a-2"]
    assert "a-2" in p["close"]


def test_halt_brake_and_resume(tmp_path):
    r = _root(tmp_path)
    assert I.run("0", session="t", root=r)["results"][0]["action"] == "halt"
    p = I.run("1", session="t", root=r)
    assert p["results"][0]["ok"] is False  # executing keys refuse
    p = I.run("2", session="t", root=r)
    assert p["results"][0]["ok"] is True   # read-only survives halt
    assert I.run("0", session="t", root=r)["results"][0]["action"] == "resume"
    assert I.run("1", session="t", root=r)["results"][0]["ok"] is True


def test_pick_ok_no_tell_flow(tmp_path):
    r = _root(tmp_path)
    p = I.run("41", session="t", root=r)
    assert "option 1" in p["results"][0]["close"]  # picked "safe"
    p = I.run("5", session="t", root=r)
    assert "approved h-a1" in p["close"]
    p = I.run("5", session="t", root=r)
    assert p["results"][0]["ok"] is False  # nothing left to approve
    p = I.run("6", session="t", root=r)
    assert p["results"][0]["ok"] is False  # nothing left to deny


def test_tell_guards_and_delivers(tmp_path):
    r = _root(tmp_path)
    p = I.run("7", session="t", root=r)
    assert p["results"][0]["action"] == "needs-text"
    p = I.run("7", session="t", root=r,
              payloads={"7": "sk-" + "abc123XYZ4567890DEF"})
    assert p["results"][0]["action"] == "secret-refused"
    p = I.run("7", session="t", root=r, payloads={"7": "user@mail.com"})
    assert "delivered to h-c1" in p["close"]


def test_goal_and_fix_state(tmp_path):
    r = _root(tmp_path)
    p = I.run("84", session="t", root=r)
    assert "goal now T4" in p["close"]
    assert json.loads((tmp_path / "loop" / "goal.json").read_text())["active"] == "T4"
    p = I.run("9", session="t", root=r, payloads={"9": "brief is vague"})
    assert "correction c-" in p["close"]
    p = I.run("9", session="t", root=r)
    assert "correction c-" in p["close"]  # bare 9 works too


def test_presses_logged_with_outcomes(tmp_path):
    import press as P
    r = _root(tmp_path)
    I.run("51", session="t", root=r)
    rows = P.read(r)
    assert [x["picked_text"] for x in rows] == ["OK", "GO"]
    assert all(x["session"] == "t" and x["chain"] == "51" for x in rows)
    assert rows[0]["outcome"] == {"action": "approve", "ok": True}
