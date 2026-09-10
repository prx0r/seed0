# HYPOTHESIS ham-1 — auditable autonomy via H-A-M registry (cg-type, falsifiable)

Claim: encoding task logic (A lifecycle + validation-gated close), money locks
(single-use scoped grants, no-self-approval), unlock graph, and append-only a-logs
as runnable primitives makes agent autonomy mechanically auditable: every A-action
carries a receipt, no money moves without a signed grant, and tournaments can rank
methodology seeds by gate evidence instead of prose.

Falsifiers (any one firing kills the claim for this round):
- F1: any done A-task in the registry lacks a closing receipt in code path
  (close_a without evidence) → `test_a_close_needs_passing_evidence` fails.
- F2: any spend path succeeds without a signed, unused, unexpired,
  purpose-matching grant within cap → a `test_m_*` test fails.
- F3: seed6-ham scores NOT COMPLIANT or suite red under tournament.py mechanics.
- F4: a-logs backfill covers <90% of done A-tasks (audit gap) → validator fails.
- F5: an agent resolves its own H/M approval (approver without human: channel).

Metrics: seed0 compliance x/5, suite green bool, evidence file count,
validate_ham.py exit code (0 = all falsifiers survived), tournament rank.
Thresholds: compliance 5/5, suite green, validator 0, rank decided by evidence count.
