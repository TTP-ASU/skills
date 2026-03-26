# SSOT-SUR — Cursor command reference

## Quick reference

| Command | What to type |
|---------|-------------|
| Pull meeting notes | `Capture meeting: [name / link / "latest"]` |
| Resolve open question | `Answer: A1 — [text]. Source: [person, date]` |
| Pull Notion comments | `Sync Notion notes` |
| Process a new document | `Ingest document: @path/to/file.pdf` |
| ServiceBench field table (OQ F1) | `Ingest document: @servicebench-docs/[file]` |
| Draft story AC (DAX + SB rules) | `Write story: [ID]` |
| Validate story AC against sources | `Validate AC: [ID]` |
| Change a specific FR | `Update FR-4: [describe the change]` |
| Mark story ready to groom | `Story ready: [story ID]` |
| Log ADO work item | `ADO created: [story ID] = [URL]` |
| Audit PRD health | `PRD health check` |
| Draft weekly update | `Draft leadership update: week of [date]` |
| Archive past updates | `Archive updates` |
| Log a scope change | `Scope change: [description]` |
| Sync to Notion | `Push PRD` / `Push TDR` / `Push all` |

---

Copy-paste (or paraphrase) any command below. Cursor will follow the workflow defined in `.cursor/rules/pm-document-style.mdc` and `.cursor/rules/meeting-notes-and-open-questions.mdc`. For DAX field names and ServiceBench F1 placeholders, also apply `project/ssot-sur/.cursor/rules/dax-api-reference.mdc` when working in SSOT-SUR.

**All commands follow the review-before-push rule:** Cursor drafts locally and shows you a diff before touching Notion.

---

## Meeting notes

```
Capture meeting: [meeting name or Notion link or "latest from the meetings DB"]
```
**What happens:** Fetches notes from the Notion meetings database (or the link/paste you provide) → extracts decisions, scope changes, new requirements, and answered questions → proposes specific edits to PRD-FR, open-questions.md, and TDR. Shows a diff. Waits for approval before pushing.

**Variants:**
- `Capture meeting: DAX-SB Integration Mar 6` — fetch by name
- `Capture meeting: [paste notes here]` — inline notes
- `Capture meeting: latest` — pull the most recent row from the Notion meetings DB

---

## Answer an open question

```
Answer: [question ID] — [answer]. Source: [person / meeting / date]
```
**What happens:** Marks the question Resolved in open-questions.md → removes `[ARCH]` tag from the relevant FR(s) if the blocker is cleared → updates the affected TDR story's `Blocked by` column → moves the story to `Grooming Ready` if all blockers are gone → updates the FR body with the decision. Shows diff. Waits for push approval.

**Examples:**
- `Answer: A1 — DAX owns peril-to-equipment-type translation. Source: Ankit, arch call Mar 20`
- `Answer: E2 — routing uses SB account ID + pipe-delimited location suffix to distinguish ISP vs SUR. Source: Bryant, Slack Mar 18`
- `Answer: B1 — Plan B confirmed (LCM-only + bypass flag). TELUS will not provide full inventory. Source: Ankit / TELUS call Mar 25`

---

## Notes or comments left in Notion

```
Sync Notion notes
```
**What happens:** Fetches the PRD-FR and TDR Notion pages → extracts any inline comments, callouts, or notes (e.g. from reviewers) → maps each note to the relevant FR, story, or open question → proposes updates. Shows diff.

**Variants:**
- `Sync Notion notes: PRD only` — limit to the PRD-FR page
- `Sync Notion notes: TDR only` — limit to the TDR page
- `Sync Notion notes: [paste comment here]` — process a specific comment you copy from Notion

---

## New document (PDF, Word, notes file)

```
Ingest document: [drag file into chat or provide path]
```
**What happens:** Reads the document → extracts requirements, decisions, scope changes, and constraint details → maps each item to an existing FR (or proposes a new FR if nothing fits) → shows a diff of proposed additions and changes to PRD-FR and TDR. Flags any conflicts with current content.

**Examples:**
- `Ingest document: @pdfs/DAX-API-spec-v2.pdf` — extract technical constraints and map to FRs
- `Ingest document: @pdfs/TELUS-plan-B-decision.docx` — extract decision and answer the relevant open questions
- `Ingest document: [paste raw text]` — process a block of text directly

---

## ServiceBench field documentation (OQ F1)

```
Ingest document: @servicebench-docs/[file name or path]
```
**What happens:** Reads the uploaded or pasted document (Raghu/SCM field table, export, or spreadsheet) → maps each ServiceBench field to rows in `01-discovery/servicebench-docs/field-table.md` → proposes updates to `01-discovery/open-questions.md` (mark **F1** Resolved with source/date when the table is complete) → proposes **TRD §4 Data Mapping** stubs or full content in `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md` → re-evaluates stories with `Blocked by: F1` (e.g. EP5-S4, EP6-S1) and proposes `Grooming Ready` only when **F1** and any other blockers (e.g. **F2**) are resolved. Shows diff. Waits for approval before Notion push.

**Examples:**
- `Ingest document: @servicebench-docs/raghu-part-master-fields.xlsx`
- `Ingest document: @01-discovery/servicebench-docs/paste-field-table.txt`

