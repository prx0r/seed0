# METERING AUDIT — high-signal report (2026-09-10, live 429 run)

## Verdict in one line

The metering machinery works; there was nothing to meter. Two live attempts,
six blocked calls, $0.00 spend, both failures receipted. Everything below is
measured, not claimed.

## Per-question answers (with evidence)

**Tokens per run?** NO (live). Path: `pyeval.complete → extract_usage →
Meter`. Both attempts died at HTTP 429 before any usage block arrived, so
in=0/out=0. The meter recorded absence (zeros), never estimates. Stubbed
tests prove the path with nonzero numbers.
**$ per run given the model?** `$0.0 = cost_usd(mimo-v2.5, 0, 0)` — correct
arithmetic on empty inputs. Price table live (mimo 0.14/0.28, spark
0.10/0.20 per 1M). `metered_run` proven in tests (2.8e-05 example, both
pydantic + fallback paths). Judge-model second calls would merge into the
same meter with no per-case split (gap G1).
**Time in 0.000s?** Run-level YES (1.43s/1.39s) — but that is 429-wait time,
not inference. Per-case NO: result rows carry no time/tokens fields, so no
case is attributable (gap G2).
**Why?** (1) Provider 429: daily free-tier neuron allocation exhausted — the
exact constraint our model policy predicts; not our bug. Handling correct:
per-case fail-open, budget intact ($0.01 cap untouched), receipts banked.
(2) Design gaps G1 (per-case metering), G3 (no bounded retry — deliberate
fail-fast, queued as policy choice), G4 (no invoice reconciliation path),
G5 (subagent cognition unmetered), G6 (funnel Meter unfed for subprocesses).
Rate etiquette held: stopped after 2 attempts, no hammering.

## Git estate: done vs not-done (granular)

DONE (verified this turn): bundles/notes/refs/worktrees transport proofs;
freeze_run + lane_risk + keyed proposals + rollback + context + map +
branch-per-task + stoplight + receipts; test-exhaust purge (40 tournament
files + 1 receipt deleted); CLI-test CWD fix (pollution vector closed);
59/59 receipts verify; stoplight sweep 6 GO / 38 NOGO-grandfathered.
NOT DONE: H1b push (~180 files — blocks ALL downstream clone story);
S19–S23 (WIP checkpoints, branch protection, scoped recall, attempt schema,
pre-commit hooks); freeze/notes/bundles used only in tests, never a real
bout; learn.py never fired on real failures (all bouts all-green);
eval_arch + csec packs never on winners; assisted-eval + certificates
(endgame only); A-log coverage 6/44 DONE (pre-chain1 era grandfathered).

## Queued from this audit

G1 per-case time/tokens in pyeval results · G3 bounded-retry policy decision ·
G4 invoice-reconciliation path · M4 live re-run when quota clears (capped).
