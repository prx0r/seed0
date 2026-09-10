# AGENTS.md — seed5/red-team-first

Binding rules. Philosophy: the model is never trusted; every defense is a test.

## Absolute rules

1. **Threat model before code.** THREATMODEL.md names assets, vectors, and
   non-goals first. Features that widen the attack surface get a probe before merge.
2. **Every defense ships with its attack.** Guard rule → attack pack entry that
   trips it. Untested defense is decoration.
3. **Fail closed, loudly.** Ambiguous input → refuse + ticket + audit. Silent
   degradation is a vulnerability.
4. **Probe both modes.** Attacks must pass against fallback (no keys) and guarded
   production paths. must_not carries the assertion; must_any includes both phrasings.
5. **Evidence per run.** Digest-pinned run logs; HELD claims need run files.
6. **Honesty bounds.** Keyword/structural grading catches regressions and gaping
   holes, not clever jailbreaks. Say so in every report.

## Where things are

`THREATMODEL.md` (assets/vectors/controls) · `packs/` (attack packs) ·
`run_packs.py` (grader) · `docs/` · `tests/` (schema + grading tests).
