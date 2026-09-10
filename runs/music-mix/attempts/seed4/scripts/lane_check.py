#!/usr/bin/env python3
"""lane_check: lanes own their paths. Stdlib only.
Usage: python3 scripts/lane_check.py [LANES.md] [CHANGED ...]
With no CHANGED args: validates the table (unique lanes, non-empty owners/paths).
With CHANGED paths: reports which lane owns each; unknown paths fail (claim it first).
Exit 1 on any violation.
"""
import fnmatch
import os
import re
import sys
from pathlib import Path


def load(path: str = "LANES.md") -> list[dict]:
    rows = re.findall(r"^\| ([\w-]+) \| (.+?) \| (.+?) \|$", Path(path).read_text(), re.M)
    return [{"lane": l, "owner": o.strip(), "paths": [p.strip() for p in ps.split(",")]}
            for l, o, ps in rows if l.lower() != "lane"]


def check_table(lanes: list[dict]) -> list[str]:
    errs = []
    seen = set()
    for l in lanes:
        if l["lane"] in seen:
            errs.append(f"duplicate lane {l['lane']}")
        seen.add(l["lane"])
        if not l["owner"] or l["owner"].lower() in ("tbd", "?"):
            errs.append(f"{l['lane']}: owner missing")
        if not l["paths"]:
            errs.append(f"{l['lane']}: no paths")
    # overlapping claims between lanes
    for i, a in enumerate(lanes):
        for b in lanes[i + 1:]:
            if set(a["paths"]) & set(b["paths"]):
                errs.append(f"overlap: {a['lane']} x {b['lane']}")
    return errs


def owner_of(lanes: list[dict], path: str) -> str | None:
    for l in lanes:
        if any(fnmatch.fnmatch(path, p) for p in l["paths"]):
            return l["lane"]
    return None


if __name__ == "__main__":
    args = sys.argv[1:]
    lanes_path = os.getenv("LANES_PATH", "LANES.md")
    if args and args[0] == "--lanes":
        lanes_path = args[1]
        args = args[2:]
    lanes = load(lanes_path)
    errs = check_table(lanes)
    for changed in args:
        lane = owner_of(lanes, changed)
        if lane:
            print(f"{changed} -> {lane}")
        else:
            errs.append(f"{changed}: unclaimed path")
    print("LANES OK" if not errs else "\n".join("FAIL " + e for e in errs))
    raise SystemExit(0 if not errs else 1)
