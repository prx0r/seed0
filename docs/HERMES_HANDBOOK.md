# HERMES HANDBOOK — operating the agent (distilled from llms-full, 2026-09-10)

Full corpus: `docs/vendor/hermes-llms-full.txt` (4.2MB). This page is the 5-minute
operator cut: sessions, skills, kanban, cron, safety. Canonical docs win on conflict.

## 1. Sessions (never lose work)
- Interactive: `hermes` (TUI) or `hermes --cli`. Resume: `--resume [SESSION|latest|./dir]`.
- One-shot for automation: `hermes -q "prompt"` (single query, exits; adapter pattern).
- Crash safety: checkpoints + `/rollback`; background sessions survive disconnects.
- Rule: long work always resumable — name sessions per project directory.

## 2. Skills (procedural memory, agentskills.io-compatible)
- Preload at launch, invoke by slash command, or let the agent self-create them
  after complex tasks (they self-improve during use; writes are approval-gated).
- Two sources merge: managed skills + `~/.hermes/skills/` (read-only native).
- Rule: repeating yourself twice = write a skill. Skill writes need approval.

## 3. Kanban (multi-agent board — the fleet primitive)
- Durable SQLite board (`~/.hermes/kanban.db`, per-board DBs); tasks flow
  `triage|todo|ready|running|blocked|review|done|archived`, deps via links.
- Agents use `kanban_*` tools (claim/complete/block/comment/heartbeat); humans use
  `hermes kanban` CLI + dashboard. Same DB, consistent view.
- Workspaces: `scratch` (ephemeral, deleted on done — declare artifacts to keep),
  `dir:<abspath>` (preserved), `worktree[:path]` (preserved, for coding).
- Completion contracts: declare PR URLs at creation; required checks must be green —
  a commit alone never completes a card. Block (don't fake-done) on human need.
- Use Kanban (not `delegate_task`) when work crosses agents, must survive restarts,
  or needs humans. `delegate_task` = function call; Kanban = durable queue.
- Budgets: finite iterations + 90% checkpoint notice; per-task model override.

## 4. Cron + hooks + profiles
- Cron: natural-language schedules with platform delivery; child sessions fall back
  gracefully. Stale sessions from automation get reaped — don't fight it.
- Hooks: `~/.hermes/hooks/` (event → handler.py) for alerts/logging; e.g. long-task
  alerts, command logging, kanban claimed/completed/blocked events.
- Profiles: named identities with descriptions so orchestrators can route
  (`--description "<role>"`); per-task model override on the board.

## 5. Safety knobs that matter
- Command approval + container isolation; secret redaction ON (leave it on).
- Iteration budgets + circuit breaker (auto-blocks after repeated spawn failures).
- Contributor-tier models train on your prompts — never send customer data there.
- Session/token usage is metered: watch `hermes status`, set budgets on fleets.

## 6. Models + providers + MCP + voice
- 8 providers; switch with `hermes model`, no code changes. Pin per task, not globally.
- MCP client: connect any server, filter tools aggressively (least privilege).
- Voice mode: CLI/Telegram/Discord; TTS/STT configured, not magic.
- Multi-provider = quota strategy: route bulk work to cheap/fast models, reserve
  frontier for judgment calls. Record which model did what (tournament substrate field).
