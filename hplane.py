#!/usr/bin/env python3
"""hplane.py — control plane funnel: one ranked H-queue across repos. Stdlib.

Reads every repo's loop/registry_h.jsonl (hinbox format). Ranks by T0 rule:
(value_usd or 0, priority_score) desc — revenue first, unlocks break ties.
Dark repos (no registry) are reported, not skipped: adoption bootstraps itself.
Resolution stays per-repo (hserver); the plane writes only review receipts.

  python3 hplane.py funnel [--repos plane/repos.txt]
  python3 hplane.py review [--repos plane/repos.txt]   # + STALE + receipt
  python3 hplane.py sync [--remotes plane/remotes.txt] [--mirrors plane/mirrors]
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinbox

REPOS = "plane/repos.txt"
REMOTES = "plane/remotes.txt"
MIRRORS = "plane/mirrors"


def parse_entry(line: str) -> dict:
    """`label|source[|box]` or bare path (label = basename, box = '')."""
    parts = [p.strip() for p in line.split("|")]
    if len(parts) == 1:
        return {"label": Path(parts[0]).name, "source": parts[0], "box": ""}
    return {"label": parts[0] or Path(parts[1]).name, "source": parts[1],
            "box": parts[2] if len(parts) > 2 else ""}


def repo_list(path: str = REPOS) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def sync(remotes_file: str = REMOTES, mirrors_dir: str = MIRRORS,
         timeout: int = 120) -> list[dict]:
    """Multi-box transport (git as bus): mirror every listed repo locally.
    Clone once (`--depth 1`), then fetch + hard-reset (mirrors are caches,
    never edited). Failures recorded per mirror, never raised — one dead
    box must not blind the whole funnel."""
    import subprocess as _sp
    out = []
    Path(mirrors_dir).mkdir(parents=True, exist_ok=True)
    for line in repo_list(remotes_file):
        e = parse_entry(line)
        dest = str(Path(mirrors_dir) / e["label"])
        try:
            if Path(dest, ".git").exists():
                _sp.run(["git", "fetch", "-q", "origin"], cwd=dest, check=True,
                        capture_output=True, timeout=timeout)
                _sp.run(["git", "reset", "-q", "--hard", "origin/HEAD"],
                        cwd=dest, capture_output=True, timeout=timeout)
                op = "fetched"
            else:
                _sp.run(["git", "clone", "-q", "--depth", "1", e["source"], dest],
                        check=True, capture_output=True, timeout=timeout)
                op = "cloned"
            out.append({"label": e["label"], "ok": True, "op": op,
                        "fetched_at": time.time()})
        except Exception as ex:
            out.append({"label": e["label"], "ok": False,
                        "error": str(ex)[:160]})
    return out


def collect(repos: list[str]) -> list[dict]:
    """Gather open H-records from every repo + darkness reports.

    Entries are `label|path` (local) or plain paths; labels travel as the
    repo field so 6 agents × 3 boxes stay distinguishable in one funnel."""
    out = []
    for line in repos:
        e = parse_entry(line) if "|" in line else {
            "label": Path(line).name, "source": line, "box": ""}
        repo = e["source"]
        tag = e["label"]
        reg = str(Path(repo) / "loop" / "registry_h.jsonl")
        queue = str(Path(repo) / "loop" / "tasks.jsonl")
        if not Path(reg).exists():
            out.append({"repo": tag, "box": e["box"], "status": "dark"})
            continue
        try:
            items = hinbox.poll(reg, queue_path=queue)
        except Exception as ex:
            out.append({"repo": tag, "box": e["box"],
                        "status": f"unreadable: {ex}"[:80]})
            continue
        for it in items:
            age = time.time() - it.get("ts", time.time())
            row = {"repo": tag, "box": e["box"], "status": "open",
                   "stale": age > it.get("timeout_s", 86400) / 2}
            row.update(it)
            row["repo"], row["box"] = tag, e["box"]  # labels win over payload
            out.append(row)
    return out


def rank(items: list[dict]) -> list[dict]:
    """T0 order: revenue first, unlock priority breaks ties, dark repos top."""
    def key(r):
        if r.get("status") == "dark":
            return (2, 0.0, 0.0)
        if r.get("status") != "open":
            return (-1, 0.0, 0.0)
        stale_boost = 1 if r.get("stale") else 0
        return (stale_boost, float(r.get("value_usd") or 0),
                float(r.get("priority_score") or 0))
    return sorted(items, key=key, reverse=True)


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("funnel", "review", "sync"):
        print(__doc__)
        return 2
    if argv[0] == "sync":
        kw = {}
        it = iter(argv[1:])
        for x in it:
            if x.startswith("--"):
                try:
                    kw[x] = next(it)
                except StopIteration:
                    print(f"flag {x} needs a value")
                    return 2
        results = sync(kw.get("--remotes", REMOTES),
                       kw.get("--mirrors", MIRRORS))
        print(json.dumps(results, indent=1, sort_keys=True, default=str))
        return 0 if all(r.get("ok") for r in results) else 1
    repos = repo_list(argv[argv.index("--repos") + 1] if "--repos" in argv else REPOS)
    if not repos:
        print(f"no repos (missing {REPOS}?)")
        return 2
    rows = rank(collect(repos))
    print(json.dumps(rows, indent=1, sort_keys=True, default=str))
    if argv[0] == "review":
        from runs import new_receipt, save, verify
        opens = [r for r in rows if r.get("status") == "open"]
        rec = new_receipt("plane-review", {
            "repos": repos,
            "open": len(opens),
            "stale": sum(1 for r in opens if r.get("stale")),
            "dark": sum(1 for r in rows if r.get("status") == "dark"),
            "top": [{"repo": r.get("repo"), "id": r.get("id"),
                     "value_usd": r.get("value_usd", 0),
                     "priority_score": r.get("priority_score", 0)}
                    for r in rows[:5]]})
        save(rec)
        assert verify(rec)
        print(f"receipt: {rec['run_id']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
