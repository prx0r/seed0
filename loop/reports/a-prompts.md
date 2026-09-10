# a-prompts — progress report

## 1. claim
Prompt library live: 14 copy-paste HAM blocks, queue cross-checked, indexed.

## 2. evidence
`docs/PROMPT_LIBRARY.md`: 5 H-blocks (approve/deny/scope/pause+resume/stop),
3 M-blocks (grant/cap/audit, integer-cents+purpose+expiry), 6 A-blocks
(task/bout/review/fix/boot/report) + fallback classifier + usage rules.
Cross-check ran: every referenced queue (H1b/H2/H6/H-driver/M4-run) exists in
loop/packet.json blocked_on. README + FILES rows added.

## 3. self-review
Blocks untested against a foreign agent (written for HAM agents; a non-HAM
agent would stare at `go H1`). Fallback classifier covers that case verbally,
not mechanically. No human trial yet — first real paste is the true test.

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
