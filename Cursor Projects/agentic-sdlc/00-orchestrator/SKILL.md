---
name: orchestrator
description: >-
  Choose the right SDLC phase and skills for the current task. Use when the user
  starts a project, switches context, or asks "what should I do next?" so the agent
  can route to discover-define, review, handoff, verify, or operate.
---

# Orchestrator (SDLC phase selection)

Use this skill when the user is **starting work**, **switching projects**, or asking **"what phase am I in?"** or **"what should I do next?"** Route them to the right phase and remind them of project-specific docs and connections.

## Phase map

| Phase | When to use | Key skills |
|-------|-------------|------------|
| **01-discover-define** | New initiative, Product Brief, PRD, scope | discover-define |
| **02-review** | Reviewing briefs, PRDs, designs, or code | review |
| **03-handoff** | Passing to eng, creating epics/stories, kickoff | handoff |
| **04-verify** | Acceptance criteria, QA, sign-off | verify |
| **05-operate** | Launch, runbooks, monitoring, incidents | operate |
| **domain** | Need architecture or domain context | domain |
| **reference** | Consume standards, templates, existing docs | reference |

## What to do

1. **Clarify current goal:** "Are you starting a new brief, reviewing something, handing off to eng, or something else?"
2. **Point to the phase skill:** "Use the **discover-define** skill to create the Product Brief" (or the appropriate phase).
3. **Remind about project context:** If they have project-specific docs (Notion, wiki, ubif-docs) or MCPs (Notion, Jira, DevOps), suggest using them: "I can pull from your Notion Product Brief Template or create the epic in Jira once the brief is ready."

## Cross-phase flow

- Discover-define → Review → Handoff → Verify → Operate.  
- At any step, **domain** and **reference** can be used to pull in architecture or standards.
