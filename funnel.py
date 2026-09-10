#!/usr/bin/env python3
"""Tournament funnel: idea -> isolated fresh-agent attempts -> score -> review.

  python3 funnel.py run --idea "todo API" --rubric rubric.json --seeds seed1,seed2 \\
      --agent-cmd ./agent.sh --out runs/idea1
  python3 funnel.py review --run runs/idea1 --round 1   # writes review template
  python3 funnel.py review --run runs/idea1 --round 1 --blind  # lanes + sealed map
  python3 funnel.py reveal --run runs/idea1 --round 1  # AFTER verdicts only
  python3 funnel.py amend --seed seeds/seed1 --bump 1.1 --note "..." --run runs/idea1

Isolation rule: each attempt gets a FRESH directory containing ONLY the seed +
brief.md + rubric.json. No thesis, no other seeds, no history. The agent proves
the seed carries the idea alone.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed0 import check as seed0_check
from telemetry import Meter


def run_funnel(idea: str, rubric: dict, seeds: list[str], agent_cmd: str,
               out: str, seed_root: str = "seeds", model: str = "",
               idea_id: str = "", criteria: str = "") -> dict:
    outdir = Path(out)
    (outdir / "attempts").mkdir(parents=True, exist_ok=True)
    (outdir / "brief.md").write_text(f"# Brief\n\n{idea}\n")
    (outdir / "rubric.json").write_text(json.dumps(rubric, indent=1))
    _meter = Meter(model=model, idea=idea_id, criteria=criteria)
    results = []
    for seed in seeds:
        att = outdir / "attempts" / Path(seed).name
        if att.exists():
            shutil.rmtree(att)
        src = Path(seed) if Path(seed).exists() else Path(seed_root) / seed
        shutil.copytree(src, att,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        (att / "brief.md").write_text(f"# Brief\n\n{idea}\n")
        (att / "rubric.json").write_text(json.dumps(rubric, indent=1))
        t0 = time.time()
        try:
            import os as _os
            from budgets import from_env as _budget_from_env
            env = dict(_os.environ)
            env.update(_budget_from_env().advertise())
            p = subprocess.run(agent_cmd.split() + [str(att)], capture_output=True,
                               text=True, timeout=600, env=env)
            agent_ok, agent_log = p.returncode == 0, (p.stdout + p.stderr)[-1000:]
        except subprocess.TimeoutExpired:
            agent_ok, agent_log = False, "agent timeout"
        score = score_attempt(str(att), rubric, time.time() - t0)
        score.update({"seed": seed, "agent_ok": agent_ok,
                      "agent_log": agent_log})
        results.append(score)
    (outdir / "scores.jsonl").write_text(
        "\n".join(json.dumps(r) for r in results) + "\n")
    try:
        from runs import new_receipt, save
        rec = new_receipt("funnel-round",
                          {"idea": idea,
                           "telemetry": _meter.block(),
                           "seeds": [{"seed": r["seed"],
                                      "binary_pass": r["binary_pass"],
                                      "compliance": r["compliance"],
                                      "suite_green": r["suite_green"]}
                                     for r in results]},
                          root=str(outdir / "runs"))
        save(rec, root=str(outdir / "runs"))
    except Exception:
        pass  # receipt is evidence, never load-bearing for the run itself
    return {"idea": idea, "results": results}


def score_attempt(path: str, rubric: dict, elapsed_s: float) -> dict:
    rep = seed0_check(path)
    suite_green, suite_detail = None, "no suite"
    if (Path(path) / "tests").exists():
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                               cwd=path, capture_output=True, text=True, timeout=300)
            suite_green = (r.returncode == 0)
            suite_detail = ((r.stdout + r.stderr).strip().splitlines() or ["?"])[-1][:160]
        except subprocess.TimeoutExpired:
            suite_detail = "suite timeout"
    rubric_hits = {}
    for c in rubric.get("checks", []):
        rubric_hits[c["id"]] = eval_check(path, c)
    binary_pass = (suite_green is True and rep["compliant"]
                   and all(rubric_hits.values()))
    return {"compliant": rep["compliant"], "compliance": f"{rep['passed']}/{rep['total']}",
            "suite_green": suite_green, "suite_detail": suite_detail,
            "rubric": rubric_hits, "binary_pass": binary_pass,
            "elapsed_s": round(elapsed_s, 1)}


def eval_check(path: str, c: dict) -> bool:
    root = Path(path)
    kind = c.get("type")
    if kind == "file_exists":
        return (root / c["path"]).exists()
    if kind == "contains":
        f = root / c["path"]
        return f.exists() and c["text"] in f.read_text(errors="ignore")
    if kind == "suite_green":
        return True  # folded into binary_pass; listed for readability
    return False


def review_template(run_dir: str, rnd: int, blind: bool = False,
                    seed: int = 7) -> Path:
    """Write the main-agent review scaffold. With blind=True, seeds become
    Lane A/B/C (deterministic shuffle) and identities go to sealed_map.json —
    judge behavior first, reveal names only after verdicts (DSH/clouatre pattern)."""
    import random
    run = Path(run_dir)
    scores = [json.loads(l) for l in (run / "scores.jsonl").read_text().splitlines()]
    if blind:
        order = sorted([s["seed"] for s in scores])
        rng = random.Random(f"{run_dir}|{rnd}|{seed}")
        rng.shuffle(order)
        lanes = {name: f"Lane {chr(65 + i)}" for i, name in enumerate(order)}
        (run / f"sealed_map_r{rnd}.json").write_text(json.dumps(
            {"round": rnd, "map": lanes,
             "note": "reveal only after verdicts: funnel.py reveal"}, indent=1))
        entries = [{"lane": lanes[s["seed"]], "binary_pass": s["binary_pass"],
                    "hypothesis": "", "change": "", "verdict": ""}
                   for s in scores]
    else:
        entries = [{"seed": s["seed"], "binary_pass": s["binary_pass"],
                    "hypothesis": "", "change": "", "verdict": ""}
                   for s in scores]
    doc = {"round": rnd, "at": time.time(), "blind": blind,
           "instruction": "Main agent: for EACH entry write hypothesis (why it "
                          "passed/failed), change (exact seed edit or null), "
                          "and verdict (promote/augment/drop). Then amend." +
                          (" Judge lanes only — do not unseal until verdicts done."
                           if blind else ""),
           "seeds": entries,
           "promotions": []}
    p = run / f"review_r{rnd}{'_blind' if blind else ''}.json"
    p.write_text(json.dumps(doc, indent=1))
    return p


def reveal(run_dir: str, rnd: int) -> dict:
    """Merge sealed lane identities back into the blind review. Returns map."""
    run = Path(run_dir)
    m = json.loads((run / f"sealed_map_r{rnd}.json").read_text())["map"]
    inv = {v: k for k, v in m.items()}
    p = run / f"review_r{rnd}_blind.json"
    doc = json.loads(p.read_text())
    for e in doc.get("seeds", []):
        if "lane" in e:
            e["seed"] = inv.get(e["lane"], "?")
    doc["revealed"] = True
    p.write_text(json.dumps(doc, indent=1))
    return m


def amend(seed_dir: str, bump: str, note: str, run_dir: str = "") -> dict:
    """Record a seed amendment (seed1 -> 1.1). File edits themselves are the
    main agent's diff; this stamps VERSION + log so reruns are traceable."""
    root = Path(seed_dir)
    (root / "VERSION").write_text(bump.strip() + "\n")
    rec = {"at": time.time(), "seed": root.name, "version": bump.strip(),
           "note": note, "run": run_dir}
    with open(root / "AMENDMENTS.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("run", "review", "amend", "reveal"):
        print(__doc__)
        raise SystemExit(2)
    kw, pos = {}, []
    it = iter(a[1:])
    for x in it:
        if x.startswith("--"):
            try:
                kw[x] = next(it)
            except StopIteration:
                print(f"flag {x} needs a value")
                raise SystemExit(2)
    if a[0] == "run":
        rubric = json.loads(Path(kw["--rubric"]).read_text())
        out = run_funnel(kw["--idea"], rubric, kw["--seeds"].split(","),
                         kw.get("--agent-cmd", "true"), kw["--out"],
                         model=kw.get("--model", ""),
                         idea_id=kw.get("--idea-id", ""),
                         criteria=kw.get("--criteria", ""))
        print(json.dumps({r["seed"]: r["binary_pass"] for r in out["results"]}))
    elif a[0] == "review":
        print(review_template(kw["--run"], int(kw.get("--round", "1")),
                              blind="--blind" in a))
    elif a[0] == "amend":
        print(amend(kw["--seed"], kw["--bump"], kw.get("--note", ""),
                    kw.get("--run", "")))
    elif a[0] == "reveal":
        print(reveal(kw["--run"], int(kw.get("--round", "1"))))
