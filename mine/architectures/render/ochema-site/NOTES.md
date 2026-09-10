# prx0r/ochema-site

sha=a2af73900aaac3aad8b8f52889acb1c7c37e87b1
proto=[]

## README

# Ochema Site

The Ochema corpus on the web: essays, the what-the-heck-is series, and the films.

## Content pipeline

- `data/curation.json` — which essays are featured (edit to curate)
- `scripts/sync-content.mjs` — copies curated essays from `/root/projects/ochema` into `content/bundle.json` (run on the dev box, commit the result); also writes `data/thesis.json` from the thesis object's `meta/ro.json` (current version)
- `scripts/gen-maps.mjs` — regenerates `data/concepts.json` + `data/confrontations.json` (full records + verdicts, parsed from the confrontation files and REGISTRY.md)
- `scripts/gen-works.mjs` — regenerates `data/works.json` from the film-library DB (requires node ≥22 for `node:sqlite`)
- `scripts/reconfront.mjs` — the peer-review loop: re-run a confrontation against the current thesis version
  - `node scripts/reconfront.mjs --stale` — list records whose thesis version predates the current one
  - `node scripts/reconfront.mjs <slug>` — write `<slug>.rerun.md` work order for re-grading
  - `node scripts/reconfront.mjs --all` — write work orders for every stale record
- `data/videos.json` — the film manifest (R2 public URLs)

## Re-running confrontations (the living-thesis loop)

The thesis is versioned (`the-occhema-object/meta/ro.json`). Every confrontation
records the version it was judged against (`Added in: vX.Y.Z`). When the thesis
bumps, run `node scripts/reconfront.mjs --stale` to see which verdicts are stale,
then re-grade each against the current t
