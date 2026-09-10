# a-cwdgate — progress report

## 1. claim
CWD-independence gate + fix 8 CWD-dependent tests

## 2. evidence
Suite was 38 green in-repo but 5 red from foreign CWD (sys.path hacks, relative paths). Added conftest.py root-anchoring + --cwd-independent gate. Result: 46 green both CWDs, 6/6.
Artifacts verified present this run. Suite basis: 46 passed both CWDs; self-check 6/6 (this session).

## 3. self-review
Gate runs full suite twice (~30s). Sharding not considered as suite grows.

## 4. needs
None inside these tasks (push need pre-queued as H1).

## 5. cost
$0, no manual actions.
