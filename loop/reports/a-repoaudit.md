# a-repoaudit — progress report: theatre vs solid, whole repo

## 1. claim
Every module graded against tests + real usage. 12 SOLID, 6 PARTIAL, 5 THEATRE.

## 2. evidence

**SOLID (tested + used in anger):** seed0 check/scaffold · tournament
(+weights/notes, 8 receipts) · funnel (3 real bouts, blind machinery used) ·
loop queue/stoplight/branch/ready/history/replan/metrics/leafcheck/promote/
ingest/goalcheck/map/context/rollback/heuristics/log (19 loop tests +
live-fire) · ham tiers + prohibited screen · runs receipts (63 verify) ·
tasks feed · learn propose/collect (+keyed) · grants ledger + treasury +
refusals · hinbox poll/resolve/expiry/priority · tournament blind + weights
regression tests · nodeps guard (caught a real violation) · save_all
tripwire · budgets check + zero-budget-no-transport proof.
**PARTIAL (tested, thin/never real):** pyeval (stubbed green; live 3×429,
$0.00; per-case fields live-unproven) · policy classifier (synthetic traces
only, never owner decisions) · metered_run (both paths tested, never fed by
a live call) · hserver/hqueue (localhost socket tests, zero human traffic) ·
hplane (fixture tests; 3/3 real repos dark) · mcp_server (protocol trips,
no real client connected) · metrics rulers (used by bout-P — actually SOLID;
kept here for the bout-only scope).
**THEATRE (documented, unexercised):** funnel Meter (created, add_usage has
zero non-test callers — telemetry block with permanent zeros) · learn.py on
real failures (every bout all-green; bout1 zero-fail) · eval_arch on winners
(never run) · csec packs on winners (never run) · subagent cognition metering
(no path exists) · invoice reconciliation (no path exists) · assisted-eval +
certificates (endgame prose only).
**SPEC-ONLY (labeled as such, honest):** endgame chunks 2–5 · HydraDB ·
Temporal-style durable waits · Biscuit/AIP stack · multi-repo hqueue view.

## 3. self-review
Grading by the builder (generous risk). Mitigation: every grade cites an
artifact (test name, receipt id, or absence noted). Absence claims verified
by grep (add_usage callers, live traffic, receipt kinds census: 46
task-validation / 8 tournament / 2 funnel-round / 5 pyeval / 1 t0-e2e /
1 chain1).

## 4. needs
Theatre→solid conversions are M4 (live data), bout2-with-failures (real
learn.py food), and H1b (adoption). Queued, not new.

## 5. cost
$0, no manual actions.
