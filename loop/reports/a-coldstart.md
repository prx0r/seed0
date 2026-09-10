# a-coldstart — progress report

## 1. claim
Cold-start simulation run: clone works for old tree, new machinery is
clone-invisible (158 uncommitted paths); staleness fixed (counts, FILES).

## 2. evidence
- Cloned to clean dir: old tree green (46 passed, 6/6), scaffold +
  tournament + receipts all work. `loop.py` ABSENT in clone (untracked) —
  naive agent cannot reach any loop/ham/grant/plane machinery.
- `seed0.py new` in clone does NOT git-init (feature uncommitted) — the gap
  stated precisely: deliverability == H1b push, nothing else.
- Uncommitted inventory: 158 paths incl. loop.py, ham.py, all of docs/* new
  files, all runs/ data, all new tests.
- Staleness fixed: RECIPES ~35→106, ROUTINES 71→106 (×2), FILES += policy,
  gitnotes. GUIDE 5/5 verified still true (plain check). Clone cleaned after.

## 3. self-review
Simulation ran with my knowledge of layout (not truly naive — a real naive
agent might stall earlier, e.g. at missing loop.py with a worse error).
Stated as upper bound on cold-start smoothness, not typical case.

## 4. needs
H1b (the entire fix). Nothing else unblocks clones.

## 5. cost
$0, no manual actions.
