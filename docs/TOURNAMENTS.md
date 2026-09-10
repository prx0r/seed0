# TOURNAMENTS — metaguide: how an agent decides what to test, and how to keep it honest

## Why tournaments (not reviews, not vibes)

A tournament answers one question with integers: **which implementation wins
under frozen conditions?** Reviews produce prose; prose doesn't falsify.
Hypotheses live in `ideas/` (idea0-enforced falsifiable predictions);
the bar lives in `criteria/` (criteria0-enforced binary rows); lanes
compete; code scores; receipts prove. Worked example: `runs/meta-tourney/`
(H1 transitive priority 0 vs 2; H2 keyed 1 vs naive 5).

## Exact schemas (every bout carries all six — no exceptions)

| # | Artifact | Path pattern | Frozen | Example |
|---|---|---|---|---|
| 1 | Brief (northstar) | `<run>/brief.md` | BEFORE lanes | micro-ledger contract |
| 2 | Rubric (binary) | `<run>/rubric.json` | BEFORE lanes | `{"checks":[{id,type:path|contains|suite_green}]}` |
| 3 | Validator (exit 0/1 + JSON) | `<run>/validate.py` or per-bout | BEFORE lanes | footrule thresholds, storm counts |
| 4 | Weights (preregistered) | `<run>/weights.json` | BEFORE scoring | `{"tests_green":100,"compliant":10,"evidence":1}` |
| 5 | Scores + blind review | `<run>/scores.jsonl`, `scores_blind_r1.jsonl`, `review_r1_blind.json`, `sealed_map_r1.json` | during | verdicts before identities, judges read ONLY the blind files |
| 6 | Receipts | `runs/sha256_*.json` | after | funnel-round + tournament |

Lanes: isolated dirs (seed + brief + rubric only, no cross-reads). Builders
run the validator themselves (max 3 tries); the operator RE-RUNS every
validator independently — builders never grade their own homework.

## Verdict rules (what counts as winning)

- Hypothesis verdicts come from **preregistered metric thresholds** (C2/C3
  pattern), never from tournament rank. Rank is the mechanical log.
- `binary_pass` (funnel) means suite green + compliant + all rubric hits.
- Bout lanes are variants, not kernels: 4/5 compliance is expected and
  reported, never flattered (bout1 precedent). Lane validity = validator
  exit 0 + suite green.
- Red lane invalidates its bout (C7), never the hypothesis. Shared weakness
  across passing lanes becomes a next-round rubric row, not a failure.
- Avatars/gamification only after measurement is luck-free (evidence-count
  tiebreaks are filename luck — costume on noise is theatre).
- Judges cite ONLY lane-visible fields (lane, binary_pass, metric).
  `scores.jsonl` carries seed names AND test counts ("7 passed") — judging
  from it voids blindness even with lane labels hidden (caught live in
  flow-test peer review: verdicts cited counts mappable via scores).
  Use `scores_blind_r<N>.jsonl` (lane + binary_pass, nothing else).

## Shared rulers (`metrics.py` — import, never reimplement)

`footrule`, `rank_distance`, `storm_counts`. Tested before measuring
(`tests/test_metrics.py`). Rationale (cg doctrine): the ruler is
infrastructure; private math per lane is self-grading.

## Runbook (copy-paste)

```bash
# 1. freeze
printf '...' > runs/<bout>/brief.md   # + rubric.json + validate.py + weights.json
python3 runs/<bout>/validate.py <empty-dir>; echo $?  # expect 1 (calibration)
# 2. lanes (isolated builders, max 3 validator tries each)
# 3. operator re-runs every validator + scores
python3 -c "from funnel import score_attempt; ..."
python3 funnel.py review --run runs/<bout> --round 1 --blind   # verdicts first
python3 funnel.py reveal --run runs/<bout> --round 1           # identities after
python3 tournament.py <lane-dirs> --model <label> --weights runs/<bout>/weights.json
# 4. receipts verify; packet + THREADS updated
```

## Failure log (this guide was debugged by its own bouts)

- Validator `main(argv)` signature slip (caught at baseline calibration).
- `sys.modules` caching across lane imports (del before reimport).
- `parents[N]` off-by-ones ×2 (count from the file, not the project).
- Tournament scoring its own `--weights` value as a seed (flag-skip fix +
  regression test; bogus row preserved in receipt history).
- Transitive test asserting against unspecified tie semantics (rewrote to
  DONE-vs-live contrast). Tie semantics belong in the brief, not the test.
- Blind leak via scores.jsonl (names + counts visible to judge; lane labels
  alone don't blind). Fix: `scores_blind_rN.jsonl` + judge rule above.
- Transposed receipt id accepted by non-empty check (operator typo, twice).
  Fix: DONE transitions resolve `validation_ref` to a real file.
