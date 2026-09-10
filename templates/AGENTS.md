# AGENTS.md — {{PROJECT}}

Binding rules for any coding agent working in this repository.
(Seeded by seed0. Fill the [brackets], keep the bones.)

## Absolute rules

1. **Authority first.** [WHAT is ground truth here — graph/schema/spec?] The model
   may word things; it may never invent [facts/prices/state]. Every claim traces
   to evidence or it doesn't ship.
2. **Side effects need approval.** [TOKENS/gates required]; refusal classes:
   [destructive/security/credential]. Nothing auto-sends, auto-orders, or
   auto-deletes. Ever.
3. **State lives in [store]; conversation/logs are not state.** Every interaction
   folds into [case/record] or it didn't happen.
4. **Degrade honestly.** Works without keys/offline via [fallback]; syncs back.
   Never block the user on a missing credential.
5. **Honesty bounds.** Mocks prove wiring, never quality. Simulated numbers labeled.
   No live claims without a live run. Exit codes never masked by pipes (`set -o
   pipefail` or check `$?` directly).
6. **Licenses.** AGPL patterns-only, never pasted. MIT/Apache vendored with
   attribution. No committed secrets (seed0 checks).
7. **Done-definition.** Code + honesty-proving test + recipe entry + FILES.md line
   + THREADS.md update. Missing any one = not done.

## Where things are

See README.md quickstart + docs/FILES.md. When unsure: grep first, ask never twice.

## Working style

- Small diffs, tested each step. Regression test per fix.
- Copy-paste runnables in docs/RECIPES.md, not prose-only procedures.
- Commit messages say what + why (one line suffices).
