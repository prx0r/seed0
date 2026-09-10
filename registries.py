#!/usr/bin/env python3
"""registries.py — one read API + schema gate over the three streams. Stdlib only.

Canonical paths (REGISTRIES.md SPEC v1):
  A (agent): loop/tasks.jsonl      (loop.py owns writes; removal only by proof)
  H (human): loop/registry_h.jsonl (hinbox.py owns writes; removal only by human)
  M (money): loop/registry_m.jsonl (grants.py owns writes; removal only by
             expiry/spend/revocation — file appears on first grant)

This module never writes stream files and offers no delete: append-only is
the law, corrections are new records referencing the old id. The hub reads
all three streams through here; check_all() is the schema gate.
"""
from __future__ import annotations
import json
from pathlib import Path

STREAMS = {"a": "loop/tasks.jsonl",
           "h": "loop/registry_h.jsonl",
           "m": "loop/registry_m.jsonl"}

A_STATUS = ("PROPOSED", "JUSTIFIED", "EXECUTING", "PAUSED", "REPORTED",
            "REJECTED", "DONE")
H_STATUS = ("open", "approved", "denied", "answered", "expired")
H_KINDS = ("request", "resolution", "expiry")  # envelope; approval|input|review
H_HKINDS = ("approval", "input", "review")     # lives in h_kind per hinbox.py
M_KINDS = ("proposed", "activated", "spent", "revoked")


def path(stream: str, root: str = ".") -> Path:
    if stream not in STREAMS:
        raise ValueError(f"stream must be one of {sorted(STREAMS)}")
    return Path(root) / STREAMS[stream]


def read(stream: str, root: str = ".") -> list[dict]:
    """All records in a stream. Missing file = empty stream, never an error."""
    p = path(stream, root)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def validate(stream: str, rec: dict) -> list[str]:
    """Schema errors for one record (empty = valid). Shape only, not proof."""
    errs: list[str] = []
    if not isinstance(rec, dict):
        return ["record is not an object"]
    if not rec.get("id"):
        errs.append("missing id")
    if stream == "a":
        for k in ("tier", "summary", "status"):
            if not rec.get(k):
                errs.append(f"missing {k}")
        if rec.get("status") not in A_STATUS:
            errs.append(f"bad status: {rec.get('status')!r}")
    elif stream == "h":
        if rec.get("kind") not in H_KINDS:
            errs.append(f"bad kind: {rec.get('kind')!r}")
        if rec.get("kind") == "request":
            if rec.get("h_kind") not in H_HKINDS:
                errs.append(f"bad h_kind: {rec.get('h_kind')!r}")
            if rec.get("status") not in H_STATUS:
                errs.append(f"bad status: {rec.get('status')!r}")
    elif stream == "m":
        if rec.get("kind") not in M_KINDS:
            errs.append(f"bad kind: {rec.get('kind')!r}")
        if "ts" not in rec:
            errs.append("missing ts")
    else:
        errs.append(f"unknown stream: {stream}")
    return errs


def check_all(root: str = ".") -> list[str]:
    """Schema-gate all three streams. Empty = hub may read with confidence."""
    errs: list[str] = []
    for s in STREAMS:
        try:
            recs = read(s, root)
        except Exception as e:
            errs.append(f"{s}: unreadable ({e})"[:120])
            continue
        for i, r in enumerate(recs):
            for e in validate(s, r):
                errs.append(f"{s}[{i}]: {e}")
    return errs
