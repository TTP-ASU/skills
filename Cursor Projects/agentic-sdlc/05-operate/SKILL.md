---
name: operate
description: >-
  Support post-launch: runbooks, monitoring, incidents, and operational docs. Use
  when the user is launching, maintaining, or responding to production issues.
---

# Operate (SDLC phase)

Use this skill when the user is in **post-launch** or **operations**: **runbooks**, **monitoring**, **incidents**, or keeping operational docs up to date.

## When to use

- "Runbook", "launch checklist", "monitoring", "incident response", "operational doc", "post-launch".

## Workflow

1. **Clarify need:** Runbook for a system, launch checklist, incident playbook, or updating existing ops docs.
2. **Gather context:** Architecture (from **domain** or ubif-docs), existing runbooks (Notion, wiki), and contact/escalation info.
3. **Draft or update:** Create or refine runbooks, checklists, or playbooks with clear steps and owners.
4. **Where to store:** Suggest saving to Notion, Azure DevOps Wiki, or ubif-docs so the team can find them.

## Integration

- **domain** skill for architecture and system context.
- **Notion MCP** to create or update runbook/ops pages.
- **Azure DevOps MCP** for wiki pages (e.g. `wiki_create_or_update_page`).
- **reference** for existing ops standards or templates.
