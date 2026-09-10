#!/usr/bin/env python3
"""instrument.py — 10-key dispatch: parse a chain, run each key against
real machinery, log every press with its outcome. Stdlib only.

  python3 instrument.py press 2943 [--root .] [--session S] [--text "7=...;9=..."]

Read-only keys (2, 3) work under halt; executing keys refuse while
loop/HALT.json exists; 0 toggles the halt. Nothing here raises past
run(): a failed key is a failed outcome row, never a crash.
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chain as _chain
import press as _press
import registries as _reg

HALT = "loop/HALT.json"
GOAL = "loop/goal.json"
CORR = "loop/corrections.jsonl"
HEUR = "loop/heuristics.md"

READY_STATUS = ("JUSTIFIED", "EXECUTING")

# TELL-guard: key-shaped payloads never enter the registry from the dash.
# (Convergent with hamjob's guard; both repos stay standalone.)
import re as _re
_SECRET_RES = [
    _re.compile(r"sk-[A-Za-z0-9]{12,}"),
    _re.compile(r"ghp_[A-Za-z0-9]{36}"),
    _re.compile(r"xox[bap]-[A-Za-z0-9-]+"),
    _re.compile(r"AKIA[0-9A-Z]{16}"),
    _re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    _re.compile(r"\d{6,12}:AA[A-Za-z0-9_-]{33}"),
    _re.compile(r"cfat_[A-Za-z0-9_-]{10,}"),
    _re.compile(r"apify_api_[A-Za-z0-9]+"),
    _re.compile(r"(?i)\b(api[_-]?key|api[_-]?token|access_token|secret|mnemonic|bearer|private_key|password|key)\b\s*[:=]\s*\S{8,}"),
]


def _halted(root: str) -> bool:
    return (Path(root) / HALT).exists()


def _open_h(root: str) -> list[dict]:
    import hinbox
    try:
        return hinbox.poll(path=str(Path(root) / "loop" / "registry_h.jsonl"),
                           queue_path=str(Path(root) / "loop" / "tasks.jsonl"))
    except Exception:
        return []


def _ready(root: str) -> list[dict]:
    import loop as _loop
    try:
        recs = _loop.load(str(Path(root) / "loop" / "tasks.jsonl"))
    except Exception:
        return []
    done = {r.get("id") for r in recs if r.get("status") == "DONE"}
    return [r for r in recs
            if r.get("status") in READY_STATUS
            and all(b in done for b in (r.get("blocked_by") or []))]


def _act(key: str, arg, root: str, session: str, payloads: dict) -> dict:
    R = Path(root)
    ok, action, detail, close = True, "", {}, ""
    if key == "0":
        hp = R / HALT
        if hp.exists():
            hp.unlink()
            action, close = "resume", "resumed — halt lifted"
        else:
            hp.parent.mkdir(parents=True, exist_ok=True)
            hp.write_text(json.dumps({"ts": time.time(), "session": session}) + "\n")
            action, close = "halt", "halted — packet pending; 2,3 still work; 0 resumes"
    elif key == "2":
        a = _reg.read("a", root)
        h = _reg.read("h", root)
        m = _reg.read("m", root)
        done = [r for r in a if r.get("status") == "DONE"]
        missing = [r for r in a if r.get("status") not in ("DONE", "REJECTED")]
        schema = _reg.check_all(root)
        goal = {}
        try:
            goal = json.loads((R / GOAL).read_text())
        except Exception:
            pass
        action = "zoom"
        detail = {"done": len(done), "missing": len(missing),
                  "open_h": len([r for r in h if r.get("kind") == "request"]),
                  "m_events": len(m), "goal": goal.get("active"),
                  "halted": _halted(root)}
        close = (f"achieved {len(done)} / missing {len(missing)}; "
                 f"schema {'clean' if not schema else f'{len(schema)} errors'}")
    elif key == "3":
        heur = ""
        try:
            heur = (R / HEUR).read_text()[:800]
        except Exception:
            pass
        opens = _open_h(root)[:3]
        action = "dig"
        detail = {"heuristics": heur,
                  "blockers": [o.get("summary", "")[:100] for o in opens]}
        close = ("obvious answer: " + (detail["blockers"][0] if detail["blockers"]
                 else "no open blockers — queue is the finding"))
    elif key == "1":
        if _halted(root):
            return {"key": key, "arg": arg, "ok": False, "action": "refused",
                    "detail": {}, "close": "halted — press 0 to resume"}
        ready = _ready(root)
        action = "drain-ordered"
        detail = {"ready": [r.get("id") for r in ready]}
        close = (f"drained {len(ready)} ready ({', '.join(detail['ready'][:4])}"
                 f"{'…' if len(ready) > 4 else ''}); agent working; H surfaces on block"
                 if ready else "nothing ready — halt-legal")
    elif key in ("4", "5", "6", "7"):
        if _halted(root):
            return {"key": key, "arg": arg, "ok": False, "action": "refused",
                    "detail": {}, "close": "halted — press 0 to resume"}
        import hinbox
        opens = _open_h(root)
        hp = str(R / "loop" / "registry_h.jsonl")
        mp = str(R / "loop" / "registry_m.jsonl")
        if key == "4":
            cand = next((o for o in opens if o.get("options")), None)
            if cand is None:
                ok, action, close = False, "no-choice", "no open task with options to pick from"
            else:
                opts = cand.get("options") or []
                pick = opts[arg] if arg < len(opts) else f"option-{arg}"
                hinbox.resolve(cand["id"], "answered", note=f"picked: {pick}",
                               by="human(key4)", path=hp)
                action, detail = "pick", {"rid": cand["id"], "pick": pick}
                close = f"resolved {cand['id']} as option {arg}"
        elif key == "5":
            cand = next((o for o in opens if o.get("h_kind") == "approval"), None)
            if cand is None:
                ok, action, close = False, "nothing", "nothing to approve"
            else:
                r = hinbox.resolve(cand["id"], "approved", by="human(key5)",
                                   path=hp, mreg_path=mp)
                action, detail = "approve", {"rid": cand["id"]}
                close = f"approved {cand['id']}" + (
                    " — grant activated" if r.get("grant_id") else "")
        elif key == "6":
            if not opens:
                ok, action, close = False, "nothing", "nothing to deny"
            else:
                hinbox.resolve(opens[0]["id"], "denied", note="denied via key 6",
                               by="human(key6)", path=hp)
                action, detail = "deny", {"rid": opens[0]["id"]}
                close = f"denied {opens[0]['id']}, replanning"
        else:  # 7 TELL
            text = (payloads or {}).get("7", "")
            hit = next((rx for rx in _SECRET_RES if rx.search(text or "")), None)
            if not text:
                ok, action, close = False, "needs-text", "TELL needs text (key 7 opens capture)"
            elif hit:
                ok, action, close = False, "secret-refused", (
                    "key-shaped input refused — secrets travel server-side only")
            elif not opens:
                ok, action, close = False, "nothing", "no open task to tell"
            else:
                tgt = next((o for o in opens if o.get("h_kind") == "input"), opens[0])
                hinbox.resolve(tgt["id"], "answered", note=text[:500],
                               by="human(key7)", path=hp)
                action = "tell"
                detail = {"rid": tgt["id"], "unblocks": tgt.get("unlocks", [])}
                close = f"delivered to {tgt['id']}, unblocked {detail['unblocks']}"
    elif key == "8":
        gp = R / GOAL
        gp.parent.mkdir(parents=True, exist_ok=True)
        gp.write_text(json.dumps({"active": f"T{arg}", "ts": time.time(),
                                  "session": session}, sort_keys=True) + "\n")
        action, detail, close = "goal", {"active": f"T{arg}"}, f"goal now T{arg}, queue reordered"
    elif key == "9":
        if _halted(root):
            return {"key": key, "arg": arg, "ok": False, "action": "refused",
                    "detail": {}, "close": "halted — press 0 to resume"}
        text = (payloads or {}).get("9", "")
        cp = R / CORR
        cp.parent.mkdir(parents=True, exist_ok=True)
        cid = f"c-{int(time.time()) % 100000:05d}"
        ctx = {"open_h": [o.get("id") for o in _open_h(root)][:5],
               "ready": [r.get("id") for r in _ready(root)][:5]}
        with open(cp, "a") as f:
            f.write(json.dumps({"id": cid, "ts": time.time(), "session": session,
                                "text": text[:1000] or None, "auto_context": ctx},
                               sort_keys=True) + "\n")
        action, detail = "fix", {"cid": cid}
        close = f"correction {cid} logged, replanning"
    return {"key": key, "arg": arg, "ok": ok, "action": action,
            "detail": detail, "close": close}


def _context(root: str) -> dict:
    opens = _open_h(root)
    return {"open_h": [o.get("id") for o in opens][:8],
            "goal": None, "halted": _halted(root)}


def run(chain_str: str, session: str | None = None, root: str = ".",
        payloads: dict | None = None) -> dict:
    """Parse + dispatch a chain; log every press with its outcome."""
    t0 = time.monotonic()
    actions = _chain.parse(chain_str)
    results = []
    for a in actions:
        ctx = _context(root)
        res = _act(a["key"], a["arg"], root, session or "", payloads or {})
        _press.log(root, session, a["key"], a["arg"], chain_str, ctx,
                   {"ok": res["ok"], "action": res["action"]})
        results.append(res)
    return {"session": session, "chain": chain_str,
            "described": _chain.describe(actions),
            "results": results,
            "elapsed_s": round(time.monotonic() - t0, 3),
            "cost_usd": 0.0,
            "close": " | ".join(r["close"] for r in results)}


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] != "press":
        print(__doc__)
        return 2
    root, session, payloads = ".", None, {}
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    if "--session" in argv:
        session = argv[argv.index("--session") + 1]
    if "--text" in argv:
        for part in argv[argv.index("--text") + 1].split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                payloads[k.strip()] = v
    try:
        print(json.dumps(run(argv[1], session, root, payloads), indent=1)[:3000])
    except ValueError as e:
        print(json.dumps({"ok": False, "error": str(e)[:200]}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
