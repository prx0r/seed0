# a-branchguard — progress report

## 1. claim
Dirty-workdir refusal on branch + boolean-flag parser fix; S20 posture live.

## 2. evidence
- `loop.py branch` refuses on dirty tree without `--allow-dirty` (split-brain
  refusal, tested both directions).
- Found + fixed live: boolean flags (`--allow-dirty`, `--force`) consumed the
  next arg as a value — rollback `--force` was silently broken until now.
  Global BOOLEANS set in the parser; both commands re-tested green.
- M-watch (same batch): quota still 429, $0.00, receipted; a-push closed
  (acceptance amended to fa478bb reality, report + receipt banked).

## 3. self-review
Parser fix touches every CLI path — full suite (not just loop tests) re-ran
green as the guard.

## 4. needs
None. Queues unchanged except a-push DONE.

## 5. cost
$0, no manual actions.
