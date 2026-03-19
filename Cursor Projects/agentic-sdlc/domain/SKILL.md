---
name: domain
description: >-
  Use domain and architecture context for the current project. Use when the user
  needs system context, architecture docs, or domain knowledge to write briefs,
  PRDs, or runbooks.
---

# Domain (architecture & system context)

Use this skill when the user needs **architecture**, **system context**, or **domain knowledge** to create or update Product Briefs, PRDs, runbooks, or decisions.

## When to use

- "What's the architecture for X?", "pull in architecture doc", "system context", "domain knowledge", "how does X work?", referencing ubif-docs or Notion architecture pages.

## What to do

1. **Identify the system or domain:** e.g. UBIF Stores, specific service, integration, or capability.
2. **Find sources:**  
   - **Notion:** Use Notion MCP to search or open architecture/ADR pages the user names or links.  
   - **Azure DevOps Wiki:** Use DevOps MCP to read wiki pages (e.g. architecture, ADRs).  
   - **Repo docs:** If ubif-docs (or similar) is open in the workspace, read relevant markdown/docs.  
   - **User-provided:** User pastes or attaches architecture snippets or links.
3. **Summarize or apply:** Give a short summary, answer a specific question, or weave the relevant parts into the current artifact (Brief, PRD, runbook).
4. **Cite:** Name the doc or page so the user can trace back.

## Integration

- Feeds **discover-define** (briefs/PRDs), **review**, **handoff** (scope), **operate** (runbooks).
- Works with **reference** when standards or templates are also needed.
