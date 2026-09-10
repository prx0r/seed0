# prx0r/sanskritree

sha=c36c980c5ef5e2c4ce3763b06684afadcec3bbbb
proto=['pipeline']

## README

# Sanskrit Proof Engine

> **V2 status:** the legacy engine remains intact. New provenance-aware work lives in `src/sanskritree/`; its activation gates are in `docs/PIPELINE_ACTIVATION.md`.

Truth compressor: decomposes Sanskrit philosophical claims into Lean4 proofs or honest boundary findings. Per `proofenginge.md` and `instruction.md`.

## What It Does

- Takes claims from Sanskrit texts (Nyaya, Shiva Sutras, Tantraloka)
- Recursively decomposes until: **PROVED** (Lean4), **OUTSIDE_FORMAL** (empirical), or **HOLLOW** (unsayable)
- Output: node graph with traceable paths. High `reuse_count` = centre nodes.

**Critical**: No bias toward proofs. PARTIAL and OUTSIDE_FORMAL are correct when the text doesn't support formalization.

## Quick Start

```bash
pip install -r requirements.txt
python run_proof_engine.py
```

## Structure

```
proof_engine/
  db.py           - SQLite schema, node CRUD
  api.py          - LeanSearch, Loogle HTTP clients
  lean_checker.py - Pantograph/fallback Lean4 checker
  fol_lean_bridge.py - FOL -> Lean4 (Navya-Nyaya operators)
  algorithm.py    - 5-step core: Sayability -> Library -> Formalize -> Prove -> Decompose
  sanskrit_pipeline.py - Heritage/SanskritShala pipeline
  phase1_nyaya.py - Phase 1: Nyaya-Sutras validation
run_proof_engine.py - CLI entry point
```

## Phase 1 Terms (Nyaya)

1. **pramana** - valid means of cognition
2. **samsaya** - doubt
3. **vyapti** - universal concomitance (core inference principle)
4. **anumana** - five-membered
