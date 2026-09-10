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


def run(dataset: str, model: str, base: str, key: str,
        judge_model: str | None = None, idea: str = "", criteria: str = "",
        meter: Meter | None = None) -> dict:
    ds = json.loads(Path(dataset).read_text())
    meter = meter or Meter(model=model, idea=idea, criteria=criteria)
    meter.model, meter.idea, meter.criteria = model, idea, criteria
    results, score, total = [], 0.0, 0.0
    session = f"seed0-pyeval-{int(time.time())}"
    for case in ds.get("cases", []):
        w = float(case.get("weight", 1))
        total += w
        try:
            ans = complete(base, key, model,
                           [{"role": "user", "content": case["input"]}],
                           session=session, meter=meter)
        except Exception as e:
            results.append({"id": case["id"], "pass": False,
                            "why": f"transport: {e}"[:160], "weight": w})
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
        results.append({"id": case["id"], "pass": ok, "why": why,
                        "weight": w, "answer": ans[:300]})
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
    rep = run(ds_path, kw.get("--model", "mimo-v2.5"), base, key,
              kw.get("--judge-model"), idea=kw.get("--idea", ""),
              criteria=kw.get("--criteria", ""))
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
                                                "weight": r["weight"]}
                                               for r in rep["results"]]},
                          root=kw["--out"])
        print(f"receipt: {save(rec, root=kw['--out'])} {rec['run_id'][:19]}…")
    raise SystemExit(0 if rep["pass"] else 1)
