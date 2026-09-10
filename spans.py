#!/usr/bin/env python3
"""spans.py — OTel-shaped tracing without the SDK. Stdlib only.

Why a shim, not opentelemetry-sdk (research-backed call):
  - OTel's power is the SCHEMA (trace/span/parent ids, names, monotonic
    start/end, attributes, events, status), not the package. Console/file
    exporters prove the shape carries the value; OTLP endpoint swaps later.
  - Box doctrine: stdlib-only (test_nodeps), 93% disk. The SDK + gRPC
    exporter stack buys nothing until a collector exists to receive it.
  - Adapter path: `to_otlp(span)` emits OTLP-shaped JSON; when the SDK is
    ever installed, feed these dicts straight into SpanContext creation.
    Attribute names follow gen_ai.* conventions (prompt/completion tokens,
    response.model, estimated_cost_usd) + ham.* (tier, gate) + seed0.*
    (receipt id, compliance) so a future backend indexes them unchanged.

Usage:
  from spans import Tracer
  t = Tracer("runs/money-t2/spans.jsonl", service="seed0-funnel")
  with t.span("bout.money-t2", seed="seed1") as s:
      ...work...
      s.attr("llm.prompt_tokens", 10)
  # or: t.rollup() -> per-trace totals {spans, tokens, cost_usd, elapsed_s}
"""
from __future__ import annotations
import json
import secrets
import time
from pathlib import Path


def _hid(nbytes: int) -> str:
    return secrets.token_hex(nbytes)


class Span:
    def __init__(self, tracer, name: str, parent_id: str | None,
                 attrs: dict | None = None):
        self._tracer = tracer
        self.name = name
        self.trace_id = tracer.trace_id
        self.span_id = _hid(8)
        self.parent_id = parent_id
        self.attrs: dict = dict(attrs or {})
        self.events: list[dict] = []
        self.status = "OK"
        self._t0 = time.monotonic()
        self.start_wall = time.time()

    def attr(self, key: str, value) -> "Span":
        self.attrs[key] = value
        return self

    def event(self, name: str, attrs: dict | None = None) -> "Span":
        self.events.append({"name": name, "at_s": round(time.monotonic() - self._t0, 3),
                            "attrs": attrs or {}})
        return self

    def error(self, message: str) -> "Span":
        self.status = f"ERROR: {message}"[:160]
        return self

    def to_dict(self, end_mono: float | None = None) -> dict:
        end = time.monotonic() if end_mono is None else end_mono
        return {"trace_id": self.trace_id, "span_id": self.span_id,
                "parent_id": self.parent_id, "name": self.name,
                "service": self._tracer.service,
                "start_wall": self.start_wall,
                "elapsed_s": round(end - self._t0, 3),
                "status": self.status, "attributes": self.attrs,
                "events": self.events}

    def __enter__(self) -> "Span":
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.error(f"{exc_type.__name__}: {exc}")
        self._tracer._emit(self)
        return False


class Tracer:
    """One trace per Tracer (one bout/run). Sinks: file (JSONL) + memory."""

    def __init__(self, path: str | None = None, service: str = "seed0"):
        self.trace_id = _hid(16)
        self.service = service
        self.path = Path(path) if path else None
        self._stack: list[Span] = []
        self.finished: list[dict] = []
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def span(self, name: str, **attrs) -> Span:
        parent = self._stack[-1].span_id if self._stack else None
        s = Span(self, name, parent, attrs)

        class _Ctx(Span):
            def __enter__(_self):
                self._stack.append(s)
                return s

            def __exit__(_self, *a):
                self._stack.pop()
                return s.__exit__(*a)

        _c = _Ctx(self, name, parent, attrs)
        _c.span_id = s.span_id
        _c.trace_id = s.trace_id
        return _c

    def _emit(self, span: Span) -> None:
        d = span.to_dict()
        self.finished.append(d)
        if self.path:
            with open(self.path, "a") as f:
                f.write(json.dumps(d, sort_keys=True) + "\n")

    def rollup(self) -> dict:
        """Per-trace totals = the $/run answer. Tokens+cost summed over spans
        carrying gen_ai.* attrs (BATS-style cost rollup, analyze.py shape)."""
        tok_in = 0
        tok_out = 0
        cost = 0.0
        elapsed = 0.0
        for d in self.finished:
            a = d.get("attributes", {})
            tok_in += int(a.get("gen_ai.usage.prompt_tokens",
                               a.get("llm.prompt_tokens", 0)) or 0)
            tok_out += int(a.get("gen_ai.usage.completion_tokens",
                                a.get("llm.output_tokens", 0)) or 0)
            c = a.get("llm.estimated_cost_usd", a.get("cost_usd"))
            try:
                cost += float(c or 0)
            except (TypeError, ValueError):
                pass
            if d.get("parent_id") is None:
                elapsed = max(elapsed, d.get("elapsed_s", 0))
        return {"trace_id": self.trace_id, "spans": len(self.finished),
                "input_tokens": tok_in, "output_tokens": tok_out,
                "cost_usd": round(cost, 6), "elapsed_s": elapsed}


def to_otlp(span_dict: dict) -> dict:
    """Adapter stub: our dict -> OTLP-shaped JSON for a future exporter."""
    return {"traceId": span_dict["trace_id"], "spanId": span_dict["span_id"],
            "parentSpanId": span_dict.get("parent_id") or "",
            "name": span_dict["name"], "kind": "SPAN_KIND_INTERNAL",
            "startTimeUnixNano": int(span_dict["start_wall"] * 1e9),
            "attributes": [{"key": k, "value": {"stringValue": str(v)}}
                           for k, v in span_dict.get("attributes", {}).items()],
            "status": {"code": 2 if str(span_dict.get("status")) == "OK" else 1}}
