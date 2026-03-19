# Project context: SSOT-SUR

Use this file so Cursor uses the right Notion pages and meeting database for SSOT-SUR.

---

## Current project

- **Name:** SSOT-SUR
- **Phase:** Discover

## Key documents

- **Project page (APC-2299):** https://www.notion.so/3179532a1f8680daad25f1f0a0215679 ← post status updates here
- **Product Brief:** https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b · local: `01-discovery/Product-Brief-SSOT-SUR.md`
- **PRD — Functional Requirements:** https://www.notion.so/3259532a1f8680b08cc4ebb72fe7b535 · local: `01-discovery/PRD-Functional-Requirements-SSOT-SUR.md`
- **PRD — Technical Development Requirements:** https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f · local: `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`
- **Architecture / ADRs:** _(If applicable)_
- **Template to use:** `templates/product-brief.md`, `templates/prd.md` (or your Notion templates)
- **Meeting notes:** https://www.notion.so/3259532a1f8680c79296c1be61fa982d (Meetings database) · to process a raw transcript, use `Ingest document: @path/to/file`
- **Open questions:** `01-discovery/open-questions.md` (table: Question | Source | Owner | Status | Answer | Date). Brief/PRD §7 point here.
- **Reference PDFs:** `references/` (source documents, exports, PDFs)

## Connections

- **Notion:** Asurion workspace; Brief and PRD pages and meeting DB linked above.
- **Jira:** _(To be connected at handoff)_
- **Azure DevOps:** 
  - Org: `axasurion` · Project: `AX7 Core`
  - Area path: `AX7 Core\Global\Supply Chain\Client and New Channel`
  - Epic: [676287 — Inventory SSOT for SUR](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676287)
  - Teams: Client and New Channel · The Avengers · BeyondX

## Notion MCP (global)

- **Config:** Cursor global MCP, not from this repo. Server: `npx @notionhq/notion-mcp-server` (NOT mcp.notion.com / OAuth).
- **Auth:** `NOTION_TOKEN` env in `~/.cursor/mcp.json` (Notion Internal Integration Secret). Same setup as AT&T BYOD prototype; no project-level `.cursor/mcp.json`.
- **Tools:** Use **notion-fetch**, **notion-update-page**, **notion-search** (and related Notion tools) when reading or updating Notion. Server name in MCP: **plugin-notion-workspace-notion** (or the server that exposes these tool names).
- **401:** Token invalid or the page/database is not shared with the integration. In Notion: open the page or DB → **⋯ → Connections** → add the integration.

## Phase gates — deferred actions

Actions to take when the project moves to the next phase. Cursor: surface these when the phase changes.

### On entering Grooming / Review phase

- [ ] **Convert TDR to Notion relational database (Option 2)**
  - Set up 3 linked Notion databases on the TDR page: FRs · Epics · Stories
  - Schema: Stories have Relation properties back to Epic and FR rows; ADO Story ID (Number) + ADO URL fields
  - Seed from the flat master table in `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`
  - Views to create: "Ready to groom" (Status = Draft, Blocked by = empty) · "By Epic" · "By FR" · "Not in ADO yet"
  - Reference: TDR restructuring conversation, 2026-03-16

- [ ] **Connect DAX and ServiceBench via MCP** (see `01-discovery/mcp-integration-proposal.md`)
  - Tier 1: add `mcp-fetch` pointing at D365 `$metadata` endpoint (non-prod) — ask DAX team for endpoint + service account
  - Tier 2: `servicebench-mcp` (field defs, job types) + `dax-ivs-mcp` (availability, BOM, item)
  - Pre-req: confirm non-prod D365 endpoint and SB API spec with Bryant / DAX Arch

### On entering Build / Sprint phase

- [ ] Switch TDR from PM authoring tool to ADO-driven status view
  - ADO stories drive sprint tracking; Notion TDR becomes read-only FR-coverage view
  - Sync ADO Feature/Story status back to TDR Status column weekly

## Notes

_(Stakeholders, key dates, definitions of done.)_
