# a-agentrun — progress report

## 1. claim
Per-agent measurement is real: external timing + usage capture + budget,
proven on 5 live stub agents; strict guide banked.

## 2. evidence
- `agentrun.py`: monotonic external stopwatch, timeout kill, usage-file
  parsing (nested shapes), three-valued honesty
  (provider-reported/no-inference/unknown), timed receipts. 4 tests green
  (timing accuracy ±, kill proof, shape parsing, failure recording).
- Live proof: 5 lanes measured 0.232/0.435/0.634/0.839/1.032s against
  programmed 0.2s steps — order correct, total 3.17 agent-seconds, all
  no-inference $0.0.
- Hermes `--usage-file` found as the real token channel (probed, not run —
  quota out). opencode `--format json` noted unverified.
- `docs/STRICT_GUIDE.md`: measurement/money/work rules + banned list.
- Gold-star message saved verbatim at `loop/ingests/og-hermes5.md`.

## 3. self-review
Stub proof validates TIMING only; token path validated by parser tests +
  stubbed pyeval, never a live provider block (quota). Hermes agents NOT
  launched (would 429-burn 45 min × 5 — staged as runs/hermes-music with
  quota gate instead). Task-tool subagent tokens remain unmeasurable —
  stated, routed around via subprocess agents.

## 4. needs
Quota clearing (or paid key) to fire the staged Hermes run. Nothing else.

## 5. cost
$0, no manual actions.
