# prx0r/agentic-infra

sha=f2345195582be215f4204a22bb5246b4f24c7fb8
proto=['MANIFEST', 'check.py', 'pipeline', 'agent']

## README

# AGENTIC-INFRA — the reusable agentic operating system (objective scaffolding)

*2026-08-16 · A reusable, objective scaffolding for building **agent-runnable, self-organizing,
handover-able projects** with Hermes. Extracted from the sanskritbenchy build — the pattern that lets an
agent work autonomously, stay organized, and hand over cleanly. Use this to stand up ANY new project:
copy it, fill in your domain, and it's immediately agent-runnable.*

---

## 1. WHAT THIS IS (and isn't)

- **IS:** the reusable structure + conventions + gates + verification spine + handover template that every
  agent-runnable project needs. Copy it, add your domain kernels, and you have a working agent-driven lab.
- **ISN'T:** a specific domain. This is the empty harness — the "how an agent operates," not "what it
  builds." (sanskritbenchy is the worked example of this scaffolding; it lives in `/root/sanskritbenchy`.)

---

## 2. THE STRUCTURE (copy this for a new project)

```
agentic-infra/            → copy as the skeleton of your project
  AGENTS.md               → the governing rules + the anti-mess standard
  CODING-AGENT.md         → the strict operational discipline
  HANDSOVER-TEMPLATE.md   → the canonical handover spec
  check.py                → the drift gate (manifest + refs + data)
  MANIFEST.json           → the machine resolver
  agent/                  → run.py · verify.py · audit.py · trace.py · memory.py · ramwatch.py
  pipeline/               → schemas.py · run_recorder.py ·
