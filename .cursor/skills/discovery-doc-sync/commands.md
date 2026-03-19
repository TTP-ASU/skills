# Discovery Sync — Command Reference

Extended patterns and step-by-step behavior for each command trigger.

---

## `capture meeting: [name / link / "latest"]`

**Trigger examples:**
- `capture meeting: latest`
- `capture meeting: SSOT EA Support 2026-03-18`
- `capture meeting: https://www.notion.so/...`

**Steps:**
1. Read `PROJECT-CONTEXT.md` → get Notion meetings database URL.
2. Use `notion-fetch` or `notion-query-data-sources` to pull the meeting row(s). If "latest", fetch the most recent entry by date.
3. Open the linked meeting page and read full content.
4. Extract: decisions made, scope changes, answers to open questions, new blockers.
5. Map extracted content to the document hierarchy:
   - Answers → `open-questions.md` (update Status, Answer, Date, Source)
   - New questions → `open-questions.md` (add row in correct section, tag `[ARCH]` if applicable)
   - Scope changes → PRD-FR §5 (Dependencies) and §2a (flow tables)
   - RACI changes → PRD-FR §2
   - New blockers → TDR Blocked by column for affected stories
6. Show proposed diffs for each file. Wait for approval before editing.
7. On approval: edit local files, then push to Notion.

---

## `answer: [ID] — [text]. source: [meeting/date/person]`

**Trigger examples:**
- `answer: A1 — DAX owns peril mapping. source: Architecture review 2026-03-24`
- `answer: I1 — BOM embedded in EIAA (Option 2). source: Ankit 2026-03-25`

**Steps:**
1. Find the OQ row in `open-questions.md`.
2. Update: Status → Resolved, Answer → [text], Date → today, Source → [source].
3. If `[ARCH]` tag: remove `[ARCH]` from the `#` column if the decision fully resolves it.
4. Update the relevant **FR body** in PRD-FR (not just §7 — update the actual requirement description too).
5. Update **TDR Blocked by** column: remove this OQ ID from all story rows. If a story's Blocked by is now empty → change Status to `Grooming Ready`.
6. Show diff summary across all three files (open-questions.md, PRD-FR, TDR). Wait for approval.
7. On approval: push changed sections to Notion.

**[ARCH] tag removal rule:** Only remove `[ARCH]` if the decision is final and confirmed. If still pending EA sign-off, keep `[ARCH]` and note "partial answer" in the Answer column.

---

## `PRD health check`

**Trigger examples:**
- `PRD health check`
- `how many blockers do we have?`
- `what stories are ready to groom?`

**Read-only audit. No edits. Report:**

1. **Open [ARCH] blockers** — count and list all OQs with `[ARCH]` and Status = Open. Group by section.
2. **Stories blocked vs ready** — scan TDR master backlog:
   - `Draft` with non-empty Blocked by → blocked; list the OQ IDs blocking each
   - `Draft` with empty Blocked by → eligible for `Grooming Ready`
3. **FR coverage gaps** — any FRs in PRD-FR that have no TDR story mapped to them.
4. **OQs without owner** — any open-questions.md rows where Owner is blank.
5. **Stale dates** — check `**Last updated:**` in PRD-FR and TDR; flag if more than 7 days old.

Output as a brief table or bullet list. Highlight anything that is a blocker to Q1 grooming.

---

## `sync docs`

**Trigger examples:**
- `sync docs`
- `are all documents up to date?`
- `what's out of sync?`

**Read all four local files and compare:**
1. OQs resolved in `open-questions.md` but not reflected in PRD-FR §7 → flag.
2. OQ IDs in TDR Blocked by that are Resolved in open-questions.md → flag (should be removed).
3. Stories in TDR with empty Blocked by but Status = Draft → flag as eligible for Grooming Ready.
4. `**Last updated:**` dates in PRD-FR and TDR vs today → flag if stale.
5. Notion sync: check if Notion PRD page content matches local file for key sections (§2 RACI, §7 OQs).

Report drift found. Propose fixes. Wait for user confirmation before applying.

---

## `push PRD` / `push TDR` / `push all`

**Trigger examples:**
- `push PRD`
- `push TDR`
- `push all`

**Steps:**
1. Identify which sections changed since last push (compare local file to what was last fetched from Notion).
2. Show a **diff summary** — bullet list of changed sections (never push without showing this first).
3. Wait for user approval.
4. Use `notion-update-page` with `command: update_content` and targeted `old_str` / `new_str` pairs.
   - Always `notion-fetch` the page first to get exact current strings.
   - Use targeted section replacements, not `replace_content` (avoids accidentally deleting child pages/databases).
5. Confirm which Notion page(s) and sections were updated.

**Push targets:**
- `push PRD` → page ID `3259532a1f8680b08cc4ebb72fe7b535`
- `push TDR` → page ID `3259532a1f8680e0946ec9fbb1e85d2f`
- Leadership update → post to project page `3179532a1f8680daad25f1f0a0215679` (not PRD or TDR)

---

## `ingest document: [file or paste]`

**Trigger examples:**
- `ingest document: @/Users/.../DDD-Feature-Breakdown.pdf`
- `ingest document: [pasted content]`

**Steps:**
1. Read the document. If PDF with images only, ask user to export as PNG.
2. Map content to existing FRs: does it clarify, extend, or contradict a current requirement?
3. Surface new engineering teams, components, or open decisions not yet captured.
4. Propose: new OQ rows, updated FR bodies, new TDR stories or epic adjustments.
5. Flag conflicts with current content for user to resolve.
6. Show proposed diffs. Wait for approval.

---

## `scope change: [description]`

**Trigger examples:**
- `scope change: ATT Tech Express is no longer in scope`
- `scope change: EU vendors confirmed out of scope`

**Steps:**
1. Update PRD-FR §5 Dependencies and/or §9 Appendix (Out of scope confirmed).
2. Find all FRs, flow rows (§2a), and personas that reference the removed/changed scope.
3. Update or remove affected rows. Add a note with date and source.
4. Check TDR: are any stories scoped to the removed item? Mark them as cancelled or add a note.
5. Add a new OQ if the scope change creates ambiguity (e.g. "H15: EU vendors removed — confirm no LATAM integration dependency").
6. Show diff summary. Wait for approval.

---

## `draft leadership update: week of [date]`

**Steps:**
1. Read PRD-FR (goals, status, key milestones, risks).
2. Read TDR (stories in sprint vs blocked; epic status).
3. Read open-questions.md (count open [ARCH] blockers; any resolved this week).
4. Draft update using the structure in `project/ssot-sur/templates/weekly-leadership-update.md` (if present) or inline.
5. Post to **project page** `3179532a1f8680daad25f1f0a0215679` — not the PRD or TDR page.
6. Append as a new dated section: `## Project Latest Update — Week of [date]`.

**Content rules:** Include meetings held, decisions made, risks with mitigants. Exclude story counts, Notion tooling changes, internal PM process tasks. Tables and bullets only; no prose paragraphs.
