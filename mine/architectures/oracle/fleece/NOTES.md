# prx0r/fleece

sha=38687c7c7bb60fffb7636944f2e7d2ff7cb9ae6b

## README excerpt

# DeltaTuna 🐟 — Evolving Options Capital Allocation

**Swarm intelligence + options + honest measurement.** A league of allocation
"schools" competes on standardized market scenarios; failures go to a
graveyard; a graph database remembers everything; a meta-controller named
Orca reads that memory and proposes what to try next. Built for the Alpaca
AI Trading Agents Hackathon (Aug 28 – Sep 4, 2026, paper trading).

```
Fish (7 fixed option strategies)
 └─ 5 Pools per school
     └─ Shark genome routes capital by regime
         └─ SCHOOL = shark + pools          ← unit of evolution
             └─ LEAGUE of 12 schools
                 ├─ ranked on hash-locked scenarios (ARENA-v1)
                 ├─ bottom 20% → ⚰️ graveyard (tombstones, never deleted)
                 └─ capital allocated by rank
HydraDB = shared memory (posteriors · lineage · traits · proposals)
Orca    = meta-controller reading the graph, proposing next moves
```

## Quickstart

```bash
# services
python3 -m uvicorn fleece.api.server:app --port 8000 &      # API
cd dashboard && npm run dev &                               # Dashboard :5173
setsid nohup python3 -u fleece/options/live_runner.py >> logs/live_runner.log 2>&1 &
setsid nohup python3 -u fleece/options/school_league.py 20 >> logs/school_league.log 2>&1 &

# science
cd experiments/deltatuna_lab && python3 run_edt01.py --analyze   # preregistered verdicts
python3 fleece/options/orca.py                                   # meta-controller cycle
python3 
