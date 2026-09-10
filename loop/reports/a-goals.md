# a-goals — progress report

## 1. claim
a-goal machinery live: ready/branch/history commands + full chain fired
end-to-end (3/3 DONE, merged, deleted, base_rate 1.0).

## 2. evidence
- `loop.py ready`: blocked_by gating proven (bbb absent until aaa DONE).
- `loop.py branch`: creates `tasks/<id>` from main, resumes existing,
  records branch field; tested in scratch git repo.
- `loop.py history`: counts + base_rate_done + median hours from A-log ts.
- Live fire (/tmp/goaldemo, since cleaned): g1→g2→g3 dependency order
  enforced by ready; each branched, executed, logged, stoplight-GO, DONE,
  FF-merged, branch deleted. Final: 3 DONE, zero leftover branches.
- Friction found live: queue-state vs branch switching (dirty queue blocks
  checkout) → queue-state commit rule, now in GOALS.md. First attempt failed
  loudly; second with rule passed clean.

## 3. self-review
Monte Carlo correctly refused (spec §3: base rates + clusters, no tree
search). Demo chain is synthetic (file writes) — proves the MACHINERY
(ordering, branching, gating, memory), not task intelligence. Median hours
null on fast demos (sub-second spans) — honest null, not zero.

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
