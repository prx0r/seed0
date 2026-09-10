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
               idea_id: str = "", criteria: str = "",
               timeout_s: int = 600) -> dict:
    outdir = Path(out)
    (outdir / "attempts").mkdir(parents=True, exist_ok=True)
    (outdir / "brief.md").write_text(f"# Brief\n\n{idea}\n")
    (outdir / "rubric.json").write_text(json.dumps(rubric, indent=1))
    _meter = Meter(model=model, idea=idea_id, criteria=criteria)
    import hashlib as _h
    brief_sha = _h.sha256(idea.encode()).hexdigest()[:12]
    try:
        from spans import Tracer as _Tracer
        _tracer = _Tracer(str(outdir / "spans.jsonl"), service="seed0-funnel")
    except Exception:
        _tracer = None
    results = []
    _round = (_tracer.span("funnel.round", seed0_idea=idea[:80],
                           brief_sha12=brief_sha, model=model or "none")
              if _tracer else None)
    if _round is not None:
        _round.__enter__()
    try:
        for seed in seeds:
            _s = (_tracer.span("funnel.seed", seed=Path(seed).name)
                  if _tracer else None)
            if _s is not None:
                _s.__enter__()
            try:
                score = _run_one_seed(outdir, seed_root, seed, rubric, idea,
                                      brief_sha, agent_cmd, timeout_s)
            finally:
                if _s is not None:
                    _s.__exit__(None, None, None)
            if _s is not None and _tracer is not None:
                # re-open span record to attach outcome (spans are values too)
                _tracer.finished[-1]["attributes"].update(
                    {"seed0.binary_pass": score.get("binary_pass"),
                     "seed0.suite_green": score.get("suite_green"),
                     "seed0.elapsed_s": score.get("elapsed_s")})
            results.append(score)
    finally:
        if _round is not None:
            passes = sum(1 for r in results if r.get("binary_pass") is True)
            _round.attr("seed0.seeds", len(seeds)).attr("seed0.passes", passes)
            _round.__exit__(None, None, None)

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


