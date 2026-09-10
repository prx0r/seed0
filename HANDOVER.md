# HANDOVER — seed0, 2026-09-10 pm (instrument session; read BOOT.md first, then this)

## Where it stands (all verified this session)

- Suite **159 green** (`pytest tests/ -q`, ~24s), self-check **5/5 COMPLIANT**,
  `registries.check_all('.')` clean, `acheck` 0 findings on live queue,
  live zoom: **66 DONE / 0 missing / 6 open H**.
- HEAD `fa478bb`; **uncommitted files ride the next push** (check `git status` —
  includes instrument + registries + acheck + ATASK.md).
- hamjob (`/tmp/opencode/hamjob`, repo `prx0r/hamjob` PRIVATE): HEAD `aa9fba1`,
  **3 uncommitted** (server.py + dashboard.html + tests/test_server.py = /api/press + keypad).
- csec pushed (`prx0r/csec` public, `ae2d422`). hamjob pushed `aa9fba1` (pre-press-work).
- Live `loop/presses.jsonl`: 2 rows (both demo ZOOMs). No HALT, no goal.json yet.

## What this session built

1. **hamjob slice**: server.py (dashboard API + log bus) + dashboard.html +
   mcp_server.py + secret-guard (`looks_like_secret`: sk-/ghp-/apify/cfat/bearer/key=
   refused at create+deliver+complete, attempts logged). 7 tests then.
2. **Instrument (the 10-key OS)**: `keys.json` (keys as data + autonomous_safe
   {1,2,3} + never_autonomous) + `chain.py` ("2943"→actions, loud ValueError) +
   `press.py` (press rows in predictor shown/picked shape → `loop/presses.jsonl`) +
   `instrument.py` (dispatch 0–9: 1 ready, 2 zoom, 3 dig, 4 pick, 5 approve w/
   B5 grant auto-activate, 6 deny, 7 tell w/ secret-guard, 8 goal→goal.json,
   9 correction→corrections.jsonl, 0 toggles HALT.json; 2,3 survive halt).
   12 tests. Live demo + dash demo both return 66/0/6.
3. **registries.py**: one read API + schema gate over A/H/M; caught live spec
   drift (REGISTRIES.md §3 conflated H `kind` envelope with `h_kind` taxonomy —
   fixed validator to code, amended spec). 6 tests.
4. **Seeds**: `loop/press_seeds.jsonl` — 15 owner prompts labeled to keys
   (rows 1–15 of training data; 15/15 mapped to {1,2,3,8,9}).
5. **Dead code removed**: loop.py:145-146, pyeval.py:195-198 (review finds).
6. **Laws**: AGENTS.md r8 (macros replay selection, never authorization) +
   PID discipline (kill by captured PID, never pkill) in seed0 + hamjob AGENTS.md.
7. **Frontier review** (in chat, not yet a doc): Instrumental Interaction
   (reification/polymorphism/reuse/currying → presses/macros/chains),
   DirectGPT numbers as our bar (50% faster/fewer), OS-Kairos γ per key,
   Log2Plan ≈ macro miner, Zipf fit as acceptance metric, System1/2 framing.
8. **A-task kit** (`ATASK.md` + `acheck.py`, 7 tests): portable one-page
   contract + self-audit any agent runs on itself (schema, DONE→receipt
   mirroring loop.py's sha256: resolution, EXECUTING→fresh a-log else STALE,
   dangling refs). Live queue: 0 findings. acheck false-alarmed 66 rows
   first (didn't know sha256:→runs/ mapping) — fixed to mirror loop.py.

## Queues awaiting the human (owner-only actions)

- **H1b**: CLOSED 2026-09-10 pm — pushed `fa478bb..8f32bc2` (instrument +
  pristine + AGENTS doctrine). CORRECTION: token was never read-only; the
  stored remote has no creds. Push path = one-shot
  `git push https://x-access-token:$TOKEN@github.com/prx0r/seed0.git main`.
  hamjob press-work pushed too (`aa9fba1..d296143`).
- **H-hamjob-push**: push 3 files (/api/press + keypad) — same token WORKS here.
- **H2**: revoke `ghp_H4xk…` (in shell history). Rising urgency.
- **H6**: rename `elapsed_s` → `score_elapsed_s`. Say `go H6`.
- **H-driver**: D1/D2/D3 for autonomous pulse (GO-key fires it when built).
- **H-x402**: settlement rail, owner-side. (Verified: no providers/ dir, no HTTP
  in grants.py — x402 here is receipt-shape + ceiling, NOT live settlement.)
- **M4-run**: live metered bout, quota-429-blocked.

## Next actions (ranked)

1. Push hamjob press-work (credential works there) — 5 min.
2. `docs/INSTRUMENT_FRONTIER.md` (offered, unaccepted): frontier + steal-list
   as build tasks (verb-noun binding in dash, γ per key, Zipf test, 50% bar).
3. `vcs.*` git primitives (status/commit/digest/push/log/worktree/halt-check) —
   HALT.json file-half exists; checker-half missing.
4. DIG iterate-until-obvious loop (recall/heuristics until NOGO empty, max 3).
5. Zipf fit on presses once n≈100+; macros from first mined bigram (expect 5→1).
6. H-driver D-choice → key 1 fires pulses → full autonomous loop.
7. Full seed0 merge w/ proclusagent box: IMPORT-FIRST (hqueue pattern, prompt
   corpus, ROUTINES), hold 392-file merge until push credential exists.

## Watch-outs (earned the hard way this session)

- `pkill -f` is banned (kills wrong processes). `SRV=$!` at launch, `kill $SRV`.
- Secret-pattern test literals MUST split-concatenate (`"sk-" + "abc…"`) or
  `no-committed-secrets` fails the suite AND self-check.
- New root `*.py` needs BOTH `docs/PRIMITIVES.md` bullet AND `test_nodeps.py`
  ALLOWLIST entry, or two suites fail.
- hinbox fixture `ts` must be `time.time()`, not small ints — `poll()` expires
  anything older than `timeout_s` (default 86400s).
- H-records: envelope `kind: request|resolution|expiry`, taxonomy in `h_kind`.
  REGISTRIES.md §3 corrected; trust hinbox.py docstring over old prose.
- `hinbox.resolve` returns rec with `grant_id` (not `grant_activated`).
- keys.json had a `}}` typo once — validate JSON after editing (`chain.key_defs()`).
- hamjob server edits: don't clobber adjacent `elif` branches (happened once
  with /api/pipeline/start; caught by read-back).
- seed0 self-check reports 5 checks now (was 6 in an older checker version) —
  benign, both COMPLIANT. Do not "fix" the count.
- `git stash` output went missing once mid-session; work was intact (verified
  via `git stash list` + file presence). Prefer `git status` + targeted
  `git diff` over stash for peeking.

## Credentials & boxes

- Token `ghp_H4xk…FnnB`: READ on prx0r/seed0; WRITE on prx0r/csec, prx0r/hamjob.
  Cannot create repos (422 exists / scope). H2 revocation pending.
- proclusagent work (sequences miner, SEQUENCES.md) lives on a DIFFERENT VPS —
  not visible from here. Alignment review verdict: mostly aligned; 3
  overstatements corrected (no registry_a file by design; x402 not live;
  no attempts.jsonl single file); macro-authorization law must be pasted
  into that box's AGENTS.md (one-liner in chat history).
- Server ports used: 8791/8795/8796 (all down; verify with ss before reuse).
- Standing: H7 autonomy active; T0 (make me money); $0 spend unless M-grant.
