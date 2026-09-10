"""Tournament scorer: one idea, N seeds, honest leaderboard. Stdlib only.

Each seed = a directory built by an agent from the same idea (+ its run log).
Scoring is mechanical, no judges:
  compliance  — seed0.py check (layout, tests exist, no secrets, live index)
  tests_green — its own suite passes (subprocess pytest, timeout-guarded)
  evidence    — run/scenario logs present (proof it actually ran, not claimed)
Ranked: tests_green desc, compliance desc, evidence desc. Failures keep their
logs — reviewing WHY seeds fail is the point (augment the weak, rerun).
"""
from __future__ import annotations
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed0 import check as seed0_check


def score_seed(path: str, timeout_s: int = 300, meta: dict | None = None) -> dict:
    import time as _t
    t0 = _t.time()
    root = Path(path)
    rep = seed0_check(str(root))
    tests_green, tests_detail = None, "no suite attempted"
    if (root / "tests").exists():
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                               cwd=root, capture_output=True, text=True,
                               timeout=timeout_s)
            tail = (r.stdout + r.stderr).strip().splitlines()
            tests_detail = tail[-1] if tail else "empty output"
            tests_green = (r.returncode == 0)
        except subprocess.TimeoutExpired:
            tests_detail = f"timeout after {timeout_s}s"
            tests_green = False
    evidence = [str(p.relative_to(root)) for p in root.rglob("*")
                if p.is_file() and any(k in p.name for k in
                ("evidence", "run_", "report", "results"))
                and ".git" not in p.parts and "__pycache__" not in p.parts
                and p.suffix != ".pyc"][:20]
    return {"seed": root.name, "path": str(root),
            "substrate": (meta or {}).get("substrate", "unknown"),
            "model": (meta or {}).get("model", ""),
            "elapsed_s": round(time.time() - t0, 2),
            "compliant": rep["compliant"],
            "compliance": f"{rep['passed']}/{rep['total']}",
            "tests_green": tests_green, "tests_detail": tests_detail[:160],
            "evidence": evidence, "scored_at": time.time()}


def leaderboard(paths: list[str], timeout_s: int = 300,
                substrates: dict | None = None,
                meta: dict | None = None) -> list[dict]:
    substrates = substrates or {}
    meta = meta or {}
    rows = [score_seed(p, timeout_s,
                       {**( {"substrate": substrates[p]} if p in substrates else {}),
                        **meta.get(p, {})})
            for p in paths]
    weights = meta.get("__weights__", {}) if isinstance(meta, dict) else {}
    wt = float(weights.get("tests_green", 100))
    wc = float(weights.get("compliant", 10))
    we = float(weights.get("evidence", 1))
    for r in rows:
        r["rank_score"] = round(
            (wt if r["tests_green"] is True else 0.0)
            + (wc if r["compliant"] else 0.0)
            + we * len(r["evidence"]), 4)
        r["weights"] = {"tests_green": wt, "compliant": wc, "evidence": we}
    rows.sort(key=lambda r: r["rank_score"], reverse=True)
    return rows


def report(rows: list[dict]) -> str:
    lines = []
    for i, r in enumerate(rows, 1):
        det = str(r["tests_detail"])[:100]
        lines.append("#" + str(i) + " " + str(r["seed"]) +
                     " tests_green=" + str(r["tests_green"]) +
                     " compliant=" + str(r["compliant"]) +
                     " (" + str(r["compliance"]) + ")" +
                     " evidence=" + str(len(r["evidence"])) + " :: " + det)
    return "\n".join(lines)


if __name__ == "__main__":
    raw = sys.argv[1:]
    model = ""
    if "--model" in raw:
        try:
            model = raw[raw.index("--model") + 1]
        except IndexError:
            pass
    skip = set()
    for i, x in enumerate(raw):
        if x == "--model":
            skip.update((i, i + 1))
    paths = [x for i, x in enumerate(raw)
             if i not in skip and not x.startswith("--")]
    if not paths:
        print("usage: tournament.py <seed-dir> [<seed-dir> ...] [--model m]")
        raise SystemExit(2)
    metas = {p: {"model": model} for p in paths} if model else None
    weights = None
    if "--weights" in sys.argv:
        try:
            weights = json.loads(Path(sys.argv[sys.argv.index("--weights") + 1]).read_text())
        except IndexError:
            pass
    if weights:
        metas = dict(metas or {})
        metas["__weights__"] = weights
    rows = leaderboard(paths, meta=metas)
    print(report(rows))
    with open(f"tournament_{int(time.time())}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    try:
        from runs import new_receipt, save
        rec = new_receipt("tournament",
                          {"seeds": [{"seed": r["seed"],
                                      "substrate": r.get("substrate", "unknown"),
                                      "model": r.get("model", ""),
                                      "elapsed_s": r.get("elapsed_s", 0),
                                      "compliant": r["compliant"],
                                      "tests_green": r["tests_green"],
                                      "rank_score": r.get("rank_score", 0)}
                                     for r in rows],
                          "weights": rows[0].get("weights", {}) if rows else {}})
        save(rec)
        print(f"receipt: runs/{rec['run_id'].replace(':', '_')}.json")
    except Exception:
        pass
