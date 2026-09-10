# prx0r/qdw-workbench

sha=ee4cc18cd28d6dea21889bbfa0eb4da3b7d5262d

## README excerpt

# QDW Workbench

A lightweight Tauri 2 control plane and coding workbench for QDW.

QDW Workbench is deliberately **not another agent framework** and not another QDW kernel. It is the human surface over canonical QDW state plus a replaceable workstation/VPS execution daemon (`qdw-node`). Hermes is the primary agent runtime through ACP; other ACP-compatible runtimes can be attached without changing Workbench semantics.

## Goals

- Open one desktop app and immediately know the state of the QDW estate.
- Switch between local and remote workspaces without rebuilding project context manually.
- See products, factories, work graphs, verification, human approvals, nodes, CPU/RAM, costs, agent runs and context usage in one place.
- Compile task-specific agent context from QDW doctrine + code + memory + current evidence instead of dumping entire repositories into a prompt.
- Preserve session handovers as timestamped, hashed artifacts when a context window approaches its limit or a user ends a session.
- Treat human approvals as canonical QDW HumanQueue transitions, never frontend-only state.
- Keep the laptop light: no Electron, no mandatory Docker, Redis, Postgres, ClickHouse or background Chromium.

## Architecture

```text
Tauri Workbench
  ├── QDW bridge -> canonical QDWSystem / ledger / HumanQueue / Products
  ├── qdw-node local
  ├── qdw-node remote through SSH tunnels
  └── ACP host
       ├── hermes acp
       ├── Codex/other ACP agents
       └── future runtimes

qdw-node
  
