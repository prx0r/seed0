# METAPROCESS — bout1 tournament, full cognitive log (2026-09-10)

How this tournament was actually run: every action, finding, and on-the-spot
decision, including the flaws. Written so the next run avoids them by construction.

## Phase 0 — framing (my decisions, pre-launch)
- **Action:** chose 3 seeds (seed1/seed2/seed5) over 5 to bound cost/time.
- **Action:** wrote a detailed shared brief (idea1 summary + money prompt + worked
  examples: "lead-time tracker", "bottleneck scorer", "EICR reminder engine").
- **Finding (against me, found later):** the examples primed convergence. All three
  built dB/dt scorers — I called it "convergent evolution" in the report. Honest
  relabel: **prompted convergence**. True independence needs blind prompts with
  examples withheld. Logged as theatre class A (overclaimed independence).
- **Action:** launched all three subagents in one parallel block. Correct call —
  wall time collapsed to one bout duration.

## Phase 1 — execution (subagents, ~15 min each, unattended)
- **Observed:** all three returned green suites + BUILDLOGs + honest self-reviews
  ("mechanism real, no buyer"). No intervention needed. The seed kernels + brief
  format demonstrably produce shippable-shaped output without supervision.
- **Finding:** self-reported effort ("~15 min") is unverifiable and unmetered.
  I have no token/time/cost numbers for the most expensive part of the tournament
  (the subagent inference itself). Budgeting did NOT work here — see § theatre.

## Phase 2 — scoring (mechanical, mine)
- **Action:** ran each suite in its own dir (12/4/10 pass as claimed) AND from a
  foreign CWD. Second context caught seed5's 4 failures (CWD-relative paths).
- **Finding:** green suites are CWD-relative claims. New law proposed: suites must
  pass from any working directory (added to PRIMITIVES, pending criteria0).
- **Action:** seed0 compliance check → 4/5 each (correct: they're apps, not kernels;
  the checker correctly refuses to flatter them).

## Phase 3 — review/amend (judgment, mine)
- **Action:** ranked seed2 ≥ seed1 > seed5 with stated reasons; wrote R2 review +
  scores.jsonl; proposed (not applied) criteria0 rule + demand-side next bout.
- **Finding:** I am judge, jury, and tournament designer. No blind judging, no
  second reviewer, no pre-registered ranking weights. Verdicts are reasoned but
  unfalsifiable. Fix: pre-register weights + use an independent judge call
  (pyeval judge pattern) for future bouts.

## Theatre inventory (claimed vs actual this bout)
| Claimed | Actual | Verdict |
|---|---|---|
| Budgeting works | pyeval caps tested on stubs; $0.000558 live micro-run metered; subagent spend ($ real cost) completely unmetered | THEATRE (worst one) |
| Fresh-agent isolation | attempt dirs isolate files, but all agents shared my brief (priming) | PARTIAL |
| learn.py loop | ran on demo data only, not bout data | DEMOED, not exercised |
| eval_arch ablation | not run on bout winners | SKIPPED (next bout must) |
| csec packs vs bout outputs | not run | SKIPPED |
| Hermes/Pydantic/mw integration | referenced in docs, zero runtime use | LITERATURE, not stack |
| Timings | elapsed on suites/funnel; my own deliberation time unlogged | PARTIAL |

## What genuinely worked (keep)
1. Parallel subagent launch with tight briefs → three shippable-shaped builds, zero supervision.
2. Mechanical scoring caught what self-report hid (seed5 CWD fragility).
3. Research primitive (websearch+arxiv cited unprompted by all three).
4. Fail-closed design (seed5 RefuseError) + honest self-reviews ("no buyer").
5. Receipts/scores/reviews all on disk, committed, pushed. The loop is real; its coverage is what needs widening.

## Amendments filed from this review (do before bout2)
- [ ] Meter subagent spend (wrap launches; log tokens/time/cost per seed).
- [ ] Blind prompts: worked examples move to a sealed appendix agents never see.
- [ ] Pre-register ranking weights before launching.
- [ ] Run eval_arch ablation + csec packs on every winner.
- [ ] learn.py over real bout data; promote ≥1 rule per bout or log why none.
- [ ] CWD-independence gate in CI for all suites (own repos included).
