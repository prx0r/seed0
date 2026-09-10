"""Execution traces: time + tokens for every action, time 0 to finish, per agent.
Stdlib only. Data model stolen from Langfuse/OpenLLMetry so traces export cleanly
later (trace -> spans, kinds workflow/task/llm/tool, gen_ai.usage.* attributes):
a span is {id, parent, name, kind, model, start, end, duration_s, in/out tokens,
cost_usd, attrs}. Durations are measured spans, not estimates — granularize by
adding spans, never by guessing. Self-hosted Langfuse (Postgres+ClickHouse+Redis)
is the graduate path when volume justifies it; this file is the MVP that runs
anywhere, including a 5GB box.
"""
from __future__ import annotations
import json
import time
import uuid
from pathlib import Path

KINDS = ("workflow", "task", "llm", "tool", "agent")


def _now() -> float:
    return time.time()


class Tracer:
    def __init__(self, clock=_now):
        self._clock = clock
        self.spans: list[dict] = []

    def start(self, name: str, kind: str = "task", model: str = "",
              parent: str | None = None, attrs: dict | None = None) -> str:
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {KINDS}")
        sid = "sp_" + uuid.uuid4().hex[:12]
        self.spans.append({"id": sid, "parent": parent, "name": name,
                           "kind": kind, "model": model, "start": self._clock(),
                           "end": None, "duration_s": None,
                           "input_tokens": 0, "output_tokens": 0,
                           "cost_usd": None, "attrs": attrs or {}})
        return sid

    def end(self, sid: str, attrs: dict | None = None):
        for s in self.spans:
            if s["id"] == sid and s["end"] is None:
                s["end"] = self._clock()
                s["duration_s"] = round(s["end"] - s["start"], 4)
                if attrs:
                    s["attrs"].update(attrs)
                return s
        raise KeyError(f"unknown or finished span: {sid}")

    def tokens(self, sid: str, input_n: int, output_n: int, model: str = ""):
        for s in self.spans:
            if s["id"] == sid:
                s["input_tokens"] += int(input_n or 0)
                s["output_tokens"] += int(output_n or 0)
                if model:
                    s["model"] = model
                s["cost_usd"] = _cost(s["model"], s["input_tokens"],
                                      s["output_tokens"])
                return s
        raise KeyError(f"unknown span: {sid}")

    def summary(self) -> dict:
        done = [s for s in self.spans if s["duration_s"] is not None]
        total = round(sum(s["duration_s"] for s in done), 4)
        ti = sum(s["input_tokens"] for s in self.spans)
        to = sum(s["output_tokens"] for s in self.spans)
        costs = [s["cost_usd"] for s in self.spans
                 if s["cost_usd"] is not None]
        by_action: dict[str, dict] = {}
        for s in done:
            b = by_action.setdefault(s["name"], {"calls": 0, "total_s": 0.0,
                                                 "in": 0, "out": 0})
            b["calls"] += 1
            b["total_s"] = round(b["total_s"] + s["duration_s"], 4)
            b["in"] += s["input_tokens"]
            b["out"] += s["output_tokens"]
        return {"spans": len(self.spans), "finished": len(done),
                "total_s": total, "input_tokens": ti, "output_tokens": to,
                "cost_usd": round(sum(costs), 6) if costs else None,
                "by_action": by_action}

    def save(self, path: str) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(json.dumps(s) for s in self.spans) + "\n")
        return p

    @classmethod
    def load(cls, path: str) -> "Tracer":
        t = cls()
        for line in Path(path).read_text().splitlines():
            try:
                t.spans.append(json.loads(line))
            except Exception:
                continue
        return t


def _cost(model: str, inp: int, out: int) -> float | None:
    try:
        from telemetry import cost_usd
        return cost_usd(model, inp, out)
    except Exception:
        return None
