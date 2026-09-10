#!/usr/bin/env python3
"""Bout-I validator: 5x retry storm vs naive and keyed lanes.
Preregistered: naive_count == 5 and keyed_count == 1. Exit 0 = H2 holds."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lanes" / "naive"))
from variant import NaiveInbox
del sys.modules["variant"]
sys.path.pop(0)
sys.path.insert(0, str(Path(__file__).resolve().parent / "lanes" / "keyed"))
from variant import file_storm


def main() -> int:
    box = NaiveInbox()
    for _ in range(5):
        box.file("approve push?", key="k1")
    naive_n = len(box.records)
    with tempfile.TemporaryDirectory() as tmp:
        recs = file_storm(str(Path(tmp) / "h.jsonl"), "approve push?", "k1", 5)
        keyed_n = len({r["id"] for r in recs})
        lines = len(Path(tmp, "h.jsonl").read_text().splitlines())
    ok = naive_n == 5 and keyed_n == 1 and lines == 1
    print(json.dumps({"naive_count": naive_n, "keyed_unique": keyed_n,
                      "keyed_lines": lines, "pass": ok}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
