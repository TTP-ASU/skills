# Project context: SSOT-SUR

Use this file so Cursor uses the right Notion pages and meeting database for SSOT-SUR.

---

## Current project

- **Name:** SSOT-SUR
- **Phase:** Discover

## Key documents

- **Product Brief:** https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b
- **PRD:** https://www.notion.so/asurionproduct/PRD-SUR-SSOT-3259532a1f8680b08cc4ebb72fe7b535
- **Architecture / ADRs:** _(If applicable)_
- **Template to use:** `templates/product-brief.md`, `templates/prd.md` (or your Notion templates)
- **Meeting notes:** https://www.notion.so/3259532a1f8680c79296c1be61fa982d (Meetings database)
- **Open questions:** `project/ssot-sur/docs/open-questions.md` (table: Question | Source | Owner | Status | Answer | Date). Brief/PRD §7 point here.

## Connections

- **Notion:** Asurion workspace; Brief and PRD pages and meeting DB linked above.
- **Jira:** _(To be connected at handoff)_
- **Azure DevOps:** _(To be connected at handoff)_

## Notion MCP (global)

- **Config:** Cursor global MCP, not from this repo. Server: `npx @notionhq/notion-mcp-server` (NOT mcp.notion.com / OAuth).
- **Auth:** `NOTION_TOKEN` env in `~/.cursor/mcp.json` (Notion Internal Integration Secret). Same setup as AT&T BYOD prototype; no project-level `.cursor/mcp.json`.
- **Tools:** Use **notion-fetch**, **notion-update-page**, **notion-search** (and related Notion tools) when reading or updating Notion. Server name in MCP: **plugin-notion-workspace-notion** (or the server that exposes these tool names).
- **401:** Token invalid or the page/database is not shared with the integration. In Notion: open the page or DB → **⋯ → Connections** → add the integration.

## Notes

_(Stakeholders, key dates, definitions of done.)_
