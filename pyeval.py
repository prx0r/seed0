#!/usr/bin/env python3
"""pyeval: run an eval dataset against an OpenAI-compatible chat-completions
endpoint. Stdlib only (urllib, no SDK to install).

  OPENCODE_GO_API_KEY=... python3 pyeval.py run datasets/safety_sample.json \\
      --model mimo-v2.5 --base https://opencode.ai/zen/go/v1

Dataset: {"cases": [{"id", "input", "expect": {"contains"|"absent"|"regex": [...]},
"evaluator": "rule", "weight": 1} | {"evaluator": "judge", "rubric": "...",
"judge_model": "..."}]}. Judge cases call the model a second time with a
grading prompt (same endpoint). Results JSONL to stdout + summary line.
Exit 1 unless every weighted case passes. Key travels via env only, never logs.
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

from telemetry import Meter, extract_usage


def complete(base: str, key: str, model: str, messages: list,
             session: str = "seed0-pyeval", timeout: int = 90,
             meter=None) -> str:
    body = json.dumps({"model": model, "messages": messages,
                       "temperature": 0}).encode()
    r = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body,
                               headers={"Content-Type": "application/json",
                                        "Authorization": f"Bearer {key}",
                                        "x-opencode-session": session,
                                        "User-Agent": "seed0-pyeval/0.1"},
                               method="POST")
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    if meter is not None:
        u = extract_usage(data)
        meter.input_tokens += u["input_tokens"]
        meter.output_tokens += u["output_tokens"]
        if os.getenv("SPEND_LOG"):  # a-metering-design: per-call spend line
            from grants import log_spend
            log_spend(os.getenv("SPEND_LOG"),
                      {"model": model, "in": u["input_tokens"],
                       "out": u["output_tokens"]})
    return data["choices"][0]["message"]["content"]


def grade_rule(answer: str, expect: dict) -> tuple[bool, str]:
    a = answer or ""
    for w in expect.get("contains", []):
        if w.lower() not in a.lower():
            return False, f"missing: {w[:60]}"
    for w in expect.get("absent", []):
        if w.lower() in a.lower():
            return False, f"forbidden present: {w[:60]}"
    for pat in expect.get("regex", []):
        if not re.search(pat, a):
            return False, f"regex miss: {pat[:60]}"
    return True, "rule pass"


def grade_judge(complete_fn, answer: str, rubric: str) -> tuple[bool, str]:
    verdict = complete_fn([
        {"role": "system", "content": "Grade PASS or FAIL only, then a reason. "
         "Format: VERDICT: PASS|FAIL. Reason: ..."},
        {"role": "user", "content": f"Rubric: {rubric}\n\nAnswer:\n{answer}"}])
    m = re.search(r"VERDICT:\s*(PASS|FAIL)", verdict, re.I)
    if not m:
        return False, "judge gave no verdict"
    return m.group(1).upper() == "PASS", verdict.strip()[:200]


TIER_MODELS = {"free": "mimo-v2.5", "cheap": "mimo-v2.5",
               "strong": "muse-spark-1.3-contributor"}


def resolve_model(kw: dict, bgt=None) -> tuple[str, str]:
    """BATS wiring: --model auto picks cheapest tier the budget allows
    (WorkerKit lineage). Returns (model, reason). No network, pure logic."""
    model = kw.get("--model", "mimo-v2.5")
    if model != "auto":
        return model, "explicit"
    from grants import select_tier
    remaining = (bgt.max_usd - bgt.spent_usd) if bgt and bgt.max_usd else 1.0
    tier = select_tier(remaining, float(kw.get("--uncertainty", "0.5")))
    return TIER_MODELS[tier["tier"]], f"tier={tier['tier']} {tier['reason']}"


def run(dataset: str, model: str, base: str, key: str,
        judge_model: str | None = None, idea: str = "", criteria: str = "",
        meter: Meter | None = None, budget=None) -> dict:
    ds = json.loads(Path(dataset).read_text())
    meter = meter or Meter(model=model, idea=idea, criteria=criteria)
    meter.model, meter.idea, meter.criteria = model, idea, criteria
    results, score, total = [], 0.0, 0.0
    session = f"seed0-pyeval-{int(time.time())}"
    from telemetry import cost_usd
    for case in ds.get("cases", []):
        w = float(case.get("weight", 1))
        total += w
        if budget is not None and budget.exhausted():
            results.append({"id": case["id"], "pass": False,
                            "why": "budget exhausted — run stopped, not failed",
                            "weight": w, "elapsed_s": 0.0,
                            "input_tokens": 0, "output_tokens": 0,
                            "cost_usd": 0.0})
            continue
        if budget is not None:
            try:
                budget.check(case["id"])  # refuse BEFORE the call, not after
            except Exception as e:
                results.append({"id": case["id"], "pass": False,
                                "why": f"pre-call refusal: {e}"[:160],
                                "weight": w, "elapsed_s": 0.0,
                                "input_tokens": 0, "output_tokens": 0,
                                "cost_usd": 0.0})
                continue
        i0, o0 = meter.input_tokens, meter.output_tokens
        t0 = time.time()
        try:
            ans = complete(base, key, model,
                           [{"role": "user", "content": case["input"]}],
                           session=session, meter=meter)
        except Exception as e:
            results.append({"id": case["id"], "pass": False,
                            "why": f"transport: {e}"[:160], "weight": w,
                            "elapsed_s": round(time.time() - t0, 2),
                            "input_tokens": 0, "output_tokens": 0,
                            "cost_usd": 0.0})
            continue
        if case.get("evaluator", "rule") == "judge":
            jm = case.get("judge_model") or judge_model or model
            try:
                ok, why = grade_judge(
                    lambda ms: complete(base, key, jm, ms, session=session,
                                        meter=meter),
                    ans, case.get("rubric", ""))
            except Exception as e:
                ok, why = False, f"judge transport: {e}"[:160]
        else:
            ok, why = grade_rule(ans, case.get("expect", {}))
        score += w if ok else 0.0
        if budget is not None:
            di, do = meter.input_tokens - i0, meter.output_tokens - o0
            try:
                budget.record(tokens=di + do,
                              cost=cost_usd(model, di, do), label=case["id"])
            except Exception as e:
                ok, why = False, f"budget refused next call: {e}"[:160]
        di, do = meter.input_tokens - i0, meter.output_tokens - o0
        results.append({"id": case["id"], "pass": ok, "why": why,
                        "weight": w, "answer": ans[:300],
                        "elapsed_s": round(time.time() - t0, 2),
                        "input_tokens": di, "output_tokens": do,
                        "cost_usd": cost_usd(model, di, do)})
    return {"model": model, "score": score, "total": total,
            "pass": bool(total) and score >= total, "results": results,
            "telemetry": meter.block()}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] != "run":
        print(__doc__)
        raise SystemExit(2)
    a = sys.argv[1:]
    if not a or a[0] != "run":
        print("usage: pyeval.py run DATASET [--model m] [--base url] [--judge-model m] [--out runs/]")
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
        else:
            pos.append(x)
    if not pos:
        print("usage: pyeval.py run DATASET [--model m] [--base url] [--judge-model m] [--out runs/]")
        raise SystemExit(2)
    ds_path = kw.get("--dataset", pos[0])
    base = kw.get("--base", os.getenv("OPENCODE_GO_BASE_URL",
                                      "https://opencode.ai/zen/go/v1"))
    key = os.getenv("OPENCODE_GO_API_KEY", "")
    if not key:
        print("OPENCODE_GO_API_KEY not set (env only, never a file)")
        raise SystemExit(2)
    from budgets import Budget
    bgt = None
    if kw.get("--budget-usd") or kw.get("--budget-tokens"):
        bgt = Budget(max_usd=float(kw["--budget-usd"]) if kw.get("--budget-usd") else None,
                     max_tokens=int(kw["--budget-tokens"]) if kw.get("--budget-tokens") else None)
    model, why = resolve_model(kw, bgt)
    if why != "explicit":
        print(f"BATS {why} -> {model}")
    rep = run(ds_path, model, base, key,
              kw.get("--judge-model"), idea=kw.get("--idea", ""),
              criteria=kw.get("--criteria", ""), budget=bgt)
    for r in rep["results"]:
        print(json.dumps(r))
    print(f"SCORE {rep['score']}/{rep['total']} "
          f"{'PASS' if rep['pass'] else 'FAIL'} model={rep['model']}")
    t = rep["telemetry"]
    print(f"TELEMETRY elapsed={t['elapsed_s']}s in={t['input_tokens']} "
          f"out={t['output_tokens']} cost=${t['cost_usd']} "
          f"idea={t['idea_version'] or '-'} criteria={t['criteria_version'] or '-'}")
    if kw.get("--out"):
        from runs import new_receipt, save
        rec = new_receipt("pyeval", {"model": rep["model"], "dataset": ds_path,
                                     "score": rep["score"], "total": rep["total"],
                                     "pass": rep["pass"],
                                     "telemetry": rep["telemetry"],
                                      "cases": [{"id": r["id"], "pass": r["pass"],
                                                 "weight": r["weight"],
                                                 "elapsed_s": r.get("elapsed_s", 0),
                                                 "input_tokens": r.get("input_tokens", 0),
                                                 "output_tokens": r.get("output_tokens", 0),
                                                 "cost_usd": r.get("cost_usd", 0)}
                                                for r in rep["results"]]},
                          root=kw["--out"])
        print(f"receipt: {save(rec, root=kw['--out'])} {rec['run_id'][:19]}…")
    raise SystemExit(0 if rep["pass"] else 1)
