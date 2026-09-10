# AGENTS.md — seed4/lanes

Binding rules. Philosophy: parallel agents never collide because lanes say who
owns what, and worktrees keep their hands apart.

## Absolute rules

1. **One lane per agent.** Claim your lane in LANES.md before touching code.
   Unclaimed work belongs to no one — file a lane proposal first.
2. **Lane owns its paths.** `scripts/lane_check.py` enforces ownership: a diff
   touching another lane's paths without a joint thread is rejected.
3. **One worktree per lane.** `scripts/new-lane.sh <name>` — never two agents on
   one checkout. Merge through the lane owner, never around them.
4. **Joint threads for seams.** Anything crossing lanes gets a THREADS.md entry
   naming both owners before implementation.
5. **Honesty bounds.** Exit codes never masked; ownership claims verified by the
   checker, not by announcement.

## Where things are

`LANES.md` (ownership table) · `scripts/lane_check.py` (enforcer) ·
`scripts/new-lane.sh` (worktree spawner) · `docs/` · `tests/`.
