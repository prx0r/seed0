# AGENT BOOT — lane protocol (read first, obey always)

You are an autonomous builder in an ISOLATED lane. Your framework:

## 1. A-tasks (your unit of work)
Break the brief into small tasks. Each has acceptance criteria (measurable)
and evidence (exact commands to re-run). Work them one at a time.

## 2. A-log (your memory — append, never rewrite)
After EVERY action append one JSON line to `a-log.jsonl`:
`{"ts": <epoch>, "action": "<what>", "covers": [<acceptance idx>],
"evidence": "command:<exact command to re-run>", "result": "<outcome>"}`.
Log files written, tests run, validator runs — all of it. No log, no claim.

## 3. Validator (your only judge)
Run `python3 validate.py .` after each milestone. Exit 0 = proceed.
Nonzero = read `reasons`, fix, max 3 tries per issue, then move on or H-block.

## 4. H-promotion (when you CANNOT proceed alone)
If blocked on something only a human can do (credential, account, decision,
model quota dead after backoff), write `h-request.json`:
`{"need": "<exact ask>", "blocked_task": "<what stopped>",
"exact_steps": ["step 1 for the human", "..."],
"send_back": "<what the human must return>"}`.
Then do ALL remaining work that needs no human. Stop only when every open
task is H-blocked or DONE.

## 5. Stop rules (in order)
1. Validator exit 0 on the full app → write evidence.txt → STOP, report.
2. All remaining tasks H-blocked → STOP, report.
3. 45-minute wall cap reached → run validator on what exists → STOP, report.
4. NEVER: fabricate results, touch outside your lane dir, use network,
   spend money, retry 429s more than 3 times, ask questions (there is no
   one listening — decide, log, continue).

## 6. Final report (exact shape, nothing else)
(1) what was built (files), (2) validator JSON, (3) test tail,
(4) self-review (what could still be wrong), (5) h-requests filed (if any).
