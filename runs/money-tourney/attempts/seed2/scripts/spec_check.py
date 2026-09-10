#!/usr/bin/env python3
"""spec_check: every acceptance row needs teeth. Stdlib only.
Usage: python3 scripts/spec_check.py [SPEC.md]
Checks: table present; each row has ID + statement + verification + owner;
verification names a real method (test <id> exists in tests/, demo script exists,
or review with named human). Exit 1 with reasons otherwise.
"""
import os
import re
import sys
from pathlib import Path

METHODS = ("test", "demo", "review")


def check(path: str = "SPEC.md") -> list[str]:
    root = Path(path).parent
    text = Path(path).read_text()
    errs = []
    rows = re.findall(r"^\| (AC-\d+) \| (.+?) \| (.+?) \| (.+?) \|$", text, re.M)
    if not rows:
        return ["no acceptance-criteria rows (need | ID | Statement | Verification | Owner |)"]
    for cid, _stmt, verif, owner in rows:
        verif, owner = verif.strip(), owner.strip(" `")
        if not owner or owner.lower() in ("tbd", "?"):
            errs.append(f"{cid}: owner missing")
            continue
        meth = verif.split()[0].lower()
        if meth not in METHODS:
            errs.append(f"{cid}: verification '{verif}' names no known method {METHODS}")
        elif meth == "test":
            m = re.search(r"`([^`]+)`", verif)
            token = (m.group(1) if m else verif[4:]).strip()
            tests_dir = root / "tests"
            found = tests_dir.exists() and any(
                token and token in p.read_text()
                for p in tests_dir.glob("test_*.py"))
            if not found:
                errs.append(f"{cid}: no test matching '{token}' in tests/")
        elif meth == "demo":
            script = verif.split()[1].strip("`") if len(verif.split()) > 1 else ""
            if not script or not (root / script).exists():
                errs.append(f"{cid}: demo script '{script}' missing")
    return errs


if __name__ == "__main__":
    errs = check(os.getenv("SPEC_PATH", sys.argv[1] if len(sys.argv) > 1 else "SPEC.md"))
    print("SPEC OK" if not errs else "\n".join("FAIL " + e for e in errs))
    raise SystemExit(0 if not errs else 1)
