# a-hinbox — progress report

## 1. claim
hinbox.py live: idempotent filing, resolve-once, expiry, transitive unlock priority; 5 tests green.

## 2. evidence
`tests/test_hinbox.py`: 5 passed. Priority pinned: unlock-b (transitive c)
scores 3.5 > unlock-d 1.5; DONE nodes score 0 direct but still route through
dependents. Defaults-None fix: module-level `path=HREG` defaults bound at def
time broke monkeypatching — now resolved at call time (2 real bugs found by
own tests during build).

## 3. self-review
Urgency weight (0.5x) is arbitrary, uncalibrated. Value proxy (1+len(acceptance))
is a stand-in for real task value. Both flagged for calibration once real
H-traffic exists.

## 4. needs
None. No H/M discovered.

## 5. cost
$0, no manual actions.
