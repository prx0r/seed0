# a-peerreview — full analytics (10-todo peer review of meta + flow tournaments)

## 1. Evidence table (all re-run live this review)

| Bout | Metric | Predicted | Actual | Verdict |
|---|---|---|---|---|
| P | transitive_total | 0 | 0 ([A,B]x2) | HOLD |
| P | direct_total | 2 | 2 ([B,A],[A,B]) | HOLD (as predicted: order-luck) |
| P | invariance | true | true | HOLD |
| I | naive_count | 5 | 5 | HOLD |
| I | keyed_unique/lines | 1/1 | 1/1 | HOLD |
| flow | lanes validator exit 0 | 3/3 | 3/3 first try | HOLD |
| flow | tournament rank | merit | luck (see §3) | DIVERGE → fixed process, not score |
| all | receipts verify | all | 28/28 True | HOLD |

## 2. Per-hypothesis analytics

- **H1**: exact predicted integers (0v2). Mechanism visible in orders: direct
  copies filing order (ties broken by position = arbitrary), transitive
  ignores it. Micro-fixture; proves machinery + direction, not generality.
- **H2**: exact predicted integers (5v1/1). Note: keyed lane reuses shipped
  hinbox (tests the pattern in situ, not a fresh implementation — stated).
- **H0**: all lanes exit-0 + suites green + receipts verify. One wobble:
  transitive lane test initially failed on unspecified tie semantics (test
  bug, not code bug — fixed to DONE-vs-live contrast).

## 3. Theater vs signal, per metric

- **Footrule distances (0v2)**: SIGNAL. Pre-registered, integer, replicated
  across refactors (shared ruler import preserved the numbers exactly).
- **Storm counts (5v1)**: SIGNAL (mechanical, no judgment).
- **Tournament rank, flow bout (seed3>seed5>seed1)**: THEATER. Proven luck:
  evidence glob matched kernel filenames (evidence.py/test_evidence.py in
  seed3, run_packs.py in seed5) + 1 bout file each. Rank = pre-existing
  filenames, not merit. (Known-gameable flag in AGENTS.md now has a case file.)
- **Tournament rank, meta lanes (4-way tie)**: NOISE. All green+4/5, order by
  elapsed_s jitter. Logged as-is per verdict rules.
- **elapsed_s**: SIGNAL as cost proxy at scale, THEATER as ranker (±20%
  run-to-run jitter measured: 0.20/0.24/0.20s same suite).
- **model labels** (mock/variant/lane-task): THEATER (echoed flags, zero info).
- **compliance 4/5 lanes**: SIGNAL of honesty (checker refuses to flatter
  non-kernels — bout1 precedent holds).
- **Flow-test blindness**: PARTIAL-THEATER. Labels hidden but scores.jsonl
  exposed names+counts and my verdicts cited counts mappable through it.
  Fixed: `scores_blind_rN.jsonl` (lane+binary_pass only) + judge rule in
  TOURNAMENTS.md + regression test. Prior verdicts stand (all-promote,
  metric-independent) — stated, not rewritten.

## 4. Divergences → changes (with tiers)

1. Blind leak → blinded scores view + judge rule (A, DONE this review).
2. Evidence-luck ranking → documented, no code change (luck can't be patched,
   only disclaimed; metric-threshold verdicts already bypass rank).
3. Suite-time jitter → elapsed_s demoted to cost-proxy in docs (A, noted in
   metaguide failure log; no code change).
4. Lane tests asserting unspecified semantics → tie-semantics-in-brief rule
   (A, in metaguide).
5. Orphan receipt from crashed run → kept, content-matched (process precedent).

## 5. Cost

$0, no manual actions. 10/10 todos complete.
