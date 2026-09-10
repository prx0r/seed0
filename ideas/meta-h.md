# idea2meta — tournament hypotheses for H/A/M machinery (frozen 2026-09-10)

Status: under test this session. Competing interpretations welcome — log them
in ideas/idea1.reviews.md style append-only notes, never by editing this file.

## Problem

H/A/M mechanisms (unlock priority, idempotent filing) were built on reasoning
and unit tests, never pitted against rival implementations under frozen
conditions. Reasoning is not evidence: a simpler mechanism could match them,
and complexity without measured gain is theatre (METAPROCESS popcorn rule).

## Mechanism

Two bouts, each with a frozen fixture, two rival lane implementations, a
mechanical metric, and a preregistered threshold. Lanes are built by the
agent, scored by code, reviewed blind. Bout P (priority): direct-count
ranking vs transitive-BFS ranking on a fixture H-queue with a constructed
ground-truth order, filed in adversarial order (decoy first). Bout I
(idempotency): naive append vs idempotency-key filing under a 5x retry storm.
Metrics are order distance (footrule) and record counts — no LLM judgment
anywhere in scoring. A shared `metrics()` helper computes both so the ruler
is identical across lanes. Tournament ranks lane implementations; hypothesis
verdicts come from preregistered thresholds, not ranks.

## Falsifiable predictions

- [ ] H1: transitive total footrule distance to ground truth across both filing orders is strictly less than direct total distance, and transitive order is filing-order-invariant.
- [ ] H2: naive record count after storm equals 5 while keyed count equals 1.
- [ ] H0 (validity): every lane passes the bout validator (exit 0) and every receipt verifies; a red lane invalidates the bout, not the hypothesis.

## Non-goals

Not a test of seed quality, model quality, or revenue. Not a beauty contest:
settled by integers. Avatar/gamification layers wait until measurement is
luck-free (flow-test verdict).

## Verification plan

Run `runs/meta-tourney/bout-P/validate.py` and `bout-I/validate.py` (exit 0 =
thresholds met, prints distances/counts). Re-run from clean checkout for
independence. Receipts in runs/ verify via runs.verify_file.
