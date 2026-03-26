---
name: handoff
description: >-
  Support handoff from product to delivery: epics, user stories, Jira/DevOps work
  items, kickoff prep. Use when the user is ready to pass work to engineering or
  create trackable items.
---

# Handoff (SDLC phase)

Use this skill when the user is **handing off** approved briefs/PRDs to engineering: creating **epics**, **user stories**, and **trackable work** in Jira or Azure DevOps.

## When to use

- "Create epics from this PRD", "break down into user stories", "hand off to eng", "add to Jira/DevOps", "sprint planning prep".

## Workflow

1. **Confirm source:** Approved Product Brief or PRD (link, Notion page, or pasted summary).
2. **Choose destination:** Jira (Asurion), Azure DevOps, or Notion (backlog database).
3. **Break down:**  
   - One **epic** per major capability or theme.  
   - **User stories** with clear "As a… I want… So that…" and acceptance criteria.
4. **Create items (when MCP connected):**  
   - **Jira:** Use Atlassian MCP to create epics and stories, link as needed.  
   - **Azure DevOps:** Use `wit_create_work_item` (Epic, Feature, User Story, Task) and `wit_add_child_work_items` to keep hierarchy.  
   - **Notion:** Use Notion MCP to create or update database rows for epics/stories.
5. **Kickoff prep:** Suggest a short kickoff agenda or checklist (what was agreed, where things live, next review date).

## Integration

- **discover-define** and **review** feed into handoff; **verify** uses the same work items for acceptance.
