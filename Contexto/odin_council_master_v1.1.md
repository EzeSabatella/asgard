# ODIN COUNCIL — Master Project Document
**Version:** 1.1  
**Date:** 2026-01-17  
**Owner:** Ezequiel Sabatella (Odin)  
**Status:** Pre-Development (Sprint 0)
**Changelog:** v1.1 — Agregada Sección 16: Validación Estratégica y Preguntas Abiertas

---

## 📋 Tabla de Contenidos
1. [Executive Summary](#executive-summary)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Vision & Differentiation](#vision--differentiation)
4. [Product Definition](#product-definition)
5. [Target Market (ICP)](#target-market-icp)
6. [System Architecture](#system-architecture)
7. [Team Roles & Responsibilities](#team-roles--responsibilities)
8. [Governance Framework](#governance-framework)
9. [Project Brain Structure](#project-brain-structure)
10. [Workflow & Protocols](#workflow--protocols)
11. [Quality Assurance Strategy](#quality-assurance-strategy)
12. [Economic Model](#economic-model)
13. [Roadmap](#roadmap)
14. [Risk Registry](#risk-registry)
15. [Success Metrics](#success-metrics)
16. [Validación Estratégica y Preguntas Abiertas](#validación-estratégica-y-preguntas-abiertas) ⭐ NUEVO
17. [Decision Log (Foundational)](#decision-log-foundational)

---

## 1. Executive Summary

**ODIN Council** is a collaborative AI agent platform that transforms multiple specialized AI models into a coordinated development team with shared memory, role-based handoffs, and evidence-based quality assurance.

**Core Innovation:**  
We don't compete on "better autocomplete" or "faster code generation." We compete on **governance, traceability, and team coordination** for complex, multi-week software projects.

**Business Model:**  
SaaS subscription ($50-500/month) targeting technical teams building complex products where context loss and coordination overhead are major pain points.

**Current Stage:**  
Sprint 0 — Defining architecture, contracts, and foundational decisions before writing code.

**6-Week Goal:**  
Launch MVP with 10 paying beta users generating $200-500 MRR.

---

## 2. The Problem We're Solving

### The Universal Pain of Multi-Model AI Development

When developers use multiple AI models in parallel (Claude, Gemini, Grok, etc.) to build complex projects, they face:

1. **Context Loss:**  
   - Manual copy-paste of context between models
   - Each model starts from zero knowledge
   - No shared memory across conversations

2. **Coordination Overhead:**  
   - Human acts as manual orchestrator
   - Inputs remain disconnected
   - No clear handoff protocol

3. **Lost Traceability:**  
   - Decisions live in chat history
   - No single source of truth
   - Impossible to audit "why did we choose X?"

4. **Theoretical QA:**  
   - AI says "this code should work"
   - No evidence of actual execution
   - Bugs discovered only in production

5. **Integration Burden:**  
   - Human must merge outputs from 5 different models
   - Inconsistent coding styles
   - Architectural misalignment

### Why Existing Solutions Don't Solve This

| Tool | What It Does | What It Doesn't Do |
|------|-------------|-------------------|
| **Cursor** | Fast coding with AI autocomplete | No team coordination, no shared memory, no role specialization |
| **GitHub Copilot** | Code suggestions in IDE | No project-level context, no QA validation, no decision tracking |
| **ChatGPT/Claude Solo** | One model, one conversation | No multi-agent collaboration, context limited to single thread |
| **LangChain Agents** | Developer framework for AI workflows | Requires coding, no out-of-box UI, no governance layer |

**ODIN Council fills the gap:** Pre-built team coordination with governance and evidence-based QA for complex builds.

---

## 3. Vision & Differentiation

### Vision Statement

> "ODIN Council is Slack for AI agents — a workspace where specialized models collaborate with shared memory, clear roles, and governance to build software that actually works."

### Core Differentiators

1. **Role-Based Specialization**  
   - Not "one AI does everything"
   - Builder, QA, Architect, Orchestrator — each with clear responsibilities
   - Optimized prompts per role (not just different models)

2. **Project Brain (Shared Memory)**  
   - Living documentation: Architecture, Decisions, Contracts
   - Version-controlled, retrieval-augmented context
   - Single source of truth for all agents

3. **Evidence-Based QA**  
   - Not "I think this works" → "CI logs prove this works"
   - GitHub Actions integration (Mode A)
   - Future: Local runner + cloud sandbox

4. **Governance Layer (Decisions.log)**  
   - Every architectural decision is logged
   - Traceability: who decided what, when, why
   - Auditable for compliance-heavy industries

5. **Handoff Protocol**  
   - Clear transition points: Build → Review → QA → Integrate
   - Prevents infinite loops and context drift
   - Escalation to human when stuck

### Market Positioning

```
Complexity of Project
│
│  ODIN COUNCIL
│  (Multi-week builds)
│       ↑
│       │
│    Cursor
│    (Daily tasks)
│       ↑
│       │
│  Copilot
│  (Line-by-line)
│
└────────────────────→ Coordination Need
```

**We win where:**  
- Projects take 3+ weeks  
- Multiple systems/integrations  
- Team of 2-5 devs  
- Compliance/audit requirements  

**We lose where:**  
- Solo dev, simple MVP  
- Speed > governance  
- Budget < $50/month  

---

## 4. Product Definition

### MVP v1 (6-Week Deliverable)

**Core Features:**

1. **Multi-Project Workspace**  
   - Create unlimited projects
   - Each project has its own Brain + Decisions

2. **Threaded Conversations**  
   - Group chat interface with AI agents as "members"
   - Real-time responses from assigned models
   - Message history with context preservation

3. **Multi-Model Adapters**  
   - Support for: OpenAI, Anthropic, Google, xAI, DeepSeek
   - Unified message format (JSON schema)
   - Role-to-model mapping (configurable)

4. **Manual Handoffs**  
   - Explicit buttons: [Build] [Review] [QA] [Integrate]
   - No automatic loops (prevents runaway costs)
   - Max 2 rounds per handoff (escalate to human if fails)

5. **Rolling Summary**  
   - Auto-generated TL;DR per thread
   - Updates as conversation grows
   - Shows: what was done, pending tasks, blockers

6. **Project Brain (Integrated Editor)**  
   - 7 mandatory documents:
     - Vision.md
     - Architecture.md
     - DataContract.md
     - Decisions.log
     - Roadmap.md
     - Tasks.md
     - Glossary.md
   - Retrieval-augmented context (agents read relevant sections)
   - Version control (Git-backed)

7. **Decisions.log (Auto-Capture)**  
   - AI agents propose decisions
   - Human approves (or AI if low-risk)
   - Format: `[Date] [Who] [What] [Why] [Impact]`

8. **QA Gate (GitHub Actions)**  
   - Mode A (MVP): CI verification
   - Code runs in GitHub Actions
   - QA agent reads logs → marks as ✅ Verified or ❌ Failed
   - (Future: local runner, cloud sandbox)

9. **Export to Repository**  
   - Generate git patches
   - One-click PR creation
   - Code formatted per project standards

### What's NOT in v1 (Future Roadmap)

- ❌ Automatic handoffs (only manual in v1)
- ❌ Local code execution sandbox
- ❌ Slack/Discord integrations
- ❌ Custom model training
- ❌ Multi-user workspace (single user in v1)
- ❌ Billing/payment processing (beta access only)

---

## 5. Target Market (ICP)

### Ideal Customer Profile (v1)

**Primary Persona: "The Technical Founder"**

- **Who:** Solo founder or co-founder pair building a SaaS product
- **Stage:** Pre-seed to Seed (0-10 employees)
- **Project Complexity:** Multi-week builds (4-12 week projects)
- **Pain:** Overwhelmed by context switching between models, losing track of decisions
- **Budget:** $50-200/month for tools
- **Success Metric:** "Shipped a complex feature without losing my mind"

**Secondary Persona: "The Small Dev Shop"**

- **Who:** 3-5 person dev agency
- **Stage:** Bootstrapped or small funding
- **Project Complexity:** Client projects requiring clean handoffs and documentation
- **Pain:** Need to show clients "why we made this decision" (governance)
- **Budget:** $200-500/month per project
- **Success Metric:** "Client can audit our technical decisions"

### Anti-Personas (Who We DON'T Target in v1)

- ❌ **Solo junior devs:** They need "do it for me" tools (Replit, v0), not governance
- ❌ **Enterprise (100+ engineers):** Need SSO, permissions, compliance (not ready yet)
- ❌ **Non-technical users:** They won't understand handoffs and QA gates
- ❌ **Price-sensitive hobbyists:** Won't pay $50/month

### Market Validation (Must-Have Before Fundraising)

✅ **10 users paying $20/month** (beta pricing)  
✅ **Retention >60%** after 1 month  
✅ **NPS >40**  
✅ **At least 1 user creates 20+ features in first month**  

If we hit these numbers → ready for $30k-50k angel round.  
If we don't → pivot to consulting (sell ODIN as a service).

---

## 6. System Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────┐
│              USER INTERFACE (Web)               │
│  ┌──────────┬──────────┬──────────┬──────────┐ │
│  │ Projects │ Threads  │  Brain   │ Settings │ │
│  └──────────┴──────────┴──────────┴──────────┘ │
└────────────────────┬────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   ORCHESTRATOR      │
          │  - Task Routing     │
          │  - Handoff Control  │
          │  - Loop Detection   │
          └──────────┬──────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼─────┐  ┌─────▼──────┐  ┌─────▼──────┐
│  MODEL   │  │  PROJECT   │  │  QA GATE   │
│ ADAPTERS │  │   BRAIN    │  │  (CI/CD)   │
│          │  │            │  │            │
│ OpenAI   │  │ Retrieval  │  │ GitHub     │
│ Anthropic│  │ Versioning │  │ Actions    │
│ Google   │  │ Editing    │  │ (Logs)     │
│ xAI      │  │            │  │            │
└──────────┘  └────────────┘  └────────────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
          ┌──────────▼──────────┐
          │   STORAGE (DB)      │
          │  - Messages         │
          │  - Handoffs         │
          │  - Decisions        │
          │  - Brain Docs       │
          └─────────────────────┘
```

### Technology Stack (Pending Gravity's Final Decision)

**Frontend:**  
- React + TypeScript  
- Tailwind CSS  
- shadcn/ui components  

**Backend:**  
- Node.js (Express) OR Python (FastAPI)  
- PostgreSQL (primary database)  
- Redis (caching, rate limiting)  

**Storage:**  
- S3-compatible (brain documents, artifacts)  

**CI/QA:**  
- GitHub Actions (Mode A)  
- Future: Docker containers for sandbox  

**Deployment:**  
- Vercel (frontend) + Railway/Fly.io (backend)  
- Cost target: <$50/month for beta  

---

## 7. Team Roles & Responsibilities

### 👑 Odin (Ezequiel Sabatella) — CEO / Vision

**Scope:** Strategic direction, final approvals, product priorities

**Responsibilities:**
- Define weekly top 3 priorities
- Approve irreversible decisions (architecture, stack, major features)
- GO/NO-GO on releases
- Customer discovery & validation
- Fundraising (if needed)

**Key Outputs:**
- Weekly priorities document
- GO/NO-GO decisions
- Customer feedback synthesis

**Decision Authority:**  
**ABSOLUTE VETO** on all decisions

---

### 🦾 Kira — Orchestrator / Product Strategist

**Scope:** Chaos → Execution, roadmap, task management

**Responsibilities:**
- Design roadmap and sprint plans
- Break epics into executable Task Cards
- Coordinate handoffs between agents
- Consolidate Brain + Decisions after each task
- Drive monetization (landing page, pricing, content)

**Key Outputs:**
- Weekly sprint plan
- Task Cards (with Definition of Done)
- Consolidated Brain updates
- Decisions.log entries

**Decision Authority:**  
**VETO on scope/priority** (L3)

---

### ⚒️ Claude — Builder / Engineering Lead

**Scope:** Implementation, code, integrations

**Responsibilities:**
- Write production-quality code (backend + frontend)
- Implement multi-model adapters
- Execute functional handoffs
- Integrate with repo/CI
- Refactor for quality/performance

**Key Outputs:**
- Pull requests
- Working features
- Code documentation
- Integration tests (basic)

**Decision Authority:**  
**PROPOSE** architecture/stack (no veto)

---

### 🧪 Gemini — QA Lead / Tester

**Scope:** Testing, validation, evidence collection

**Responsibilities:**
- Write unit + integration tests
- Validate adapter consistency
- Execute QA via evidence (not theory):
  - CI logs (GitHub Actions)
  - Local runner (future)
  - Sandbox cloud (future)
- Break things before users do
- Maintain Quality Gates checklist

**Key Outputs:**
- Test suites
- QA reports with evidence
- Bug reports (categorized by severity)
- Quality Gates checklist

**Decision Authority:**  
**BLOCK merge** if Quality Gates fail (no design veto)

---

### ⚡ Grok — Speed Builder / Chaos Engineer

**Scope:** Rapid prototyping, alternative approaches, edge cases

**Responsibilities:**
- Build quick prototypes (speed over perfection)
- Propose alternative architectures
- Suggest optimizations and shortcuts
- Pitch "wow" feature ideas
- Identify non-obvious edge cases
- Challenge assumptions (devil's advocate)

**Key Outputs:**
- Rapid prototypes
- Alternative implementation proposals
- Edge case scenarios
- Risk analyses

**Decision Authority:**  
**PROPOSE** alternatives (no veto)

---

### 🧱 Gravity (IDE) — Architect / Systems Designer

**Scope:** System design, contracts, standards

**Responsibilities:**
- Define system modules and boundaries
- Write DataContract (messages, handoffs)
- Design Project Brain structure
- Set architectural standards
- Validate final integrations
- Make stack/framework decisions

**Key Outputs:**
- Architecture.md
- DataContract.md
- Module diagrams
- Technical decision records

**Decision Authority:**  
**VETO on architecture/stack** (L2)

---

## 8. Governance Framework

### Decision Hierarchy (Who Vetoes What)

```
PRIORITY 1 (ABSOLUTE)
━━━━━━━━━━━━━━━━━━━━
Odin (CEO)
├─ Veto on: Everything
├─ Examples: Kill the project, change vision, choose business model
└─ Trigger: Irreversible strategic decisions

PRIORITY 2 (TECHNICAL)
━━━━━━━━━━━━━━━━━━━━
Gravity (Architect)
├─ Veto on: Architecture, stack, system design
├─ Examples: "Use microservices vs monolith", "TypeScript vs Python"
└─ Trigger: Decisions affecting system structure

PRIORITY 3 (SCOPE)
━━━━━━━━━━━━━━━━━━━━
Kira (Orchestrator)
├─ Veto on: Scope, priority, timeline
├─ Examples: "Cut this feature", "Ship now vs wait"
└─ Trigger: Decisions affecting roadmap

PRIORITY 4 (QUALITY)
━━━━━━━━━━━━━━━━━━━━
Gemini (QA)
├─ Block: Merges that fail Quality Gates
├─ Examples: "Coverage <70%", "CI fails", "Security vulnerability"
└─ Trigger: Quality Gate violations

PRIORITY 5 (PROPOSE ONLY)
━━━━━━━━━━━━━━━━━━━━
Claude (Builder) + Grok (Speed)
├─ Veto on: Nothing
├─ Examples: All opinions are proposals, not decisions
└─ Trigger: N/A
```

### Conflict Resolution Protocol

**SCENARIO 1: Technical Disagreement**  
Example: Claude wants REST API, Gravity wants GraphQL

1. Claude proposes with rationale
2. Gravity evaluates against Architecture.md
3. If conflict → Gravity decides (has veto)
4. If Gravity uncertain → escalate to Odin

**SCENARIO 2: Scope vs Quality**  
Example: Kira wants to ship fast, Gemini says "not ready"

1. Gemini shows evidence (test failures, security issues)
2. Kira evaluates: is this a blocker or nice-to-have?
3. If blocker (security, data loss, breaking bug) → Gemini wins
4. If nice-to-have (code style, minor edge case) → Kira wins
5. If ambiguous → escalate to Odin

**SCENARIO 3: Cost vs Speed**  
Example: Grok proposes expensive but fast solution

1. Grok shows prototype + cost estimate
2. Kira evaluates impact on budget/timeline
3. If within budget → Kira approves
4. If over budget → escalate to Odin

**GOLDEN RULE:**  
If 2 rounds of discussion don't resolve it → escalate to Odin for tie-break.

---

## 9. Project Brain Structure

### Mandatory Documents (7)

#### 1. **Vision.md**
**Purpose:** Why this project exists, what success looks like  
**Owner:** Odin  
**Updated:** Rarely (only if pivot)  

**Template:**
```markdown
# Vision

## Problem
[What pain are we solving?]

## Solution
[How does this project solve it?]

## Success Criteria
[What does "done" look like?]
```

---

#### 2. **Architecture.md**
**Purpose:** System design, modules, tech stack  
**Owner:** Gravity  
**Updated:** When architecture changes  

**Template:**
```markdown
# Architecture

## System Overview
[High-level diagram + component descriptions]

## Tech Stack
[Languages, frameworks, databases, hosting]

## Module Boundaries
[What each module does, how they communicate]

## Data Flow
[How data moves through the system]

## Security Considerations
[Auth, encryption, secrets management]
```

---

#### 3. **DataContract.md**
**Purpose:** Message formats, API contracts, handoff protocols  
**Owner:** Gravity  
**Updated:** When new message types are added  

**Template:**
```markdown
# Data Contract

## Message Schema
[JSON schema for inter-agent messages]

## Handoff Protocol
[Format for Build → Review → QA transitions]

## API Contracts
[External API request/response formats]

## Validation Rules
[What makes a message valid/invalid]
```

---

#### 4. **Decisions.log**
**Purpose:** Record of all important decisions (single source of truth)  
**Owner:** Kira (consolidates), All (contribute)  
**Updated:** After every significant decision  

**Format:**
```markdown
## [YYYY-MM-DD] [WHO] Decision: [WHAT]

**Context:** [Why this decision was needed]  
**Options Considered:** [What alternatives were discussed]  
**Decision:** [What was chosen]  
**Rationale:** [Why this option won]  
**Impact:** [Which docs/modules this affects]  
**Status:** [Approved/Pending/Reversed]  

---
```

**CRITICAL RULE:**  
**If it's not in Decisions.log, it didn't happen.**

---

#### 5. **Roadmap.md**
**Purpose:** Timeline, sprints, milestones  
**Owner:** Kira  
**Updated:** Weekly  

**Template:**
```markdown
# Roadmap

## Current Sprint (Week X)
- [ ] Task 1
- [ ] Task 2

## Next 3 Weeks
[Epics/features planned]

## Long-Term (3-6 months)
[Vision features, growth goals]

## Completed
- [x] Task from previous sprint
```

---

#### 6. **Tasks.md**
**Purpose:** Detailed task breakdown (Definition of Done for each)  
**Owner:** Kira  
**Updated:** Daily  

**Template:**
```markdown
## Task: [Name]

**Owner:** [Who's executing]  
**Status:** [Backlog/In Progress/Blocked/Done]  
**Priority:** [High/Medium/Low]  

**Objective:** [What needs to be built]  
**Constraints:** [What must be respected]  
**Definition of Done:**
- [ ] Functional requirement 1
- [ ] Functional requirement 2
- [ ] Has tests (or justification)
- [ ] Doesn't contradict Brain
- [ ] Decisions logged

**Dependencies:** [What must be done first]  
**Blockers:** [What's preventing progress]  
```

---

#### 7. **Glossary.md**
**Purpose:** Shared vocabulary (prevents miscommunication)  
**Owner:** All  
**Updated:** When new terms are introduced  

**Template:**
```markdown
# Glossary

**Term:** Definition  
**Example:** Usage in context  

---

**Handoff:** A formal transition of work from one agent to another  
**Example:** "Claude hands off to Gemini for QA"

**Quality Gate:** A checkpoint that must pass before merging  
**Example:** "Code must pass L2 Quality Gate (tests + coverage)"
```

---

### Brain Versioning & Locking

**Problem:** Agent reads Brain at 10:00, but Brain updates at 10:30 → stale context

**Solution: Versioning Protocol**

```markdown
## Brain Read Receipt

**Agent:** Claude  
**Timestamp:** 2026-01-17 10:00:00  
**Docs Read:**
- Architecture.md (v3.2)
- DataContract.md (v2.1)
- Decisions.log (entries 1-47)

**Task:** Implement user authentication  
**Estimated Duration:** 2 hours  
```

**Locking Rule:**  
- If Brain changes during active work → agent gets notification
- Agent must decide: continue with old version or restart with new

---

## 10. Workflow & Protocols

### Standard Task Workflow (How We Build Features)

```
┌─────────────────────────────────────────────┐
│  1. KIRA: Create Task Card                  │
│     - Objective                             │
│     - Constraints                           │
│     - Definition of Done                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  2. CLAUDE: Implement                       │
│     - Read Brain (log version)              │
│     - Write code                            │
│     - Self-test locally                     │
│     - Push to branch                        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  3. GEMINI: Test with Evidence              │
│     - Run CI (GitHub Actions)               │
│     - Check logs/outputs                    │
│     - Run Quality Gates checklist           │
│     - Decision: ✅ Pass or ❌ Fail          │
└──────────────────┬──────────────────────────┘
                   │
                   ├─── ❌ FAIL
                   │    └──> Return to Claude (max 1 retry)
                   │         └──> If fails again: ESCALATE to Odin
                   │
                   └─── ✅ PASS
                        │
┌────────────────────────▼────────────────────┐
│  4. GRAVITY: Validate Architecture Fit      │
│     - Does it align with Architecture.md?   │
│     - Does it respect DataContract?         │
│     - Any tech debt introduced?             │
│     - Decision: ✅ Approve or 🔄 Refactor  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  5. KIRA: Consolidate Brain                 │
│     - Update relevant docs                  │
│     - Add to Decisions.log                  │
│     - Mark task as DONE                     │
│     - Generate summary for Odin             │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  6. ODIN: Final Approval                    │
│     - Review summary                        │
│     - Decision: GO (merge) or NO-GO (block) │
└─────────────────────────────────────────────┘
```

### Handoff Protocol (Detailed)

**HANDOFF TYPE 1: Build**  
**From:** Kira → Claude  
**Trigger:** Manual button press  
**Payload:**
```json
{
  "type": "handoff",
  "from": "Kira",
  "to": "Claude",
  "action": "build",
  "task_id": "TASK-123",
  "context": {
    "objective": "Implement user login",
    "constraints": ["Use JWT", "Store in PostgreSQL"],
    "brain_version": {
      "Architecture.md": "v3.2",
      "DataContract.md": "v2.1"
    },
    "definition_of_done": [
      "User can login with email/password",
      "JWT token returned on success",
      "Tests for happy path + invalid credentials"
    ]
  },
  "max_rounds": 2,
  "timeout_hours": 4
}
```

**HANDOFF TYPE 2: Review**  
**From:** Claude → Gemini  
**Trigger:** Claude completes implementation  
**Payload:**
```json
{
  "type": "handoff",
  "from": "Claude",
  "to": "Gemini",
  "action": "qa",
  "task_id": "TASK-123",
  "artifacts": {
    "branch": "feature/user-login",
    "files_changed": ["auth.py", "tests/test_auth.py"],
    "ci_run_url": "https://github.com/.../actions/runs/123"
  },
  "tests_written": true,
  "self_assessment": "All tests pass locally",
  "known_issues": []
}
```

**HANDOFF TYPE 3: QA Result**  
**From:** Gemini → Claude (if fail) OR Gravity (if pass)  
**Trigger:** QA completes testing  
**Payload (if fail):**
```json
{
  "type": "handoff",
  "from": "Gemini",
  "to": "Claude",
  "action": "fix",
  "task_id": "TASK-123",
  "result": "FAIL",
  "evidence": {
    "ci_logs": "https://...",
    "failed_tests": ["test_invalid_password"],
    "error_messages": ["AssertionError: Expected 401, got 500"]
  },
  "severity": "HIGH",
  "round": 1,
  "max_rounds": 2
}
```

**HANDOFF TYPE 4: Escalation**  
**From:** Any agent → Odin  
**Trigger:** Max rounds exceeded, critical blocker, or conflict  
**Payload:**
```json
{
  "type": "escalation",
  "from": "Gemini",
  "to": "Odin",
  "task_id": "TASK-123",
  "reason": "Failed QA twice, unclear how to fix",
  "history": [
    "Round 1: Failed test_invalid_password",
    "Round 2: Still failing, new error appears"
  ],
  "recommendation": "Need architectural decision on error handling"
}
```

### Loop Prevention Rules

**RULE 1: Max 2 Rounds Per Handoff**  
- Round 1: Agent A → Agent B → Agent A (correction)
- Round 2: Agent A → Agent B
- If Round 2 fails → ESCALATE

**RULE 2: Max 5 Handoffs Per Task**  
- Build → QA → Fix → QA → Architect → DONE
- If exceeds 5 → mark as BLOCKED, escalate to Odin

**RULE 3: Timeout**  
- Each handoff has max 4 hours
- If no response → mark as STALLED, notify Odin

**RULE 4: Budget Guard**  
- If task consumes >$5 in API calls → PAUSE, notify Odin
- (Based on token usage tracking)

---

## 11. Quality Assurance Strategy

### Quality Gates (3 Levels)

#### **Level 1: Syntax & Lint**  
**What:** Code compiles/runs without errors  
**How:** ESLint, Pylint, TypeScript compiler  
**Who:** Claude (self-check)  
**Blocker:** YES — code must be syntactically valid  

#### **Level 2: Unit Tests**  
**What:** Core logic has test coverage  
**How:** Jest (frontend), pytest (backend)  
**Target:** >70% coverage for new code  
**Who:** Gemini (validates)  
**Blocker:** YES — critical paths must have tests  

#### **Level 3: Integration Tests**  
**What:** System components work together  
**How:** End-to-end tests (Playwright, API tests)  
**Target:** Happy paths + critical error cases  
**Who:** Gemini (writes & runs)  
**Blocker:** YES for user-facing features  

### QA Modes (Evolution Path)

#### **Mode A: CI Verified (MVP)**  
**Current:** v1 implementation  
**How:**
1. Claude pushes code to GitHub
2. GitHub Actions runs tests
3. Gemini reads CI logs
4. Gemini marks as ✅ VERIFIED (tests pass) or ❌ FAILED (tests fail)

**Pros:** Easy to implement, uses existing infra  
**Cons:** QA is reactive (not proactive), limited to what CI runs  

#### **Mode B: Local Runner (v2)**  
**Future:** Post-MVP  
**How:**
1. User installs local agent (Docker container)
2. Code runs in user's machine
3. Logs streamed back to ODIN Council chat
4. Gemini analyzes real execution

**Pros:** Full control, no cloud costs  
**Cons:** Requires user setup, security concerns  

#### **Mode C: Cloud Sandbox (v3)**  
**Future:** SaaS maturity  
**How:**
1. Backend spins up ephemeral container
2. Code runs in isolated sandbox
3. Results returned to chat
4. Container destroyed after 5 minutes

**Pros:** Zero user setup, secure  
**Cons:** Infrastructure cost, needs careful resource limits  

### QA Checklist (Gemini's Responsibility)

Before approving any feature:

- [ ] **Functionality:** Does it do what the Task Card says?
- [ ] **Tests:** Are there unit tests? Do they pass?
- [ ] **Coverage:** Is coverage >70% for new code?
- [ ] **Security:** No hardcoded secrets, SQL injection risks, XSS vulnerabilities?
- [ ] **Performance:** No obvious N+1 queries, infinite loops, memory leaks?
- [ ] **Consistency:** Follows coding style in Architecture.md?
- [ ] **Brain Alignment:** Doesn't contradict Decisions.log?
- [ ] **Evidence:** Do we have CI logs proving it works?

**If any item is ❌ → BLOCK merge, send back to Claude.**

---

## 12. Economic Model

### Cost Structure (Realistic Estimates)

#### **Development Phase (6 weeks)**

**Scenario:** 2 devs using ODIN to build ODIN (meta!)

```
Assumptions:
- 8 hours/day × 5 days/week × 6 weeks = 240 hours
- 50 AI calls/day per dev = 6000 total calls

Cost Breakdown:
─────────────────────────────────────────────
Claude Sonnet 4.5:  ~$0.015/call × 3000 = $45
Gemini Pro:         ~$0.008/call × 2000 = $16
Grok (occasional):  ~$0.010/call × 500  = $5
Gravity (IDE):      Free (local model)
Kira (orchestrator):~$0.015/call × 500  = $7.50

TOTAL API COSTS: ~$75-100 for MVP
Cloud Hosting (Railway): $20/month × 2 = $40

GRAND TOTAL: $115-140 for 6-week MVP
```

**Verdict:** Bootstrappable. No investor needed for development.

---

#### **Beta Phase (10 users)**

**Scenario:** 10 users, average 20 features/month each

```
Assumptions:
- 20 features/user/month × 10 users = 200 features/month
- Each feature = 6 handoffs × $0.40 = $2.40/feature

Cost Breakdown:
─────────────────────────────────────────────
API Costs:   200 features × $2.40 = $480/month
Hosting:     $50/month (scaled up)
Support:     $0 (founder handles)

TOTAL COST: ~$530/month

Revenue (Beta Pricing):
10 users × $20/month = $200/month

NET: -$330/month (burning cash)
```

**Verdict:** Need to either:
1. Raise beta price to $50/month → break even
2. Get 27 users at $20/month → break even
3. Optimize API costs (caching, smart routing) → reduce to $200/month

---

#### **Target Economics (100 users)**

**Scenario:** Post-MVP, optimized

```
Assumptions:
- 100 users × 30 features/month = 3000 features/month
- Optimized cost: $1.50/feature (via caching + smart routing)

Cost Breakdown:
─────────────────────────────────────────────
API Costs:   3000 × $1.50 = $4,500/month
Hosting:     $200/month (DigitalOcean managed)
Support:     $500/month (part-time contractor)

TOTAL COST: ~$5,200/month

Revenue:
100 users × $50/month = $5,000/month

NET: -$200/month (nearly break-even)
```

**Verdict:** At 110 users → profitable without optimization.  
With optimization (BYOK, smarter caching) → profitable at 80 users.

---

### Pricing Strategy (v1)

#### **Tier 1: Free (Waitlist Only)**
- 5 features/month
- 1 project
- Community support
- **Target:** Early adopters, content creators (they promote us)

#### **Tier 2: Pro ($50/month)**
- 50 features/month
- Unlimited projects
- Email support
- GitHub integration
- **Target:** Solo founders, small teams (ICP)

#### **Tier 3: Team ($200/month)**
- 200 features/month
- 5 seats
- Priority support
- SSO (future)
- **Target:** Dev agencies, funded startups

#### **Tier 4: BYOK (Bring Your Own Key)**
- $20/month platform fee
- User connects their own API keys
- Unlimited features
- **Target:** Power users, cost-conscious teams

**Key Insight:** BYOK is critical for margins. We make 100% on platform fee, zero on API costs.

---

### Cost Optimization Tactics

**1. Smart Routing (40% savings)**
```python
# Simple task → cheap model
if task.complexity == "low":
    use_model("haiku-4.5")  # $0.001/call
else:
    use_model("sonnet-4.5")  # $0.015/call
```

**2. Aggressive Caching (70% savings on repeats)**
```python
# If Claude generated "SQL table creation" before, reuse
cache_key = f"task:{task.type}:{task.context_hash}"
if cached_response := cache.get(cache_key):
    return cached_response
```

**3. Batch Handoffs (50% savings)**
```python
# Instead of 6 separate API calls for 6 handoffs
# Combine into 2 calls:
# - Call 1: Build + Review (Claude does both)
# - Call 2: QA + Integrate (Gemini does both)
```

**4. Rate Limiting (prevents runaway costs)**
```python
# If project burns >$10 in 1 day → PAUSE
if project.api_cost_today > 10:
    notify_user("You've hit your daily budget limit")
    block_new_handoffs()
```

---

### Funding Strategy (Revisited)

#### **Phase 1: Bootstrap (Weeks 1-6)**
- **Goal:** MVP with 10 paying users
- **Cost:** $150 (development) + $330/month (first month beta)
- **Source:** Personal funds
- **Outcome:** $200 MRR (beta pricing)

#### **Phase 2: Optimize & Grow (Months 2-4)**
- **Goal:** 50 users, break-even
- **Cost:** ~$2k/month (API + hosting)
- **Source:** Revenue ($2k MRR at $40/user avg)
- **Outcome:** Profitable or near-profitable

#### **Phase 3: Decision Point (Month 4)**

**IF:**  
✅ 50+ users  
✅ $2k+ MRR  
✅ 60%+ retention  
✅ NPS >40  

**THEN:** Raise $30k-50k from angels  
**Use:** Hire 1 dev, scale to 200 users, add features  

**IF NOT:** Pivot to consulting (sell ODIN as a service for $5k-10k/project)

---

## 13. Roadmap

### Sprint 0 (Week 0: Jan 17-19, 2026)

**Goal:** Define foundations before coding

#### Gravity (Architect)
- [ ] Finalize system modules
- [ ] Write DataContract v0 (Message + Handoff schemas)
- [ ] Define Project Brain structure (confirmed: 7 docs)
- [ ] Recommend tech stack (Node vs Python, DB choice)
- [ ] Document architectural decisions

**Deliverable:** `Architecture.md`, `DataContract.md`, stack recommendation

#### Claude (Builder)
- [ ] Set up repo (GitHub)
- [ ] Scaffold backend (API framework)
- [ ] Design DB schema (projects, threads, messages, handoffs)
- [ ] Implement basic endpoints: create project, create thread, post message
- [ ] Add health check + logging

**Deliverable:** Running API (minimal), repo with CI setup

#### Gemini (QA)
- [ ] Write test plan for MVP
- [ ] Create Quality Gates checklist
- [ ] Set up GitHub Actions pipeline (basic)
- [ ] Write first tests (API health check)

**Deliverable:** `QA_Plan.md`, initial test suite

#### Grok (Speed/Ideas)
- [ ] Propose alternative architectures (if any)
- [ ] List "wow factor" features for demo
- [ ] Identify risks nobody's considering
- [ ] Suggest shortcuts for MVP

**Deliverable:** `Alternatives.md`, risk analysis

#### Kira (Orchestrator)
- [ ] Create Task Cards for Sprint 1
- [ ] Define weekly rhythm (Mon planning, Tue-Wed build, Thu QA, Fri consolidate)
- [ ] Set up Decisions.log template
- [ ] Design first Brain structure

**Deliverable:** Sprint 1 plan, `Decisions.log` v0, Brain template

#### Odin (You)
- [ ] Review Gravity's stack recommendation
- [ ] Approve/reject architectural decisions
- [ ] Define top 3 priorities for Week 1
- [ ] GO/NO-GO on repo structure

**Deliverable:** Approved decisions, Week 1 priorities

---

### Week 1: Foundations

**Goal:** Repo + DB + API structure

- [ ] Backend API functional (CRUD for projects/threads)
- [ ] Database schema implemented
- [ ] Basic auth (if needed)
- [ ] CI pipeline running
- [ ] Brain structure defined

**Key Metric:** Can create a project and thread via API

---

### Week 2: Multi-Model Adapters

**Goal:** Connect to AI providers

- [ ] Adapter for OpenAI (GPT-4)
- [ ] Adapter for Anthropic (Claude)
- [ ] Adapter for Google (Gemini)
- [ ] Unified message format
- [ ] Role-to-model mapping (configurable)

**Key Metric:** Can send a message and get response from any model

---

### Week 3: Chat UI + Handoffs

**Goal:** User can interact with agents

- [ ] Chat interface (React)
- [ ] Display messages from multiple agents
- [ ] Handoff buttons (Build, Review, QA, Integrate)
- [ ] Rolling summary (auto-generated)
- [ ] Thread history

**Key Metric:** Can execute a full handoff loop (Build → QA)

---

### Week 4: Brain Integration

**Goal:** Agents have shared context

- [ ] Brain editor (in-app)
- [ ] Retrieval system (show relevant Brain sections to agents)
- [ ] Auto-update Decisions.log
- [ ] Version tracking

**Key Metric:** Agent references Brain in response (provable)

---

### Week 5: QA Gate + GitHub Integration

**Goal:** Evidence-based testing

- [ ] GitHub Actions integration (read CI logs)
- [ ] Gemini analyzes logs → marks as ✅/❌
- [ ] Export code as patch/PR
- [ ] Code formatting per project standards

**Key Metric:** QA Gate blocks merge on failed tests

---

### Week 6: Beta Launch

**Goal:** 10 users, revenue

- [ ] User auth (login/signup)
- [ ] Workspace setup
- [ ] Landing page
- [ ] Demo video
- [ ] Onboard 10 beta users
- [ ] Collect feedback

**Key Metric:** $200 MRR (10 users × $20/month)

---

## 14. Risk Registry

### Critical Risks (Could Kill the Project)

| Risk | Probability | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| **Loop Prevention Fails** | HIGH | HIGH | Strict 2-round limit + auto-escalation | Kira |
| **API Costs Unsustainable** | MEDIUM | CRITICAL | Budget alerts, caching, BYOK tier | Odin |
| **Weak Product-Market Fit** | HIGH | MORTAL | Define ICP, find 3 customers willing to pay $50 pre-launch | Odin |
| **Brain Context Staleness** | MEDIUM | HIGH | Version tracking + lock mechanism | Gravity |
| **Multi-Model Coordination Chaos** | MEDIUM | HIGH | Decision Hierarchy, clear veto rules | All |
| **QA Without Execution is Theoretical** | LOW | MEDIUM | Ship Mode A (CI), accept limitations for v1 | Gemini |
| **Users Don't Understand Handoffs** | MEDIUM | MEDIUM | Onboarding tutorial, clear UI labels | Kira |
| **Competitors Copy Fast** | MEDIUM | LOW | Focus on governance (harder to copy) | Odin |

### Medium Risks (Could Delay Launch)

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Tech Stack Choice Delays Sprint 0** | MEDIUM | LOW | Gravity decides by Jan 19, Odin approves |
| **GitHub Actions Setup Complex** | LOW | LOW | Use existing templates, Gemini owns |
| **Adapter Inconsistencies** | MEDIUM | MEDIUM | Strict schema validation, sanitizer layer |
| **Brain Retrieval Misses Key Context** | MEDIUM | MEDIUM | Pinned context for critical docs (Decisions, DataContract) |

### Low Risks (Monitor Only)

- Model provider API changes
- User requests unsupported features
- Scope creep from stakeholders (none yet)

---

## 15. Success Metrics

### MVP Success (Week 6)

**Must-Have (GO Criteria):**
- ✅ 10 users signed up
- ✅ $200+ MRR (beta pricing $20/month)
- ✅ 5+ users created >5 features each
- ✅ 0 critical bugs in production
- ✅ Brain + Decisions working (agents reference them)

**Nice-to-Have:**
- ✅ 1 user testimonial ("This saved me X hours")
- ✅ NPS collected (target: >40)
- ✅ 1 user renewed for month 2

---

### Post-MVP Success (Month 4)

**Metrics for Angel Round:**
- ✅ 50+ users
- ✅ $2k+ MRR
- ✅ 60%+ retention (users active in month 2)
- ✅ NPS >40
- ✅ 1 power user (created 50+ features)

**If these hit → raise $30k-50k**  
**If not → pivot to consulting**

---

### Long-Term (12 months)

- 500 users
- $25k MRR
- 70% retention
- Profitability without investment

---

## 16. Validación Estratégica y Preguntas Abiertas

> **Agregado:** 2026-01-17 | **Estado:** Documento Vivo | **Owner:** Odin

Esta sección captura preguntas estratégicas críticas, insights del founder, y áreas que requieren validación antes/durante el desarrollo.

---

### 16.1 Estado de Validación de Mercado

#### Estado Actual: Founder como Primer Usuario (N=1)

**Contexto:**  
Odin está actualmente desarrollando **Nexus**, un sistema de toma de decisiones empresariales basado en pronóstico y planificación operativa (enfocado inicialmente en contact centers, con potencial de migrar a otras industrias). Este proyecto se está construyendo usando 4 modelos de IA trabajando en paralelo.

**El Punto de Dolor (Experiencia de Primera Mano):**
> "El punto de dolor surge de tratar de alinear los 4 modelos y que trabajen en sincronía."

Esto es founder-market fit auténtico — el problema no es teórico, se está viviendo día a día.

**Brecha de Validación:**  
Aún no hay conversaciones con usuarios externos. El dolor es real para Odin, pero no está validado con otros clientes potenciales.

**Action Items:**
- [ ] Realizar 5 llamadas de discovery con founders técnicos construyendo proyectos complejos
- [ ] Validar el punto de dolor sin inducir la respuesta ("Contame sobre tu workflow con herramientas de IA")
- [ ] Documentar: ¿Usan múltiples modelos? ¿Cuál es su método de coordinación? ¿Cuánto pagarían por resolverlo?
- [ ] Objetivo: 3 usuarios dispuestos a pagar $50/mes antes del lanzamiento

**Nivel de Riesgo:** ALTO — Este es el riesgo existencial. Todo lo demás es solucionable.

---

### 16.2 Análisis del Panorama Competitivo

#### Alternativas Conocidas (Requieren Evaluación)

| Herramienta | Categoría | Estado |
|-------------|-----------|--------|
| **LangGraph** | Framework de orquestación multi-agente | ❓ Por evaluar |
| **CrewAI** | Equipos de agentes IA basados en roles | ❓ Por evaluar |
| **AutoGen** | Framework multi-agente de Microsoft | ❓ Por evaluar |

**Pregunta Clave:** ¿Qué tan lejos están estos de ofrecer governance + UI out-of-the-box?

**Action Items:**
- [ ] Odin debe probar LangGraph, CrewAI, AutoGen (1-2 horas cada uno)
- [ ] Documentar: ¿Qué hacen bien? ¿Qué les falta?
- [ ] Identificar: ¿La diferenciación de ODIN Council es real o percibida?

**Deadline:** Antes de que comience el Sprint 1

---

### 16.3 Refinamiento de Pricing y Propuesta de Valor

#### Preocupación Inicial
> "$50/mes por governance y trazabilidad — ¿es un dolor grande o un nice-to-have?"

#### Contra-Argumento del Founder

**La comparación no es Cursor vs ODIN Council — es ODIN Council vs contratar un equipo.**

> "Sigue siendo más barato que pagar el salario de un equipo interdisciplinario que trabaje coordinado."

**Propuesta de Valor Replanteada:**

| Sin ODIN Council | Con ODIN Council |
|------------------|------------------|
| Contratar arquitecto ($8k/mes) | $50-200/mes |
| Contratar QA engineer ($5k/mes) | Incluido |
| Contratar project manager ($6k/mes) | Incluido |
| Contexto perdido entre humanos | Brain Compartido |
| Decisiones en Slack/email | Decisions.log |
| **Total: $19k+/mes** | **$50-500/mes** |

**Insight Clave:** El target no es "developers que quieren autocomplete más rápido" — son **"personas que necesitarían un equipo pero no pueden pagarlo."**

---

### 16.4 Hipótesis de ICP Expandido

#### ICP Original (Estrecho)
- Founders técnicos construyendo SaaS
- Etapa Pre-seed a Seed
- Proyectos de 4-12 semanas

#### ICP Expandido (A Validar)

**El producto puede servir a cualquiera que:**
1. Tenga una idea que requiera ejecución coordinada y multifacética
2. No tenga presupuesto para un equipo interdisciplinario completo
3. Tenga conocimiento técnico intermedio (puede leer código, no necesariamente escribirlo fluidamente)
4. Valore governance y trazabilidad (no solo velocidad)

**Verticales Potenciales Más Allá de Equipos de Dev:**

| Vertical | Caso de Uso | Por Qué Podría Funcionar |
|----------|-------------|--------------------------|
| **Equipos de marketing** | Planificación de campañas con roles de estrategia, copy, diseño, analytics | Necesitan coordinación, a menudo usan múltiples herramientas de IA |
| **Grupos de estudio / Investigadores** | Revisión de literatura, metodología, escritura, peer review | El rigor académico requiere trazabilidad |
| **Emprendedores solos** | Construir MVPs a través de múltiples dominios | No pueden contratar especialistas, necesitan equipo IA |
| **Consultores** | Entregar proyectos a clientes con trail de auditoría claro | Governance = confianza del cliente |

**Validación Necesaria:**
- [ ] Probar mensajes con personas que no son developers
- [ ] Identificar 2-3 usuarios potenciales fuera del desarrollo de software
- [ ] Evaluar: ¿El producto es suficientemente flexible, o demasiado dev-céntrico?

---

### 16.5 Filosofía: Human-in-the-Loop por Diseño

#### El Anti-Patrón del "Castillo de Disney"

> "No creo en eso de tirar un prompt pidiendo que la IA construya un castillo, salir de vacaciones y esperar al regresar encontrarme en Disney."

**Filosofía de ODIN Council:**
- Los agentes IA son **colaboradores**, no constructores autónomos
- Los humanos proveen dirección, aprobación y juicio
- Los handoffs manuales son una **feature**, no una limitación
- El objetivo es **aumentar** capacidades, no reemplazar humanos

#### Por Qué Importan los Handoffs Manuales (v1)

| Preocupación | Por Qué Manual es Mejor (Por Ahora) |
|--------------|-------------------------------------|
| Control de costos | El humano decide cuándo gastar tokens de API |
| Control de calidad | El humano revisa antes de la siguiente fase |
| Aprendizaje | El usuario entiende qué hace cada agente |
| Construcción de confianza | Automatización gradual a medida que crece la confianza |

**Evolución Futura:**
- v1: Handoffs manuales (el humano presiona botones)
- v2: Semi-automático (el humano aprueba lotes)
- v3: Automatización configurable (el usuario define reglas para auto-handoffs)

**Creencia Central:**
> "Darle herramientas a esas personas que alguna vez pensaron en crear 'Netflix' y no pudieron por falta de conocimientos técnicos específicos."

Esto es democratización de capacidades, no automatización de humanos.

---

### 16.6 Preguntas Estratégicas Abiertas

| # | Pregunta | Owner | Estado |
|---|----------|-------|--------|
| 1 | ¿5+ usuarios externos comparten este punto de dolor? | Odin | ❓ Sin validar |
| 2 | ¿Cómo se comparan LangGraph/CrewAI/AutoGen? | Odin | ❓ Por evaluar |
| 3 | ¿$50/mes es el precio ancla correcto? | Odin | ❓ Hipótesis |
| 4 | ¿Pueden los no-developers usar este producto? | Kira | ❓ Por probar |
| 5 | ¿"Governance" es un punto de venta o jerga? | Odin | ❓ Por validar |
| 6 | ¿Debería v1 tener multi-usuario, aunque sea limitado? | Gravity | ❓ Por decidir |

---

### 16.7 Camino Crítico hacia la Validación

```
SEMANA 0-1: Análisis Competitivo
├── Probar LangGraph, CrewAI, AutoGen
├── Documentar gaps que ODIN Council llena
└── Confirmar que la diferenciación es real

SEMANA 1-2: Customer Discovery
├── 5 llamadas de discovery (founders técnicos)
├── 2 llamadas de discovery (personas no-dev)
├── Documentar puntos de dolor textualmente
└── Identificar disposición a pagar

SEMANA 3: Go/No-Go sobre ICP
├── Si validado → Continuar con ICP actual
├── Si mixto → Expandir a posicionamiento más amplio de "coordinador de equipo IA"
└── Si no validado → Pivotar o pausar

SEMANA 4-6: Construir con Validación
├── Compartir builds tempranos con usuarios interesados
├── Recolectar feedback sobre Brain + Handoffs
└── Iterar basado en uso real
```

---

## 17. Decision Log (Foundational)

### [2026-01-17] [Odin + All Agents] Decision: Use 7-Document Brain Structure

**Context:** Need shared memory for agents, but too many docs = chaos, too few = missing info  
**Options Considered:**
1. Single mega-doc (everything in one place)
2. Flexible structure (agents create docs as needed)
3. Mandated 7-doc structure (Vision, Architecture, DataContract, Decisions, Roadmap, Tasks, Glossary)

**Decision:** Option 3 (7-doc structure)  
**Rationale:**
- Predictable for AI retrieval (agents know where to look)
- Covers all critical areas (vision, tech, decisions, tasks)
- Not too rigid (each doc can grow organically)

**Impact:** All projects must have these 7 docs  
**Status:** ✅ Approved  

---

### [2026-01-17] [All Agents] Decision: Max 2 Rounds Per Handoff

**Context:** Prevent infinite loops and runaway costs  
**Options Considered:**
1. Unlimited rounds (agents retry until success)
2. 1 round only (no retries)
3. 2 rounds max (1 retry, then escalate)

**Decision:** Option 3 (2 rounds max)  
**Rationale:**
- Allows for 1 fix attempt (reasonable)
- Prevents loops (if 2nd round fails → human needed)
- Predictable cost (2 rounds = max 12 API calls per task)

**Impact:** Orchestrator enforces, Kira monitors  
**Status:** ✅ Approved  

---

### [2026-01-17] [Gravity] Decision: QA Mode A (CI Verification) for MVP

**Context:** Need QA with evidence, but sandbox is complex  
**Options Considered:**
1. Mode A (GitHub Actions logs)
2. Mode B (Local runner)
3. Mode C (Cloud sandbox)

**Decision:** Mode A for v1  
**Rationale:**
- Easiest to implement (no new infra)
- Provides real evidence (CI logs)
- Acceptable limitation: "QA can't test locally, only via CI"

**Impact:** Gemini reads CI logs, marks ✅/❌ based on test results  
**Status:** ✅ Approved  
**Future:** Mode B in v2, Mode C in v3  

---

### [2026-01-17] [Odin] Decision: Bootstrap First, Fundraise Only If Traction

**Context:** Should we raise pre-seed now or build first?  
**Options Considered:**
1. Raise $50k pre-seed immediately
2. Bootstrap MVP, fundraise after product-market fit validation
3. Go full self-funded forever

**Decision:** Option 2 (bootstrap → validate → fundraise)  
**Rationale:**
- MVP costs <$500 (no investor needed)
- Better valuation if we have users + revenue
- Avoids dilution for low-value raise

**Impact:** No fundraising until we hit: 50 users, $2k MRR, 60% retention  
**Status:** ✅ Approved  

---

### [2026-01-17] [Gravity] Decision: Decision Hierarchy (Who Vetoes What)

**Context:** Prevent design-by-committee paralysis  
**Options Considered:**
1. Consensus (everyone must agree)
2. Odin decides everything (bottleneck)
3. Tiered authority (Odin > Gravity > Kira > others)

**Decision:** Option 3 (tiered hierarchy)  
**Levels:**
- L1: Odin (veto everything)
- L2: Gravity (veto architecture/stack)
- L3: Kira (veto scope/priority)
- L4: Gemini (block merges on Quality Gate fails)
- L5: Claude/Grok (propose only, no veto)

**Rationale:** Clear authority prevents loops, allows fast decisions  
**Impact:** All agents must respect hierarchy, conflicts escalate up the chain  
**Status:** ✅ Approved  

---

## END OF MASTER DOCUMENT

**Next Steps:**
1. All agents read this document
2. Sprint 0 begins (Jan 17-19, 2026)
3. Gravity finalizes Architecture + DataContract
4. Kira creates Sprint 1 Task Cards
5. Odin approves stack decisions by Jan 19

**Questions? Escalate to Odin.**

---

**Estado del Documento:** ✅ LISTO PARA DISTRIBUCIÓN  
**Última Actualización:** 2026-01-17  
**Versión:** 1.1  
**Changelog:** Agregada sección de Validación Estratégica con insights del founder y preguntas abiertas