# AGENTS.md — seed3/evidence-maximalist

Binding rules. Philosophy: no claim without a chained receipt.

## Absolute rules

1. **Every action appends evidence.** Code change, test run, decision, external
   call — each is a hash-chained JSONL record (`evidence.py`). If it isn't in the
   log, it didn't happen.
2. **Chain verifies or work stops.** `evidence.verify()` must pass before any
   report, merge, or claim. A broken chain means tampering or corruption — halt.
3. **Receipts over prose.** Status updates quote record digests, not adjectives.
   "Done" means a `done` record exists with passing gate output attached.
4. **Honesty bounds.** Records are tamper-evident, not tamper-proof; digests are
   sha256 of canonical JSON. Exit codes never masked.

## Where things are

`evidence.py` (append + verify) · `evidence/` (run logs) · `docs/` index, recipes,
files, threads · `tests/` (chain + tamper tests).
