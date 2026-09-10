# SPEC — example contract: this seed's own gate (replace per project)

## Goal
The spec gate catches toothless criteria.

## Non-goals
Example: judging whether criteria are wise, only whether they're verifiable.

## Acceptance criteria
| ID | Statement | Verification | Owner |
|---|---|---|---|
| AC-1 | Missing owners fail the gate | test `test_missing_owner_and_method_fail` | human |
| AC-2 | Dangling test refs fail the gate | test `test_dangling_test_reference_fails` | human |
| AC-3 | Demo runs end-to-end | demo `scripts/demo.sh` expects `Hello, Jo` | human |
