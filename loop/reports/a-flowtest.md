# a-flowtest — progress report

## 1. claim
Prompt-pattern flow tested live in seeds: 3 isolated lanes, all validator-clean
first try, blind review, preregistered-weight tournament, receipts banked.

## 2. evidence
- Frozen: runs/flow-test/brief.md + rubric.json + validate.py (written BEFORE
  lanes launched; baseline validator exit=1 on empty attempts).
- 3 parallel lanes (seed1/3/5, brief+rubric only, no cross-reads): all exit 0
  first try (7/7/6 tests). Independent re-run by me: 3x exit 0.
- score_attempt: 3x binary_pass=True, 5/5 compliance, all rubric hits.
- Blind review: verdicts written to lanes (seed3=A, seed1=B, seed5=C revealed
  after) — all promote; shared gap: input validation (all 3 self-reviews agree).
- Tournament (weights 100/10/1 preregistered): seed3 #1, seed5 #2, seed1 #3 —
  ALL green+compliant, rank decided purely by evidence filename count.
- Caught live: tournament.py scored `--weights` VALUE as a 4th seed (receipt
  sha256_ad68… carries the bogus row); fixed flag-skip + regression test;
  clean re-run receipted (sha256_a7ae…).
- Funnel receipt sha256:0d8e… + tournament receipts verify.

## 3. self-review
Thin brief → thin convergence (all lanes same gap; rubric didn't demand
validation). Evidence-count tiebreak ranked perfect scorers by filename luck
(known-gameable, AGENTS.md-flagged). 3 lanes, 1 micro-task: machinery proven,
not seed quality. /bitt /fleece + Chris basket are the other agent's domain —
untouched here by design.

## 4. needs
None new. Flow verdict delivered in chat (freeze+validator+bounded loops hold;
add independent re-run + prereg weights + blind judging; avatars last).

## 5. cost
$0 (3 subagent lanes inside session compute), no manual actions.
