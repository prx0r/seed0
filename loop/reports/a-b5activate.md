# a-b5activate — progress report

## 1. claim
B5 closed: approving an H-record with a grant spec activates the grant
inline; denial moves nothing; hserver surfaces both outcomes.

## 2. evidence
- `hinbox.new_request(grant={...})` public API (replaced test file-surgery).
- `hinbox.resolve` on approved+grant: creates + activates grant, stamps
  `grant_id`; spend to ceiling works, over-ceiling refused (GrantDenied).
- Denied + grant spec: no grant record, queue empties normally.
- `hserver` resolve response carries `grant_id`/`grant_error`.
- Activation failure path: recorded on resolution, decision stands, spend
  stays locked (fail-closed both directions).

## 3. self-review
Grant spec travels inside the H-record (no separate M-approval step) —
correct per "button IS release," but means a compromised inbox writer could
propose spend (mitigation: human still presses; amounts visible pre-press).

## 4. needs
Live traffic to prove the path end-to-end (H-inbox still quiet).

## 5. cost
$0, no manual actions.
