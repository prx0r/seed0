# prx0r/cge

sha=100c214e3412c108f43a83c332fbfe3d3cd2afa9

## README excerpt

# cogymkernel

**Deterministic agentic evolution laboratory.**
Worlds are replayable. Runs are content-addressed proofs. Quality gates are
hard constraints. An experience graph remembers everything.

```
pip install -e ".[dev]"        # or: uv pip install -e .
python3 -m pytest tests/ -q    # determinism is CI-enforced
cg status                      # razor alias: cg == cogym_kernel
cg run --seed 42
# also: from cg.k.ids import content_id  (2 chars vs 12)
```

That last command prints a **RunReceipt** with a `run_id` — a blake3 content
hash over worldpack + scenario + candidate + seed + merkle root of every event.
Anyone, anywhere, re-running it gets the identical id. That is the proof
primitive the whole stack builds on.

## What's inside

| Module | Role |
|---|---|
| `kernel/` | contracts · async runner · content-addressed run ids |
| `executors.py` | deterministic · replay-tape · cached-model executors |
| `eval/` | quality gates · lexicographic selection · layered suites (dev/validation/secret) · Wilson/bootstrap stats |
| `evo/` | 10 evolution recipes · 33 reasoning styles (16 families) · typed search spaces |
| `experience/` | async HydraDB client (capability probe, batching) · learning loop |
| `orchestration/` | embedded SQLite scheduler (WAL, atomic claims); hermes adapter optional |
| `science/` | experiment cycle · three-tier verification |
| `worlds/` | registry + shipped toy worldpack |

## Documentation

- [`docs/GUIDE.md`](docs/GUIDE.md) — **start here**: full
