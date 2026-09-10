# ECOSYSTEM — where seed0 sits among the factory builders (reviewed 2026-09-10)

Cloned + read: `github/gh-aw` (643 workflows), `gastownhall/gascity` (beads/orders/
formulas), `Hona/opencode-ralph` (trivial loop), `actual-software/sf-tutorial`.
Assessed from research (too big to clone on this box): Paperclip, Open SWE, herdr,
OpenHands, Invoker, Soren. Clones in /tmp are research copies (.git stripped).

## The single most important finding
**Do not build orchestration; seed0 already occupies the correct layer.** The field
splits into substrates (run workers: Ralph loops, Gas City fleets, gh-aw Actions,
herdr sessions) and shapes (what "a finished project" means + how to score one).
Every substrate vendor converges on needing: a compliance gate, an evidence log, a
bake-off harness. That is seed0's tournament.py + checker + tasks.py. seed0 stays
substrate-agnostic: score Ralph-built and Gas-City-built seeds identically
(`substrate` is now a leaderboard field — compare substrates, don't marry one).

## Steals (concrete, mapped)
- gh-aw "bounded improvement + verification gate + draft PR" → tournament run shape;
  their deterministic-vs-LLM split mirrors our kernel/guard doctrine. Mine their 643
  workflows for maintenance-pack ideas (docs/lint/security/test loops).
- Gas City beads (id/title/status/parent/Needs/labels) → tasks.py already isomorphic
  (blocked_by = Needs, runnable_only = Ready). No change needed; cite it.
- herdr WORKING/BLOCKED/IDLE → covered by open/predicted/done + agent_tasks filter.
- Ralph → the lower bound that disciplines us: seed0's own loop (check + suite) must
  stay trivially runnable. It is (stdlib-only, seconds).
- Paperclip layer (goals/budgets above workers) → HUMAN_LOOP.md autonomy ladder +
  task cost fields are the thin version; do NOT build company-management.
- HumanLayer/CodeLayer UX (worktrees, diff review, ticket→task) → tournament seeds
  should each build in isolated worktrees; add when running real tournaments.

## Explicit non-builds (validated by this review)
No fleet controller, no sandbox infra (Daytona/E2B territory), no company/governance
layer, no agent framework (CrewAI et al. solve a problem we don't have — we already
have the agent). seed0 = shape + compliance + tournament + task feeds. Everything
else is someone else's maintained substrate.
