# VENDORED — syncing-memory-filesystem SKILL.md (Letta)

Source: https://github.com/letta-ai/letta-code/blob/main/src/skills/builtin/syncing-memory-filesystem/SKILL.md
License: Apache-2.0 (letta-code repo). Vendored 2026-09-10 for pattern reference.
DO NOT EDIT below this header (upstream changes re-fetched, not hand-merged).

---
name: syncing-memory-filesystem
description: Diagnose and repair MemFS repository setup, remote sync, authentication failures, optional backup remotes, or merge/rebase conflicts. Do not load for routine memory reads or edits.
---

# MemFS Repository Repair

Use this skill only when the Git repository behind an agent's memory is not
setting up or syncing correctly. For ordinary memory reads and edits, use the
memory files or the memory tools without loading this skill.

## Current Model

MemFS is a Git repository projected onto the computer where the agent is
running. `$MEMORY_DIR` is the repository root. There is no second `memory/`
directory inside it.

The repository can use either memory layout. Inspect its current tree and the
memory rules in the system prompt before editing files:

```text
Root layout                         Existing layout
$MEMORY_DIR/                        $MEMORY_DIR/
├── MEMORY.md     # root index      ├── system/     # in-context memory
├── persona.md    # core memory     ├── reference/  # deferred memory
├── <topic>/                        └── skills/     # agent-owned skills
│   └── MEMORY.md # child index
└── skills/       # agent-owned skills
```

Cloud-backed agents have a hosted MemFS remote. Local-backend agents keep a
local-only Git repository and do not need a remote or cloud credentials.

The memory tools commit their changes. After each turn, the harness pushes
clean committed changes for cloud-backed agents. Local-backend commits remain
on the current machine. Do not run `git push` for normal MemFS sync; let the
harness push after the turn.

Committed memory changes do not alter the current compiled prompt immediately.
Use `/recompile` when the current conversation must see changed core memory
right away. Otherwise, the next prompt compilation or compilation will use
the committed revision.

## Start With the Harness

Prefer the harness commands over manual API calls, remote construction, or
credential-helper edits:

```text
/memfs status    # show whether MemFS is enabled and its path
/memfs sync      # pull the hosted repository
/memfs enable    # initialize or repair MemFS setup
```

From a shell, the standalone status and pull commands are:

```bash
letta memory status --agent "$AGENT_ID"
letta memory pull --agent "$AGENT_ID"
```

`letta memory pull` is a no-op for a local-backend agent because there is no
hosted remote.

Do not reproduce `/memfs enable` by PATCHing agent tags or constructing a Git
remote by hand. The enable flow also updates the system prompt mode, recompiles
the agent, persists local settings, detaches legacy memory tools, preserves and
adds tags, initializes the checkout, installs hooks, configures identity, and
seeds default memory files.

## Inspect a Broken Checkout

Use `$MEMORY_DIR` instead of a hard-coded path. Local and cloud-backed agents
use different parent directories.

```bash
git -C "$MEMORY_DIR" status --short --branch
git -C "$MEMORY_DIR" remote get-url origin | sed -E 's#(https?://)[^/@]+@#\1<redacted>@#'
git -C "$MEMORY_DIR" log -5 --oneline
```

Do not print credential-helper values or tokens. Do not change global Git
configuration.

## Uncommitted Changes

Raw file edits must preserve the active layout's rules. In the root layout,
root and child `MEMORY.md` indexes have no frontmatter; every other memory
Markdown file has exactly `name` and `description`. Stage named memory files
only and create a new commit. Review the complete diff before committing.

## Merge or Rebase Conflicts

Fast-forward pull first; on rejection, `git pull --rebase` and retry. If the
rebase conflicts, leave for manual resolution with affected files reported.
Do not start a new merge when a rebase is already in progress. Do not reset,
abort, or discard either side without the user's approval.

## Optional Backup Remote

`/memory-repository` mirrors `main` to an additional Git URL via post-commit
hook (failures never block commits). Never embed tokens in URLs.

## Failure Checklist

1. Confirm `$MEMORY_DIR` points to the active agent's repository.
2. Check backend: cloud-backed or local-only.
3. Inspect `git status`, origin URL, and current Git operation.
4. `/memfs enable` for missing checkout, `/memfs sync` for pull.
5. Preserve indexes/frontmatter, finish existing merges first.
6. Leave hosted pushes to post-turn sync once clean.
7. Rerun with `LETTA_DEBUG=1` on failure; never print credential values.

## Why vendored (our take)

Harness-over-manual (commands, not API surgery); redaction discipline
(`sed` the userinfo, never print helpers); per-repo identity + hooks;
background mirror that never blocks commits; conflicts surface to human,
never auto-resolved destructively. Every one of these maps onto our
BOOT/queue/branch discipline — see GITNATIVE S-steals.
