# Proposed Product management rules

These rules are defined in `.cursor/rules/` so the agent applies them when you work on Product artifacts. You can edit the `.mdc` files to change behavior.

---

## 1. Project building blocks (`project-building-blocks.mdc`)

**What it does:** Tells the agent to use PROJECT-CONTEXT (project name, docs, meeting notes, open questions), templates (Brief, PRD, open-questions), and SDLC phase skills. Use Notion/Jira/DevOps when the user asks to create or track work or read docs.

**You define:** Nothing required; fill in PROJECT-CONTEXT.md per project. Optionally add project-specific paths or conventions in the rule if your team standardizes them.

---

## 2. Meeting notes and open questions (`meeting-notes-and-open-questions.mdc`)

**What it does:** Meeting notes can be a **Notion database** (or database view link) in PROJECT-CONTEXT. The agent uses the **Notion MCP** to read that database and **source meeting scripting** to update the PRD during discovery so you don’t have to do it manually. When you ask to update a PRD or requirements, the agent fetches from that database (or page/path), extracts decisions and requirements, and proposes concrete PRD/Brief edits. When you give an answer to an open question, the agent updates the open-questions list and the relevant requirement.

**You define:** Ensure PROJECT-CONTEXT has “Meeting notes” and “Open questions” paths. Optionally add how your team formats meeting notes (e.g. “Decisions” section at top) in the rule.

---

## 3. Product management (`product-management.mdc`)

**What it does:**
- **Artifact types:** Brief = exec-level; PRD = implementation-ready. Use the right template; don’t mix them.
- **Quality bar:** Problem, success criteria, scope/out-of-scope, open questions, dependencies. Cite sources; don’t assume.
- **Decisions and ownership:** Open questions and prioritization are owned by the PM; the agent captures answers and drafts, doesn’t decide. Call out decisions needed; cite sources; flag conflicts.

**You define:** If Asurion or your team has a stricter quality bar (e.g. required sections, approval workflow), add them to this rule. You can also add file patterns (e.g. `**/brief*.md`, `**/prd*.md`) if you want the rule to apply only when those files are open (set `alwaysApply: false` and add `globs`).

---

## Summary

| Rule | Purpose |
|------|--------|
| **project-building-blocks** | Use PROJECT-CONTEXT, templates, SDLC skills, and tools (Notion/Jira/DevOps). |
| **meeting-notes-and-open-questions** | Use meeting notes to update PRDs; capture answers to open questions and keep requirements in sync. |
| **product-management** | Brief vs PRD; quality bar for artifacts; PM owns decisions and sign-off; agent assists and cites. |

---

**To change a rule:** Edit the corresponding `.mdc` file in `.cursor/rules/`. Use `description` and `alwaysApply` (and optional `globs`) in the frontmatter; keep content concise and actionable.
