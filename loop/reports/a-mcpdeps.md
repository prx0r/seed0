# a-mcpdeps — progress report

## 1. claim
Clone-and-use complete: zero-deps proven by test, MCP server live with
round-trip tests, config documented.

## 2. evidence
- `tests/test_nodeps.py`: AST-walks every root module, asserts stdlib-only
  (2 passed). Adding a third-party import breaks it on purpose.
- `mcp_server.py`: initialize/list/call/ping over stdio; 6 read-only tools
  (check, list, ready, stoplight, history, ham check). `tests/test_mcp.py`:
  real-subprocess round trips (COMPLIANT text, NOGO ghost, PROHIBITED force-
  push, unknown-tool error code). No writes exposed — connecting it cannot
  approve, mutate, or spend (stated in docstring + RECIPES).
- `docs/RECIPES.md`: opencode.json snippet. Deps section states Python 3.11+.
- Mystery interim: `save_all` went missing with green tests behind it —
  restored + `test_public_api_intact` tripwire added (14 loop tests green).
  Cause unproven; tripwire prevents recurrence regardless.

## 3. self-review
MCP surface untested against a real client (Claude Code/opencode MCP host) —
stdio round-trip is protocol-level, not integration. No auth on stdio (local
pipe is the trust boundary — same model as hserver; stated).

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
