# Templates (Brief, PRD, open questions)

Use these with Cursor so the agent has a consistent structure for Briefs, PRDs, and capturing answers to open questions.

| File | Use |
|------|-----|
| **product-brief.md** | Exec-level Product Brief. Reference in PROJECT-CONTEXT as "Template to use" or when creating a new brief. |
| **prd.md** | Implementation-ready PRD. Reference in PROJECT-CONTEXT; use with meeting notes to keep requirements updated. |
| **open-questions.md** | Track open questions and capture answers. Set its path in PROJECT-CONTEXT under "Open questions." |

## Meeting notes and open questions

- **PROJECT-CONTEXT.md:** Set **Meeting notes** (path or Notion link) and **Open questions** (path or Notion link).
- **Meeting notes → PRD/Brief:** Ask e.g. "Use the kickoff meeting notes to update the PRD." Cursor will extract decisions and propose edits.
- **Capture answers:** Say e.g. "Capture the answer: [question] was resolved by [answer]." Cursor will update the open-questions list and the relevant requirement in the Brief/PRD.

You can copy these files into a project folder or point PROJECT-CONTEXT to Notion templates instead.
