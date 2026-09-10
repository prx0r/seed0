# a-registries — progress report

## 1. claim
Registry-v2 spec banked with verified imports; 3-stream design closed.

## 2. evidence
`docs/REGISTRIES.md` (7 sections). WorkerKit money stack read at source
(05119b2: treasury/bats/broker/registry + x402 provider). x402 bundle
confirmed live ($0.005 exact-amount mainnet). mw queue.html POSTs grepped
(retargetable). tasks.py blocked_by confirmed as graph substrate. Frontier:
HumanLayer (pattern), AIP/IBCT integer-cents, Temporal (rejected with
reasons), Ravi poll-inbox (validates our poll-not-block inversion).

## 3. self-review
No code written — spec only. Unlock-value weighting function unspecified
(count vs value judgment left to build). HumanLayer schema compatibility
claimed, not tested against their SDK.

## 4. needs
Build tasks queued as ready A-work (§7 items 1–3). M-run stays queued.

## 5. cost
$0 (reads + searches), no manual actions.
