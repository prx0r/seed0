# prx0r/gitgoblin

sha=11516d8173ab11abeaffd7d79806a82431cddd16

## README excerpt

# GitGoblin

**Technical alpha before virality.** GitGoblin watches high-signal builders, repositories, papers, dependencies and technical discourse; converts their activity into evidence-backed observations; detects independent expert convergence; extracts the underlying technical primitive; and emits downstream product opportunities.

GitGoblin is designed as both:

1. a standalone frontier-intelligence product; and
2. a specialized oracle for VentureLab/venture-lab.

## What is implemented

- GitHub public-profile, following, starred-repository, public-event and repository collectors.
- OpenAlex recent-work collector.
- arXiv Atom collector.
- ecosyste.ms repository-metadata collector.
- Hacker News official API collector.
- Generic RSS/Atom technical-publication collector.
- SQLite WAL store with idempotent append-only observation ingestion.
- Evidence hashes and source URLs on every observation.
- Builder expertise scoring that caps raw popularity influence.
- Time-decayed weighted attention, momentum, novelty and independence scoring.
- Frontier convergence signals ("technical alpha").
- Rule-based architectural primitive extraction with sector overrides.
- Product-opportunity derivation and build/research/watch/reject decisions.
- License classifier to prevent accidental source-code incorporation.
- FastAPI service, CLI, dashboard, Docker image and scheduler.
- VentureLab-compatible `MarketObservation` and `Opportunity` export.
- Deterministic tests and a certificate g
