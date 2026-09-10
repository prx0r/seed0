# a-metering-design — progress report

## 1. claim
Metering enforced (not advertised): per-call spend lines + refusal paths tested.

## 2. evidence
Acceptance mapping: (1) wrap calls metering tokens — `metered_call()` in
grants.py + `SPEND_LOG` hook in pyeval.complete (env-gated, default off,
existing tests unaffected); stubbed-urlopen test proves per-call lines with
zero network. (2) budget enforced — grant ceiling + treasury refusals raise
GrantDenied (test_grants), i.e. over-spend is structurally impossible, not
just logged. (3) no network — all new tests stubbed/localhost.

## 3. self-review
pyeval hook is opt-in via env (safe default, weaker coverage). Funnel Meter
still unfed for agent subprocesses (can't meter what you can't observe —
stated, not hidden). Wiring SPEND_LOG into funnel receipts is follow-up.

## 4. needs
M-run (live metered bout) stays queued.

## 5. cost
$0, no manual actions.
