# a-grants — progress report

## 1. claim
grants.py live: integer-cent grants, ceiling/purpose/expiry locks, receipt
gate, Treasury buckets, BATS-lite tiers; 5 tests green.

## 2. evidence
`tests/test_grants.py`: 5 passed — exact-amount lifecycle (60+40=100 → spent),
over-ceiling/purpose/proposed-state refusals, non-integer rejection, receipt
shape gate, treasury fail-closed (empty bucket, unknown bucket, cash
shortfall), tier selection. Ledger append-only (proposed/activated/spent/
revoked) with state() fold; WorkerKit lineage cited per function.

## 3. self-review
No on-chain settlement in tests (receipts are shape-checked, not chain-
verified — x402 facilitator does that live). activate() is a function call;
production wiring to inbox resolve is T-follow-up.

## 4. needs
M-run (live spend) stays queued. No new H/M.

## 5. cost
$0, no manual actions.
