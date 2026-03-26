---
name: pm-project-structure
description: >-
  Set up or advise on PM project folder structure, file organization, and
  naming conventions. Use when the user asks how to organize a project, whether
  to add a folder, where a file should live, or how to set up a new project
  in the workspace.
---

# PM project structure

## Core principle

**Add structure when a file has no obvious home — not before.**
A project that fits on one screen needs no sub-folders yet.

---

## Workspace layout

```
skills/                          ← workspace root (git repo)
├── .cursor/
│   └── rules/                   ← workspace-wide Cursor rules (apply to ALL projects)
│       ├── pm-document-style.mdc
│       └── meeting-notes-and-open-questions.mdc
├── project/
│   └── <project-slug>/          ← one folder per project
│       ├── PROJECT-CONTEXT.md   ← Notion links, ADO config, phase, MCP setup
│       ├── COMMANDS.md          ← copy-paste command triggers for this project
│       ├── README.md            ← one-liner: what this project is
│       ├── 01-discovery/        ← active when: Discover / Define phase
│       ├── 02-grooming/         ← add when: entering Grooming / Review phase
│       ├── 03-build/            ← add when: entering Sprint / Build phase
│       ├── references/          ← source PDFs, exports, vendor docs (read-only)
│       └── templates/           ← reusable doc templates for this project
└── skills/                      ← personal/shared agent skills
```

---

## File placement rules

| File type | Where it lives |
|-----------|---------------|
| Notion links, ADO org/project/area, MCP setup | `PROJECT-CONTEXT.md` |
| Command trigger reference | `COMMANDS.md` |
| Product Brief, PRD-FR, PRD-TDR, open questions | `01-discovery/` |
| Meeting notes | Notion database (not local); use `Ingest document: @file` for raw transcripts |
| Source PDFs, vendor exports, stakeholder decks | `references/` |
| Grooming artifacts, story maps, sprint plans | `02-grooming/` (add when needed) |
| ADO-driven sprint artifacts | `03-build/` (add when needed) |

---

## Phase gate — when to add a folder

| Folder | Add when you have… |
|--------|--------------------|
| `01-discovery/` | A Product Brief or first PRD draft |
| `02-grooming/` | Stories being groomed for a sprint |
| `03-build/` | Active sprint in ADO; TDR becomes read-only |
| `references/` | ≥1 source PDF or external doc that is not authored by you |
| `templates/` | A reusable template specific to this project |

Never create a folder for a single file you haven't written yet.

---

## Key files explained

### `PROJECT-CONTEXT.md`
Cursor reads this to know which Notion pages, ADO org/project/area, and MCP server to use. Keep it updated when:
- A new Notion page is created for the project
- The phase changes
- ADO Epic/Feature IDs are assigned

### `COMMANDS.md`
Quick-reference card for natural-language Cursor triggers (`Capture meeting:`, `Push PRD`, `PRD health check`, etc.). Add a row whenever a new repeatable workflow is established.

### Workspace-level rules
Rules in `.cursor/rules/` apply to **all projects** automatically — do not duplicate them inside a project folder. Only add a project-level rule (`.cursor/rules/<project>.mdc`) if a behavior is genuinely project-specific and would conflict with other projects.

---

## Setting up a new project

1. Create `project/<slug>/` with `PROJECT-CONTEXT.md`, `COMMANDS.md`, `README.md`
2. Add `01-discovery/` and drop the first Brief or PRD draft in it
3. Add `references/` if source PDFs exist
4. Fill in `PROJECT-CONTEXT.md`: Notion URLs, ADO config, phase = Discover
5. Do **not** create `02-grooming/` or `03-build/` yet

## Anti-patterns

- Creating all phase folders upfront "to be ready" — adds noise, no value
- Storing meeting notes locally when they already exist in Notion
- Duplicating workspace rules inside a project folder
- Using `docs/` or `drafts/` as folder names — phase-numbered folders are self-documenting and sort correctly
