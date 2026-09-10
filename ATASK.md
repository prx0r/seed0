# ATASK.md — the A-task native contract (portable, one page)

Paste this file (or its 5 rules) into ANY agent's instructions — opencode,
Claude Code, Hermes, Codex, cron job, other VPS. No dependencies, no daemon.
The queue is files; the audit is `acheck.py`. If the agent follows this,
it is A-task native and your life gets easier: one shape everywhere, one
dashboard over all boxes, one press language.

## The 5 rules

1. **The queue is truth.** `tasks.jsonl` (one JSON record per line) holds all
   work. Read open tasks at turn start. Never invent work outside the queue —
   propose it as PROPOSED first.
2. **Execute lowest-blocked.** READY = status in (JUSTIFIED, EXECUTING) AND
   every `blocked_by` id is DONE. Work ready tasks; blocked tasks wait.
   Parallel where independent.
3. **Log every action.** Append a-log lines as you go (`a-logs/<id>.jsonl`):
   what you did, what it covers, where the evidence is. No log, no claim.
4. **DONE needs proof.** Status DONE requires a report file + a validation
   receipt the checker can re-run. No receipt, no DONE — forever.
5. **Blocked on human/money → file, never guess.** Write an H/M record with
   exactly what you need from whom, park the lane, keep working the rest.
   Irreversible/external/spend steps are H/M by definition.

## Record shape (required keys)

```json
{"id": "a-slug", "tier": "A", "summary": "what done looks like",
 "acceptance": ["checkable end-state 1"],
 "evidence_required": [{"kind": "command", "spec": "pytest tests/ -q"}],
 "blocked_by": [], "status": "PROPOSED",
 "report_ref": "reports/a-slug.md", "validation_ref": "runs/sha256….json"}
```

Lifecycle: `PROPOSED → JUSTIFIED → EXECUTING → REPORTED → DONE`
(`PAUSED` = H/M need found mid-task, need id cited; `REJECTED` carries
reasons and re-enters at PROPOSED, never straight to DONE.)

## Turn loop

```
read queue → drain READY (execute → a-log → report → receipt → DONE)
         → file H/M where blocked → propose next PROPOSED w/ justification
         → halt ONLY with dryness proof (nothing ready, nothing splittable)
```

## Self-audit

`python3 acheck.py --queue tasks.jsonl --alogs a-logs --reports reports`
Exit 0 = native. Wire it into CI or run it on any agent's output before
trusting it. An agent that passes acheck on its own queue is A-task native
by measurement, not by promise.
