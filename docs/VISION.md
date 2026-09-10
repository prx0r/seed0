# VISION — the one-page mental model

> **One idea in. Five seeds compete. Binary rubrics decide. Failures become
> criteria. The system converges on what works — with receipts for all of it.**

```
idea ──► [seed1..seed5] ──► funnel ──► scores ──► review ──► amend ──► repeat
              │                │           │           │          │
         isolated         binary pass   hypotheses   VERSION   converge on
         attempts         mechanical    logged       bumps     canonical seed0
              │                │           │                     ▲
              └──── telemetry (time/tokens/cost/model) ─────────┘
                           │              │
                      learn.py ──► criteria1.1 proposals ──► criteria0 lessons
```

## The three loops

| Loop | Question it answers | Proof artifact |
|---|---|---|
| Tournament | which seed wins this idea? | leaderboard + receipt |
| Funnel | did isolated agents pass the rubric? | scores.jsonl + review record |
| Learn | what do shared failures teach? | CR-1.1-N proposals + lessons |

## The five seeds (what each believes)

| Seed | Belief | Fails when |
|---|---|---|
| seed1 ralph-minimal | the loop is trivial; the gate does the work | plans are wrong (faithful wrongness) |
| seed2 spec-first | no code before verifiable contract | specs cost more than the build |
| seed3 evidence-maximalist | no claim without chained receipt | audit overhead exceeds value |
| seed4 lanes | parallel agents need ownership, not meetings | coordination cost < collision cost |
| seed5 red-team-first | the model is never trusted | threats are imaginary |

## Honesty bounds (read before believing any output)

- Mocks prove wiring, never quality. Simulated numbers are labeled.
- A HELD verdict means "this probe, this config, today" — not "secure".
- Tournament ranks only what it measures: compliance, suite, evidence.
  Cost/latency/quality beyond that need pyeval rows and live keys.
- Leaderboard ties break on evidence count — visible, gameable, flagged.
- Fresh-agent isolation is by directory copy (seed + brief + rubric only).
  It defeats casual leakage, not exfiltration by a motivated agent.
