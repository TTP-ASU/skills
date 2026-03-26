---
name: discovery-doc-sync
description: >-
  Keeps discovery documents in sync with meeting notes and decisions during the discovery phase of a project.
  Use when the user wants to pull in meeting notes, capture an open question answer, update the PRD or TDR,
  run a document health check, or push changes to Notion. Triggers on phrases like "capture meeting",
  "update discovery docs", "sync docs", "PRD health check", "push PRD", "push TDR", "answer [ID]",
  "update open questions", "ingest document", "ingest servicebench", "write story", "validate ac",
  or any request to refresh discovery artifacts.
---

# Discovery Document Sync

Manages the full update cycle for discovery documents: meeting notes → open questions → PRD-FR → TDR → Notion.

## Step 0: Load project context

Always start by reading `PROJECT-CONTEXT.md` in the project root (e.g. `project/ssot-sur/PROJECT-CONTEXT.md`). Extract:
- Notion page IDs for PRD-FR, TDR, and project page
- Notion meetings database URL
- Local file paths for all discovery docs
- For **SSOT-SUR**: paths to `01-discovery/dax-repos/` (confirmed DAX) and `01-discovery/servicebench-docs/` (ServiceBench — pending OQ F1 until field table is delivered)

## Document hierarchy (changes flow downward only)

```
Meeting notes → open-questions.md → PRD-FR → TDR → Notion
```

ADO stories never update the PRD without a meeting decision first. Notion is the published layer; local `.md` files are the draft/review layer.

## Key files (SSOT-SUR)

| File | Purpose |
|------|---------|
| `01-discovery/open-questions.md` | Single source of truth for all open questions |
| `01-discovery/PRD-Functional-Requirements-SSOT-SUR.md` | Functional PRD (§2 RACI, §2a flows, §7 OQs) |
| `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md` | TDR (master backlog, story blockers) |
| `01-discovery/personas.md` | Persona definitions linked to flows and OQs |
| `01-discovery/dax-repos/` | Confirmed DAX read/write field names and patterns for AC and architecture (inventory API + GitHub write-path analysis) |
| `01-discovery/servicebench-docs/` | ServiceBench Part Master field reference — **`field-table.md` is a stub until OQ F1** (Raghu/SCM); use `[pending F1 — Raghu/SCM]` in AC when SB fields are unknown |
| `project/ssot-sur/.cursor/rules/dax-api-reference.mdc` | Project rule: never invent DAX/SB field names; DAX from `dax-repos/`, SB from `servicebench-docs/` or F1 placeholder |

## Field validation during document ingestion (SSOT-SUR)

When ingesting any document for **SSOT-SUR** (general `ingest document:` or ServiceBench-specific — see `project/ssot-sur/COMMANDS.md`):

1. **DAX fields** — Cross-check extracted field names against `01-discovery/dax-repos/` (`inventory-api.md`, `github-repos.md`, `README.md`). Treat names in those files as **confirmed** for acceptance criteria wording unless the source document explicitly supersedes them (then flag a conflict).
2. **ServiceBench fields** — Cross-check against `01-discovery/servicebench-docs/field-table.md`. If a field is not listed there, mark it **unconfirmed** or use **`[pending F1 — Raghu/SCM]`** until the Part Master table is complete.
3. **Unknown names** — Flag any field name that appears in ingested content but is not found in either source as **unconfirmed**; do not silently add to PRD/TDR as fact without user acknowledgment.
4. **OQ F1 delivery (ServiceBench field table)** — When the ingested document **is** (or completes) Raghu’s ServiceBench field table:
   - Populate or replace `01-discovery/servicebench-docs/field-table.md` with the full table (remove `[STUB — pending OQ F1 completion]` banner when done).
   - Update `01-discovery/open-questions.md`: **F1** → Resolved, Answer + Date + Source.
   - Update **TRD §4 Data Mapping** in `PRD-Technical-Development-Requirements-SSOT-SUR.md` with SB → DAX/F&O mapping columns as appropriate.
   - Re-evaluate every story with **`Blocked by: F1`** (e.g. EP5-S4, EP6-S1); if all blockers for that story are Resolved, propose **Grooming Ready** per existing gating rules (F2 may still block some stories).

