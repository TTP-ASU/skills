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
- PRD = **what and why** (business context, product requirements, functional requirements, user/process flows)  
- §1 Overview · §2 Stakeholders & RACI · §3 Business Problem · §4 Goals · §5 Scope · §6 Dependencies · §7 Product Requirements + FRs (grouped by theme/epic) · §8 NFRs · §9 User/Process Flows · §10 Success Metrics · §11 Roadmap · §12 Open Questions · §13 Appendix  
- Do not include technical design, architecture, or implementation detail here  

**TRD (technical design + backlog)** – see `templates/trd.md`  
- TRD = **how** (architecture, system interactions, data mapping, APIs, migration, cutover, validation, support model, engineering backlog)  
- §1 Overview (refs PRD) · §2 Architecture · §3 System Interactions · §4 Data Mapping · §5 APIs/Interfaces · §6 Migration Mechanics · §7 Cutover · §8 Technical Validation · §9 Operational Support · §10 Engineering Backlog (epics + stories) · §11 Open Questions (technical) · §12 FR Coverage Audit  
- Do not restate business context; reference the PRD  

**Sync rules between PRD and TRD:**  
- PRD is source of truth for intent; TRD is source of truth for implementation  
- Shared terms (initiative name, system names, flow IDs, FR IDs, entity names) must be identical across both docs  
- Every PRD flow must trace to a TRD implementation; every FR must trace to TRD stories via the FR Coverage Audit  
- Product/business open questions stay in the PRD; technical open questions stay in the TRD  
- Both docs open with a short cross-reference: the PRD points to the TRD and vice versa  

If they use a Notion template, mirror that structure. For in-repo work, use `templates/product-brief.md`, `templates/prd.md`, and `templates/trd.md`; for open-question tracking use `docs/open-questions.md` or the PRD §12.

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
