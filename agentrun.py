#!/usr/bin/env python3
"""agentrun.py — measured agent execution. Stdlib only.

The rule this file enforces: every agent run produces time + tokens + cost,
measured from OUTSIDE the agent (our stopwatch, our file reads). The agent's
own claims about its effort are never used. What can't be measured is labeled,
never estimated:

usage_source: "provider-reported" (usage file / API usage block)
            | "no-inference"      (stub/local command — zero tokens, KNOWN)
            | "unknown"           (no usage channel — e.g. opaque subagents)

Supports Hermes natively: pass --usage-file and hermes writes its own usage
JSON (`hermes -z PROMPT --usage-file lane/usage.json`); we read it after.
opencode: `opencode run --format json` streams events (usage parsing:
best-effort key scan, stated as such).
"""
from __future__ import annotations
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telemetry import cost_usd


def _scan_usage(obj, depth: int = 0) -> dict:
    """Best-effort token extraction from unknown usage-file shapes."""
    found = {}
    if depth > 6 or not isinstance(obj, dict):
        return found
    low = {str(k).lower(): v for k, v in obj.items()}
    for k_in in ("input_tokens", "prompt_tokens", "inputtokens"):
        if k_in in low and isinstance(low[k_in], (int, float)):
            found["input_tokens"] = int(low[k_in])
    for k_out in ("output_tokens", "completion_tokens", "outputtokens"):
        if k_out in low and isinstance(low[k_out], (int, float)):
            found["output_tokens"] = int(low[k_out])
    if "input_tokens" in found and "output_tokens" in found:
        return found
    for v in obj.values():
        if isinstance(v, dict):
            r = _scan_usage(v, depth + 1)
            if "input_tokens" in r and "output_tokens" in r:
                return r
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    r = _scan_usage(item, depth + 1)
                    if "input_tokens" in r and "output_tokens" in r:
                        return r
    return found


def read_usage_file(path: str) -> dict:
    """Parse a Hermes --usage-file (or any JSON); {} when absent/unparseable."""
    try:
        return _scan_usage(json.loads(Path(path).read_text()))
    except Exception:
        return {}


def run_agent(name: str, cmd: list[str], model: str = "",
              timeout_s: int = 2700, usage_file: str = "",
              cwd: str | None = None) -> dict:
    """Launch one agent, time it externally, kill on timeout, collect usage.
    Returns the timed receipt. Never raises on agent failure (records it)."""
    t0 = time.monotonic()
    w0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout_s, cwd=cwd)
        rc, tail = p.returncode, (p.stdout + p.stderr)[-800:]
        timed_out = False
    except subprocess.TimeoutExpired as e:
        rc, timed_out = -1, True
        out = (e.stdout or b"").decode(errors="ignore") if e.stdout else ""
        tail = (out + (e.stderr or b"").decode(errors="ignore"))[-800:] or "timeout"
    elapsed = round(time.monotonic() - t0, 3)
    usage = read_usage_file(usage_file) if usage_file else {}
    if usage:
        source = "provider-reported"
        inp, out = usage["input_tokens"], usage["output_tokens"]
    elif usage_file:
        source, inp, out = "unknown", 0, 0
    else:
        source, inp, out = "no-inference", 0, 0
    return {"agent": name, "model": model, "command": " ".join(cmd)[:160],
            "returncode": rc, "timed_out": timed_out,
            "elapsed_s": elapsed, "wall_start": w0,
            "input_tokens": inp, "output_tokens": out,
            "cost_usd": cost_usd(model, inp, out) if (inp or out) else 0.0,
            "usage_source": source,
            "usage_file": usage_file, "log_tail": tail[:800]}


def main(argv: list[str]) -> int:
    if "--" not in argv or len(argv) < 4:
        print("usage: agentrun.py --name N --model M [--timeout S] [--usage-file P] -- <cmd...>")
        return 2
    ix = argv.index("--")
    rest, cmd = argv[:ix], argv[ix + 1:]
    kw: dict[str, str] = {}
    it = iter(rest)
    for x in it:
        if x.startswith("--"):
            try:
                kw[x] = next(it)
            except StopIteration:
                print(f"flag {x} needs a value")
                return 2
    for f in ("--name",):
        if f not in kw:
            print("usage: agentrun.py --name N [--model M] [--timeout S] [--usage-file P] -- <cmd...>")
            return 2
    rec = run_agent(kw["--name"], cmd, model=kw.get("--model", ""),
                    timeout_s=int(kw.get("--timeout", "2700")),
                    usage_file=kw.get("--usage-file", ""))
    print(json.dumps(rec, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
