# a-stoplight — progress report

## 1. claim
A-log convention + `loop.py log/stoplight` live; GO/NOGO proven both directions.

## 2. evidence
`loop.py log <id> --covers i,j --action --detail` appends tagged lines to
loop/a-logs/<id>.jsonl. `stoplight` matches covers→acceptance + report file +
receipt: 7 loop tests green incl. NOGO-on-missing-index then GO after logging.
Fixed during build: report resolution widened (queue-dir itself counts).

## 3. self-review
covers[] tags are self-asserted (a liar tags everything). Mitigation: validator
re-runs evidence independently (§6) — stoplight checks COMPLETENESS of logging,
not truth. Stated in code comment? No — stating here; code comment follow-up.

## 4. needs
None.

## 5. cost
$0, no manual actions.
