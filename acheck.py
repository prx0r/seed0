#!/usr/bin/env python3
"""acheck.py — self-audit for A-task nativeness. Stdlib only.

  python3 acheck.py --queue loop/tasks.jsonl --alogs loop/a-logs \
      --reports loop/reports [--stale-hours 24]

Exit 0 = native. Exit 1 = findings listed (one per line, machine-readable).
Checks: schema keys, lifecycle values, DONE→receipt+report resolve,
REPORTED→report exists, EXECUTING→fresh a-log (else STALE), blocked_by
refs resolve. Read-only: never writes, never deletes.
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

STATUS = ("PROPOSED", "JUSTIFIED", "EXECUTING", "PAUSED", "REPORTED",
          "REJECTED", "DONE")
REQUIRED = ("id", "tier", "summary", "status")
# META_LOOP §5: required report sections (numbered or bare headers).
REPORT_SECTIONS = ("claim", "evidence", "self-review", "needs", "cost")


def _resolve(vr: str, base: Path) -> bool:
    """Mirror loop.py set-status DONE resolution: sha256: URIs map to
    runs/sha256_<hash>.json beside the repo; plain paths resolve directly."""
    if vr.startswith("sha256:"):
        name = vr.replace(":", "_") + ".json"
        return ((base / "runs" / name).exists()
                or (base.parent / "runs" / name).exists())
    return (base / vr).exists() or Path(vr).exists()


def _report_path(rr: str, base: Path) -> Path | None:
    for c in (base / rr, Path(rr)):
        if c.exists() and c.is_file():
            return c
    return None


def _report_sections(p: Path) -> list[str]:
    """Missing META_LOOP §5 sections (empty = compliant). .md only."""
    import re as _re
    if p.suffix != ".md":
        return []
    try:
        heads = set(m.group(1).lower() for m in
                    _re.finditer(r"^#+\s*(?:\d+\.\s*)?([\w-]+)",
                                 p.read_text(), _re.M))
    except Exception:
        return [f"unreadable report: {p.name}"]
    return [f"report missing section: {s}" for s in REPORT_SECTIONS
            if s not in heads]


def _load_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    out = []
    for l in p.read_text().splitlines():
        if l.strip():
            out.append(json.loads(l))
    return out


def check(queue: Path, alogs: Path, reports: Path,
          stale_hours: float = 24) -> list[str]:
    findings: list[str] = []
    if not queue.exists():
        return [f"queue missing: {queue}"]
    recs = _load_jsonl(queue)
    by_id = {r.get("id"): r for r in recs if isinstance(r, dict)}
    now = time.time()
    for i, r in enumerate(recs):
        tag = r.get("id", f"line{i}") if isinstance(r, dict) else f"line{i}"
        if not isinstance(r, dict):
            findings.append(f"{tag}: record is not an object")
            continue
        for k in REQUIRED:
            if not r.get(k):
                findings.append(f"{tag}: missing {k}")
        if r.get("status") not in STATUS:
            findings.append(f"{tag}: bad status {r.get('status')!r}")
        for b in (r.get("blocked_by") or []):
            if b not in by_id:
                findings.append(f"{tag}: dangling blocked_by {b!r}")
        st = r.get("status")
        if st == "DONE":
            vr = r.get("validation_ref", "")
            if not vr:
                findings.append(f"{tag}: DONE without validation_ref")
            elif not _resolve(vr, queue.parent):
                findings.append(f"{tag}: validation_ref unresolvable: {vr}"[:160])
            rr = r.get("report_ref", "")
            if rr:
                rp = _report_path(rr, queue.parent)
                if rp is None:
                    findings.append(f"{tag}: report_ref unresolvable: {rr}"[:160])
                else:
                    findings += [f"{tag}: {e}" for e in _report_sections(rp)]
        if st == "REPORTED":
            rr = r.get("report_ref", "")
            if not rr:
                findings.append(f"{tag}: REPORTED without report_ref")
            else:
                rp = _report_path(rr, queue.parent)
                if rp is None:
                    findings.append(f"{tag}: report missing: {rr}"[:160])
                else:
                    findings += [f"{tag}: {e}" for e in _report_sections(rp)]
        if st == "EXECUTING":
            lp = alogs / f"{r.get('id')}.jsonl"
            if not lp.exists() or not _load_jsonl(lp):
                findings.append(f"{tag}: EXECUTING with no a-log")
            elif now - lp.stat().st_mtime > stale_hours * 3600:
                findings.append(f"{tag}: STALE (no a-log in {stale_hours}h)")
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default="loop/tasks.jsonl")
    ap.add_argument("--alogs", default="loop/a-logs")
    ap.add_argument("--reports", default="loop/reports")
    ap.add_argument("--stale-hours", type=float, default=24)
    a = ap.parse_args(argv)
    findings = check(Path(a.queue), Path(a.alogs), Path(a.reports),
                     a.stale_hours)
    for f in findings:
        print(f)
    print(f"acheck: {len(findings)} findings over {a.queue}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
