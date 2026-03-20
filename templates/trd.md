# TRD: [Feature / Initiative Name]

**Tech lead / architect:** _Name_
**Last updated:** _YYYY-MM-DD_
**Status:** _Draft | In review | Approved_
**Related PRD:** _(Link to PRD — business context, product requirements, and functional requirements are defined there)_
**Synced with PRD:** _YYYY-MM-DD_

> **Purpose:** This document defines the technical design and implementation approach for the initiative approved in the PRD. It does not restate business context; it implements and extends it.

---

## 1. Overview

_Short summary of the technical solution and how it supports the PRD. Reference PRD goals and FRs. Do not restate the full business problem._

---

## 2. Architecture

_High-level design, system boundaries, and major components. Must support PRD scope and FRs. Should not introduce business capabilities not in the PRD._

_Reference architecture diagrams from Confluence or ADRs here rather than embedding them inline (especially while architecture is being finalized)._

**External references:**
- _Confluence / ADR link_

---

## 3. System Interactions

_How systems, services, or modules exchange information and coordinate behavior. Reference PRD flows by ID where relevant. Focus on interaction patterns, ownership, and processing behavior._

| Flow ID | Flow name | Systems involved | Interaction pattern | Notes |
|---------|-----------|-----------------|---------------------|-------|
| _F-1_ | _(match PRD flow name)_ | _System A → System B_ | _Sync / async / event_ | |

---

## 4. Data Mapping

_How source data, configuration, or records map into target structures. Belongs only in the TRD. Must support the entities and behaviors defined in the PRD. If a mapping constraint impacts product behavior, that must also be reflected in the PRD._

| Source field | Source system | Target field | Target system | Transformation | Notes |
|--------------|--------------|--------------|--------------|----------------|-------|
| _FieldName_ | _System_ | _FieldName_ | _System_ | _Logic_ | |

---

## 5. APIs / Interfaces

_Technical contracts, endpoints, payloads, and integration touchpoints. Belongs only in the TRD. Align to system interactions and architecture. Reference FR IDs for traceability._

| API / Interface | FR | Direction | Endpoint / contract | Auth / security | Notes |
|-----------------|----|-----------|---------------------|-----------------|-------|
| _Name_ | _FR-1_ | _In / Out_ | _Endpoint or schema ref_ | _Mechanism_ | |

---

## 6. Migration Mechanics

_Technical method for moving data, configuration, process ownership, or traffic from source to target. Includes waves, sequencing, backfill logic, coexistence patterns, and migration handling. If migration mechanics create user-visible constraints, those must be reflected in the PRD scope or flows._

---

## 7. Cutover Approach

_Phases, rollback logic, readiness checks, and transition handling. The PRD should mention cutover only at a high level; detailed transition mechanics live here._

| Phase | Scope | Readiness gate | Rollback | Owner |
|-------|-------|---------------|---------|-------|
| _Phase 1_ | _What is cut over_ | _Gate criteria_ | _How to reverse_ | _Owner_ |

---

## 8. Technical Validation

_How implementation will be tested and validated. Must support the functional expectations defined in the PRD._

| Test type | FR / NFR covered | Method | Owner | Notes |
|-----------|-----------------|--------|-------|-------|
| _Integration / E2E / Load_ | _FR-1_ | _Test plan ref_ | _Team_ | |

---

## 9. Operational Support Model

_Post-launch support structure, monitoring ownership, escalation paths, and sustainment. If support constraints affect product experience, note them in the PRD as a dependency._

| Area | Approach | Owner | Tooling | Notes |
|------|----------|-------|---------|-------|
| _Monitoring_ | _What is monitored_ | _Team_ | _Tool_ | |
| _Escalation_ | _Path_ | _Owner_ | | |

---

## 10. Engineering Backlog

> Stories must not move to **Grooming Ready** while any open question in their `Blocked by` column has Status = Open.

### Master Backlog

| Type | ID | Summary | FR | Quarter | Priority | Status | ADO ID | Blocked by |
|------|----|---------|----|---------|----|--------|--------|-----------|
| **Epic** | EP-1 | _Epic name_ | _FR IDs_ | _Q1_ | — | Discovery | _(pending)_ | _OQ IDs_ |
| Story | EP1-S1 | _Story summary_ | _FR-1_ | _Q1_ | P0 | Draft | _(pending)_ | _OQ IDs_ |

**Story status lifecycle:** `Draft` → `Grooming Ready` → `In ADO` → `In Sprint` → `Done`

### Epic header format

Each epic section opens with a metadata table:

| Field | Value |
|-------|-------|
| **Goal** | _One sentence — what this epic delivers_ |
| **Linked FRs** | _FR-1, FR-2_ |
| **ADO Feature(s)** | _(pending)_ |
| **Quarter** | _Q1_ |
| **Status** | _Discovery_ |
| **Architecture blockers** | _OQ IDs — stories `[BLOCKED]` until resolved_ |

### Story details

#### EP1-S1 — [Story name]

**As a** [persona]
**I want** [capability]
**So that** [business outcome]

**Acceptance criteria:**
1. _Criterion_

**Blocked by:** _OQ IDs_ | **ADO Story ID:** _(pending)_

---

## 11. Open Questions (Technical)

_Technical design questions only. Product/business questions belong in the PRD. If a decision affects both documents, reference it in both but assign a single owning document._

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| _T1 [ARCH]_ | _Technical design question_ | _Architect_ | Open | |

---

## 12. FR Coverage Audit

_Map each PRD FR to the implementation path in this TRD. Identifies gaps. Update when stories are groomed or architecture changes._

| FR | Description (brief) | Epic(s) | Story / stories | Coverage status | Gap |
|----|---------------------|---------|----------------|----------------|-----|
| _FR-1_ | _Short label_ | _EP-1_ | _EP1-S1_ | _Covered_ | |
| _FR-2_ | | | | _Partial_ | _What is missing_ |
