# Asurion Product skills (Cursor)

Product-management skills and structure **as proposed by Asurion**: agentic SDLC phases, project context, and templates for Briefs and PRDs.

**New to this repo?** See **[STRUCTURE.md](STRUCTURE.md)** for how everything is organized (skills vs skill-template vs templates, rules, PROJECT-CONTEXT) so you can use it as the master for any project.

**For Cursor and MCP setup** (Notion, Jira, Azure DevOps connections), follow **Asurion’s official guidance** (e.g. UBIF Stores Cursor Setup in Notion or your IT team).

**Notion (global MCP):** Configured via Cursor's global MCP (`npx @notionhq/notion-mcp-server`; auth: `NOTION_TOKEN` in `~/.cursor/mcp.json`). Use **notion-fetch**, **notion-update-page**, **notion-search** when reading or updating Notion. 401 → check token or share the page with the integration (Notion → Connections).

---

## What’s in this repo (Product only)

### 1. Agentic SDLC skills (`skills/agentic-sdlc/`)

Phases that appear in the Cursor Skills panel:

| Phase | Use for |
|-------|--------|
| **00-orchestrator** | Route to the right phase; suggest project docs and tools |
| **01-discover-define** | Product Briefs, PRDs, scope |
| **02-review** | Review briefs, PRDs, designs |
| **03-handoff** | Epics, user stories, Jira/DevOps creation |
| **04-verify** | Acceptance criteria, sign-off |
| **05-operate** | Runbooks, launch, incidents |
| **domain** | Architecture and system context |
| **reference** | Templates and standards |

Use the **orchestrator** when you’re not sure which phase to use.

### 2. Project context (`PROJECT-CONTEXT.md`)

Fill in the current project name, key docs (Brief, PRD, architecture), meeting notes path, and open questions path. The agent uses this when working on a project.

### 3. Templates (`templates/`)

- **product-brief.md** – Product Brief structure
- **prd.md** – PRD structure  
- **open-questions.md** – Track and capture answers to open questions

Reference these when creating or updating Briefs and PRDs. Use meeting notes (path in PROJECT-CONTEXT) to update PRDs; use the open-questions list to capture answers and keep requirements in sync.

### 4. Cursor rules (`.cursor/rules/`)

Product management rules the agent follows:

| Rule | Purpose |
|------|--------|
| **project-building-blocks.mdc** | Use PROJECT-CONTEXT, SDLC phases, templates, and project docs/tools (Notion, Jira, DevOps). |
| **meeting-notes-and-open-questions.mdc** | Use meeting notes to update PRDs/requirements; capture answers to open questions and keep requirements in sync. |
| **product-management.mdc** | Brief vs PRD; quality bar for artifacts; PM owns decisions and sign-off; agent assists and cites. |

To see what each rule does and how to customize: **docs/PRODUCT-MANAGEMENT-RULES.md**.

---

## Quick reference

| Goal | Action |
|------|--------|
| Create a Product Brief or PRD | Use skill **01-discover-define** or ask “create a Product Brief for…” |
| Review a Brief or PRD | Use skill **02-review** |
| Create epics/user stories | Use skill **03-handoff** (with Jira/DevOps connected per Asurion setup) |
| Set project context | Edit **PROJECT-CONTEXT.md** with current project, docs, meeting notes, open questions |
| Connect Notion / Jira / DevOps | Follow **Asurion’s official Cursor/MCP setup** (Notion page or IT) |
