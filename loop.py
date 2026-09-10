#!/usr/bin/env python3
"""loop.py — thin driver for META_LOOP task queues. Stdlib only.

The queue is loop/tasks.jsonl (one JSON record per line, §2 schema).
This driver does bookkeeping, not thinking: add/list/status with schema
checks. The teeth: set-status DONE requires report_ref + validation_ref
(non-empty), so DONE without proof is rejected by the tool, not by discipline.

  python3 loop.py list
  python3 loop.py list --status PAUSED
  python3 loop.py show a-push
  python3 loop.py add --record '{"id":"...","tier":"A",...}'
  python3 loop.py set-status a-push EXECUTING
  python3 loop.py set a-push report_ref --value '"loop/reports/a-push.md"' 
  python3 loop.py check            # validate whole queue file
  python3 loop.py ready              # actionable now (deps satisfied)
  python3 loop.py branch a-x         # tasks/a-x branch + record
  python3 loop.py history [--like k] # base rates over tasks
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

QUEUE = "loop/tasks.jsonl"
ALOG_DIR = "loop/a-logs"
INGEST_DIR = "loop/ingests"
STATUS = {"PROPOSED", "JUSTIFIED", "EXECUTING", "PAUSED", "REPORTED",
          "REJECTED", "DONE"}
TIERS = {"A", "H", "M"}
REQ = {"id", "tier", "summary", "justification", "acceptance",
       "evidence_required", "cost_note", "status", "report_ref",
       "validation_ref"}
REQ_JUST = {"parent", "why_now", "why_tier"}


def load(path: str = QUEUE) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def problems(rec: dict, queue_path: str = QUEUE) -> list[str]:
    errs = []
    if not REQ <= set(rec):
        errs.append(f"missing keys: {sorted(REQ - set(rec))}")
    if rec.get("tier") not in TIERS:
        errs.append(f"bad tier: {rec.get('tier')}")
    if rec.get("status") not in STATUS:
        errs.append(f"bad status: {rec.get('status')}")
    j = rec.get("justification", {})
    if not isinstance(j, dict) or not REQ_JUST <= set(j):
        errs.append("justification needs parent/why_now/why_tier")
    if not rec.get("acceptance"):
        errs.append("acceptance empty (nothing would prove this done)")
    if rec.get("status") == "REPORTED":
        rr = rec.get("report_ref", "")
        base = Path(queue_path).resolve().parent
        if not rr or not (Path(rr).exists() or (base / rr).exists()
            or (base.parent / rr).exists()):
            errs.append("REPORTED requires report_ref to an existing report file")
    if rec.get("status") == "DONE" and not (
            rec.get("report_ref") and rec.get("validation_ref")):
        errs.append("DONE requires report_ref + validation_ref (no receipt, no DONE)")
    return errs


def save_all(records: list[dict], path: str = QUEUE) -> None:
    Path(path).write_text("\n".join(
        json.dumps(r, sort_keys=True) for r in records) + "\n")


MAX_REPLANS = 3


def replan(recs: list[dict], tid: str, reason: str) -> dict:
    """Send a task back for a fresh attempt. Circuit breaker: after
    MAX_REPLANS replans the task escalates to H instead of looping forever
    (XBSTACK max_replanning_count pattern). Returns outcome dict."""
    rec = next((r for r in recs if r.get("id") == tid), None)
    if rec is None:
        return {"ok": False, "error": f"unknown id: {tid}"}
    n = int(rec.get("replans", 0))
    if n >= MAX_REPLANS:
        return {"ok": False, "error":
                f"breaker tripped ({n} replans) — escalate to H with reason log",
                "escalate": True, "replan_log": rec.get("replan_log", [])}
    rec["replans"] = n + 1
    rec["replan_log"] = rec.get("replan_log", []) + [reason]
    rec["status"] = "PROPOSED"
    return {"ok": True, "replans": n + 1, "status": "PROPOSED"}


def plan_metrics(recs: list[dict], queue_path: str = QUEUE) -> dict:
    """Plan-validity metrics (XBSTACK pattern): how healthy is planning itself."""
    valid, total = 0, 0
    replanned, replan_ok = 0, 0
    covered, coverable = 0, 0
    for r in recs:
        total += 1
        if not problems(r, queue_path):
            valid += 1
        n = int(r.get("replans", 0))
        if n:
            replanned += 1
            if r.get("status") == "DONE":
                replan_ok += 1
        acc = r.get("acceptance", []) or []
        if r.get("status") == "DONE" and acc:
            coverable += 1
            cov = set()
            for e in alog_read(r.get("id", ""), queue_path):
                cov.update(e.get("covers", []))
            if all(i in cov for i in range(len(acc))):
                covered += 1
    return {"tasks": total,
            "plan_validity_rate": round(valid / total, 3) if total else None,
            "replanned": replanned,
            "replan_success_rate": round(replan_ok / replanned, 3) if replanned else None,
            "done_fully_covered": f"{covered}/{coverable}"}


def leafcheck(rec: dict) -> list[str]:
    """STEP leaf-termination rule, dumb version: every acceptance item must
    map to ≥1 evidence_required entry of an EXECUTABLE kind (command|file).
    Review/pyeval/judge opinions don't terminate leaves — primitives do."""
    errs = []
    evs = rec.get("evidence_required", []) or []
    prims = [e for e in evs if isinstance(e, dict)
             and e.get("kind") in ("command", "file")]
    if len(rec.get("acceptance", []) or []) > len(prims):
        errs.append(f"leaf not mappable: {len(rec.get('acceptance', []))} "
                    f"acceptance items but only {len(prims)} primitive evidence")
    for e in evs:
        if isinstance(e, dict) and e.get("kind") not in ("command", "file"):
            errs.append(f"non-primitive evidence kind: {e.get('kind')} "
                        f"(leaf-termination needs command|file)")
    return errs


