# THREADS — consolidated 2026-09-10 (the organized board; SESSION_REVIEW has the story)

## T0 — STANDING GOAL (owner-set, overrides all prioritization)

**Make me money.** Every bout, build, thread, and approval ladders to it.
Revenue test for new work: does this raise expected revenue or cut the cost
of finding out? If neither, it stays PROPOSED. Bouts optimize for revenue
evidence, not suite-count theatre. Full session record: `docs/SESSION_REVIEW.md`.

## BLOCKED — needs human or money (exact approval strings, demos in packet)

- **H1b**: CLOSED — fa478bb pushed, origin in sync (verified via ls-remote).
- **H2**: revoke read-scoped `ghp_…` token (shell history). Owner clicks in
  GitHub settings. Urgency rising (scope confirmed read-only, still clones).
- **H6**: rename `elapsed_s` → `score_elapsed_s` (log schema change). Say `go H6`.
- **H-driver**: pick D1 (cron+`opencode run`) / D2 (hermes-cron) / D3 (manual
  pulses). Needs quota math first (M-class). KILL-file convention specced.
- **M4-run**: live metered bout (first honest cost comparison). Cost ~$0 free
  tier, burns daily neurons. Say `go M4`.
- **a-push**: PAUSED task, rides H1b automatically.
- **H-inbox**: built and listening (`hserver.py:8791`), awaiting first human
  traffic; urgency-weight calibration needs real data, not theory.

## READY — none (halt-legal; A-backlog empty per dryness rule)
Next agent motion triggers on: any approval above, any user message (resumes
queue first per BOOT), or newly scheduled JUSTIFIED tasks below.

## BACKLOG — proposed, unscheduled (parent in parens; schedule with full §7 justification)

- **B1** funnel Meter/SPEND_LOG wiring — DONE (spend.jsonl per attempt,
  honest-zero tokens; funnel subprocess spend still unobservable by nature).
- **B2** urgency-weight calibration (needs H-traffic; do not theorize).
- **B3** unlock-value weighting — DONE (`value_usd` counts as priority
  points, documented policy; hplane ranks revenue-first).
- **B4** BATS full ladder port (tiers exist; escalation policy partial).
- **B5** grant `activate()` ← inbox resolve wiring (human button → live grant).
- **B6** hserver auth/TLS note (localhost-only is the whole model; restate before any exposure).
- **B7** evidence tiebreak hardening — avatars/measurement only after scoring
  is luck-free (flow-test verdict).
- **B8** bout2 demand-side slice — DONE (T39, de-primed brief).
- **B9** eval_arch ran on bout3 winner (load-bearing verdict); csec packs on
  winners STILL OPEN.
- **B10** T5 HUMAN_LOOP checkpoint wiring (oldest open thread, carried over).
- **B11** learn.py real-bout promotion — DONE (fired on meta-tourney:
  2 failures → 1 criteria0 proposal).

## CLOSED this session (proof in loop/ receipts + SESSION_REVIEW §2)

T1 self-compliance · T2 weights prereg · T3 blind review · T4 learn-on-real-data
(bout1 zero-fail, honestly reported) · T6 ham v1 · T7 endgame spec · T8 audit ·
T9 META_LOOP + loop.py · T10 hardening (REPORTED guard, `set` cmd) · T11
continuity rules · T12 driver gap + BOOT · T13 registries spec · T14 registries
built · T15 flow-test · T16 control plane (git bus proven, hplane live) · T17 meta-tourney (H1 0v2, H2 1v5, metaguide+ruler) · T18 peer review (10 todos: luck proven, blind leak fixed) · T19 chain1 CLOSED (northstar→seed1.1→branches→stoplight→rerun→packet, 6/6 GO) · T20 canonical A-catalog (PRIMITIVES Part II, 33 things) · T21 ip-graph review (links verified, S1–S12 steals, kanban machinery deep dive, no visions skill found) · T22 cg-grade routines (R1–R6 + WHEN + combos) · T23 e2e on make-me-money (rail DOWN found, 2 H filed, M empty, $0) · T24 a-goal machinery (ready/branch/history + live fire green) · T25 frontier validation (compatible + 4 novelties + 5 gaps) + evidence-backed A-logs · T26 clone-and-use (zero-deps test + read-only MCP + save_all restore+tripwire) · T27 A→H promotion path (lowest-barrier enforced, grandfather rule) · T28 hserver funnel route (multi-repo view, dark ranks top) · T29 NORTHSTAR frozen (ingest→goal→branches→validator-stop) · T30 git-native (scaffold inits, map renders, Letta/ait/lanes mined, S17–S23) · T31 MemFS vendored + M-failsafe L0–L7 + mw cred-hygiene finding · T32 arXiv git frontier (GCC/GitOfThoughts/STORM/Ledger/OpenWeft, S24–S34, context cmd) · T33 steals wave implemented (11 mechanisms, all tested) · T34 cold-start sim (clone works for old tree; 158 paths unpushed = H1b is deliverability) · T35 money tournament (5 lanes exit 0, EICR convergence, receipt-id incident mechanized) · T36 log hygiene + metering audit · T37 per-case metering live (429s persist, $0.00) · T38 repo audit (12/6/5) + money-rail goal worked (rail DOWN, quota 429, spend zero) · T39 bout2 demand-side (de-primed brief → boilers ×3, partial success, GO confirmed) · T40 bout3 pure-mechanism (domain gone, linear family = evolution not priming) · T41 full doc re-read (36 files, rot fixed ×12, packet reconciled) · T42 autonomous batch (a-push closed, B4 escalation, S20 dirty-refusal, parser fix, M-watch 429) · T43 OTel-shim spans live (funnel+pyeval wired) + T0 money repeat (domain divergence, datacenter ×2) · T44 gold-star saved + measured runner + strict guide (5 stubs timed live) · T45 B5 grant-activation wired (button IS release, deny moves nothing) · T46 multibox funnel (git mirrors + labels, dead-box safe) · CWD gate (10 bugs) · scanner self-matches (3).
