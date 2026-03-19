---
name: discovery-doc-sync
description: >-
  Keeps discovery documents in sync with meeting notes and decisions during the discovery phase of a project.
  Use when the user wants to pull in meeting notes, capture an open question answer, update the PRD or TDR,
  run a document health check, or push changes to Notion. Triggers on phrases like "capture meeting",
  "update discovery docs", "sync docs", "PRD health check", "push PRD", "push TDR", "answer [ID]",
  "update open questions", or any request to refresh discovery artifacts.
---

# Discovery Document Sync

Manages the full update cycle for discovery documents: meeting notes → open questions → PRD-FR → TDR → Notion.

## Step 0: Load project context

Always start by reading `PROJECT-CONTEXT.md` in the project root (e.g. `project/ssot-sur/PROJECT-CONTEXT.md`). Extract:
- Notion page IDs for PRD-FR, TDR, and project page
- Notion meetings database URL
- Local file paths for all discovery docs

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