**Cross-check:** Validated DAX field names remain in `01-discovery/dax-repos/`; this command fills the **ServiceBench** side of the mapping.

---

## Write or validate story acceptance criteria

```
Write story: [story ID]
```
**What happens:** Opens the story block in the TDR (`01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`) → drafts or expands **Acceptance criteria** using **confirmed DAX** field names from `01-discovery/dax-repos/` (`inventory-api.md`, `github-repos.md`) → for any required **ServiceBench** field not yet in `01-discovery/servicebench-docs/field-table.md`, inserts **`[pending F1 — Raghu/SCM]`** instead of inventing names → checks `Blocked by` in the master backlog against `01-discovery/open-questions.md` and does **not** recommend `Grooming Ready` while a blocker is Open. Shows diff.

**Examples:**
- `Write story: US-2.1`
- `Write story: US-5.4`

```
Validate AC: [story ID]
```
**What happens:** Reads the story's numbered AC → checks each technical field name against `01-discovery/dax-repos/` (DAX) and `01-discovery/servicebench-docs/field-table.md` (ServiceBench) → lists **unknown or unconfirmed** fields → suggests replacing guessed SB fields with **`[pending F1 — Raghu/SCM]`** where applicable. Read-only or suggested edits only (user approves).

**Examples:**
- `Validate AC: US-2.1`
- `Validate AC: US-6.1`

---

## Update a specific FR

```
Update FR-[X]: [describe the change]
```
**What happens:** Updates the FR row in PRD-FR → checks TDR for all stories linked to that FR → proposes cascading updates to acceptance criteria or blockers. Shows diff.

**Examples:**
- `Update FR-4: Plan B confirmed for TELUS. Remove Plan A as preferred option; bypass flag approach is now the design.`
- `Update FR-8: JIT order creation is a single combined API call (not separate). Resolves D4.`

---

## Mark a story as ready / update ADO ID

```
Story ready: [story ID]
```
```
ADO created: [story ID] = [ADO work item URL]
```
**What happens (story ready):** Sets TDR status to `Grooming Ready` for that story, after confirming all `Blocked by` items are resolved.

**What happens (ADO created):** Fills the ADO Story ID column in the TDR master backlog with the link and changes status to `In ADO`.

**Examples:**
- `Story ready: US-2.1` — mark as Grooming Ready
- `ADO created: US-2.1 = https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/688001`

---

## PRD health check

```
PRD health check
```
**What happens:** Audits the full PRD-FR + TDR and produces a snapshot:
- Open `[ARCH]` blockers by FR
- Stories blocked vs grooming-ready vs in ADO
- FRs with no story coverage
- Open questions with no owner
- Any FR/TDR drift (FR updated but TDR not reflecting it)

No changes made — read-only output.

---

## Weekly leadership update

```
Draft leadership update: week of [date]
```
**What happens:** Pulls current project status from PRD-FR, TDR, and open questions → drafts the weekly update → posts to the APC-2299 project page in Notion under `## Project Latest Update — Week of [date]`. Shows draft first, pushes on approval.

**Leadership update rules (applied automatically):**
- **Include:** meetings held, working sessions, decisions made, milestones, architecture progress, risks with mitigants, decisions needed from leadership
- **Exclude:** internal document changes (PRD edits, RACI updates, story counts, Notion tooling, COMMANDS.md), story-level backlog details, Notion/ADO links in the body
- **Format:** tables and bullets only; no prose; no story IDs or page URLs

---

## Archive past updates

```
Archive updates
```
**What happens:** Moves the previous week's leadership update from the main project page into the **Past Updates Archive** child page (`🗂️`), formatted as a collapsible toggle. The current week's update stays visible on the project page. Older entries accumulate in the archive, each as an expandable toggle labelled `Week of [date] — [status emoji] [STATUS]`.

- Archive page: [Past Updates Archive](https://www.notion.so/32d9532a1f8681659c54d87f503f1aad) (child of APC-2299 project page)
- Always shows a diff before making any Notion changes.

**Variants:**
- `Archive updates` — auto-detects all sections older than the current week and moves them
- `Archive updates: March 16` — archive a specific week by date

---

## Scope change

```
Scope change: [describe what's in or out and why]
```
**What happens:** Identifies all affected FRs and TDR stories → proposes PRD §5 (scope) and appendix updates → flags open questions that need revisiting. Shows diff.

**Examples:**
- `Scope change: UBIF Legacy is out of scope. All stores migrating to Next Gen by Q3; no bridge solution needed.`
- `Scope change: BAU Portal feed migration is now confirmed in scope for Q4.`

---

## Full Notion push (all local changes)

```
Push PRD
```
```
Push TDR
```
```
Push all
```
**What happens:** Pushes any pending local changes in the specified document(s) to their Notion pages. Always shows a diff summary first unless you say `push directly`.

---

> **Tip:** You don't have to use the exact wording above. These are patterns — Cursor will recognize reasonable paraphrases. The key words are: `capture meeting`, `answer:`, `sync Notion notes`, `ingest document`, `ingest document: @servicebench-docs`, `write story`, `validate ac`, `update FR-`, `story ready`, `ADO created`, `PRD health check`, `draft leadership update`, `archive updates`, `scope change`.
