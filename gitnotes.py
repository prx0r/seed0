#!/usr/bin/env python3
"""gitnotes.py — scores as git notes (GitOfThoughts pattern). Stdlib only.

Thoughts are commits; scores ride as notes; outcomes as tags. Notes travel
with explicit refspecs (verified: default clone/fetch DROPS them — see
CONTROL_PLANE). Local-first: attach + read need no network.
"""
from __future__ import annotations
import json
import subprocess


def _git(repo: str, *args: str):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=repo, timeout=30)


def attach(repo: str, rev: str, namespace: str, payload: dict) -> str:
    """Attach JSON payload as a note on rev. Returns the note blob sha."""
    r = _git(repo, "notes", f"--ref=refs/notes/{namespace}", "add", "-f",
             "-m", json.dumps(payload, sort_keys=True), rev)
    if r.returncode != 0:
        raise RuntimeError(f"notes attach failed: {r.stderr.strip()[:160]}")
    r = _git(repo, "notes", f"--ref=refs/notes/{namespace}", "list", rev)
    return r.stdout.strip().split()[0] if r.stdout.strip() else ""


def read(repo: str, rev: str, namespace: str) -> dict | None:
    """Read the note payload, or None when absent (absence is data)."""
    r = _git(repo, "notes", f"--ref=refs/notes/{namespace}", "show", rev)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def tag(repo: str, name: str, rev: str, message: str = "") -> bool:
    """Outcomes as tags (success_<id>, failed_<id>)."""
    r = _git(repo, "tag", "-a", name, rev, "-m", message or name)
    return r.returncode == 0
