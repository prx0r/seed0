# a-hqueue2 — progress report

## 1. claim
hserver serves the cross-repo funnel: `/api/h/funnel[?repos=]` ranked rows.

## 2. evidence
`hserver.api_funnel` delegates to hplane rank/collect with `?repos=` override
(defaults to plane/repos.txt). Test spins live socket against fixture repos:
open record + dark repo returned, dark ranks top. 2 hserver tests green.

## 3. self-review
UI page still single-repo (pending endpoint); funnel JSON is API-only until
hqueue.html gains a multi-repo view (proposed, unscheduled). Default repos
file lists 3 paths that may not exist on other boxes (documented constraint).

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
