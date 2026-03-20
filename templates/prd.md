# PRD: [Feature / Initiative Name]

**Product owner:** _Name_
**Last updated:** _YYYY-MM-DD_
**Status:** _Draft | In review | Approved_
**Related brief:** _(Link to Product Brief)_
**Related TRD:** _(Link to TRD — technical design and implementation details are documented there)_
**Synced with TRD:** _YYYY-MM-DD_

> **Purpose:** This document defines the business context, product requirements, functional requirements, and user/process flows for the initiative. For technical design, architecture, and implementation details, see the TRD.

---

## 1. Overview

_Brief summary of the initiative: what is being built or changed, and why it matters. Keep business-oriented; do not include technical design._

**Success metrics (summary):** _Link to §10 or list 1–3 key metrics here._

---

## 2. Stakeholders & RACI

> **RACI key:** R = Responsible · A = Accountable · C = Consulted · I = Informed

| Name | Role / Team | Area of ownership | RACI |
|------|-------------|-------------------|------|
| _Name_ | _Role_ | _What they own_ | A |
| _Name_ | _Role_ | _What they own_ | R |
| _Name_ | _Role_ | _What they own_ | C |

---

## 3. Business Problem

_Clear description of the current business, user, or operational problem being solved. Focus on pain points, inefficiencies, business risk, or user friction. Do not describe system architecture here._

---

## 4. Goals

_The intended business and product outcomes. Must be measurable or testable. TRD implementation choices must support these goals._

| # | Goal | How it is measured |
|---|------|--------------------|
| G-1 | _Goal_ | _Metric / test_ |
| G-2 | | |

---

## 5. Scope

**In scope:**
- _Key capability or deliverable_

**Out of scope (confirmed):**
- _Explicit exclusion_

---

## 6. Dependencies

_External systems, teams, decisions, or timelines this initiative depends on._

| Dependency | Owner | Notes |
|------------|-------|-------|
| _System / team_ | _Owner_ | _What blocks us or what we depend on_ |

---

## 7. Product Requirements

> Each PR is a required business capability. It groups one or more functional requirements. Trace each PR → FR(s) → TRD implementation.

### [Theme Name] · [Epic ID]

_One sentence: what this capability delivers and why it matters._

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-1 | **[Name]** | As a **[persona]**, I need [this] so that [outcome]. | _Detailed behavior description. Avoid API/schema detail._ | _OQ IDs_ | _TRD Epic/Story IDs_ |
| FR-2 | | | | | |

_Repeat `### Theme · Epic` block per product capability._

---

## 8. Non-Functional Requirements

_Performance, scalability, availability, security, compliance, rollback expectations. These are testable product constraints._

| # | Requirement | Notes | Open Qs |
|---|-------------|-------|---------|
| NFR-1 | _e.g. API response time ≤ SB local-lookup baseline_ | _Context_ | |
| NFR-2 | | | |

---

## 9. User / Process Flows

> Focus on flow logic, user actions, triggers, and business outcomes. Keep technical internals light — system-level realization belongs in the TRD. Flow IDs and names must match the TRD where both docs reference them.

_Group flows by category (e.g. Runtime, Integration, Inventory Lifecycle, Configuration)._

### [Category Name]

| Flow | ID | Current state | Future state | Gap / pain point | Open Qs |
|------|----|---------------|--------------|------------------|---------|
| _Flow name_ | _ID_ | _What happens today_ | _What happens in future state_ | _What's broken today_ | _OQ IDs_ |

---

## 10. Success Metrics & Acceptance Criteria

_Tie back to Goals §4. May include adoption, quality, efficiency, accuracy, or deprecation milestones._

| Release / Quarter | Goals covered | Acceptance criteria |
|-------------------|---------------|---------------------|
| _Q1_ | _G-1, G-2_ | _Definition of done for this release_ |
| _Q2_ | | |

---

## 11. Roadmap

> Business-level sequencing: why this order, what each phase unblocks. Implementation details belong in the TRD.

| Quarter | Milestone | Why this order | FRs | Key dependencies | Target outcome |
|---------|-----------|----------------|-----|-----------------|----------------|
| _Q1_ | _Milestone_ | _Rationale_ | _FR IDs_ | _Blockers_ | _Measurable outcome_ |

---

## 12. Open Questions

Full detail in **`docs/open-questions.md`** (if exists). Items tagged `[ARCH]` are TRD-owned; untagged items are PRD-owned. Must resolve before grooming.

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| _A1 [ARCH]_ | _Technical architecture question_ | _TRD owner_ | Open | |
| _B1_ | _Product/business question_ | _PRD owner_ | Open | |

---

## 13. Appendix _(optional)_

_References, architecture links (Confluence, ADRs), meeting notes links, personas link._

---

_When answers to open questions are captured: update Status → Resolved, fill Answer, update the relevant FR or flow, and sync with the TRD. Use `docs/open-questions.md` and PROJECT-CONTEXT.md to keep Cursor updated._
