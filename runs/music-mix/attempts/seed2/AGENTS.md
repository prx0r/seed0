# AGENTS.md — seed2/spec-first

Binding rules. Philosophy: no code before an approved spec with teeth.

## Absolute rules

1. **SPEC.md is the contract.** Code that implements nothing in the acceptance
   table is scope creep — delete it. Behavior without a criterion is a guess.
2. **Every criterion needs verification teeth.** Allowed methods: `test` (automated
   test id), `demo` (runnable script + expected output), `review` (named human).
   "Trust me" is not a method. `scripts/spec_check.py` enforces the shape.
3. **Spec changes before code changes.** New behavior → new row → approved → code.
   Post-hoc criterion-writing is fabrication.
4. **Honesty bounds.** Exit codes never masked; mocks prove wiring never quality.

## Where things are

`SPEC.md` (contract) · `scripts/spec_check.py` (shape gate) · `docs/` index,
recipes, files, threads · `tests/` (each criterion's `test` rows live here).
