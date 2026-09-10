# a-stealgit — progress report

## 1. claim
Git-layer steals live: notes, keyed proposals, freeze commits, rollback.

## 2. evidence
- `gitnotes.py` (attach/read/tag) + `tournament.py --notes` + CLI test in tmp
  repo (note round-trips, top recorded). Best-effort: never fails runs.
- `learn.py --keyed`: per-signature files + index; rerun byte-identical
  (dedupe by construction = S26 + S32 in one mechanism).
- `funnel.freeze_run`: brief+rubric+validator+weights committed; later edits
  can't rewrite the freeze (test proves frozen copy immune).
- `loop.py rollback`: restores queue+registries to a sha; refuses dirty
  workdir without --force (tested both directions).

## 3. self-review
Notes need explicit refspecs to travel (documented in CONTROL_PLANE, not
automated — fetch config is per-box manual work). Rollback restores only the
3 known registry paths (custom paths silently skipped — stated).

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
