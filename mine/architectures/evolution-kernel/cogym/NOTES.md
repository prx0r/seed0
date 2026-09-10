# prx0r/cogym

sha=765f9c0f9377b21e9e6c0e3036da488786451a83
proto=['canonical']

## README

# Cogym — Deterministic Reasoning Laboratory

**Cogym measures whether reasoning strategies actually improve decisions under uncertainty.**

Trading is the experimental organism — objective outcomes, sequential decisions, regime changes, noisy evidence, calibration pressure, deterministic replay.

## START HERE (new agent onboarding)

Read these IN ORDER:

| Step | File | Why |
|------|------|-----|
| 1 | [`canonical/AGENTS.md`](canonical/AGENTS.md) | Rules, conventions, repo layout, what NOT to do |
| 2 | [`canonical/IMPLEMENTATION-PLAN.md`](canonical/IMPLEMENTATION-PLAN.md) | What's built, what's next, what's frozen |
| 3 | [`canonical/docs/REFERENCE.md`](canonical/docs/REFERENCE.md) | Every module documented |
| 4 | [`docs/PEER-REVIEW-CHECKLIST.md`](docs/PEER-REVIEW-CHECKLIST.md) | Run this after EVERY experiment |
| 5 | [`docs/papers/FRONTIER-PAPERS.md`](docs/papers/FRONTIER-PAPERS.md) | Arxiv papers that justify our methodology |

## The ONE rule

> **Hermes proposes. Cogym disposes. No LLM grades itself.**

Extraction is not verification. A model saying "this skill is useful" means nothing.
Only paired evaluation on held-out deterministic worlds counts as evidence.

## Experiment workflow

Every experiment follows the SAME cycle:

```
1. DESIGN     Write PROTOCOL.md (hypothesis + variables + controls)
              Freeze BEFORE running anything
2. MATERIALS  Write treatment materials in materials/
3. RUN        Execute subjects via hermes adapter (logged)
4. GRADE     
