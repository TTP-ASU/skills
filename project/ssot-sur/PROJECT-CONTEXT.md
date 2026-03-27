# Project context: SSOT-SUR

Use this file so Cursor uses the right Notion pages and meeting database for SSOT-SUR.

---

## Current project

- **Name:** SSOT-SUR
- **Phase:** Discover

## Key documents

- **Project page (APC-2299):** https://www.notion.so/3179532a1f8680daad25f1f0a0215679 ← post status updates here · **Leadership updates (local):** template `01-discovery/leadership-update-TEMPLATE.md` · dated drafts `01-discovery/leadership-updates/YYYY-MM-DD.md` (see folder `README.md`)
- **Product Brief:** https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b · local: `01-discovery/Product-Brief-SSOT-SUR.md`
- **PRD — Functional Requirements:** https://www.notion.so/3259532a1f8680b08cc4ebb72fe7b535 · local: `01-discovery/PRD-Functional-Requirements-SSOT-SUR.md`
- **PRD — Technical Development Requirements:** https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f · local: `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`
- **Architecture / ADRs:** _(If applicable)_
- **Template to use:** `templates/product-brief.md`, `templates/prd.md` (or your Notion templates)
- **Meeting notes:** https://www.notion.so/3259532a1f8680c79296c1be61fa982d (Meetings database) · to process a raw transcript, use `Ingest document: @path/to/file`
- **Open questions:** `01-discovery/open-questions.md` (table: Question | Source | Owner | Status | Answer | Date). Brief/PRD §7 point here.
- **WMA–SB Cycle Count Gap Analysis (Q3 prep):** https://www.notion.so/asurionproduct/WMA-SB-Cycle-Count-Tool-Gap-Analysis-32f9532a1f868024b736fa8dfabf21ea — analysis before user-flow sessions; referenced in PRD §6/§13 and TRD §2.
- **DAX API reference (confirmed):** `01-discovery/dax-repos/` — read path, write path, cross-validation, and source-level function analysis; use for acceptance-criteria field names and grooming prep in all DAX-facing stories. Source: `asurion-private` GitHub org (read access confirmed 2026-03-24). ADO connection to be established at QA validation phase.
- **ServiceBench field reference (pending OQ F1):** `01-discovery/servicebench-docs/` — partial knowledge from OQ F1; stub populated when Raghu/SCM delivers the full field table.
- **Reference PDFs:** `references/` (source documents, exports, PDFs)
- **Confluence (DDD — Feature Breakdown):** [Feature Breakdown](https://asurion.atlassian.net/wiki/spaces/DDD/pages/614007633/Feature+Breakdown) — SSOT / architecture feature list (space **DDD**). Use for traceability to DDD features in PRD/TRD; Cursor **Confluence MCP** must be authorized for automated fetch.

## Connections

- **Notion:** Asurion workspace; Brief and PRD pages and meeting DB linked above.
- **Confluence:** DDD space — [Feature Breakdown (614007633)](https://asurion.atlassian.net/wiki/spaces/DDD/pages/614007633/Feature+Breakdown). If MCP returns 401, open the page in a browser while on VPN; refresh the gateway **Bearer** token in `~/.cursor/mcp.json` if needed.
- **Jira:** _(To be connected at handoff)_
- **Azure DevOps:** 
  - Org: `axasurion` · Project: `AX7 Core`
  - Area path: `AX7 Core\Global\Supply Chain\Client and New Channel`
  - Epic: [676287 — Inventory SSOT for SUR](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676287)
  - Teams: Client and New Channel · The Avengers · BeyondX

## Notion MCP (Cursor)

Use whichever of these matches your machine — both talk to the same Notion workspace once auth is valid.

### A. Asurion MCP gateway (typical)

- **Config:** `~/.cursor/mcp.json` — server key is often `notion-mcp-server`, with the Notion route on the org MCP gateway (HTTPS URL under `mcp-prod-gateway.mcp.prd.aws.asurion.net`), **not** `mcp.notion.com` OAuth.
- **Auth:** `Authorization: Bearer <SSO token>` in headers (refresh when expired). Your org may also set profile/context headers; keep them aligned with other gateway MCPs (e.g. Jira, Confluence).
- **Tools in Cursor:** The same integration may appear as **plugin-notion-workspace-notion** in the MCP filesystem. Prefer tools such as **notion-fetch**, **notion-update-page**, and **notion-search** when reading or updating pages.

### B. Direct Notion official MCP (legacy / local)

- **Config:** `npx @notionhq/notion-mcp-server` with a Notion **internal integration** secret (e.g. `NOTION_TOKEN` in the server `env` in `~/.cursor/mcp.json`).
- **Sharing:** Each page and database must grant access: Notion **⋯ → Connections →** add the integration.

### Troubleshooting

- **401:** Bearer token expired (regenerate via your SSO/gateway flow) **or** (for B) invalid token **or** page/database not connected to the integration.
- **Wrong workspace:** Confirm the gateway profile/context headers match the workspace where these SSOT pages live.

## Azure DevOps MCP (Cursor)

SSOT work items live in **org** `axasurion`, **project** `AX7 Core` (spell this in natural-language prompts to ADO tools). This project uses the **Microsoft local** Azure DevOps MCP server (`@azure-devops/mcp`), not the Asurion HTTPS gateway — there is no separate `azure-devops` gateway block alongside Notion/Jira in typical setups.

### Configuration (`~/.cursor/mcp.json`)

Add (or restore) a server entry named e.g. `azure-devops`:

- **Command:** `npx`
- **Args:** `-y`, `@azure-devops/mcp`, `axasurion`, `-a`, `envvar`, `-d`, `core`, `work`, `work-items`, `wiki`
  - **`-a envvar`** is required for headless Cursor use. Without it, the server defaults to **interactive** OAuth and cannot authenticate in MCP.
  - `-d` lists **domains** (tool groups), not the ADO project name. `core` is required so tools can resolve org/project context.
- **Env:** `ADO_MCP_AUTH_TOKEN` = a [Personal Access Token](https://learn.microsoft.com/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate) for `dev.azure.com` / `*.visualstudio.com` with at least **Work Items** (read/write as needed) and **Wiki** if you use wiki tools. The `@azure-devops/mcp` package reads **this** variable name; `AZURE_DEVOPS_EXT_PAT` alone is not used by the MCP server (you may mirror the same PAT into both if other CLIs expect the old name).

Example shape (replace the PAT with your secret; do not commit this file to git):

```json
"azure-devops": {
  "command": "npx",
  "args": [
    "-y",
    "@azure-devops/mcp",
    "axasurion",
    "-a",
    "envvar",
    "-d",
    "core",
    "work",
    "work-items",
    "wiki"
  ],
  "env": {
    "ADO_MCP_AUTH_TOKEN": "<paste PAT from Azure DevOps user settings>"
  }
}
```

### Restore when tools stop working

1. In Azure DevOps: **User settings → Personal access tokens** → create a new token (or extend scope if using fine-grained tokens).
2. Paste into **`ADO_MCP_AUTH_TOKEN`** in `~/.cursor/mcp.json` (and optionally `AZURE_DEVOPS_EXT_PAT` if you keep both in sync).
3. **Restart Cursor** (or reload MCP servers) so the process picks up the new env.

### Troubleshooting

- **401 / auth errors:** PAT expired, revoked, or missing **Work Items** scope for the org.
- **Wrong project in results:** Specify **project** `AX7 Core` in prompts; the org alone is not enough for scoped queries.
- **Remote MCP (optional):** Microsoft also offers a [Remote Azure DevOps MCP](https://learn.microsoft.com/azure/devops/mcp-server/remote-mcp-server); migrating is optional if the local `npx` server meets your needs.

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
