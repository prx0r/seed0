# ENDGAME — visionary endgoals, validation, and how we get there

## The end state (5-year horizon)
A tournament that never stops: ideas spawn seeds, seeds build, rubrics score,
failures become criteria, criteria harden into law. Human touches only R2-style
reviews and real-money decisions. Out the other end, on demand: working businesses
(voiceagent/cmail pattern), scored investment theses (idea1 pattern), and the
kernel itself, compounding.

## Endgoals worth naming
1. **Overnight business builder.** Idea at 8pm → scored working product + review
   by 8am. Validated by: bout1 pattern (15-min builds, all green, honest
   self-reviews). Gap: distribution hypotheses, not code.
2. **Encode-the-owner agent.** 41k events / 3k messages / 11.8k tool parts live in
   the local opencode.db (R2 holds 6GB backup). Trajectories (prompt→tool→result),
   not just prompts, are the training signal: SFT on tool trajectories + intent
   priors from prompts + todo patterns for planning style. Caveats: single-user
   overfit, staleness as you change, privacy (never train shared models on it;
   per-user LoRA or local-only). Next: schema export script + small style-clone eval.
3. **Continuous criteria convergence.** Every bout's shared failures → criteria1.1
   → criteria0 rules (learn.py already does this). Terminal state: the rubric set
   that kills bad builds in minutes. Validated by: bout1 unanimously surfacing
   CWD-independence + demand-side gaps.
4. **mw-budgeted tournaments.** Every seed attempt metered (tokens, time, $) against
   idea purses; H-levels track human touches. Leaderboard gains $/pass and
   autonomy columns. Validity: no tournament result counts without its spend receipt.

## Validation ladder (how we know we're getting there, in order)
1. Bout N+1 cites bout N's lessons unprompted (culture transmission check).
2. A seed built entirely by agents passes a rubric written entirely by agents,
   reviewed once by a human in <10 min.
3. First dollar: a tournament output earns or verifiably saves money (paper first).
4. Criteria stop growing: three consecutive bouts propose zero new global rules
   (convergence signal for criteria0).
5. Owner-clone passes a blind Turing review on planning style (endgame 2 check).

## What NOT to chase
Bigger tournaments before faster verdicts (latency of truth > number of seeds);
more seeds before better rubrics (rubric quality dominates — bout1 proved all
three converged, so the differentiator was never seed count); autonomy theater
(sleepwalking agents with no receipts).
