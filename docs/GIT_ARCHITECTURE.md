# GIT ARCHITECTURE — branches for attempts, data on main (2026-09-10)

Lesson adopted from mw's peer review: **branches-as-components rot fast.**
Components live as directories on main (`seeds/`, `ideas/`, `criteria/`, runners).
Branches exist for exactly one purpose — isolating agent *attempts* — and die
after merge.

## Layout on main (canonical tree)
- code + seeds + ideas/criteria + runners (this repo as-is)
- `runs/<idea>-r<n>/`: scores.jsonl, review_r*.json, brief.md, rubric.json,
  funnel receipts. Data, committed. This is the ledger.
- `runs/<...>/attempts/`: NOT committed (reproducible from seed version + brief).
  Attempt branches deleted after merge.

## Attempt lifecycle
1. `git checkout -b tourn/<idea>-r<n>/<seed>` from main.
2. Agent builds ONLY in that branch (fresh-agent rule: seed + brief + rubric).
3. Score on the branch (`seed0.py check`, suite, rubric). Record in review doc.
4. Merge results as data: scores + review + receipts into `runs/` on main.
5. `git branch -D` the attempt branch. Branches never accumulate, never fork features.

## Why not branches per seed/version
Seed versions are data too (`seeds/<k>/VERSION` + `AMENDMENTS.jsonl`), so any
checkout at any commit reproduces any tournament exactly. History stays linear
and reviewable; `git log -- runs/` IS the tournament journal.
