# seed0 THESIS — the encoded way of working (vision, not built)

## One line
Point an agent at seed0 plus a project idea, and it has everything it needs to
operate autonomously: how to start, how to build, how to verify, and when to
stop and ask a human.

## The problem it solves
Every autonomous coding run currently starts from tribal knowledge: which files
matter, what "done" means, how this org tests, what must never be done. That
knowledge lives in chat history and dies there. seed0 encodes it once — laws,
layout, runbook, done-definition — so any agent, on any box, on any idea,
produces the same shape of output: working code, honest tests, runnable docs,
evidence logs.

## How it works (intended)
1. Human supplies an IDEA (a paragraph or a tech spec) and points at seed0.
2. Agent scaffolds (`seed0.py new`) → canonical layout with laws pre-installed.
3. Agent builds in loops, each gated by `seed0.py check` + the repo's own suite.
4. Agent reports back ONLY at defined checkpoints (see HUMAN_LOOP.md); everything
   else it decides, attempts, verifies, or rolls back itself.
5. A finished project is indistinguishable regardless of which agent built it:
   same layout, same runbook shape, same evidence discipline. Portfolios compose.

## Why this compounds
- Each project built under seed0 feeds patterns BACK into seed0 (templates harden,
  checker rules grow from real failures, recipes accumulate).
- The checker is the moat: "compliant" becomes a machine-verifiable property of a
  codebase, not an opinion. CI gates on it; humans review deltas, not everything.
- Multi-agent safe: lanes, ownership, and thread registries are part of the shape,
  so parallel agents (or two boxes, like ours) don't collide.

## Explicitly not
Not a framework, not a runtime, not a model, not an orchestrator. No daemons, no
control plane. seed0 is a dormitory, not a foreman: it houses the work correctly
and inspects it on exit. Orchestration (who runs which agent when) lives elsewhere.
