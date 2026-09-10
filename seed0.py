#!/usr/bin/env python3
"""seed0 — project-standard compliance checker + scaffolder. Stdlib only.

  python3 seed0.py check ./myproject     score a project against the standard
  python3 seed0.py new NAME --idea "..." scaffold a new standard-shaped project

Exit 0 when compliant (new: always 0 on success). Human-readable report + counts.
"""
import os
import re
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = ["AGENTS.md", "README.md", ".env.example",
                  "docs/README.md", "docs/RECIPES.md", "docs/FILES.md",
                  "docs/THREADS.md"]
# NOTE: private-key pattern is concatenated so this source file does
# not literally contain the string it scans for (self-match).
SECRET_RES = [re.compile(r"sk-[A-Za-z0-9]{12,}"),
              re.compile(r"ghp_[A-Za-z0-9]{12,}"),
              re.compile(r"-----BEG" + "IN " + r".*PRIV" + "ATE KEY-----")]
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv",
             ".pytest_cache", "runtime", "var"}


def _tree(root: Path):
    return [p for p in root.rglob("*") if p.is_file()
            and not any(d in p.parts for d in SKIP_DIRS)]


def check(root: str, cwd_independent: bool = False) -> dict:
    root = Path(root)
    checks, notes = [], []

    def rec(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    missing = [f for f in REQUIRED_FILES if not (root / f).exists()]
    rec("required-files", not missing, f"missing={missing}" if missing else "all present")
    tests = [p for p in _tree(root) if p.name.startswith("test_") and p.suffix == ".py"]
    rec("tests-exist", len(tests) > 0, f"{len(tests)} test files")
    rec("env-committed", not (root / ".env").exists(),
        ".env present — never commit it" if (root / ".env").exists() else "clean")
    leaks, skipped = [], 0
    for p in _tree(root):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("tests/fixtures/"):
            skipped += 1
            continue
        if p.suffix not in {".py", ".md", ".yaml", ".yml", ".json", ".ts", ".js", ".txt", ".toml"}:
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        for rx in SECRET_RES:
            if rx.search(text):
                leaks.append(f"{p.relative_to(root)}:{rx.pattern[:18]}…")
                break
    scanned = sum(1 for _ in [p for p in _tree(root) if p.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".ts", ".js", ".txt", ".toml"}])
    detail = f"leaks={leaks}" if leaks else ("clean" if scanned else "clean (nothing scanned)")
    if skipped:
        detail += f" ({skipped} fixture files skipped as intentionally-dirty test data)"
    rec("no-committed-secrets", not leaks, detail)
    # docs index must not point at missing files
    idx = root / "docs" / "README.md"
    dead = []
    if idx.exists():
        for m in re.finditer(r"[`'\[]([\w\-./]+\.md)[`'\]]", idx.read_text()):
            rel = m.group(1).lstrip("/")  # leading / = repo-root absolute
            cands = [(root / rel).resolve(),
                     (root / "docs" / rel).resolve()]
            base = root.resolve()
            live = any(base in c.parents and c.exists() for c in cands)
            if not live and not m.group(1).startswith("http"):
                dead.append(m.group(1))
    rec("index-links-live", not dead, f"dead={dead}" if dead else "all resolve")
    if cwd_independent:
        # Run the suite from a FOREIGN cwd with absolute paths: catches tests
        # that secretly depend on the repo directory (imports, data files).
        import subprocess
        try:
            r = subprocess.run(
                [sys.executable, "-m", "pytest", "--rootdir", str(root.resolve()),
                 "-q", str(root.resolve() / "tests")],
                cwd="/tmp", capture_output=True, text=True, timeout=300)
            ok = r.returncode == 0
            tail = (r.stdout.strip().splitlines() or ["?"])[-1][:120]
        except Exception as e:
            ok, tail = False, f"harness: {e}"[:120]
        rec("suite-green-any-cwd", ok, tail)
    passed = sum(1 for c in checks if c["pass"])
    return {"project": str(root), "passed": passed, "total": len(checks),
            "compliant": passed == len(checks), "checks": checks}


def new(name: str, idea: str, dest: str = ".") -> Path:
    src = Path(__file__).resolve().parent / "templates"
    out = Path(dest) / name
    shutil.copytree(src, out)
    subs = {"{{PROJECT}}": name, "{{IDEA}}": idea or "(fill in: one paragraph)"}
    for p in out.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".txt", ""}:
            try:
                t = p.read_text()
            except Exception:
                continue
            for k, v in subs.items():
                t = t.replace(k, v)
            p.write_text(t)
    _git_init(out)
    return out


def _git_init(out: Path) -> str | None:
    """git-init on scaffold (Letta MemFS pattern): every agent start gets a
    versioned tree from byte zero. Local identity, no remotes, no network.
    Returns initial commit sha, or None if git unavailable (non-fatal)."""
    import subprocess as _sp
    try:
        _sp.run(["git", "init", "-qb", "main"], cwd=out, check=True,
                capture_output=True)
        _sp.run(["git", "config", "user.name", "seed0"], cwd=out, check=True,
                capture_output=True)
        _sp.run(["git", "config", "user.email", "seed0@local"], cwd=out,
                check=True, capture_output=True)
        _sp.run(["git", "add", "-A"], cwd=out, check=True, capture_output=True)
        _sp.run(["git", "commit", "-qm", "seed0: scaffold + frozen intent"],
                cwd=out, check=True, capture_output=True)
        r = _sp.run(["git", "rev-parse", "HEAD"], cwd=out, check=True,
                    capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return None


def main(argv):
    if len(argv) < 2 or argv[1] not in ("check", "new"):
        print(__doc__)
        return 2
    if argv[1] == "check":
        target = argv[2] if len(argv) > 2 and not argv[2].startswith("--") else "."
        rep = check(target, cwd_independent="--cwd-independent" in argv)
        for c in rep["checks"]:
            print(f"[{'PASS' if c['pass'] else 'FAIL'}] {c['check']} {c['detail']}")
        print(f"{rep['passed']}/{rep['total']} — "
              f"{'COMPLIANT' if rep['compliant'] else 'NOT COMPLIANT'}")
        return 0 if rep["compliant"] else 1
    name = argv[2] if len(argv) > 2 else None
    if not name:
        print("usage: seed0.py new NAME --idea '...'")
        return 2
    idea = ""
    if "--idea" in argv:
        idea = argv[argv.index("--idea") + 1]
    print(f"scaffolded {new(name, idea)} — now fill NORTHSTAR.users intent, then build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
