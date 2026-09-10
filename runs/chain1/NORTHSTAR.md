# NORTHSTAR chain1 (frozen 2026-09-10 — amend by new file version only)

Close the full autonomous chain on seed0, then run it without supervision:

1. Amend seeds from results with logged justifications (seed1 → 1.1 now;
   every change cites the parent finding + re-verifies).
2. All work on git attempt branches (`tourn/chain1/<name>`); merge results
   as data to main; delete branches after merge (GIT_ARCHITECTURE law).
3. Every A-task keeps an A-log (`loop/a-logs/<id>.jsonl`, entries tag which
   acceptance indices they cover); `loop.py stoplight <id>` matches A-log to
   A-task and says GO (all acceptance covered + receipt) or NOGO + missing.
4. Re-run the tournament with the amended seed; log justifications; receipts.
5. Emit a peer-review packet: one A-report per A-task + validation evidence
   table. Reviewer hunts hallucinations; send-backs re-enter as tasks until
   every item is GO.

Stop rule: all chain A-tasks GO and packet banked. T0 (make me money) governs
priority throughout; spend stays $0 (no live calls this chain).
