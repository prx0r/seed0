#!/usr/bin/env python3
"""learn: shared failures -> criteria1.1 proposals + criteria0 global lessons.
Stdlib only. Mechanical, honest: clusters identical normalized failure
signatures across seeds (threshold --min-seeds, default 2) and DRAFTS proposals.
Nothing is auto-applied — a human promotes proposals into criteria files.

  python3 learn.py runs/idea1 [--min-seeds 2] [--out learnings/]

Reads runs/<idea>/scores.jsonl + review_r*.json. Prints clusters + proposals,
writes proposals.json. Convergence story: repeated shared failures become
criteria1.1 rows; repeated row-classes become criteria0 validator rules; over
rounds the schema converges and only novel failures remain.
"""
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path


def normalize_sig(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"[a-f0-9]{6,}", "#", t)  # hashes, ids, hex
    t = re.sub(r"\d+(\.\d+)+", "#.#", t)  # versions, timings-ish numbers
    t = re.sub(r"\s+", " ", t).strip()
    return t[:220]


def collect(run_dir: str) -> list[dict]:
    run = Path(run_dir)
    fails = []
    scores = run / "scores.jsonl"
    if scores.exists():
        for line in scores.read_text().splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("binary_pass") is False:
                sigs = []
                for cid, ok in (r.get("rubric") or {}).items():
                    if not ok:
                        sigs.append(f"rubric:{cid}")
                if r.get("suite_green") is False:
                    sigs.append(f"suite:{normalize_sig(r.get('suite_detail', ''))}")
                if not r.get("compliant", True):
                    sigs.append(f"compliance:{r.get('compliance', '?')}")
                if r.get("agent_ok") is False:
                    sigs.append("agent:failed")
                for s in sigs or ["binary_fail:unspecified"]:
                    fails.append({"seed": r.get("seed", "?"), "sig": s,
                                  "round": run.name})
    for rp in sorted(run.glob("review_r*.json")):
        try:
            doc = json.loads(rp.read_text())
        except Exception:
            continue
        for s in doc.get("seeds", []):
            if (s.get("verdict") or "").lower() in ("drop", "augment") \
                    and s.get("hypothesis"):
                fails.append({"seed": s.get("seed", "?"),
                              "sig": "review:" + normalize_sig(s["hypothesis"]),
                              "round": run.name})
    return fails


LESSON_RULES = [
    (re.compile(r"^rubric:"), "criteria1.1 row",
     "Shared rubric failure — add a criteria1.1 row pinning the capability with a seeded test."),
    (re.compile(r"^suite:"), "criteria0 rule",
     "Shared suite failure — propose a criteria0 validator rule (e.g. gate the environment/tool named in the output)."),
    (re.compile(r"^compliance:"), "criteria0 rule",
     "Shared compliance failure — propose a seed0 checker rule for the missing artifact class."),
    (re.compile(r"^agent:"), "funnel rule",
     "Shared agent failure — tighten agent-cmd contract (timeout, workdir, output schema)."),
    (re.compile(r"^review:"), "human note",
     "Reviewer-flagged pattern — read the hypothesis, decide manually."),
]


def propose(fails: list[dict], min_seeds: int = 2) -> dict:
    by_sig = defaultdict(list)
    for f in fails:
        by_sig[f["sig"]].append(f["seed"])
    proposals, lessons = [], []
    for i, (sig, seeds) in enumerate(sorted(by_sig.items()), 1):
        uniq = sorted(set(seeds))
        if len(uniq) < min_seeds:
            continue
        kind, guidance = "human note", "Shared failure — decide manually."
        for rx, k, g in LESSON_RULES:
            if rx.search(sig):
                kind, guidance = k, g
                break
        proposals.append({"id": f"CR-1.1-{i}", "signature": sig,
                          "seeds": uniq, "rounds": sorted({f['round'] for f in fails
                                                           if f["sig"] == sig}),
                          "proposal": kind, "guidance": guidance,
                          "status": "proposed"})
        if kind in ("criteria0 rule", "funnel rule"):
            lessons.append({"from": sig, "seeds": uniq,
                            "lesson": guidance, "status": "proposed"})
    return {"generated_at": time.time(), "min_seeds": min_seeds,
            "clusters": len(by_sig), "proposals": proposals,
            "global_lessons": lessons}


def main(argv) -> int:
    run_dir = argv[0] if argv else "."
    min_seeds = 2
    out = None
    if "--min-seeds" in argv:
        min_seeds = int(argv[argv.index("--min-seeds") + 1])
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    fails = collect(run_dir)
    rep = propose(fails, min_seeds)
    print(f"{len(fails)} failure events, {rep['clusters']} signatures, "
          f"{len(rep['proposals'])} proposals, {len(rep['global_lessons'])} lessons")
    for p in rep["proposals"]:
        print(f"  [{p['proposal']}] {p['id']} seeds={','.join(p['seeds'])} :: {p['signature'][:100]}")
    if out:
        Path(out).mkdir(parents=True, exist_ok=True)
        (Path(out) / "proposals.json").write_text(json.dumps(rep, indent=1))
        print(f"wrote {out}/proposals.json")
    if "--keyed" in argv:
        # S26 keyed layout: one file per failure signature so concurrent
        # amend attempts merge-conflict on disagreement instead of silently
        # coexisting (GitOfThoughts contradiction-surfacing rule).
        import hashlib as _h
        kd = Path(argv[argv.index("--keyed") + 1])
        kd.mkdir(parents=True, exist_ok=True)
        index = {}
        for p in rep["proposals"] + rep["global_lessons"]:
            sig = p.get("signature", p.get("from", "?"))
            fid = _h.sha256(sig.encode()).hexdigest()[:12]
            (kd / f"{fid}.json").write_text(json.dumps(p, indent=1, sort_keys=True))
            index[fid] = sig[:100]
        (kd / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True))
        print(f"wrote {len(index)} keyed proposals to {kd}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
