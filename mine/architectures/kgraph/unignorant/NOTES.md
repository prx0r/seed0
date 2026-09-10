# prx0r/unignorant

sha=836f1b269004f039b11dd952d660918f02e26595

## README excerpt

# Unignorant

**Global life, not global news.**

A world-reality data graph that assembles what ordinary humans in 191 countries are actually experiencing — work, wages, food prices, housing, trade, aid, and real pictures of daily life — sourced from public world data APIs, served via REST + MCP + static frontend.

## Why this exists

Western media covers the world through drama — war, politics, celebrities. That's not what life *is*. Unignorant answers the question no one else answers:

> Show me what ordinary humans elsewhere are actually experiencing that I would otherwise never hear about.

Not "global news." **Global life.** The texture of an ordinary Thursday in Kampala — what people complain about, what they eat, what a teacher's salary buys, how they talk about the West, what's getting better and worse. From the people living it, in their own words.

## Architecture

```
connectors/        one module per external API (25 sources)
    ↓  normalized
core/              entities, reality-scoring, Suffering Index, countries registry,
                   TTL cache, SQLite, pydantic schemas, .env loader
    ↓
api/               FastAPI REST app (~45 endpoints, typed, cached, fail-soft)
mcp/               MCP server (33 tools, agent-native)
web/               Astro static frontend (served by the API)
```

## Quick Start

```bash
# Clone
git clone https://github.com/prx0r/unignorant.git
cd unignorant

# Install
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

#
