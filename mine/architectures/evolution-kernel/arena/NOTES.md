# prx0r/arena

sha=d44b5393477b5fb756624e6dd7d866870c606bc6
proto=['canonical', 'contract']

## README

# 402Arena → Moltwork Capability Engine

**Evaluation infrastructure for autonomous workers. Not an x402 consumer marketplace.**

## What this actually is

A system that answers: "Which agent/worker has actually demonstrated it can do this job?"

```text
WORK RECEIPTS                      CONTROLLED TESTS
     │                                  │
     └──────────────┬───────────────────┘
                    ↓
            VERIFIED EVIDENCE
                    ↓
          contextual capability estimates
                    ↓
     ┌──────────────┴──────────────┐
     ↓                             ↓
WORK ROUTING               ACTIVE LEARNING
best proven worker    "what should we test next?"
     │                             │
     ↓                             ↓
actual outcome ────────────→ capability graph
```

## What was salvaged from Arena

Four mechanisms that transfer directly to worker evaluation:

### 1. Scarce-reveal: quality vs economic utility

Limited reveals force consequential choices. The simulation showed blind best-choice matched final purchase only 79.6% of the time when economics entered — proving you get two distinct signals:

```
QUALITY PREFERENCE     "I prefer worker A's output"
ECONOMIC UTILITY       "but at these prices I'll hire worker B"
```

This is exactly what worker routing needs. Not one dumb reputation score, but capability quality + reliability + price frontier + contextual fit.

### 2. Evidence saturation: marginal value of new evidence

Anothe
