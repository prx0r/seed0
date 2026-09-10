#!/usr/bin/env python3
"""hplane.py — control plane funnel: one ranked H-queue across repos. Stdlib.

Reads every repo's loop/registry_h.jsonl (hinbox format). Ranks by T0 rule:
(value_usd or 0, priority_score) desc — revenue first, unlocks break ties.
Dark repos (no registry) are reported, not skipped: adoption bootstraps itself.
Resolution stays per-repo (hserver); the plane writes only review receipts.

  python3 hplane.py funnel [--repos plane/repos.txt]
  python3 hplane.py review [--repos plane/repos.txt]   # + STALE + receipt
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinbox

REPOS = "plane/repos.txt"


def repo_list(path: str = REPOS) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def collect(repos: list[str]) -> list[dict]:
    """Gather open H-records from every repo + darkness reports."""
    out = []
    for repo in repos:
        reg = str(Path(repo) / "loop" / "registry_h.jsonl")
        queue = str(Path(repo) / "loop" / "tasks.jsonl")
        if not Path(reg).exists():
            out.append({"repo": repo, "status": "dark"})
            continue
        try:
            items = hinbox.poll(reg, queue_path=queue)
        except Exception as e:
            out.append({"repo": repo, "status": f"unreadable: {e}"[:80]})
            continue
        for it in items:
            age = time.time() - it.get("ts", time.time())
            out.append({"repo": repo, "status": "open",
                        "stale": age > it.get("timeout_s", 86400) / 2, **it})
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
    if not argv or argv[0] not in ("funnel", "review"):
        print(__doc__)
        return 2
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
