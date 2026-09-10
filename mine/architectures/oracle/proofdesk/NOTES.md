# prx0r/proofdesk

sha=d7f37d0a432f7ddb3367655018246bd63a31514d
proto=[]

## README

# ProofDesk

**Your agent shouldn't sign that.**

[![Hackathon](https://img.shields.io/badge/DevNetwork_API%2BCloud%2BAI_Hackathon-2026-blue)](https://api-cloud-ai-hackathon-2026.devpost.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-115_passing-brightgreen)](#tests)
[![Nutrient](https://img.shields.io/badge/Nutrient_DWS-Integrated-blue)](#nutrient-dws-integration)

> Two documents are individually read correctly. Together they describe a transaction that should not happen. The AI refuses to act.

**[Watch Demo](https://youtu.be/LWN3qNX-hk4)** | **[Try Live Demo](https://proofdesk-90q.pages.dev)** | **[View Source](https://github.com/prx0r/proofdesk)**

---

## Judge in 30 Seconds

**Sponsor API:** [Nutrient DWS](https://nutrient.io) — extracts grounded evidence from source PDFs with value, confidence, page, and bounding-box provenance. Not just text — sourced, scored evidence.

**Core workflow:**
```
High-confidence fact A (from Nutrient DWS extraction)
  + High-confidence fact B (from Nutrient DWS extraction)
  → Cross-document contradiction detected
  → AUTHORITY BLOCKED
  → Human examines the exact evidence
  → Explicit resolution
  → Approved hashed record
  → Tamper-evident audit receipt (hash chain + Merkle proofs)
```

**The magic moment:** Two documents pass extraction individually. But together they describe a transaction that should not happen. ProofDesk detects the contradiction and
