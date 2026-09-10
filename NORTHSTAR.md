# NORTHSTAR — the impenetrable flow (frozen 2026-09-10; amend by version only)

## The flow, exactly

1. **INGEST.** A big spec (1000 lines, any origin) lands via
   `loop.py ingest --as ingest1 --file spec.md` (or stdin). Stored byte-
   identical under `loop/ingests/` with content-hash dedup. Output: id +
   section headers (`##`) available for citation. Cost: $0.
2. **RESTATED GOAL.** The agent restates ingest1 as a-goal 1: end-state +
   acceptance where EVERY item cites its spec section (`[spec:Section]`).
   `loop.py goalcheck` verifies each citation resolves — invented
   requirements die here, mechanically. No human approval needed to restate;
   the trace IS the approval.
3. **BINARY BRANCH.** Goal decomposes to A-tasks (`blocked_by` DAG); each
   EXECUTING task gets branch `tasks/<id>` (merge FF + delete after DONE).
   Commit queue state before every switch (split-brain refusal is the
   control plane working, not a bug).
4. **AUTONOMOUS WORK.** Tournaments (rival lanes, frozen brief/rubric/
   validators, blind review) + iterations (max 3 validator tries, replan
   breaker at 3 → H). A-logs tag covered acceptance indices with
   re-executable evidence (`--evidence command:/file:`).
5. **VALIDATOR STOP.** `loop.py stoplight` re-runs every evidence claim;
   GO iff all acceptance covered + report exists + receipt set. The LLM's
   only moves: read NOGO reasons, run something likely to pass. DONE needs
   report + receipt. No receipt, no DONE — forever, no exceptions.

## Why impenetrable (each wall is code, not policy)

| Wall | Enforcer | Cheat attempted | Outcome |
|---|---|---|---|
| Invented requirements | `goalcheck` section resolution | acceptance without `[spec:]` | rejected with missing section |
| Grading own homework | builders ≠ re-runner (validator re-run by operator) | lane asserts its own win | verdicts from preregistered thresholds only |
| Silent scope creep | frozen brief/rubric/validator (idea0/criteria0) | mid-bout edits | baseline calibration fails |
| Claimed-but-unrun evidence | stoplight re-executes `command:`/`file:` | tagged covers without proof | NOGO naming the exact line |
| Infinite loops | max 3 tries, replan breaker at 3 → H | retry forever | escalated with reason log |
| Lost history | content-hashed receipts + git branches | "trust me" | verify fails loudly |
| Asking instead of working | no-questions rule + dryness proof | ending with a question | spec violation, logged |

## Standing parameters

- T0 (make me money) governs priority; spend $0 unless an M-grant exists.
- Tiers H/A/M + promotion path (HAM_DELEGATION). Prohibited list absolute.
- This file changes by versioned amendment only; the flow changes by tested
  code + receipts, never by chat agreement.
