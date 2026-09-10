# prx0r/feedify

sha=1d5796fa567e68b883f96cbba959ca7287486a85

## README excerpt

# Feedify 2.0

**Knowledge graph compiler for post-AGI scarcity intelligence.**

Feedify ingests X/Twitter posts from researchers and engineers, classifies them into typed knowledge objects, builds relationships between objects, and tracks predictions over time. The core thesis: "What does increasing abundance make newly scarce?"

```
cd /root/feedify2
source .venv/bin/activate
uvicorn feedify.api:app --reload --port 8788

# Quick test
curl http://localhost:8788/api/health
curl http://localhost:8788/api/convergence?days=30
curl http://localhost:8788/api/predictions?limit=5
```

## What's inside

| Module | Role |
|---|---|
| `feedify/adapters/` | 9 source adapters (X, GitHub, HN, SEC, OpenInsider, TrustMRR, StoreLeads, Appfigures, Glama) |
| `feedify/services/` | Core logic (25 files) — classification, scoring, convergence, graph building |
| `feedify/api.py` | FastAPI server (55+ routes) |
| `feedify/models.py` | 7 tables: artifacts, objects, edges, feeds, interactions, feed_versions, channels |
| `feedify/schemas.py` | Pydantic schemas for API |
| `august/` | Extracted tweet data (101 accounts, 3,357 tweets) |
| `specs/` | Analysis docs, thesis, account registry |
| `tests/` | 41 tests, all passing |

## Documentation

- [`AGENTS.md`](AGENTS.md) — binding rules for coding agents
- [`HANDOVER.md`](HANDOVER.md) — full project state
- [`NEXT_STEPS.md`](NEXT_STEPS.md) — what's done and what's next
- [`QUICKSTART.md`](QUICKSTART.md) — fresh agent entry point
- [`docs/RECIPES.md`
