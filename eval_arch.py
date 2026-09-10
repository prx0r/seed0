#!/usr/bin/env python3
"""eval_arch: prove an essay-derived pattern earns its keep. Stdlib only.

  python3 eval_arch.py --arch ledger --seed seeds/seed1 --rubric rubric.json \\
      --ablate ralph.py --agent-cmd true --out runs/eval-ledger

Runs the seed intact (A) and with listed paths removed (B) through the funnel
binary rubric, then reports the delta:
  A pass + B fail  -> pattern load-bearing HERE (keep + dig deeper)
  A pass + B pass  -> pattern inert here (cut it or find a harder rubric)
  A fail           -> broken regardless (fix the seed before crediting ideas)
Writes a digest-pinned receipt. This is idea2's falsifier, mechanized.
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from funnel import run_funnel


def run_eval(arch: str, seed: str, rubric: dict, ablate: list[str],
             agent_cmd: str, out: str) -> dict:
    t0 = time.time()
    a = run_funnel(f"eval/arch={arch} intact", rubric, [Path(seed).name],
                   agent_cmd, f"{out}/A", seed_root=str(Path(seed).parent))
    ablated = Path(tempfile.mkdtemp(prefix="ablate-")) / Path(seed).name
    shutil.copytree(seed, ablated,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    removed = []
    for rel in ablate:
        p = ablated / rel
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            removed.append(rel)
    b = run_funnel(f"eval/arch={arch} ablated", rubric, [ablated.name],
                   agent_cmd, f"{out}/B", seed_root=str(ablated.parent))
    ra, rb = a["results"][0], b["results"][0]
    if ra["binary_pass"] and not rb["binary_pass"]:
        verdict = "load-bearing"
    elif ra["binary_pass"] and rb["binary_pass"]:
        verdict = "inert-here"
    else:
        verdict = "broken-regardless"
    rep = {"arch": arch, "seed": seed, "ablated": removed,
           "A_pass": ra["binary_pass"], "B_pass": rb["binary_pass"],
           "verdict": verdict, "elapsed_s": round(time.time() - t0, 2)}
    Path(out).mkdir(parents=True, exist_ok=True)
    (Path(out) / "eval.json").write_text(json.dumps(rep, indent=1))
    try:
        from runs import new_receipt, save
        rec = new_receipt("eval-arch", rep)
        save(rec, root=f"{out}/runs")
    except Exception:
        pass
    return rep


if __name__ == "__main__":
    a = sys.argv[1:]
    kw, pos = {}, []
    it = iter(a)
    for x in it:
        if x.startswith("--"):
            try:
                kw[x] = next(it)
            except StopIteration:
                print(f"flag {x} needs a value")
                raise SystemExit(2)
    rubric = json.loads(Path(kw["--rubric"]).read_text())
    rep = run_eval(kw.get("--arch", "unnamed"), kw["--seed"], rubric,
                   kw.get("--ablate", "").split(",") if kw.get("--ablate") else [],
                   kw.get("--agent-cmd", "true"), kw["--out"])
    print(json.dumps(rep, indent=1))
