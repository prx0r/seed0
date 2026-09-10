# a-b4escalation — progress report

## 1. claim
BATS escalation policy implemented + tested; live wiring deliberately held.

## 2. evidence
- `grants.escalate_tier(current, failed)`: hold on success, step up
  free→cheap→strong on failure, `escalate_human: True` at top+fail, unknown
  resets to free. 5-case test green.
- NOT wired into pyeval's loop: auto-escalation changes the spend profile,
  which is M-territory. Helper waits for explicit approval (stated).

## 3. self-review
Tiers are coarse (3 levels); uncertainty thresholds (0.7/0.01) uncalibrated
against real traffic. Fine for policy-shaped code awaiting data.

## 4. needs
M-approval to wire into live loop. Nothing else.

## 5. cost
$0, no manual actions.
