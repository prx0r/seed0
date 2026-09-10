# a-spans — progress report

## 1. claim
OTel-shaped tracing live with zero deps: spans emit from funnel + pyeval,
rollup answers $/run; research-backed shim-not-SDK call.

## 2. evidence
- `spans.py`: trace/span/parent ids (16/8-byte hex), monotonic timing,
  attributes, events, error status, JSONL sink, `rollup()` (tokens/cost/
  elapsed), `to_otlp()` adapter stub. `tests/test_spans.py`: 3 passed
  (nesting, error emission without suppression, OTLP shape).
- funnel: round span (idea/weights/passes) + per-seed spans, exception-safe
  finally-close (survived a real refactor breakage mid-build, repaired).
- pyeval: run span + per-case spans (tokens/cost/judge split).
- Docs: TELEMETRY_HONESTY carries the mapping table; RECIPES row added.
- Research: OTel console/file exporter pattern (no collector needed) +
  Google BATS (budget-awareness in-context, dig-vs-pivot, analyze rollup)
  both confirm the shape; SDK declined on doctrine+disk grounds (stated).

## 3. self-review
Lane-build wall time NOT captured (subagent builds happen outside any span
I control — honest gap; suite times + validator events are). Token counts
remain provider-claimed where present, zero where unobservable. Shim is
schema-compatible, not wire-compatible, with real OTLP.

## 4. needs
Nothing new.

## 5. cost
$0, no manual actions.
