# a-promote — progress report

## 1. claim
A→H promotion path live: H-tasks promote from blocked A-tasks with enforced
lowest-barrier form; direct filing grandfathered and deprioritized.

## 2. evidence
- `hinbox.new_request` gains `from_task`/`exact_steps`/`send_back` +
  computed `promoted` flag (backward compatible: old callers unaffected,
  20 hinbox+hserver tests still green).
- `loop.py promote` refuses without `--steps-json` + `--send-back` (tested),
  creates linked H-record, pauses task with `need` id, prints the human block
  (summary + numbered steps + SEND BACK).
- HAM_DELEGATION (tiers table + Promotion §) + META_LOOP §3 updated to the
  only-legal-path rule.

## 3. self-review
Pre-rule H-records (6 live, incl. H1b/H-driver) lack linkage — exempt by
documented rule, but the two revenue H-items predate the form (exact steps
live in TRIAGE/packet, not in-record). Backfill would rewrite history;
leaving as-is per append-only law. New promotions comply from now.

## 4. needs
None. Queues unchanged (promotion path unused by live items yet — correct,
nothing newly blocked).

## 5. cost
$0, no manual actions.
