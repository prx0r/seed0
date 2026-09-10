# AGENTS.md — seed1/ralph-minimal

Binding rules. Philosophy: the loop is trivial; the gate does the work.

## Absolute rules

1. **One task per run.** Read the next unchecked item in plan.md, do only that,
   verify, mark done, stop. Never batch tasks; context is killed between runs.
2. **Fresh eyes each run.** Assume nothing from last run except plan.md state.
   Re-read the task; re-verify from scratch.
3. **Verify before mark-done.** `pytest` (or the plan's stated gate) must pass.
   A task marked done without a green gate is a lie — the loop replays it.
4. **Small diffs.** If a task needs more than ~100 lines, split the plan first.
5. **Honesty bounds.** Exit codes never masked; mocks prove wiring never quality;
   no live claims without a live run.

## Where things are

`ralph.py` (the loop) · `plan.md` (the state) · `docs/RECIPES.md` (operations) ·
`tests/` (loop + plan tests). See `docs/FILES.md`.
