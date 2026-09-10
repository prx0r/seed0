#!/usr/bin/env python3
"""mcp_server.py — seed0 as an MCP server (stdio JSON-RPC, stdlib only).

Lets any MCP-capable agent use the harness upon clone, no install:
read-only surface (check/list/ready/stoplight/history/screen). NOTHING here
mutates: no approvals, no status writes, no spending. Writes stay on the CLI
where a human sees them.

  python3 mcp_server.py   # speaks JSON-RPC 2.0, newline-delimited, on stdio

opencode.json:
  {"mcp": {"seed0": {"type": "local",
    "command": ["python3", "/path/to/seed0/mcp_server.py"]}}}
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed0 import check as seed0_check
from loop import load as queue_load, stoplight
from ham import check_prohibited
import loop as _loop

ROOT = str(Path(__file__).resolve().parent)


def _tool_defs() -> list[dict]:
    return [
        {"name": "seed0_check",
         "description": "Compliance gate a project dir (5 checks). Returns report.",
         "inputSchema": {"type": "object",
                         "properties": {"path": {"type": "string"}},
                         "required": ["path"]}},
        {"name": "loop_list",
         "description": "List queue tasks, optional status filter.",
         "inputSchema": {"type": "object",
                         "properties": {"status": {"type": "string"}}}},
        {"name": "loop_ready",
         "description": "Actionable tasks (deps satisfied).",
         "inputSchema": {"type": "object", "properties": {}}},
        {"name": "loop_stoplight",
         "description": "GO/NOGO + missing for a task id.",
         "inputSchema": {"type": "object",
                         "properties": {"id": {"type": "string"}},
                         "required": ["id"]}},
        {"name": "loop_history",
         "description": "Base rates over tasks, optional like-filter.",
         "inputSchema": {"type": "object",
                         "properties": {"like": {"type": "string"}}}},
        {"name": "ham_check",
         "description": "Prohibited screen an action string. CLEAR or hits.",
         "inputSchema": {"type": "object",
                         "properties": {"action": {"type": "string"}},
                         "required": ["action"]}},
    ]


def _text(s: str) -> dict:
    return {"content": [{"type": "text", "text": s}]}


def call_tool(name: str, args: dict) -> dict:
    if name == "seed0_check":
        rep = seed0_check(args.get("path", "."))
        lines = [f"[{'PASS' if c['pass'] else 'FAIL'}] {c['check']} {c['detail']}"
                 for c in rep["checks"]]
        lines.append(f"{rep['passed']}/{rep['total']} — "
                     f"{'COMPLIANT' if rep['compliant'] else 'NOT COMPLIANT'}")
        return _text("\n".join(lines))
    if name == "loop_list":
        st = (args or {}).get("status")
        rows = [r for r in queue_load(str(Path(ROOT) / "loop" / "tasks.jsonl"))
                if not st or r.get("status") == st]
        return _text("\n".join(
            f"{r['status']:10} {r['tier']} {r['id']:14} {r['summary'][:80]}"
            for r in rows) or "(empty)")
    if name == "loop_ready":
        recs = queue_load(str(Path(ROOT) / "loop" / "tasks.jsonl"))
        by_id = {r.get("id"): r for r in recs}
        ready = [r for r in recs
                 if r.get("status") in ("JUSTIFIED", "EXECUTING")
                 and all(by_id.get(b, {}).get("status") == "DONE"
                         for b in r.get("blocked_by", []) or [])]
        return _text("\n".join(f"{r['id']:14} {r['summary'][:80]}"
                               for r in ready) or "(none ready)")
    if name == "loop_stoplight":
        rep = stoplight(args.get("id", ""),
                        str(Path(ROOT) / "loop" / "tasks.jsonl"))
        out = ["GO" if rep["go"] else "NOGO", *["  - " + m for m in rep["missing"]]]
        return _text("\n".join(out))
    if name == "loop_history":
        import io as _io
        from contextlib import redirect_stdout as _ro
        buf, like = _io.StringIO(), (args or {}).get("like", "")
        with _ro(buf):
            _loop.main(["history"] + (["--like", like] if like else []))
        return _text(buf.getvalue())
    if name == "ham_check":
        hits = check_prohibited(args.get("action", ""))
        return _text("CLEAR" if not hits else "PROHIBITED " + json.dumps(hits))
    raise ValueError(f"unknown tool: {name}")


def handle(msg: dict):
    mid, method = msg.get("id"), msg.get("method")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"protocolVersion": "2024-11-05",
                           "capabilities": {"tools": {}},
                           "serverInfo": {"name": "seed0", "version": "0.1"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"tools": _tool_defs()}}
    if method == "tools/call":
        p = msg.get("params", {}) or {}
        try:
            out = call_tool(p.get("name", ""), p.get("arguments", {}) or {})
            return {"jsonrpc": "2.0", "id": mid, "result": out}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32000, "message": str(e)[:200]}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"unknown method: {method}"}}


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            resp = handle(json.loads(line))
        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": None,
                    "error": {"code": -32700, "message": f"parse: {e}"[:120]}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
