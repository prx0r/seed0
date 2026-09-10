# a-hqueue — progress report

## 1. claim
hqueue.html + hserver.py live: pending/resolve roundtrip over localhost; UI
renders priority-ordered cards with approve/deny buttons.

## 2. evidence
`tests/test_hserver.py`: live-socket roundtrip (pending lists, resolve
approves, queue empties, double-resolve 400, `/` serves UI). Ported from mw
queue.html aesthetic + dashboard_server.py stdlib pattern; POSTs retargeted
`/api/vault/set` → `/api/h/resolve`. Localhost-only bind (127.0.0.1).

## 3. self-review
No auth on the server — localhost-only is the entire security model. Fine for
v1 (human's own browser), must be stated: never expose this port. No TLS.

## 4. needs
None. No H/M discovered.

## 5. cost
$0, no manual actions.
