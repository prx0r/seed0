# meta-criteria — tournament validity + hypothesis bar (frozen 2026-09-10)

| C1 | Bout validator exits 0 on every lane before scoring | test runs/meta-tourney/bout-*/validate.py | agent |
| C2 | H1 decided by footrule distance integers, not ranks or prose | test metrics() in bout-P validator | agent |
| C3 | H2 decided by record counts 5 vs 1 after identical storm | test metrics() in bout-I validator | agent |
| C4 | All bout + tournament receipts verify byte-identical | test runs.verify_file over runs/sha256_*.json | agent |
| C5 | Lanes built from brief+rubric only, no cross-reads | review lane build logs for isolation | agent |
| C6 | Blind review written before identities revealed | review sealed_map timestamp precedes reveal edit | agent |
| C7 | Red lane invalidates its bout instead of failing the hypothesis | review verdict logic in review doc | agent |
