
## Review verdict (agent round 2, 2026-09-10)
F1 FALSIFIED: no blend beats best single on frozen split (len global 0.5752,
cat global 0.4039; kNN drags blends below global). F2 passes with caveat
(top other-subgroup 1.2%, topical not structural). F3 FIRED as designed:
online session>global but split global>session (adaptation vs frozen).
Verdicts: cfg-global promote (floor), cfg-knn + cfg-ensemble-uniform augment
(similarity gate; session-global alpha sweep sans kNN). learn.py: 2 criteria1.1
proposals (shared cat/len threshold failures) — human promotes, not auto-applied.
