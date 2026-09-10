# a-branches — progress report

## 1. claim
Attempt-branch lifecycle executed: created, verified on branch, FF-merged, deleted.

## 2. evidence
`git checkout -qb tourn/chain1/seed1.1` → suite 6/6 + 5/5 ON branch →
committed (15ef84e) → `checkout main` → `merge --ff-only` clean → `branch -D`.
`git branch -a` shows main only. Unrelated dirty files untouched throughout.

## 3. self-review
FF was available because nothing else landed concurrently; a divergent main
would have needed rebase policy (unspecified — follow-up if it ever happens).

## 4. needs
None.

## 5. cost
$0, no manual actions.
