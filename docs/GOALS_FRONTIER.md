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

## 4. Gaps worth closing (ranked by leverage)

1. **Learned check-in policy** (Hedwig-style online classifier over our
   approval/denial traces) to graduate the count-based ratchet. (Proposed B12.)
2. **Enforced budgets** — `budgets.py` advertises; nothing enforces. XBSTACK
   cuts network access at the token cap. Ours is theatre until wired. (M4.)
3. **Replanner as a first-class node** (ours is manual send-back).
4. **Plan-validity metrics** (valid-plan rate, replan success rate) tracked
   per bout, not just pass/fail.
5. **Leaf-termination formalism** (STEP mappability criteria ≈ our
   acceptance+evidence, but stated as checkable predicates).

## 5. Bottom line

Build like Plan-and-Execute, gate like XBSTACK, learn like Hedwig, settle
like nobody else. The framework stands; the next unit of work is gap 1+2.
