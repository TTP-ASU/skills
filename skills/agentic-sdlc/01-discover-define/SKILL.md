---
name: discover-define
description: >-
  Guide Product Managers through the discover-and-define phase: creating Product Briefs,
  PRDs, and aligned scope. Use when the user wants to create a Product Brief, PRD, product
  requirements, discovery doc, or define scope for a project or epic. Works with Notion
  templates and MCPs when available.
---

# Discover & Define (Product Briefs & PRDs)

Use this skill when the user wants to **create a Product Brief**, **PRD**, or other discovery/definition artifacts. Guide them through structure, content, and (when possible) creation in Notion or export for Jira/DevOps.

## When to use

- User says: "create a Product Brief", "write a PRD", "product requirements", "discovery doc", "define scope", "brief for [feature/project]".
- User is starting a new initiative and needs a structured doc before development.

## Workflow

### 1. Clarify intent and source material

- **Document type:** Product Brief, PRD, one-pager, or other (e.g. Asurion/UBIF template).
- **Audience:** Executives, eng, design, partners.
- **Existing assets:** Ask if they have a Notion template (e.g. "Product Brief Template"), existing PRDs, or architecture/docs to align with. If they share Notion links or paths, use the Notion MCP to read structure and suggest alignment.
- **Scope:** Single feature, epic, or program.

### 2. Gather context

- **Problem and goals:** What problem are we solving? Success criteria?
- **Users and use cases:** Who is it for? Main flows?
- **Constraints:** Timeline, dependencies, tech/architecture (if they mention ubif-docs or architecture, offer to incorporate or summarize).
- **Out of scope:** What is explicitly not in scope for this brief/PRD?
- **Meeting notes (source and update PRD):** If PROJECT-CONTEXT has **Meeting notes** set to a **Notion database** (or database view link), use the **Notion MCP** to read that database — query or list rows, open linked pages for meeting/scripting entries — and **use the content to update the PRD (or Brief) with more context during discovery** so the user doesn’t have to do it manually. Extract: decisions, scope, requirements, acceptance criteria, answers to open questions; propose concrete section edits. If the user hasn’t set the database yet, ask for the Notion database URL or view link and offer to add it to PROJECT-CONTEXT. Proactively offer: “I can pull meeting scripting from your Notion database and update the PRD with that context.”
- **Open questions:** If there is an open-questions list (PRD section or `docs/open-questions.md`), offer to **capture answers** as they are resolved: update the list with answer and date, and reflect the answer in the relevant requirements section.

### 3. Propose structure

Suggest sections that match their doc type and org norms. Common patterns:

**Product Brief (high level)** – see `templates/product-brief.md`  
- Problem / opportunity  
- Proposed solution (summary)  
- Users & impact  
- Success metrics  
- Dependencies & risks  
- Open questions (track and capture answers)  
- Next steps / approval  

**PRD (implementation-ready)** – see `templates/prd.md`  
- Overview & goals  
- User stories / use cases  
- Functional requirements  
- Non-functional requirements  
- Dependencies (systems, teams, docs)  
- Success metrics & acceptance criteria  
- Open questions (capture answers; update requirements when resolved)  

If they use a Notion template, mirror that structure. For in-repo work, use `templates/product-brief.md` and `templates/prd.md`; for open-question tracking use `templates/open-questions.md` or the PRD section.

### 4. Draft and iterate

- Draft section by section (or full doc) in chat.
- Offer to create or update a **Notion page** if the Notion MCP is connected (e.g. "Create this as a new page under [parent]" or "Update the Product Brief at [link]").
- Call out places that should reference **architecture or other docs** (e.g. ubif-docs, ADRs) and offer to summarize or link.

### 5. Handoff to delivery

- Suggest a short **summary or checklist** for 02-review / 03-handoff (e.g. "Ready for review" vs "Needs architecture sign-off").
- If they use **Jira or Azure DevOps**, offer to break the PRD into epics/user stories once the brief/PRD is approved (using the relevant MCP).

## Integration with MCPs

- **Notion:** Create or update pages and databases; align with "Product Brief Template" or other templates the user names.
- **Jira / Azure DevOps:** After the brief/PRD is stable, help create projects, epics, and user stories from the requirements (when those MCPs are connected).
- **Documents:** Use linked or pasted architecture/docs (or content from Notion/DevOps Wiki) to keep the brief/PRD consistent with current system design.

## Quality checks before calling "done"

- [ ] Problem and success criteria are clear.
- [ ] Scope and out-of-scope are stated.
- [ ] Audience-appropriate (Brief = concise for execs; PRD = detailed enough for eng).
- [ ] Dependencies and open questions are listed.
- [ ] If referencing architecture or other docs, they are named or linked.
