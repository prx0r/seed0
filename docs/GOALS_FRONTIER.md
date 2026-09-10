# GOALS × FRONTIER — validation report for a-goal→a-task (2026-09-10)

Verdict: **frontier-compatible with 4 genuine novelties and 5 gaps worth
closing.** Every major choice in `docs/GOALS.md` was independently converged
on by published systems; nothing structural contradicts the literature.

## 1. What the frontier does (sources)

- **Hedwig** (Shukla et al., CAIS '26 + HedwigCLI repo): learned behavioral
  guidelines from longitudinal traces; hard constraints (CLI-enforced) +
  behavioral guidance (retrieved); three-tier cascade (silent proceed /
  surface summary / live check-in); online policy trained on
  approvals/denials/corrections; per-repo trust; policy- vs model-triggered
  check-ins distinguished; test-suite gate before completion. Caveat: paper
  is concept+survey (n=21); repo has since grown real implementation.
- **Plan-and-Execute** (LangGraph + BabyAGI lineage): planner/executor/
  replanner split; upfront plan constrains hallucination; DAG dependencies →
  parallel dispatch (LLMCompiler); checkpoints; replan-on-failure.
- **Production architectures** (XBSTACK pattern): typed TaskSteps, independent
  Plan Validator (tool existence, arg schemas, risk_level→HITL), circuit
  breakers (max 15 steps, 3 replans, token budgets), idempotency, plan
  validity metrics (97% target).
- **STEP planner** (embodied, VirtualHome): subgoal trees + leaf-node
  termination model (mappability + task-congruence criteria); failure taxonomy.

## 2. Convergent validity (we built these independently — good sign)

| Our mechanism | Frontier twin |
|---|---|
| Planner (goal decompose) / executor (lanes) split | Plan-and-Execute planner/executor |
| `blocked_by` DAG + ready-gating | LLMCompiler dependency dispatch |
| Validator-before-dispatch (stoplight) | XBSTACK independent Plan Validator |
| Binary accept/reject, no partial credit | Binary criterion checks (VALIDATION.md tier-2 pattern) |
| Idempotency keys (hinbox) | XBSTACK local idempotency checks |
| Max 3 validator tries per lane | Circuit breakers (max replan counts) |
| A-logs + receipts as memory | Hedwig interaction traces; run ledgers |
| Tiered human gates (H/A/M) | Hedwig 3-tier cascade; risk_level→HITL |

## 3. Our 4 novelties (not found in the sweep)

1. **Git as the bus**: branch-per-task, bundles for sneakernet, queue state
   in tree. Nobody else versions the work graph itself in git.
2. **Money as a separate tier** with grant lock + live x402 settlement rail.
   Frontier folds spend into generic "risk."
3. **Blind judging + sealed reveal** for tournaments. No counterpart found.
4. **Receipt-verified tournaments** (content-hashed run ids, verify-by-rerun
   as the scoreboard's trust anchor).

## 4. Gaps: closed since (verified 2026-09-10 re-read)

1. ~~Learned check-in policy~~ → DONE: `policy.py` (heuristic cold start +
   online SGD over approval/denial traces, three-tier cascade,
   `tests/test_policy.py`). Count-ratchet graduated, not removed.
2. ~~Enforced budgets~~ → DONE: `Budget.check()` pre-call refusal wired into
   `pyeval.py`; zero-budget run makes zero calls (tested). Funnel-subprocess
   spend still unobservable (honest zeros in spend.jsonl).
3. ~~Replanner as first-class node~~ → DONE: `loop.py replan` with reason log
   + MAX_REPLANS=3 breaker escalating to H.
4. ~~Plan-validity metrics~~ → DONE: `loop.py metrics` (validity rate, replan
   success, coverage fraction).
5. ~~Leaf-termination formalism~~ → DONE: `leafcheck` (every acceptance item
   needs an executable-kind evidence entry); `loop.py log --evidence` re-runs
   claims at stoplight.

## 5. Bottom line

Build like Plan-and-Execute, gate like XBSTACK, learn like Hedwig, settle
like nobody else. The framework stands; §4 gaps closed same-session — the
remaining frontier is live data (metered runs at quota, H-traffic for the
learned policy), not machinery.
