# a-metatourney — progress report

## 1. claim
H/A/M machinery tested as tournaments: H1 + H2 both hold on preregistered
integers; metaguide + shared ruler banked.

## 2. evidence
- `ideas/meta-h.md` IDEA OK + `criteria/meta.md` CRITERIA OK on landing.
- Bout-P: transitive_total 0 vs direct_total 2, invariant true, exit 0.
  Bout-I: naive 5 vs keyed 1/1, exit 0. Both re-run post-refactor, same ints.
- 4 lanes suite-green, rubric all-true, compliance honestly 4/5 (variants,
  not kernels). Blind reviews per bout (verdicts before reveal). Tournament
  receipted (4-way near-tie logged as-is; verdicts from metrics per C2/C3).
- `metrics.py` + 3 tests; bout-P validator imports the shared ruler.
- `docs/TOURNAMENTS.md`: schemas table, verdict rules, runbook, failure log
  (6 real bugs incl. weights-as-seed + sys.modules caching).
- Bugs caught this bout: validator argv slip, sys.modules lane caching,
  parents[] off-by-one, transitive tie-semantics test.

## 3. self-review
Agent built lanes AND validators AND judged (mechanical scoring only — no
LLM judgment, so separation holds, but an independent lane-builder would be
stronger; flow-test used subagents, this bout didn't — stated).
Micro-fixtures: proves machinery, not generality. Avatars still waiting.

## 4. needs
Bout2 with subagent-built lanes on a fatter fixture (proposed, unscheduled).

## 5. cost
$0, no manual actions.
