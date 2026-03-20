---
name: review
description: >-
  Guide review of Product Briefs, PRDs, designs, or deliverables. Use when the user
  wants to review a document, get feedback, or prepare for stakeholder sign-off.
---

# Review (SDLC phase)

Use this skill when the user wants to **review a Product Brief**, **PRD**, design, or other deliverable before handoff or sign-off.

## When to use

- "Review this brief/PRD", "get feedback on", "stakeholder review", "ready for sign-off", "design review".

## Workflow

1. **Identify what’s being reviewed:** Brief, PRD, design doc, acceptance criteria, or other artifact.
2. **Gather the artifact:** User pastes content, shares a Notion link (use Notion MCP to read), or points to a file.
3. **Check against phase goals:**
   - **Brief:** Clear problem, solution summary, success criteria, scope/out-of-scope.
   - **PRD (what and why):** §1–4 business context and goals; §5 scope (in + out); §6 dependencies; §7 FRs grouped by theme with persona anchors; §8 NFRs; §9 user/process flows; §10 success metrics; §12 open questions with owners. Confirm no architecture or implementation detail is present — that belongs in the TRD.
   - **TRD (how):** §2 architecture aligned to PRD scope; §3 system interactions reference PRD flow IDs; §10 backlog stories trace to FRs; §12 FR coverage audit shows no gaps. Confirm no business requirements are redefined here — reference the PRD instead.
   - **PRD ↔ TRD sync:** Shared terms are identical; every PRD flow has a TRD counterpart; every open question has a single owning doc; cross-reference headers are present in both.
   - **Design:** Alignment with requirements and accessibility/standards if relevant.
4. **Suggest improvements:** Gaps, unclear sections, missing stakeholders or criteria.
5. **Suggest next step:** Mark "ready for handoff" or "needs one more iteration" and point to **handoff** or back to **discover-define** as needed.

## Integration

- Use **Notion MCP** to read the live doc when the user shares a link.
- Use **reference** skill if org standards or templates should be applied during review.
