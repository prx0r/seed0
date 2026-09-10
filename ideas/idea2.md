# idea2 — Essay-substrate agentic architectures (2026-09-10)

## Problem / scarcity
Agent architectures converge on the same few patterns (ReAct, tool loops, subagents)
because they are designed from engineering habit, not from theories of agency.
Meanwhile `mine/` holds 68 dense checkpoints theorizing participation, unity,
affect (rasa), observation, and emanation structures — an untapped design space.
Cost of ignoring it: architectures that all fail the same way.

## Mechanism
1. Extract architectural hypotheses from essays (e.g. monad–series → hierarchical
   decomposition with unity constraints; participation triad → tool-grounding
   protocol; rasa theory → affect-weighted prioritization; observer proofs →
   self-verification loops; procession/reversion → expand-then-integrate cycles).
2. Implement each as a seed variant under `seeds/` (same task interface).
3. Tournament them via funnel.py with binary rubrics; telemetry (time/tokens/cost)
   recorded per run; receipts pinned.
4. Select with cg-type discipline: gates dominate objectives (pass/fail first),
   receipts as proofs, Wilson-style proportions over many trials — never vibes.
   Winners compose; losers' failure modes feed learn.py → criteria amendments.

## Falsifiable predictions
- [ ] Would be proven wrong if essay-derived variants do NOT beat the baseline
  seed on any rubric slice across 3+ tournaments (substrate adds nothing).
- [ ] Would be proven wrong if all variants fail identically (shared flaw means
  the bottleneck is elsewhere — likely tooling, not architecture).
- [ ] Would be proven wrong if a variant's advantage disappears once its essay
  concepts are removed (ablation) — i.e. the gain wasn't from the substrate.

## Non-goals
Literary fidelity to the essays (they are substrate, not scripture); claiming
consciousness for agents; single-winner thinking (keep the pareto set).

## Verification plan
criteria per tournament (binary pass/fail + telemetry); ablation runs per winning
variant; review logs with hypotheses before each amendment round.

## Out of scope (logged, not gated)
Automated essay-to-architecture extraction (human curates v1); cross-essay
synthesis architectures; live deployment of winners.
