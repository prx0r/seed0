# a-multibox — progress report

## 1. claim
One funnel across boxes: git mirrors + labeled rows + dead-box safety.

## 2. evidence
- `hplane.py sync`: clone-once, fetch+hard-reset after, per-mirror
  ok/error records; 3-test proof with local git remotes (clone, fetch
  refresh, dead-URL captured without raising).
- `label|source[|box]` entries; `repo` = label and `box` on every row, so
  6 agents × 3 VPS stay distinguishable. Existing tests green (labels
  default to basename for plain paths).
- Resolution stays per-repo AND per-box (documented rule, enforced by
  absence of any remote-write path).
- `plane/remotes.txt` template with filled-format examples commented.
- Owner fills real URLs — the one step that isn't mine to take (needs
  their box addresses, not guessable).

## 3. self-review
 Mirrors can go stale between syncs (no daemon; sync runs on pulse or
 manually — stated in docs). Hard-reset drops local mirror edits (mirrors
 documented as caches, never edited — enforced by nothing; convention).

## 4. needs
Real remote URLs (owner fills `plane/remotes.txt`). Nothing else.

## 5. cost
$0, no manual actions.