def alog_path(tid: str, queue_path: str = QUEUE) -> Path:
    base = Path(queue_path).resolve().parent
    return base / "a-logs" / f"{tid}.jsonl"


def alog(tid: str, action: str, covers: list[int], detail: str = "",
         evidence: str = "", intent: str = "", queue_path: str = QUEUE) -> dict:
    """Append one A-log line tagging which acceptance indices it covers.
    evidence is "" or "command:<cmd>" / "file:<path>" — re-executed by
    stoplight. Lines without evidence count covers on trust (pre-rule logs)."""
    import time as _t
    p = alog_path(tid, queue_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": _t.time(), "task": tid, "action": action,
             "covers": sorted(set(int(c) for c in covers)), "detail": detail,
             "evidence": evidence, "intent": intent}
    with open(p, "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def alog_read(tid: str, queue_path: str = QUEUE) -> list[dict]:
    p = alog_path(tid, queue_path)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def check_evidence(ev: str, base: Path) -> str | None:
    """Re-execute one evidence claim. Returns None if it holds, else reason.

    Ledger invalidation (S27): `command:<cmd> || inputs:a.py,b.py` memoizes
    green results keyed by (cmd + input hashes) in loop/.memo.json — unchanged
    inputs skip re-execution. No inputs list = always re-run (no free lunch).
    """
    import hashlib as _h
    import shlex
    import subprocess as _sp
    if not ev:
        return None
    if ev.startswith("command:"):
        rest = ev[len("command:"):]
        cmd, _, inputs = rest.partition(" || inputs:")
        cmd = cmd.strip()
        memo_p = base / ".memo.json"
        try:
            memo = json.loads(memo_p.read_text())
        except Exception:
            memo = {}
        hashes: list[str] | None = None
        if inputs.strip():
            hashes = []
            for rel in inputs.split(","):
                rel = rel.strip()
                hit = next((c for c in (Path(rel), base / rel, base.parent / rel)
                            if c.is_file()), None)
                if hit is None:
                    hashes = None
                    break
                hashes.append(_h.sha256(hit.read_bytes()).hexdigest()[:12])
            if hashes is not None and memo.get(cmd + "|" + ",".join(hashes), {}).get("exit") == 0:
                return None  # inputs unchanged since green run
        try:
            r = _sp.run(shlex.split(cmd), capture_output=True, text=True,
                        timeout=120, cwd=base.parent)
        except Exception as e:
            return f"evidence command failed to run: {cmd[:80]} ({e})"[:120]
        if r.returncode != 0:
            tail = ((r.stdout + r.stderr).strip().splitlines() or ["?"])[-1][:80]
            return f"evidence command red (exit {r.returncode}): {cmd[:60]} :: {tail}"
        if hashes is not None:
            memo[cmd + "|" + ",".join(hashes)] = {"exit": 0}
            try:
                memo_p.write_text(json.dumps(memo, sort_keys=True))
            except Exception:
                pass
        return None


def stoplight(tid: str, queue_path: str = QUEUE) -> dict:
    """Match A-log to A-task: GO iff every acceptance index is covered AND
    report exists AND validation receipt set AND every evidence claim
    re-executes green. Else NOGO + missing list."""
    recs = {r.get("id"): r for r in load(queue_path)}
    if tid not in recs:
        return {"go": False, "missing": ["unknown task id"]}
    rec = recs[tid]
    covered: set[int] = set()
    base = Path(queue_path).resolve().parent
    ev_failures = []
    for n, e in enumerate(alog_read(tid, queue_path)):
        covered.update(e.get("covers", []))
        bad = check_evidence(e.get("evidence", ""), base)
        if bad:
            ev_failures.append(f"a-log line {n}: {bad}")
    missing = [f"acceptance[{i}] uncovered: {a[:60]}"
               for i, a in enumerate(rec.get("acceptance", []))
               if i not in covered]
    missing.extend(ev_failures)
    base = Path(queue_path).resolve().parent
    rr = rec.get("report_ref", "")
    if rr and not (Path(rr).exists() or (base / rr).exists()
                   or (base.parent / rr).exists()):
        missing.append("report_ref file missing")
    if not rec.get("validation_ref"):
        missing.append("validation_ref empty (no receipt)")
    return {"go": not missing, "missing": missing,
            "covered": sorted(covered),
            "acceptance": len(rec.get("acceptance", []))}


def ingest_dir(queue_path: str = QUEUE) -> Path:
    base = Path(queue_path).resolve().parent
    d = base / "ingests"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ingest_spec(name: str, text: str, queue_path: str = QUEUE) -> dict:
    """Store a raw spec blob as ingest<N>. Returns id + section headers found
    (## lines) so restatement can cite them. Idempotent on identical text."""
    import hashlib as _h
    d = ingest_dir(queue_path)
    digest = _h.sha256(text.encode()).hexdigest()[:12]
    for f in d.glob("ingest*.md"):
        if _h.sha256(f.read_bytes()).hexdigest()[:12] == digest:
            return {"id": f.stem, "duplicate_of": f.stem,
                    "lines": len(text.splitlines()),
                    "sections": [l[3:].strip() for l in text.splitlines()
                                 if l.startswith("## ")]}
    p = d / f"{name}.md"
    if p.exists():
        raise ValueError(f"ingest name taken (different text): {name}")
    p.write_text(text)
    return {"id": name, "lines": len(text.splitlines()),
            "sections": [l[3:].strip() for l in text.splitlines()
                         if l.startswith("## ")]}


def goalcheck(goal: dict, queue_path: str = QUEUE) -> list[str]:
    """Traceability: every goal acceptance item must cite ≥1 [spec:Section]
    whose header exists in the linked ingest file. Restatements that invent
    requirements fail here — mechanically, no judgment."""
    errs = []
    ing = goal.get("ingest", "")
    if not ing:
        return ["no ingest linked (goal must restate a stored spec)"]
    f = ingest_dir(queue_path) / f"{ing}.md"
    if not f.exists():
        return [f"ingest file missing: {ing}"]
    text = f.read_text()
    import re as _re
    for i, a in enumerate(goal.get("acceptance", []) or []):
        refs = _re.findall(r"\[spec:(.+?)\]", a)
        if not refs:
            errs.append(f"acceptance[{i}] cites no [spec:Section]")
            continue
        for r in refs:
            if f"## {r.strip()}" not in text:
                errs.append(f"acceptance[{i}] cites missing section: {r.strip()}")
    return errs


def render_map(recs: list[dict]) -> str:
    """Goal decomposition as a git-like tree: roots (nothing blocks them)
    first, dependents nested. Cycles marked, not followed forever."""
    by_id = {r.get("id"): r for r in recs}
    children: dict[str, list[str]] = {}
    for r in recs:
        deps = r.get("blocked_by", []) or []
        if not deps:
            children.setdefault("", []).append(r.get("id"))
        for d in deps:
            children.setdefault(d, []).append(r.get("id"))
    lines: list[str] = []
    seen: set[str] = set()

    def walk(tid: str, prefix: str, last: bool):
        r = by_id.get(tid, {})
        mark = {"DONE": "[x]", "PAUSED": "[!]"}.get(r.get("status", ""), "[ ]")
        branch = f" @{r['branch']}" if r.get("branch") else ""
        lines.append(f"{prefix}{'└─ ' if last else '├─ '}{mark} {tid}{branch}")
        if tid in seen:
            lines.append(f"{prefix}    (cycle, stop)")
            return
        seen.add(tid)
        kids = sorted(children.get(tid, []))
        for i, k in enumerate(kids):
            walk(k, prefix + ("    " if last else "│   "), i == len(kids) - 1)

    roots = sorted(children.get("", []))
    orphans = sorted(set(by_id) - set(children) - {c for ks in children.values() for c in ks})
    for i, t in enumerate(roots):
        walk(t, "", i == len(roots) - 1 and not orphans)
    for o in orphans:  # blocked_by unknown ids: visible, not lost
        r = by_id[o]
        lines.append(f"○ [?] {o} (blocked by unknown: {r.get('blocked_by')})")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("list", "show", "add", "set-status",
                                   "set", "check", "init", "log",
                                   "stoplight", "ready", "branch",
                                   "history", "replan", "metrics",
                                   "leafcheck", "promote", "ingest",
                                   "goalcheck", "map", "context", "rollback",
                                   "heuristics", "claim", "release", "recall"):
        print(__doc__)
        return 2
    cmd = argv[0]
    kw: dict[str, str] = {}
    BOOLEANS = {"--force", "--allow-dirty"}
    it = iter(argv[1:])
    for x in it:
        if x.startswith("--"):
            if x in BOOLEANS:
                kw[x] = "1"
                continue
            try:
                kw[x] = next(it)
            except StopIteration:
                print(f"flag {x} needs a value")
                return 2
        else:
            kw.setdefault("_pos", []).append(x)
    pos = kw.get("_pos", [])
    path = kw.get("--queue", QUEUE)
    if cmd == "init":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch(exist_ok=True)
        print(f"queue ready: {path}")
        return 0
    recs = load(path)
    if cmd == "list":
        st = kw.get("--status")
        for r in recs:
            if st and r.get("status") != st:
                continue
            print(f"{r['status']:10} {r['tier']} {r['id']:12} {r['summary'][:70]}")
        return 0
    if cmd == "show":
        want = pos[0] if pos else kw.get("--id", "")
        for r in recs:
            if r.get("id") == want:
                print(json.dumps(r, indent=1, sort_keys=True))
                return 0
        print(f"unknown id: {want}")
        return 1
    if cmd == "add":
        try:
            rec = json.loads(kw["--record"])
        except (KeyError, json.JSONDecodeError) as e:
            print(f"bad --record: {e}")
            return 2
        if any(r.get("id") == rec.get("id") for r in recs):
            print(f"duplicate id: {rec.get('id')}")
            return 1
        errs = problems(rec, path)
        if errs:
            print("record rejected:")
            for e in errs:
                print(f"  - {e}")
            return 1
        recs.append(rec)
        save_all(recs, path)
        print(f"added {rec['id']}")
        return 0
    if cmd == "set-status":
        want, new = (pos + ["", ""])[:2]
        if new not in STATUS:
            print(f"bad status (want one of {sorted(STATUS)})")
            return 2
        for r in recs:
            if r.get("id") == want:
                old = r["status"]
                r["status"] = new
                errs = problems(r, path)
                if errs:
                    r["status"] = old
                    print("transition rejected:")
                    for e in errs:
                        print(f"  - {e}")
                    return 1
                if new == "DONE":
                    # Receipt id must resolve to a real file, not a string
                    # that merely looks like one (caught live: transposed id
                    # passed the non-empty check and pointed at nothing).
                    rid = r.get("validation_ref", "")
                    base = Path(path).resolve().parent
                    cands = [base / "runs" / (rid.replace(":", "_") + ".json"),
                             base.parent / "runs" / (rid.replace(":", "_") + ".json")]
                    if not rid.startswith("sha256:") or not any(c.exists() for c in cands):
                        r["status"] = old
                        print(f"transition rejected: validation_ref {rid[:24]}… "
                              f"resolves to no receipt file")
                        return 1
                save_all(recs, path)
                print(f"{want}: {old} -> {new}")
                return 0
        print(f"unknown id: {want}")
        return 1
    if cmd == "set":
        want, field = (pos + ["", ""])[:2]
        if "--value" not in kw:
            print("usage: loop.py set <id> <field> --value '<json>'")
            return 2
        try:
            val = json.loads(kw["--value"])
        except json.JSONDecodeError as e:
            print(f"bad --value: {e}")
            return 2
        for r in recs:
            if r.get("id") == want:
                old_v = r.get(field, "<absent>")
                r[field] = val
                errs = problems(r, path)
                if errs:
                    r[field] = old_v
                    print("update rejected:")
                    for e in errs:
                        print(f"  - {e}")
                    return 1
                save_all(recs, path)
                print(f"{want}.{field} updated")
                return 0
        print(f"unknown id: {want}")
        return 1
    if cmd == "check":
        bad = 0
        for r in recs:
            for e in problems(r):
                print(f"{r.get('id', '?')}: {e}")
                bad += 1
        print(f"{len(recs)} records, {bad} problems")
        return 1 if bad else 0
    if cmd == "log":
        want = pos[0] if pos else ""
        try:
            covers = [int(c) for c in kw.get("--covers", "").split(",") if c.strip()]
        except ValueError:
            print("--covers must be comma-separated acceptance indices")
            return 2
        if not want or "--action" not in kw:
            print("usage: loop.py log <id> --covers 0,2 --action '...' [--detail '...'] [--evidence 'command:<cmd>'|'file:<path>']")
            return 2
        e = alog(want, kw["--action"], covers, kw.get("--detail", ""),
                 kw.get("--evidence", ""), kw.get("--intent", ""), path)
        print(json.dumps(e, sort_keys=True))
        return 0
    if cmd == "stoplight":
        want = pos[0] if pos else ""
        rep = stoplight(want, path)
        print("GO" if rep["go"] else "NOGO")
        for m in rep["missing"]:
            print(f"  - {m}")
        print(f"covered {rep.get('covered', [])} of "
              f"{rep.get('acceptance', 0)} acceptance items")
        return 0 if rep["go"] else 1
    if cmd == "ready":
        by_id = {r.get("id"): r for r in recs}
        actionable = [r for r in recs
                      if r.get("status") in ("JUSTIFIED", "EXECUTING")
                      and all(by_id.get(b, {}).get("status") == "DONE"
                              for b in r.get("blocked_by", []) or [])]
        for r in actionable:
            deps = ",".join(r.get("blocked_by", []) or []) or "-"
            print(f"{r['id']:12} deps:[{deps}] {r['summary'][:70]}")
        return 0
    if cmd == "branch":
        import subprocess as _sp
        want = pos[0] if pos else ""
        base = kw.get("--base", "main")
        repo = kw.get("--repo", ".")
        rec = next((r for r in recs if r.get("id") == want), None)
        if rec is None:
            print(f"unknown id: {want}")
            return 1
        name = f"tasks/{want}"
        ex = _sp.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                     text=True, cwd=repo)
        if ex.returncode != 0:
            print(f"not a git repo: {repo}")
            return 1
        top = ex.stdout.strip()
        dirty = _sp.run(["git", "status", "--porcelain"], capture_output=True,
                        text=True, cwd=top).stdout.strip()
        if dirty and "--allow-dirty" not in argv:
            print("workdir dirty — commit/stash first, or --allow-dirty "
                  "(split-brain refusal, not a bug)")
            return 1
        has = _sp.run(["git", "show-ref", "--verify", "--quiet",
                       f"refs/heads/{name}"], cwd=top).returncode == 0
        if has:
            _sp.run(["git", "checkout", "-q", name], cwd=top, check=True)
            print(f"resumed {name}")
        else:
            _sp.run(["git", "checkout", "-qb", name, base], cwd=top, check=True)
            print(f"branched {name} from {base}")
        rec["branch"] = name
        save_all(recs, path)
        return 0
    if cmd == "claim":
        # kanban claim flow: JUSTIFIED -> EXECUTING with owner; refuses if
        # already held (no silent takeovers).
        want = pos[0] if pos else ""
        owner = kw.get("--owner", "agent")
        rec = next((r for r in recs if r.get("id") == want), None)
        if rec is None:
            print(f"unknown id: {want}")
            return 1
        if rec.get("status") == "EXECUTING" and rec.get("owner") not in ("", owner):
            print(f"held by {rec.get('owner')} — release first")
            return 1
        if rec.get("status") not in ("PROPOSED", "JUSTIFIED", "EXECUTING"):
            print(f"cannot claim from {rec.get('status')}")
            return 1
        rec["status"], rec["owner"] = "EXECUTING", owner
        save_all(recs, path)
        print(f"{want} claimed by {owner}")
        return 0
    if cmd == "release":
        want = pos[0] if pos else ""
        rec = next((r for r in recs if r.get("id") == want), None)
        if rec is None:
            print(f"unknown id: {want}")
            return 1
        rec["status"], rec["owner"] = "JUSTIFIED", ""
        save_all(recs, path)
        print(f"{want} released to JUSTIFIED")
        return 0
    if cmd == "history":
        like = (kw.get("--like", "") or "").lower()
        sel = [r for r in recs
               if like in r.get("summary", "").lower() or like in r.get("id", "")]
        hours = []
        counts: dict[str, int] = {}
        for r in sel:
            counts[r.get("status", "?")] = counts.get(r.get("status", "?"), 0) + 1
            lines = alog_read(r.get("id", ""), path)
            if len(lines) >= 2:
                hours.append((lines[-1]["ts"] - lines[0]["ts"]) / 3600)
        hours.sort()
        med = hours[len(hours) // 2] if hours else None
        print(json.dumps({"filter": like or None, "n": len(sel),
                          "by_status": counts,
                          "median_hours": round(med, 4) if med is not None else None,
                          "base_rate_done": round(counts.get("DONE", 0) / len(sel), 3)
                          if sel else None}, indent=1, sort_keys=True))
        return 0
    if cmd == "replan":
        want = pos[0] if pos else ""
        if "--reason" not in kw:
            print("usage: loop.py replan <id> --reason '...'")
            return 2
        out = replan(recs, want, kw["--reason"])
        if out.get("ok"):
            save_all(recs, path)
            print(f"{want}: sent back (attempt {out['replans']}/{MAX_REPLANS})")
            return 0
        print(out.get("error"))
        return 1
    if cmd == "metrics":
        print(json.dumps(plan_metrics(recs, path), indent=1, sort_keys=True))
        return 0
    if cmd == "leafcheck":
        bad = 0
        for r in recs:
            for e in leafcheck(r):
                print(f"{r.get('id', '?')}: {e}")
                bad += 1
        print(f"{len(recs)} records, {bad} leaf violations")
        return 1 if bad else 0
    if cmd == "ingest":
        src = kw.get("--file", "")
        if src:
            text = Path(src).read_text()
            name = kw.get("--as") or Path(src).stem
        else:
            text = sys.stdin.read()
            name = kw.get("--as", "ingest1")
        try:
            rec = ingest_spec(name, text, path)
        except ValueError as e:
            print(e)
            return 1
        print(json.dumps(rec, indent=1, sort_keys=True))
        return 0
    if cmd == "goalcheck":
        want = pos[0] if pos else ""
        rec = next((r for r in recs if r.get("id") == want), None)
        if rec is None:
            print(f"unknown id: {want}")
            return 1
        errs = goalcheck(rec, path)
        if errs:
            print("GOALCHECK FAIL:")
            for e in errs:
                print(f"  - {e}")
            return 1
        print(f"GOALCHECK PASS: {want} traces to {rec.get('ingest')}")
        return 0
    if cmd == "map":
        print(render_map(recs))
        return 0
    if cmd == "recall":
        # Scoped recall: grep DONE reports + decision log for an area keyword.
        # BOOT reads everything; recall reads one thing. Case-insensitive.
        import re as _re
        area = (pos[0] if pos else "").lower()
        if not area:
            print("usage: loop.py recall <area-keyword>")
            return 2
        base = Path(path).resolve().parent
        hits = []
        for r in recs:
            rr = r.get("report_ref", "")
            cands = [Path(rr), base / rr, base.parent / rr] if rr else []
            f = next((c for c in cands if c.is_file()), None)
            if f and area in f.read_text(errors="ignore").lower():
                hits.append(f"{r['id']} [report]")
        try:
            dlog = base.parent / "decisions.jsonl"
            if not dlog.exists():
                dlog = base / "decisions.jsonl"
            for line in dlog.read_text(errors="ignore").splitlines():
                if area in line.lower():
                    hits.append("decisions: " + line[:100])
        except Exception:
            pass
        print("\n".join(hits) if hits else f"(nothing on {area})")
        return 0
    if cmd == "heuristics":
        import re as _re
        base = Path(path).resolve().parent
        rules: dict[str, str] = {}
        rx = _re.compile(r"\b(never|always|must|must not|avoid|only)\b[^.]{0,140}", _re.I)
        for r in recs:
            if r.get("status") != "DONE":
                continue
            rr = r.get("report_ref", "")
            cands = [Path(rr), base / rr, base.parent / rr] if rr else []
            f = next((c for c in cands if c.is_file()), None)
            if not f:
                continue
            in_sr = False
            for line in f.read_text(errors="ignore").splitlines():
                if line.startswith("## 3"):
                    in_sr = True
                    continue
                if line.startswith("## ") and in_sr:
                    break
                if in_sr:
                    for m in rx.finditer(line):
                        rule = m.group(0).strip()
                        if " " in rule:  # whole phrases only, not lone keywords
                            rules.setdefault(rule, r.get("id", "?"))
        out = base / "heuristics.md"
        body = ["# HEURISTICS — distilled from DONE self-reviews (ERL-lite)",
                "", "> Regenerate with `loop.py heuristics`. Rules, not vibes; "
                "each cites its source task."]
        for rule, tid in sorted(rules.items()):
            body.append(f"- {rule} (from {tid})")
        out.write_text("\n".join(body) + "\n")
        print(f"{len(rules)} heuristics -> {out}")
        return 0
    if cmd == "rollback":
        # ChronoMem pattern: restore queue + registries to a git ref.
        # Refuses on dirty workdir unless --force (never silently clobber).
        import subprocess as _sp
        ref = kw.get("--ref", "")
        force = "--force" in argv
        if not ref:
            print("usage: loop.py rollback --ref <sha> [--force]")
            return 2
        base = Path(path).resolve().parent
        top = _sp.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, cwd=base)
        if top.returncode != 0:
            print("rollback needs a git repo above the queue")
            return 1
        root = top.stdout.strip()
        dirty = _sp.run(["git", "status", "--porcelain"], capture_output=True,
                        text=True, cwd=root).stdout.strip()
        if dirty and not force:
            print("workdir dirty — commit/stash first, or --force")
            return 1
        targets = ["loop/tasks.jsonl", "loop/registry_h.jsonl",
                   "loop/registry_m.jsonl"]
        have = [t for t in targets if _sp.run(
            ["git", "cat-file", "-e", f"{ref}:{t}"], cwd=root,
            capture_output=True).returncode == 0]
        if not have:
            print(f"ref {ref} holds none of {targets}")
            return 1
        _sp.run(["git", "checkout", ref, "--", *have], cwd=root, check=True,
                capture_output=True)
        print(f"rolled back {len(have)} files to {ref[:12]}: {', '.join(have)}")
        return 0
    if cmd == "context":
        # GCC CONTEXT pattern: hierarchical retrieval at caller-chosen depth.
        # L0 packet (where it stopped) -> L1 ready/paused -> L2 reports ->
        # L3 full records + logs. Default L1: orient without flooding.
        level = kw.get("--level", "L1")
        base = Path(path).resolve().parent
        out = []
        if level in ("L0", "L1", "L2", "L3"):
            try:
                p = json.loads((base.parent / "loop" / "packet.json").read_text())
            except Exception:
                p = json.loads((base / "packet.json").read_text())
            out.append(f"done={len(p.get('done', []))} "
                       f"blocked={[b.get('queue') for b in p.get('blocked_on', [])]}")
        if level in ("L1", "L2", "L3"):
            by_id = {r.get("id"): r for r in recs}
            ready = [r["id"] for r in recs
                     if r.get("status") in ("JUSTIFIED", "EXECUTING")
                     and all(by_id.get(b, {}).get("status") == "DONE"
                             for b in r.get("blocked_by", []) or [])]
            paused = [r["id"] for r in recs if r.get("status") == "PAUSED"]
            out.append(f"ready={ready} paused={paused}")
        if level in ("L2", "L3"):
            for r in recs:
                if r.get("status") in ("JUSTIFIED", "EXECUTING", "PAUSED", "REPORTED"):
                    out.append(f"- {r['id']}: {r.get('summary', '')[:80]}")
        if level == "L3":
            for r in recs:
                out.append(json.dumps(r, sort_keys=True))
        print("\n".join(out) if out else "(empty)")
        return 0
    if cmd == "promote":        # A-task -> H-task promotion. H-tasks don't spawn: they promote from
        # a blocked A-task, pre-digested to lowest-barrier form (exact steps
        # + what to send back). Refused without both — the teeth.
        want = pos[0] if pos else ""
        rec = next((r for r in recs if r.get("id") == want), None)
        if rec is None:
            print(f"unknown id: {want}")
            return 1
        try:
            steps = json.loads(kw.get("--steps-json", "[]"))
        except json.JSONDecodeError as e:
            print(f"bad --steps-json: {e}")
            return 2
        send_back = kw.get("--send-back", "")
        if not steps or not send_back:
            print("promotion refused: lowest-barrier form needs "
                  "--steps-json '[\"exact step 1\", ...]' AND --send-back "
                  "'what the human returns'")
            return 1
        import hinbox as _hb
        unlocks = [u.strip() for u in kw.get("--unlocks", "").split(",") if u.strip()]
        h = _hb.new_request(
            kw.get("--summary", f"H: {rec.get('summary', want)}"),
            context=f"Barrier on {want}: {kw.get('--barrier', '')}",
            h_kind=kw.get("--kind", "approval"),
            options=["done", "declined"], unlocks=unlocks or [want],
            urgency=int(kw.get("--urgency", "2")),
            from_task=want, exact_steps=steps, send_back=send_back)
        rec["status"] = "PAUSED"
        rec["need"] = h["id"]
        save_all(recs, path)
        print(f"promoted {want} -> {h['id']} (task PAUSED)")
        print(f"HUMAN: {h['summary']}")
        for i, s in enumerate(steps, 1):
            print(f"  {i}. {s}")
        print(f"SEND BACK: {send_back}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
