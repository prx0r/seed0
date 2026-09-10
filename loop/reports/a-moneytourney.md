# a-moneytourney — progress report

## 1. claim
Full money tournament on T0-through-idea1: 5/5 lanes exit 0 first try,
blind review, receipted; merit order stated openly, rank by luck as usual.

## 2. evidence
- Frozen pre-work: brief.md + context.md (P1–P6) + rubric.json + validate.py
  + weights.json (100/10/1). Baseline validator exit 1 on empty attempts.
- 5 isolated lanes, brief+context+rubric only: ALL exit 0 first try
  (10/8/8/7/6 tests). Independent re-run: 5/5 exit 0.
- score_attempt: 5/5 binary_pass, 5/5 compliance, all rubric hits.
- Blind review (seed2=A, seed5=B, seed3=C, seed1=D, seed4=E): all promote,
  verdicts from lane-visible fields only (new scores_blind file used).
- Tournament: seed3 #1 (evidence 3), seed5 #2 (2), rest 1 — evidence-luck
  again (kernel filenames), consistent with peer review, not new info.
- Merit order (OPEN judge read, not blind): seed1 (10 tests, dual disprover,
  thermal wedge) > seed5 (sharpest prediction format, dual condition) >
  seed4 (channel wedge + tripwire) > seed2 (dated Q2-2027) > seed3 (thinnest
  suite). Stated as judgment, not measurement.
- Receipts: funnel-round + tournament (sha256_e2b1…), both verify.

## 3. self-review
- Convergence red flag: 5/5 lanes chose EICR-landlord ("sparky/electrical"
  priming in brief + ecosystem). Same class as bout1 prompted-convergence.
  Next round MUST de-prime (withhold domain examples, blind prompts per
  METAPROCESS amendment).
- Strategies unexecuted in the world (no mystery shopping done, no calls) —
  predictions are structured, not validated. H-sparky pilot is where one dies
  or lives.
- a-context worked: P5 grounding check passed 5/5 (all lanes used lens
  vocabulary unprompted by the validator — required by brief, verified by code).

## 4. needs
H-sparky (kill or confirm one strategy in the world). Nothing else.

## 5. cost
$0 (5 subagent lanes inside session compute), no manual actions.

## 6. incident (caught live, fixed, mechanized)
Operator (me) mistranscribed the validation receipt id across tool calls —
TWICE — and `set-status DONE` accepted the corrupted string (non-empty
check). Caught on file-existence check before close. Fix: DONE transitions
now require `validation_ref` to resolve to a real receipt file
(`test_done_requires_resolvable_receipt`). Lesson: validators must check
references resolve, not merely exist as strings.