## Commands — run these workflows on trigger

See [commands.md](commands.md) for full detail on each. Summary:

| Trigger | Workflow |
|---------|----------|
| `capture meeting: [name/link/"latest"]` | Fetch notes from Notion meetings DB → extract decisions, scope, OQ answers → propose diffs |
| `answer: [ID] — [text]. source: [...]` | Resolve OQ row → update PRD-FR §7 + TDR Blocked by → promote story if all blockers gone |
| `PRD health check` | Read-only audit: open [ARCH] blockers, stories blocked vs ready, FR coverage gaps, OQs without owner |
| `sync docs` | Check all local files for drift vs each other; surface what is stale |
| `push PRD` / `push TDR` / `push all` | Show diff → wait for approval → push to Notion |
| `ingest document: [file or paste]` | Map content to existing FRs or propose new ones; flag conflicts |
| `ingest document: @servicebench-docs/[file]` | SB field table → `field-table.md`, OQ F1, TRD §4, unblock F1 stories (see `project/ssot-sur/COMMANDS.md`) |
| `write story: [ID]` | Draft AC using `dax-repos/`; stub SB with `[pending F1]` where needed |
| `validate ac: [ID]` | Check story AC field names against `dax-repos/` + `servicebench-docs/field-table.md` |
| `scope change: [description]` | Update PRD §5 scope + flag affected FRs and TDR stories |

## Update workflow (required sequence)

1. **Draft locally first** — edit the `.md` file.
2. **Show diff summary** — bullet list of what changed (section, what added/modified/removed). Do NOT push yet.
3. **Wait for approval** — user says "push", "looks good", or equivalent.
4. **Push to Notion** — use `notion-update-page` with `update_content` (targeted search-and-replace, not full replace). Push only changed sections.
5. **Confirm** — report which Notion page(s) were updated.

> Exception: skip step 3 only if user explicitly says "push directly".

## open-questions.md update rules

- **New answer given** → update Status → Resolved, fill Answer + Date + Source. Then update the relevant FR body and TDR Blocked by column.
- **New question** → add to the correct section (A–I), tag `[ARCH]` if it blocks a FR.
- **Section I** is reserved for API Architecture blockers (I1–I3 currently: BOM API, AOP JIT reservation, Substitution Matrix).
- One source of truth: `01-discovery/open-questions.md`. The `docs/` copy has been deleted.

## PRD-FR update rules

- **§2 RACI** — 5 named engineering teams: DAPI, Integration, BeyondX, Avengers, ETL.
- **§2a Architecture flows** — 4 categories: RT (runtime), INT (integration/feed), IL (inventory lifecycle), CF (configuration). Architecture diagrams are NOT embedded — reference Confluence link when available.
- **§7 Open questions** — mirrors open-questions.md. Update G1 answer, add new rows, mark resolved.
- Always bump `**Last updated:**` date.

## TDR update rules

- Add new OQ IDs to the `Blocked by` column of affected stories in the master backlog table.
- A story moves to `Grooming Ready` only when every OQ in its `Blocked by` column is Resolved.
- Update story detail blocks (As a / I want / So that + AC) when scope changes.
- Always bump `**Last updated:**` date.
- Current blockers to watch: I1 → EP1-S1, EP6-S1 · I2 → EP4-S1, EP4-S2, EP5-S1 · I3 → EP6-S2.

## Notion push reference

| Page | ID |
|------|----|
| PRD — Functional Requirements | `3259532a1f8680b08cc4ebb72fe7b535` |
| PRD — Technical Development Requirements | `3259532a1f8680e0946ec9fbb1e85d2f` |
| Project page (APC-2299) | `3179532a1f8680daad25f1f0a0215679` |
| Meetings database | `3259532a1f8680c79296c1be61fa982d` |

Use `notion-update-page` with `update_content` and targeted `old_str` / `new_str` pairs. Always fetch the page first to get exact strings. Notion table format uses `<table>` / `<tr>` / `<td>` XML-style syntax (not Markdown pipe tables).
