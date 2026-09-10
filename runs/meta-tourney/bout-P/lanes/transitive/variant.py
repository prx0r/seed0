"""transitive-BFS rival: rank by unlock-chain value desc, ties keep filing order."""
from __future__ import annotations


def score(h: dict, tasks: list[dict]) -> float:
    by_id = {t["id"]: t for t in tasks}
    dep: dict[str, list[str]] = {}
    for t in tasks:
        for b in t.get("blocked_by", []) or []:
            dep.setdefault(b, []).append(t["id"])
    seen, front, total = set(), list(h.get("unlocks", []) or []), 0
    while front:
        cur = front.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for d in dep.get(cur, []):
            t = by_id.get(d, {})
            if t and t.get("status") != "DONE" and d not in seen:
                total += 1 + len(t.get("acceptance", []) or [])
                front.append(d)
    direct = sum(1 for u in (h.get("unlocks", []) or [])
                 if by_id.get(u, {}).get("status", "OPEN") != "DONE")
    return total + direct


def order(requests: list[dict], tasks: list[dict]) -> list[str]:
    ids = [r["id"] for r in requests]
    by_id = {r["id"]: r for r in requests}
    return sorted(ids, key=lambda i: (-score(by_id[i], tasks), ids.index(i)))
