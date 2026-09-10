# prx0r/ip-graph

sha=2ac554bc345d0c35047e6349ef22fc93b4d26515

## README excerpt

# OPENPATALAPROJECT — the open Sanskrit translation graph

*2026-08-16 · one self-contained project: for each Sanskrit work, find the actual translations, prove they're
downloadable, tier them, serve them via a FastAPI, and verify the pipeline didn't make a mistake.*

**Read `AGENTS.md` first.** This is the entry point.

---

## What it does

```
Muktabodha/GRETIL text
   → extract verses            (harvest_to_factory, dedup + ||N/N|| fix)
   → find translation editions (translation_deepfinder: OpenLibrary + archive.org + variants)
   → prove downloadable + tier (translation_download: A/B/C + evidence ladder + language matrix)
   → compile the index         (pipeline/build_translation_availability.py → 257-work index)
   → serve via FastAPI         (python/patala_core/atlas/api.py: /works/{id}/translations, /traditions, /editions, /bundle, /download)
   → verify the pipeline       (pipeline_verify.py → pipeline-audit.jsonl)
```

## Quick start

```bash
cd /root/openpatalaproject
PY=/root/patalacheckpoints/.venv-atlas/bin/python   # the lxml host (no project-local venv)

# 1. compile the enriched index (needs lxml → the shared venv)
$PY pipeline/build_translation_availability.py --work tantraloka
#    or: make compile-one WORK=tantraloka

# 2. serve the API (backgrounded)
make serve        # = PYTHONPATH=... python ... -m uvicorn patala_core.atlas.api:app --port 8800

curl localhost:8800/works/tantraloka/translations
curl localhost:8800/traditions
curl "localhost:8800/edition
