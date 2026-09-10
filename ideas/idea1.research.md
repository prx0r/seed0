# idea1 research log R1 — papers, compliance mechanisms, working code (2026-09-10)

## Papers FOR the thesis (with teeth)
- **Novelty bottleneck as Amdahl's law (2603.27438):** fraction ν of novel
  decisions is an irreducible serial component; better agents improve the
  coefficient, not the exponent. Prescription matches our stack exactly: reduce ν
  systematically (specs, tests, conventions) + maximize verifiability (tests
  before delegating). METR RCT: AI made devs 19% SLOWER on novel tasks. Direct
  support for Jevons-for-science AND for seed0's spec-first discipline.
- **Structural Jevons via architecture (2601.12339/12338):** falling inference
  prices induce more compute-intensive agent designs (token multiplier) → demand
  super-elastic. Plus Red Queen effect (innovation depreciates rivals) and
  **Wrapper Trap** (upstream capability erodes downstream app value — warning for
  OUR agent layers too). Calibrated agent-based model, not just prose.
- **Publish and Perish (2604.05714):** AI writing >> review capacity → knowledge
  output −32% unless review acceleration exceeds writing acceleration (δ>γ).
  The thesis's verification-scarcity claim as a two-variable ODE with a falsifiable
  threshold. Steal the δ>γ framing for criteria gating.
- **Compute-vs-labor substitution (2507.23181):** whether bottlenecks bind is an
  estimated elasticity, not a vibe. frontier-experiments spec finds complements
  (σ≈0). Lesson for our dB/dt work: estimate, don't assert.
- **Reverse Big Push (2608.25602):** automation cascades + multiple equilibria —
  formal backing for threshold-cliff thinking.

## Papers that Sharpen the compliance question (how agents actually follow criteria)
Core finding across all: **never let the model grade itself** (Reflexion/self-
refine fail at self-error-detection). External deterministic checks win:
- **AgentLTL (2607.02599):** one FO-LTL spec drives offline scoring + online tool
  gating + finetuning reward (+38pp). This is the correct shape for criteria0:
  each row should compile to an enforceable trace constraint, not just a test name.
- **ABC/AgentAssert (2602.22302):** Design-by-Contract with drift bounds
  (D*<0.27), 88–100% compliance, compositionality across multi-agent chains.
  Our confirm-tokens + receipts + reconcile loop is a proto-version; adopt the
  preconditions/invariants/recovery vocabulary.
- **VeriGuard / FAVA:** offline formal verification + online monitor; SMT-backed
  permission graphs (90.5% compliance). Direction for high-stakes actions.
- **PolicyGuard → PolicyGuide:** dialogue-grounded verifier (+12pp) then compiled
  workflow graphs (+0.42→0.62). Direct upgrade path for voiceagent's guard:
  policies as traversable graphs checked at turn boundaries, not keyword lists.
- **Constrained agent framework (2607.00035):** shift LLM from free-form code to
  typed JSON slots — zero execution-stage LLM tokens. Validates our SPEC tables +
  tool schemas; extend the pattern everywhere.
- **VES Jevons conditions (2503.05816):** Jevons needs elasticity > 1 — five-phase
  taxonomy. Apply to Objection 3: cross-world P(s) must cite markets or bands.

## Working code (cloned /tmp, MIT — mine, don't worship)
- **virbahu/supplier-lead-time-predictor** (216KB, single file): lead-time
  distributions + sensitivity analysis. Closest existing code to dB/dt
  measurement — port its distribution-comparison approach, not its weights.
- **abelraphelp disruption-detection** (17MB, LSTM+GDELT+IsolationForest→0-100,
  FastAPI+React): full early-warning stack shape (ingest→fuse→score→dashboard).
  Take the architecture, replace toy models with our metric definitions.
- Vigil / nexus-risk / Aishat predictor: same category, dashboards over signal
  fusion. Surveyed, not cloned — diminishing returns past two.
- Kantamaniprakash/supply-chain-aip: Palantir-locked, unclonable; architecture
  reference only (medallion + ensemble + VaR + agent actions with thresholds).

## Implications recorded as criteria1 amendments (proposed, not yet applied)
- C2 must cite an estimated elasticity or band, not an asserted formula.
- New row candidate: δ>γ check on any automation the build itself introduces
  (the build must not worsen the verification ratio it profits from).
- Evidence hierarchy (C6) gains: replicated-real-world > benchmark, per
  mineability paper — already there, now paper-backed.
