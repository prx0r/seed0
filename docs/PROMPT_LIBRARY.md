# PROMPT LIBRARY — copy-paste blocks for HAM agents (v1)

Paste ONE block per message. Fill `[slots]`. The agent speaks HAM (tiers,
queues, receipts, no questions); these blocks are the human side of that
protocol. Conventions: approvals say `go [QUEUE-ID]`; denials always carry a
reason (denials are data); money is always integer cents + purpose + expiry.

## H — approvals & control

**H-APPROVE** (release one queued item)
```text
go [H-ID]. Scope: [exact target, e.g. push commit 01d42ba to origin/main].
Log the H-approval bound to its digest; halt if the target changed since.
```

**H-DENY** (kill it with data)
```text
deny [H-ID]: [reason in one line]. Record the denial so standing promotion
stays blocked, then propose the cheapest alternative as a new A-task.
```

**H-SCOPE** (yes, but smaller)
```text
Approve [H-ID] with limits: [e.g. read-only, max 3 files, no network].
Re-tier anything outside the limits back to H with a fresh demo.
```

**H-PAUSE / H-RESUME** (autonomy switch)
```text
pause H7. Finish the current step, park the queue, packet on disk. No new tasks.
```
```text
resume H7. Read BOOT.md, pick up the ready queue, continue without asking.
```

**H-STOP** (emergency)
```text
STOP. Halt all lanes immediately. Park every task as PAUSED with reasons.
Report state + packet. Do nothing else until I say resume.
```

## M — money (integer cents, purpose, expiry — always all three)

**M-GRANT** (release exact funds)
```text
Grant [N] cents for [purpose] to [endpoint], expiry [e.g. 24h].
Log the grant; every spend needs its x402 receipt or it didn't happen.
```

**M-CAP** (set the ceiling)
```text
Spend cap: [N] cents total for [scope], hard stop, no carryover.
Refuse over-ceiling work with GrantDenied, don't queue around it.
```

**M-AUDIT** (show me the money)
```text
Spending report: per-grant spent/remaining/receipts + metered totals +
unmetered gaps stated plainly. Numbers first, no adjectives.
```

## A — tasking (agent works, you don't)

**A-TASK** (the default work order)
```text
Do [X]. Acceptance: [measurable, e.g. pytest green + validator exit 0].
Evidence: [commands to re-run]. Tier-route each step via ham.py; queue H/M
with cost notes + demos; never end with a question; bank receipt on DONE.
```

**A-BOUT** (tournament)
```text
Tournament on [idea]: freeze brief + rubric + validator + weights BEFORE lanes.
[N] isolated lanes, builders run validator (max 3 tries), you re-run every
validator, blind review before reveal, receipts verify. Hypothesis verdicts
from preregistered thresholds, never from rank.
```

**A-REVIEW** (validation pass)
```text
Review [artifact/record]: re-read evidence files, re-run ≥1 evidence command,
per-item acceptance verdicts, write task-validation receipt. No receipt, no DONE.
```

**A-FIX** (bug with teeth)
```text
Fix [symptom]: reproduce first (failing test or command), minimal diff,
regression test proving the fix, full suite + self-check green after.
```

**A-BOOT** (cold start any session/box)
```text
Read BOOT.md and resume: packet → ready queue → decisions tail → THREADS.
Then continue the ready queue without asking. Report packet on disk when done.
```

**A-REPORT** (status without stopping work)
```text
Status, without pausing: DONE receipts this run, blocked_on with approval
strings + demos, ready backlog count. Keep working after reporting.
```

## How to use

1. Match the block to the situation (H = you decide, M = you pay, A = it works).
2. One block per message — stacked approvals (`go H1, go H2`) are fine, mixed
   tiers in one message get processed in order H, M, A.
3. Never paste secrets — grants reference endpoints, keys travel via env only.
4. If no block fits, paste this: `New situation: [describe]. Classify it H/M/A
   yourself, queue accordingly with cost note + demo, continue working.`
