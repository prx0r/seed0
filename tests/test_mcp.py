"""mcp_server round-trip: initialize -> list -> call, over real stdio."""
import json
import subprocess
import sys
from pathlib import Path

SRV = str(Path(__file__).resolve().parent.parent / "mcp_server.py")


def _session(calls: list[dict]) -> list[dict]:
    p = subprocess.run(
        [sys.executable, "-u", SRV], input="\n".join(json.dumps(c) for c in calls),
        capture_output=True, text=True, timeout=120,
        cwd=Path(__file__).resolve().parent.parent)
    assert p.returncode == 0, p.stderr[-500:]
    return [json.loads(l) for l in p.stdout.splitlines() if l.strip()]


def test_initialize_list_call_roundtrip():
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    lst = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    chk = {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
           "params": {"name": "seed0_check",
                      "arguments": {"path": "tests/fixtures/good"}}}
    bad = {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
           "params": {"name": "nope", "arguments": {}}}
    r1, r2, r3, r4 = _session([init, lst, chk, bad])
    assert r1["result"]["serverInfo"]["name"] == "seed0"
    names = {t["name"] for t in r2["result"]["tools"]}
    assert {"seed0_check", "loop_list", "loop_ready",
            "loop_stoplight", "loop_history", "ham_check"} <= names
    assert "COMPLIANT" in r3["result"]["content"][0]["text"]
    assert r4["error"]["code"] == -32000


def test_stoplight_and_ham_via_mcp():
    sl = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "loop_stoplight", "arguments": {"id": "ghost"}}}
    hc = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
          "params": {"name": "ham_check",
                     "arguments": {"action": "git push --force origin main"}}}
    r1, r2 = _session([sl, hc])
    assert "NOGO" in r1["result"]["content"][0]["text"]
    assert "PROHIBITED" in r2["result"]["content"][0]["text"]
