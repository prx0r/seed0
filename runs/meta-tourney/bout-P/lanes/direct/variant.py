"""direct-count rival: rank by len(unlocks) desc, ties keep filing order."""
from __future__ import annotations


def order(requests: list[dict]) -> list[str]:
    ids = [r["id"] for r in requests]
    by_id = {r["id"]: r for r in requests}
    return sorted(ids, key=lambda i: (-len(by_id[i].get("unlocks", [])), ids.index(i)))