def _run_one_seed(outdir, seed_root, seed, rubric, idea, brief_sha,
                  agent_cmd, timeout_s):
    att = outdir / "attempts" / Path(seed).name
    if att.exists():
        shutil.rmtree(att)
    src = Path(seed) if Path(seed).exists() else Path(seed_root) / seed
    shutil.copytree(src, att,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    (att / "brief.md").write_text(f"# Brief\n\n{idea}\n")
    (att / "rubric.json").write_text(json.dumps(rubric, indent=1))
    # S22 attempt record: prompt→artifact linkage (ait-vcs shape).
    (att / "attempt.json").write_text(json.dumps(
        {"seed": Path(seed).name, "brief_sha12": brief_sha,
         "rubric_ids": [c.get("id") for c in rubric.get("checks", [])],
         "agent_cmd": agent_cmd, "started_ts": time.time()}, indent=1))
    t0 = time.time()
    try:
        import os as _os
        from budgets import from_env as _budget_from_env
        env = dict(_os.environ)
        env.update(_budget_from_env().advertise())
        import shlex as _shlex
        try:
            argv = _shlex.split(agent_cmd) + [str(att)]
        except ValueError:
            argv = agent_cmd.split() + [str(att)]
        p = subprocess.run(argv, capture_output=True,
                           text=True, timeout=timeout_s, env=env)
        agent_ok, agent_log = p.returncode == 0, (p.stdout + p.stderr)[-1000:]
    except subprocess.TimeoutExpired:
        agent_ok, agent_log = False, "agent timeout"
        _wip_checkpoint(att)
    score = score_attempt(str(att), rubric, time.time() - t0)
    score.update({"seed": seed, "agent_ok": agent_ok,
                  "agent_log": agent_log})
    # B1 spend line: elapsed measured externally; subprocess tokens are
    # unobservable — recorded as zeros, never estimated (honest zeros).
    try:
        from grants import log_spend
        log_spend(str(outdir / "spend.jsonl"),
                  {"seed": Path(seed).name,
                   "elapsed_s": score["elapsed_s"],
                   "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0,
                   "usage_source": "subprocess-unobservable"})
    except Exception:
        pass
    return score




def _wip_checkpoint(att: Path) -> str:
    """S19 WIP auto-checkpoint (git-lanes pattern): on agent timeout, commit
    attempt state to a local branch so partial work survives the crash.
    Best-effort; returns commit sha or "" (never fails the run)."""
    import subprocess as _sp
    try:
        r = lambda *a: _sp.run(["git", *a], cwd=att, capture_output=True,
                               timeout=30)
        if r("rev-parse", "--git-dir").returncode != 0:
            r("init", "-q"), r("config", "user.email", "funnel@local"), \
                r("config", "user.name", "funnel")
        r("add", "-A")
        c = r("commit", "-qm", "wip: agent timeout snapshot")
        if c.returncode != 0:
            return ""
        return r("rev-parse", "--short", "HEAD").stdout.strip()
    except Exception:
        return ""


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
                     "metric": "", "hypothesis": "", "change": "", "verdict": ""}
                    for s in scores]
        (run / f"scores_blind_r{rnd}.jsonl").write_text("\n".join(
            json.dumps({"lane": lanes[s["seed"]],
                        "binary_pass": s["binary_pass"]}) for s in scores) + "\n")
    else:
        entries = [{"seed": s["seed"], "binary_pass": s["binary_pass"],
                    "metric": "", "hypothesis": "", "change": "", "verdict": ""}
                   for s in scores]
    doc = {"round": rnd, "at": time.time(), "blind": blind,
           "instruction": "Main agent: for EACH entry write hypothesis (why it "
                          "passed/failed), change (exact seed edit or null), "
                          "and verdict (promote/augment/drop). Then amend." +
                           (" Judge lanes only — cite only lane-visible fields "
                            "(lane, binary_pass, metric). scores.jsonl carries "
                            "seed names and counts: judging from it voids blindness. "
                            "Use scores_blind_r<N>.jsonl. Do not unseal until verdicts done."
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


def freeze_run(run_dir: str) -> str:
    """Pre-registration as a commit (S30): stage brief+rubric+validator+
    weights in the containing repo and commit. Returns the freeze sha —
    lanes built after this sha cannot claim a different brief."""
    import subprocess as _sp
    run = Path(run_dir)
    top = _sp.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                  text=True, cwd=run)
    if top.returncode != 0:
        raise RuntimeError(f"freeze needs a git repo above {run_dir}")
    root = top.stdout.strip()
    rel = run.resolve().relative_to(Path(root).resolve())
    names = ["brief.md", "rubric.json", "validate.py", "weights.json"]
    staged = [str(rel / n) for n in names if (run / n).exists()]
    if not staged:
        raise ValueError(f"nothing freezable in {run_dir} (need brief/rubric/...)")
    _sp.run(["git", "add", *staged], cwd=root, check=True, capture_output=True)
    _sp.run(["git", "commit", "-qm", f"freeze: {rel} brief+rubric+validator+weights"],
            cwd=root, check=True, capture_output=True)
    return _sp.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                   capture_output=True, text=True).stdout.strip()


def lane_risk(attempt_dirs: list[str]) -> dict:
    """Risk-scored lane scheduling (OpenWeft pattern): file overlap between
    lanes decides what runs parallel vs serialized. Returns pairwise shared
    counts + greedy phases (overlapping lanes never share a phase)."""
    SKIP = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache"}
    files: dict[str, set[str]] = {}
    for d in attempt_dirs:
        got = set()
        for p in Path(d).rglob("*"):
            if p.is_file() and not any(x in p.parts for x in SKIP):
                got.add(p.relative_to(d).as_posix())
        files[d] = got
    pairs = {}
    names = list(attempt_dirs)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            shared = sorted(files[names[i]] & files[names[j]])
            if shared:
                pairs[f"{names[i]}+{names[j]}"] = shared
    phases: list[list[str]] = []
    for d in names:
        placed = False
        for ph in phases:
            clash = any(f"{a}+{d}" in pairs or f"{d}+{a}" in pairs for a in ph)
            if not clash:
                ph.append(d)
                placed = True
                break
        if not placed:
            phases.append([d])
    return {"pairs": pairs, "phases": phases}


def amend(seed_dir: str, bump: str, note: str, run_dir: str = "",
          falsifier: str = "") -> dict:
    """Record a seed amendment (seed1 -> 1.1). File edits themselves are the
    main agent's diff; this stamps VERSION + log so reruns are traceable.
    falsifier (One-Recipe pattern): what observation would disprove that this
    amendment helped — empty means untestable, stated, not hidden."""
    root = Path(seed_dir)
    (root / "VERSION").write_text(bump.strip() + "\n")
    rec = {"at": time.time(), "seed": root.name, "version": bump.strip(),
           "note": note, "run": run_dir, "falsifier": falsifier}
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
