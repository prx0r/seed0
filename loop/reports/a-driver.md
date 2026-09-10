# a-driver — progress report

## 1. claim
Block spec'd + portable harness encoded; returns proven structural, fix queued.

## 2. evidence
`docs/DRIVER_GAP.md`: 3-layer anatomy verified on box (opencode run v1.18.30,
hermes cron create/tick, system cron all present; none aimed at seed0; no
self-schedule primitive in toolset). `BOOT.md` + `BOOT_PULSE.txt` written;
AGENTS.md points at BOOT. H-driver decision (D1/D2/D3 + costs + KILL-file
convention) queued, not taken (M+H territory).

## 3. self-review
Did not test-fire a pulse (that spends quota = M). D1 vs D2 unmeasured —
hermes-cron may need auth/daemons config; cron+opencode needs quota math.
Both flagged in the queued decision.

## 4. needs
H-driver choice (human). Nothing else.

## 5. cost
$0, no manual actions.
