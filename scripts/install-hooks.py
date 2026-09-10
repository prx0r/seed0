#!/usr/bin/env python3
"""Install seed0 pre-commit hooks (S23). Stdlib only.

Installs .git/hooks/pre-commit running the fast gates (seed0 check, no
foreign-CWD run). Reversible: delete .git/hooks/pre-commit. Never touches
global git config (Letta redaction discipline).
Usage: python3 scripts/install-hooks.py [--uninstall]
"""
from __future__ import annotations
import os
import stat
import subprocess
import sys
from pathlib import Path

HOOK = """#!/bin/sh
# seed0 pre-commit: fast gates only (foreign-CWD suite stays in CI).
python3 seed0.py check . || exit 1
python3 loop.py check || exit 1
"""
PUSH_HOOK = """#!/bin/sh
# seed0 pre-push: same fast gates before anything leaves the box.
python3 seed0.py check . || exit 1
"""


def repo_root() -> Path | None:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 else None


def main(argv: list[str]) -> int:
    root = repo_root()
    if root is None:
        print("install-hooks: not in a git repo")
        return 1
    hook = root / ".git" / "hooks" / "pre-commit"
    if "--uninstall" in argv:
        if hook.exists() and "seed0 pre-commit" in hook.read_text():
            hook.unlink()
            print("uninstalled")
        else:
            print("no seed0 hook present")
        return 0
    if hook.exists():
        print(f"hook exists, refusing to overwrite: {hook}")
        return 1
    hook.write_text(HOOK)
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"installed {hook}")
    if "--with-push" in argv:
        ph = root / ".git" / "hooks" / "pre-push"
        if ph.exists():
            print(f"pre-push exists, leaving it: {ph}")
        else:
            ph.write_text(PUSH_HOOK)
            ph.chmod(ph.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"installed {ph}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
