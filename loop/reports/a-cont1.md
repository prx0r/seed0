# a-cont1 — progress report

## 1. claim
REPORTED now requires an existing report file; call sites pass queue path; 5 loop tests green.

## 2. evidence
`loop.py problems()` gained the REPORTED guard (resolves ref against CWD and
queue root). 3 call sites pass `path`. `test_reported_requires_existing_report`
covers missing ref, ghost file, real file. Full file: 5 passed.

## 3. self-review
Guard checks existence, not content — a 1-line report passes. Content quality
remains the validator's job (§6), correctly: tools check shape, humans check
substance.

## 4. needs
None. No H/M discovered.

## 5. cost
$0, no manual actions.
