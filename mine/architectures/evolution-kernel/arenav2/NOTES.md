# prx0r/arenav2

sha=ad5cdec1fc1fc0d4dae24d9554394c7eaa0bf588
proto=[]

## README

# Arena v2 — Worker evaluation infrastructure

**Trust layer for autonomous workers.**

> Money buys evaluation, not reputation.

## What this is

A system that builds empirical capability profiles for agents/workers from actual work, controlled benchmarks, and verified outcomes.

```text
WORK RECEIPTS + CONTROLLED TESTS
          ↓
    VERIFIED EVIDENCE
          ↓
  contextual capability estimates
          ↓
  ┌───────┴───────┐
  ↓               ↓
WORK ROUTING   ACTIVE LEARNING
best worker    what to test next
```

## Thesis

The scarce thing in autonomous agent marketplaces is **trust**. Not "which API?" but "which agent can actually do this job?"

Existing approaches (star ratings, self-reported claims, transaction counts) are gameable and context-free. Arena v2 builds:

- **Per-task-cluster capability profiles** with confidence intervals
- **Quality vs price preference separation** (blind choice ≠ purchase choice)
- **Evidence saturation** (benchmark where new evidence has marginal value)
- **Recommend vs research split** (route real jobs, explore unknown workers)

## What we have

### Seed data: 402Pilot

20,575 frozen provider responses across 823 tasks and 5 providers. Quality-scored, cost-recorded, failure-flagged.

| Provider | Quality | Cost | Fail rate |
|----------|---------|------|-----------|
| P-premium | 0.865 | $0.010 | 0% |
| P-mid | 0.818 | $0.002 | 0% |
| P-adv | 0.653 | $0.002 | 0% |
| P-cheap | 0.610 | $0.0005 | 0% |
| P-flaky | 0.491 | $0.002 | 40% |

