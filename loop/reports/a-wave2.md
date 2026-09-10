# a-wave2 — progress report

## 1. claim
Wave 2 closed: 8 fixes from F1–F8 findings, all tested; learn.py fired on
real bout data for the first time.

## 2. evidence (per fix)
- F1 shlex agent_cmd (quoted commands work; plain ones split identically).
- F2 tournament --out DIR (jsonl redirect; tmp-proven, repo stays clean).
- F3 install-hooks --with-push (pre-push gate; roundtrip tested).
- F4 ham policy command (learned advice; risky action → checkin p=1.0).
- F5 learn.py on meta-tourney: 2 failures → 1 criteria0-rule proposal
  (FIRST real firing; bout1 had zero failures to learn from).
- F6 tie-break rule in TOURNAMENTS verdict rules.
- F7 judge_in/judge_out separated in pyeval rows + receipts.
- F8 runs.verify_all: 75/75 ledger-valid (CLI included).
- Bonus find: ham parser ate boolean flags (`--security` needed a value);
  BOOLS set added.
- learn.py bout1 re-check: 0 failures → 0 proposals (correct silence, kept).

## 3. self-review
Wave-2 tests are CLI/subprocess-heavy (slower suite: ~20s). learn.py's first
real proposal (compliance:4/5 on variant lanes) is unsurprising — variants
aren't kernels; the machinery working matters more than the content.

## 4. needs
Nothing new (queues unchanged).

## 5. cost
$0, no manual actions.
