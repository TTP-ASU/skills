# TRD: Technical Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Tech lead / architect:** Ankit / Tim Clemens (Enterprise Architecture)  
**Last updated:** 2026-03-26 (**Strategy Discussion 2026-03-26**: RT-6 D4 [ARCH] cleared — separate calls confirmed; Distro Migration co-dependency noted; L1/L2 new OQs · **03/25 HLE discussion** — dev sizing added to US-2.1, US-2.4, US-5.1; multi-part reservation AC + cancellation latency added; flip-and-fold BAT edge case; 03/24-03/25 meeting notes captured)  
**Status:** Draft — evolves as architecture decisions are finalized  
**Related PRD:** [PRD — Functional Requirements SUR SSOT](https://www.notion.so/3259532a1f8680b08cc4ebb72fe7b535)  
**Notion TRD page:** https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f  
**Synced with PRD:** 2026-03-26  
**Azure DevOps:** Epic [676287](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676287) · org: `axasurion` · project: `AX7 Core` · connected via Cursor MCP

> **Purpose:** This document defines the technical design and implementation approach for the initiative approved in the PRD. Business context, product requirements, functional requirements, and user/process flows are defined in the PRD. This document implements and extends them.
>
> **Status note:** Sections §2–§9 (architecture, system interactions, data mapping, APIs, migration, cutover, validation, support) are being defined through active working sessions (architecture review targeted week of 2026-03-24). They will be filled in as [ARCH] blockers resolve. Stories with Status = `Draft` and a non-empty `Blocked by` column cannot be groomed until the referenced [ARCH] question is resolved. See `open-questions.md` for owner and status. Lifecycle: `Draft` → `Grooming Ready` → `In ADO` → `In Sprint` → `Done`

---

## 1. Overview

This TRD implements the SUR SSOT initiative approved in the PRD. The technical solution replaces ServiceBench's replication-based inventory model with real-time DAX orchestration via EIAA, migrates 3rd party NAOP/AOP inventory to DAX IVS / D365, and delivers a single availability + reservation API on the DES/ISP pattern.

Key implementation components:
- **EIAA (Early Inventory Availability API)** — central real-time orchestration (DAPI Team)
- **Tyk API Connect** — NAOP vendor feed standardization (Integration Team)
- **DAX IVS / D365 F&O** — inventory lifecycle management for AOP (Avengers Team)
- **ServiceBench consumer changes** — real-time availability call, Job/Claim price model (BeyondX Team)
- **Native WMA app** — Phase 1 UI for AOP providers (Avengers Team)

PRD goals and functional requirements drive all implementation choices. See PRD §4 Goals and §7 FRs.

---

## 2. Architecture

> **Status:** Being finalized through architecture working sessions. EA review scheduled week of 2026-03-24. **[ARCH] remaining:** A2, I1 (near-resolution — combined design confirmed 2026-03-25; **I4** peril-change sub-question open), C1/C4/C5 (reservation — pending H8 scope confirm), I3 (substitution matrix), B1/B2 (TELUS — Q4), E1 (warehouse format — Q4), G2 (AOP identity — near-resolution), J1 (Product 360 overlap). Plus **A5** (job-type nomenclature — Raghu/Amir action item). **Resolved:** A1, A4, D1, D2, D3, D4, E2, G1, H6, H7, I2 (see open-questions.md). **New OQs (2026-03-26):** L1 (repair funnel broken), L2 (SUR volume decline) — operational risks, not [ARCH] blockers. **New OQ (2026-03-25):** B5 (NAOP feed frequency).

**External references (authoritative):**
- Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) — Flow 1 (AOP), 2A/2B (NAOP), 3/5 (UBIF), 4 (BOM Setup)
- [DDD Feature Breakdown](https://asurion.atlassian.net/wiki/spaces/DDD/pages/614007633/Feature+Breakdown) (Confluence space **DDD** — architecture / feature numbering reference for SSOT)
- SUR SSOT Inventory Availability Orchestration diagrams (Confluence — add link when published beside Feature Breakdown)

_This section will expand with high-level component diagram, system boundaries, and major integration patterns once architecture working sessions complete._

---

## 3. System Interactions

> **Status:** Pending architecture decisions. Flow IDs below correspond to PRD §9 flows. This section will expand with interaction patterns, sequence diagrams, and ownership per flow once [ARCH] blockers are resolved.

| Flow ID | Flow name | Systems involved | Key open question |
|---------|-----------|-----------------|-------------------|
| RT-1 | UBIF Next Gen availability | SB → EIAA → DAX Americas Availability Service | E2 resolved (LOB); A5 — exclusion dimensions in API |
| RT-2 | UBIF Legacy availability | SB → EIAA → UBIF Current State | C6 [ARCH] — reservable vs not-reservable |
| RT-3 | NAOP availability (Canada / Mexico) | SB → EIAA → Tyk API Connect → vendor | B1 [ARCH] — Plan A vs B; B2 [ARCH] — bypass flag location |
| RT-4 | BOM lookup at job creation | SB → EIAA or separate BOM API | I1 [ARCH] — embed in EIAA vs separate BOM service |
| RT-5 | Soft reservation at lead placement | SB → IVS → store confirmation | C1 [ARCH] — lifecycle ownership; C4 [ARCH] — expiration; C5 [ARCH] — double-deduction |
| RT-6 | JIT availability + order | SB → EIAA (JIT flag) → order creation | A4 resolved (SKU); A5 — API dimensions; **D3 resolved**; **D4 resolved** — separate calls confirmed 2026-03-26 |
| IL-1–IL-8 | AOP inventory lifecycle | WMA → D365 / DAX | G1 [ARCH] — UI path; G2 [ARCH] — identity |

---

## 4. Data Mapping

> **Status:** Pending. ServiceBench field documentation required before mapping can be completed (OQ F1 — Raghu / SCM). MDM setup automation design pending (OQ F2). This section will be filled in during architecture working sessions.

Key entities requiring mapping:
- Part / SKU (ServiceBench → D365 F&O)
- BOM (ServiceBench local → DAX; add OEM SKUs per part line)
- Warehouse / location identifiers (format standardization — OQ E1)
- Distro "quantity one" records (OQ D5)
- Substitution matrix (Tomlin → DAX F&O — OQ I3 [ARCH])

---

## 5. APIs / Interfaces

> **Status:** Pending EA sign-off and architecture decisions. API contracts will be defined post-[ARCH] resolution.

| API / Interface | FR | Direction | Notes |
|-----------------|----|-----------|-------|
| EIAA availability endpoint | FR-1, FR-8 | SB → DAX | Single endpoint per part line; returns availability flag, JIT flag, shipping days out, bypass flag, Asurion + OEM SKUs; **excluded job types** for job-type eligibility (DAX data; SB adjudicates — Job Type / Eligibility 2026-03-23). Aligned to DES/ISP pattern. |
| EIAA / IVS reservation endpoint | FR-1 | SB → IVS | Creates and returns Reservation ID. **D4 resolved** — separate writable API (03/26). |
| Tyk API Connect — NAOP feed | FR-4 | Vendor → DAX | AWS/JSON; standard contract for all NAOP vendors. |
| Job/Claim price API | FR-3 | UBIF → SB | Transactional price at Job/Claim creation. |
| IVS soft reservation API | FR-10 | SB → IVS | Creates soft reservation at lead placement. Expiration and reconciliation design TBD. |
| WMA — D365 integration | FR-5 | WMA ↔ D365 | Native WMA app for AOP providers; accessible via Prism link. |

---

## 6. Migration Mechanics

> **Status:** Phased rollout approach defined in PRD §11 Roadmap. Technical migration sequencing and backfill logic to be designed once [ARCH] blockers resolve.

High-level phases (from PRD §11):
1. UBIF Next Gen + NAOP feeds (RT-1, INT-4)
2. 3rd party NAOP (Canada / Mexico) — RTI → Tyk repoint (INT-1, INT-2)
3. 3rd party AOP — full D365 lifecycle migration (IL-1–IL-8)

**Rollback:** 30-day rollback for non-AOP cohorts via per-location feature flags (EP4-S1). AOP rollback approach TBD.

_Migration wave details, coexistence patterns, and backfill logic will be added here as architecture working sessions progress._

---

## 7. Cutover Approach

> **Status:** Pending. Readiness checks, traffic cutover logic, and rollback procedures to be defined once migration mechanics are finalized.

_This section will cover: phased traffic cutover per location/provider, rollback decision gates, ServiceBench legacy deprecation timeline per feed, and final retirement of replication feeds._

---

## 8. Technical Validation

> **Status:** Acceptance criteria stubs are in §10 story detail blocks. Full test plan to be developed during grooming.

| Test type | FR / NFR covered | Method | Owner |
|-----------|-----------------|--------|-------|
| Integration | FR-1, FR-2, FR-6 | End-to-end availability call: SB → EIAA → DAX; validate response time vs SB local-lookup baseline | DAPI / BeyondX |
| Load / scalability | NFR-2 | IVS soft reservation at ~800 UBIF locations; no overcommit | DAPI |
| Double-deduction prevention | NFR-3 | Soft + hard reservation state reconciliation | DAPI |
| Rollback | NFR-4 | Feature flag toggle per location; 30-day rollback validated | BeyondX / Avengers |
| Identity | FR-5 | Hydra / WMA access for all 9 AOP providers | Avengers / Sandeep |

---

## 9. Operational Support Model

> **Status:** To be defined. Support handoff and monitoring design will follow architecture finalization.

_This section will cover: post-launch monitoring ownership (DAPI, BeyondX, Avengers), alerting approach for EIAA orchestration failures, escalation paths for NAOP feed issues, and AOP D365 support model._

---

## 10. Engineering Backlog

> Stories must not move to **Grooming Ready** while any open question in their `Blocked by` column has Status = Open in `open-questions.md`.

### Master backlog

> **Sourced from ADO 2026-03-25.** Single database table — filter or sort by any column in Notion. `ADO State` is the live source of truth. ⚠️ ADO rows exist in ADO but are not yet mapped to a PRD US-ID. `—` in ADO Link = work item not yet created.
>
> **Status key:** `Draft` · `Grooming Ready` · `ADO: New` · `ADO: Committed` 🔵 · `ADO: Done` ✅ · `Discovery`
> **Work Type:** `Dev` = engineering sprint capacity · `BUS` = business / scope decision — no dev sprint needed · `—` = feature row (not a deliverable)

| Type | ID | Summary | FR | Quarter | Priority | Team | Work Type | PRD Status | ADO State | ADO Link |
|------|----|---------|----|---------|----|------|-----------|------------|-----------|----------|
| **Feature** | **F-1** | **Part price on Job/Claim** | FR-3 | Q1 | — | BeyondX | — | **Mostly Complete** | In Progress | _(pending)_ |
| Story | US-1.1 | Part price on Job/Claim — S2 UBIF providers | FR-3 | Q1 | P0 | BeyondX | Dev | **Done** | Done ✅ | _(pending)_ |
| Story | US-1.2 | Part price on Job/Claim — S1 providers | FR-3 | Q1 | P0 | BeyondX | Dev | Active | Active | _(pending)_ |
| **Feature** | **F-2a** | **UBIF inventory availability lookup NextGen** | FR-1, FR-2, FR-6 | Q2 | — | Avengers | — | Discovery | **In Progress** | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) |
| ⚠️ ADO | — | UBIF Enable IVS for F&O Data | FR-1 | Q2 | P0 | Avengers | Dev | — | Done ✅ | [680113](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680113) |
| ⚠️ ADO | — | UBIF NG Part SKU → Asurion SKU Mapping — Design | FR-1 | Q2 | P0 | Avengers | Dev | — | Committed 🔵 | [680122](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680122) |
| Story | US-2.1 | SUR availability endpoint — read-only, new contract | FR-1, FR-8 | Q2 | P0 | Avengers | Dev | Draft | New | [677037](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677037) |
| Story | US-2.2 | Distro vendor indicator in availability response | FR-2 | Q2 | P0 | Avengers | Dev | **Grooming Ready** | — | _(create)_ |
| Story | US-2.3 | ISP vs SUR routing for shared UBIF store IDs | FR-6 | Q2 | P0 | Avengers + BeyondX | Dev | **Grooming Ready** | — | _(create)_ |
| Story | US-2.4 | Reservation API — separate writable API; prereq for F-4 | FR-1 | Q2 | P0 | Avengers | Dev | Draft | — | _(create)_ |
| **Feature** | **F-2b** | **JIT Transfer orders** | FR-8 | Q2 | — | Avengers | — | Discovery | **In Progress** | [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) |
| ⚠️ ADO | — | Design contract changes for Fulfillment orders with JIT parts | FR-8 | Q2 | P0 | Avengers | Dev | — | Committed 🔵 | [679505](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679505) |
| Story | US-2.5 | JIT job-type exclusion configuration in DAX | FR-8 | Q2 | P1 | Avengers | Dev | **Grooming Ready** | — | _(create)_ |
| Story | US-2.6 | JIT order creation and eligibility logic | FR-8 | Q2 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| ⚠️ ADO | — | JIT flag management — add/remove for 3rd Party AOP providers | FR-5 | Q2 ⚠️ | P1 | Avengers | Dev | — | New | [680934](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680934) |
| ⚠️ ADO | — | JIT flag indicator for SKUs orderable via TLC for 3rd Party AOP | FR-5 | Q2 ⚠️ | P1 | Avengers | Dev | — | New | [681066](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681066) |
| **Feature** | **F-3a** | **BeyondX – SUR SSOT Configurations and Mappings** | FR-9 | Q2 | — | BeyondX | — | Discovery | New ⚠️ | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) |
| ⚠️ ADO | — | New config: Peril → Equipment Type Mapping | FR-9 | Q2 | P1 | BeyondX | BUS | — | New | [679882](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679882) |
| ⚠️ ADO | — | Validate Peril → Equipment Type Mapping config | FR-9 | Q2 | P1 | BeyondX | Dev | — | New | [679886](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679886) |
| Story | US-3.1 | Single-touch BOM setup in DAX (Asurion + OEM SKUs) | FR-9, FR-11 | Q2 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-3.3 | OEM equipment type confirmed for pricing/charging | FR-9 | Q2 | P1 | Avengers | BUS | Draft | — | _(create)_ |
| **Feature** | **F-3b** | **Avengers – Part Substitution Matrix** | FR-9 | Q2 | — | Avengers | — | Discovery | New | [681046](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681046) |
| ⚠️ ADO | — | Part Substitution Matrix — Research & Design | FR-9 | Q2 | P0 | Avengers | Dev | — | New | [681047](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681047) |
| Story | US-3.2 | Part substitution rules owned in DAX/MDM | FR-9 | Q2 | P2 | Avengers | Dev | Draft | New | [681046](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681046) |
| ⚠️ ADO | — | Availability API Logic — Part Sub Matrix Sprint 271 | FR-9 | Q2 | P1 | Avengers | Dev | — | New | [681155](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681155) |
| ⚠️ ADO | — | Availability API Logic — Part Sub Matrix Sprint 272 | FR-9 | Q2 | P1 | Avengers | Dev | — | New | [681160](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681160) |
| ⚠️ ADO | — | Part Sub Matrix config in SB1 / UAT / Testing | FR-9 | Q2 | P1 | Avengers | Dev | — | New | [681166](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681166) |
| **Feature** | **F-4** | **Soft reservations at booking time via IVS** | FR-10 | Q2 | — | Avengers | — | Discovery | — | _(pending H8)_ |
| Story | US-4.1 | Soft reservation created at lead placement | FR-10 | Q2 | P0 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-4.2 | Soft reservation reconciled with final store reservation | FR-10 | Q2 | P0 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-4.3 | Soft reservation expiration model | FR-10 | Q2 | P0 | Avengers | Dev | Draft | — | _(create)_ |
| **Feature** | **F-7** | **Phased rollout + rollback framework** | FR-7 | Q2 | — | BeyondX | — | Discovery | — | _(create)_ |
| Story | US-7.1 | Feature flag per location/provider for DAX API rollout | FR-7 | Q2 | P0 | BeyondX | Dev | Draft | — | _(create)_ |
| Story | US-7.2 | On-demand ordering scope confirmed for 3rd party providers | FR-7 | Q2 | P1 | BeyondX | BUS | Draft | — | _(create)_ |
| ⚠️ ADO | — | On Demand Ordering Configuration _(7 WMA stories)_ | FR-5 | Q2 ⚠️ | — | BeyondX | Dev | — | New | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) |
| **Feature** | **F-5** | **3rd Party AOP Migration — inventory lifecycle in D365** | FR-5, FR-12 | Q3 | — | Avengers | — | Discovery | New | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) |
| Story | US-5.1 | Full inventory lifecycle in D365 for AOP providers | FR-5 | Q3 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-5.2 | AOP inventory management via native WMA app | FR-5 | Q3 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-5.3 | AOP provider identity and access via Azure AD / Prism | FR-5 | Q3 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-5.4 | Automated SKU/MDM setup in DAX for AOP | FR-11 | Q3 | P1 | Avengers | Dev | Draft | — | _(create)_ |
| Story | US-1.3 | 3rd party price on Job/Claim _(scope TBD — moved from F-1)_ | FR-12 | Q3 | TBD | BeyondX | BUS | Draft | — | _(pending H1)_ |
| ⚠️ ADO | — | WMA On Demand Ordering — Configure availability check mode | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681260](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681260) |
| ⚠️ ADO | — | WMA On Demand Ordering — Menu entry point and navigation | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681261](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681261) |
| ⚠️ ADO | — | WMA On Demand Ordering — Shopping cart pattern | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681262](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681262) |
| ⚠️ ADO | — | WMA On Demand Ordering — Configurable availability check | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681263](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681263) |
| ⚠️ ADO | — | WMA On Demand Ordering — Write cart to staging tables | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681265](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681265) |
| ⚠️ ADO | — | WMA On Demand Ordering — Batch processing for transfer orders | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681266](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681266) |
| ⚠️ ADO | — | WMA On Demand Ordering — Mobile inquiry for order status | FR-5 | Q3 | P1 | BeyondX | Dev | — | New | [681267](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681267) |
| **Feature** | **F-6** | **NAOP migration — Mobile Clinic + Mexico** | FR-4 | Q4 | — | Integration | — | Discovery | New | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) |
| Story | US-6.1 | TELUS / Mobile Clinic feed migration to DAX IVS API | FR-4 | Q4 | P1 | Integration | Dev | Draft | — | _(create)_ |
| Story | US-6.2 | Full inventory for all repair types — Plan A (preferred) | FR-4 | Q4 | P1 | Integration | Dev | Draft | — | _(create)_ |
| Story | US-6.3 | LCM-only feed with bypass flag — Plan B (fallback) | FR-4 | Q4 | P1 | Integration | Dev | Draft | — | _(create)_ |
| Story | US-6.4 | ATT Mexico / Telcel feed migration to DAX IVS API | FR-4 | Q4 | P1 | Integration | Dev | Draft | — | _(create)_ |
| Feature | EP-5 | UBIF Legacy availability lookup _(deferred)_ | FR-2 | Q3+ | — | Avengers | Dev | Discovery | New (on hold) | [677454](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677454) |

> **ADO sourced:** 2026-03-25. ⚠️ Quarter marked `Q2 ⚠️` = filed in ADO under a Q2 feature but scope likely belongs in Q3 — confirm in grooming. `_(create)_` = ADO work item does not exist yet; create before sprint planning. See story details below for grooming callouts per feature.
---

### Story details

> Full user story and acceptance criteria per story. AC stubs — expand during architecture working sessions and grooming.

---

### F-1: Part Price on Job/Claim

| Field | Value |
|-------|-------|
| **Goal** | Set partner invoice price transactionally on the ServiceBench Job/Claim, deprecating the UBIF price replication feed. **UBIF scope only** — 3rd party price moved to F-5 / FR-12. S2 providers already live. |

| **Ref ID** | F-1 |
| **Linked FRs** | FR-3 |
| **ADO Feature(s)** | _(pending — confirm ADO ID; H7 resolved for S2)_ |
| **Quarter** | Q1 — **Mostly Complete** |
| **Status** | Mostly Complete (S2 Done · S1 Active) |
| **Architecture blockers** | None |

#### Grooming callouts

> - US-1.1 ✅ Done and live. ADO link pending — action: retrieve and fill.
> - US-1.2 Active — Apexia S1 confirmation outstanding. Confirm status before closing F-1.
> - US-1.3 **moved to F-5** — 3rd party price on Job/Claim now under AOP Migration (FR-12); see F-5 story details.

#### US-1.1 — Transactional Part Pricing — S2 UBIF Providers

> **Ref ID:** US-1.1 | **Legacy ID:** EP0-S1

**As a** claims / finance user
**I want** part price set on the ServiceBench Job at the time of transaction (UBIF Current State)
**So that** Franchise Co. reconciliation uses the transactional price, not a replicated master

**Acceptance criteria:**
1. Price is written to Job/Claim at transaction time. ✅
2. Matches UBIF invoice price. ✅
3. UBIF price replication feed deprecated for migrated stores. ✅

**Status:** **Done** — confirmed live in production for 8+ months (03/26 meeting). | **ADO Story ID:** _(pending — fill from ADO)_

---

#### US-1.2 — Transactional Part Pricing — S1 Providers (Apexia)

> **Ref ID:** US-1.2 | **Legacy ID:** EP0-S2

**As a** claims / finance user
**I want** part price on Job/Claim for S1 / Apexia stores
**So that** the same reconciliation fix applies to all UBIF stores

**Acceptance criteria:**
1. Part price set transactionally on Job/Claim for S1 stores.
2. No dependency on UBIF price replication.

**Status:** Active — awaiting Apexia confirmation (03/26). | **Blocked by:** — | **ADO Story ID:** _(pending)_

---

### F-2: SUR Real-Time Availability API and UBIF Next Gen Orchestration

| Field | Value |
|-------|-------|
| **Goal** | Replace UBIF→ServiceBench replication with a real-time read-only availability API and a separate writable reservation API. Includes JIT flag, job-type exclusion config, and order creation logic. New contract built from scratch (03/26). |

| **Ref ID** | F-2 |
| **Linked FRs** | FR-1, FR-2, FR-6, FR-8 |
| **ADO Feature(s)** | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) · [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) |
| **Quarter** | Q2 |
| **Status** | Discovery |
| **Architecture blockers** | A2 [ARCH], I1 (near-resolution — combined API confirmed 2026-03-25; I4 peril-change sub-question open)

#### Grooming callouts

> **F-2a — UBIF NextGen availability:**
> - [680113](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680113) Done ✅ "UBIF Enable IVS for F&O Data" — confirm with Matt Bertrand whether this resolves OQ K3 (UBIF IVS not enabled)
> - [680122](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680122) Committed 🔵 "UBIF NG Part SKU → Asurion SKU Mapping Design" — in sprint; contract output feeds US-2.1 AC
> - US-2.1 ([677037](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677037)): In ADO as New, **unassigned** — AC not finalized; blocked A2, I1. Do not groom until both resolved.
> - US-2.2 & US-2.3: **Grooming Ready** but no ADO stories created yet — action: create before sprint planning
> - US-2.4 (Reservation API): Draft, no ADO story — pull AC from 03/25 API contract session notes
>
> **F-2b — JIT Transfer orders:**
> - [679505](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679505) Committed 🔵 "Design contract changes for JIT parts TO" — Ashley Hickman in sprint; ensure US-2.6 AC aligns with output
> - US-2.5: **Grooming Ready** — no ADO story yet; action: create before sprint planning
> - US-2.6: Draft — gated on D5 (JIT record ownership) and 679505 design output
> - ⚠️ [680934](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680934) & [681066](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681066): JIT flag stories filed under F-2b in ADO but cover AOP scope (Q3 F-5) — confirm with team: move to F-5 or keep with Q3 target date? — **D1 resolved** (separate flags confirmed 2026-03-25); **D3 resolved**; **D4 resolved** (availability = read-only; reservation = separate writable API); **E2 closed** (ISP vs SUR by LOB); D5 (JIT record ownership — partial); internal DAX UBIF vs America's IVS routing = separate DAX PBI |

#### US-2.1 — SUR Part Availability API Endpoint (Read-Only)

> **Ref ID:** US-2.1 | **Legacy ID:** EP1-S1

**As a** ServiceBench consumer
**I want** a single DAX endpoint to check SUR part availability per part line
**So that** I get real-time data without replication lag

**Acceptance criteria:**
1. API returns availability flag, JIT flag, shipping days out, bypass flag, Asurion + OEM SKUs per part line.
2. Response includes `qty`, `allowJustInTime`, `leadTimeInDays`, `jobTypeExclusions`, `priority`, `productEquipmentType` per part per location (confirmed schema 2026-03-25).
3. Flip-and-fold edge case handled: returns multiple parts of the same `partType` (e.g., two BAT entries — primary + secondary) for applicable device SKUs.
4. Response time ≤ SB local-lookup baseline.
5. Existing UBIF replication feed is deprecated for migrated stores.

**HLE sizing (2026-03-25):** 2 sprints for the core API (includes BOM lookup, substitution matrix integration, availability checking). Does not include UI or Reservation API.

**Blocked by:** A2, I1 _(D1 resolved 2026-03-25)_ | **ADO Story ID:** _(pending)_

---

#### US-2.2 — Distro Availability Indicator in Single API Response

> **Ref ID:** US-2.2 | **Legacy ID:** EP1-S2

**As a** ServiceBench consumer
**I want** the Distro Vendor indicator returned in the same availability API response
**So that** I don't need a separate distro catalog feed

**Acceptance criteria:**
1. Distro Vendor flag included per part line in same response as availability.
2. Distro replication feed deprecated.

**Blocked by:** — _(D1 resolved 2026-03-25)_ | **Status: Grooming Ready** | **ADO Story ID:** _(pending)_

---

#### US-2.3 — ISP vs SUR Routing for Shared UBIF Store IDs

> **Ref ID:** US-2.3 | **Legacy ID:** EP1-S3

**As a** DAX / ServiceBench routing layer
**I want** logic to distinguish ISP vs SUR for stores that share the same ServiceBench ID
**So that** ISP availability calls don't mix with SUR availability calls

**Acceptance criteria:**
1. Routing correctly separates ISP and SUR calls for same UBIF store ID in all test cases (LOB: SUR repair vs replacement ISP — **WLI vs WCF** pattern per Tech Sync 2026-03-20).
2. Internal DAX work to isolate **UBIF IVS vs America's IVS** warehouse lookups is tracked as **DAX backlog / separate PBI** (not a ServiceBench integration blocker).

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### US-2.4 — Reservation API — Reservation ID on All Orders

> **Ref ID:** US-2.4 | **Legacy ID:** EP1-S4

> **03/26 decision:** Availability (read-only) and Reservation (writable) are **two separate APIs**. EP1-S4 implements the writable reservation endpoint. This is a prerequisite for F-4 (soft reservations).

**As a** store / portal user
**I want** a separate reservation API that writes a Reservation ID to UBIF and DAX orders
**So that** reservations are traceable end-to-end and soft reservations (F-4) can be implemented

**Acceptance criteria:**
1. Reservation API is a separate writable service from the read-only availability endpoint.
2. Reservation ID present in all UBIF and DAX order payloads.
3. ID can be used to look up reservation state.
4. **Multi-part requests supported:** single reservation call accepts multiple parts; returns an individual reservation ID per part (not a single ID for the whole job) — confirmed HLE 2026-03-25.
5. Reservation API returns success/failure indicator per part (not HTTP error for JIT items) — confirmed BOM/API workshop 2026-03-25.
6. Job reassignment does not trigger cancellation of the sales order — sales order remains as-is.
7. **Cancellation queue latency:** ~3 minutes for reservation to be released after cancellation via SNS message flow. Design for expiration handling must account for this delay.

**HLE sizing (2026-03-25):** 1–2 sprints (routing logic to correct IVS instances per location is the primary complexity).

**Blocked by:** — _(D4 resolved — separate APIs confirmed 03/26)_ | **ADO Story ID:** _(pending)_

---

#### US-2.5 — Job Type Restrictions Configuration in DAX

> **Ref ID:** US-2.5 | **Legacy ID:** EP1-S5

**As a** DAX / F&O configuration owner
**I want** job-type exclusions modeled at **SKU level** in D365
**So that** JIT-ineligible job types (e.g., non-OSR/CSS) are correctly excluded from JIT availability

**Acceptance criteria:**
1. Job-type exclusion stored as **SKU-level attribute** in DAX; MDM + **Robbie** security on existing DAX form (OQ **A4** resolved 2026-03-20).
2. Exclusions returned in availability/BOM response; **SB adjudicates** (OQ **D3** resolved 2026-03-20).
3. Exclusions apply to both parent and substitute SKUs.
4. ServiceBench SKU-level exclusion config deprecated for migrated stores.

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### US-2.6 — JIT Order Creation and Eligibility Logic

> **Ref ID:** US-2.6 | **Legacy ID:** EP1-S6

**As a** ServiceBench / orchestration consumer
**I want** JIT order creation behavior and eligibility logic defined and implemented
**So that** JIT orders are created correctly without incorrectly decrementing warehouse inventory

**Acceptance criteria:**
1. JIT eligibility driven by distro "quantity one" record; owner confirmed (D5).
2. No inventory decrement at warehouse for JIT orders.
3. Reservation + JIT order creation confirmed: single API call or separate calls (OQ D4 resolved).
4. JIT flag included at line level in sales order.

**Blocked by:** D5 _(D4 resolved — separate APIs 03/26)_ | **ADO Story ID:** _(pending)_

---

### F-3: BOM Automation and Substitution Matrix

| Field | Value |
|-------|-------|
| **Goal** | Automate repair asset and BOM setup in DAX; migrate substitution matrix ownership to MDM/Tomlin. Ships parallel to EP-1 in Q2. |

| **Ref ID** | F-3 |
| **Linked FRs** | FR-9, FR-11 |
| **ADO Feature(s)** | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) |
| **Quarter** | Q2 |
| **Status** | Discovery |
| **Architecture blockers** | A3, F1, F2, H4 |

#### Grooming callouts

> **F-3a — BeyondX Configurations:**
> - ⚠️ [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) target date **2026-03-30 has passed** — no progress. Immediate discussion needed with BeyondX.
> - [679882](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679882) BUS — tagged "For Biz confirmation." What decision is pending? Links to OQ A3. PM to confirm before dev starts.
> - [679886](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679886) Dev — dependent on 679882 BUS decision; do not sprint until A3 resolved.
> - US-3.1: Draft, no ADO story — gated on F1 (BOM catalog ownership decision)
> - US-3.3 BUS: OEM equipment type confirmation — who owns this decision? (OQ A3)
>
> **F-3b — Part Substitution Matrix:**
> - [681047](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681047) R&D story must complete before [681155](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681155)/[681160](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681160) sprint stories can begin
> - US-3.2: **Do not groom** until OQ I3 (substitution matrix scope/owner) is resolved — gates all implementation stories
> - 681155, 681160: Placeholder sprint stories — no AC yet; depend on 681047 R&D output + I3
> - 681166: Testing/validation — final step after above

#### US-3.1 — Single-Touch BOM Setup in DAX (Asurion and OEM Parts)

> **Ref ID:** US-3.1 | **Legacy ID:** EP1B-S1

**As a** MDM team
**I want** single-touch BOM setup in DAX (Asurion + OEM SKUs)
**So that** there are no manual steps to replicate to ServiceBench

**Acceptance criteria:**
1. BOM returns both Asurion and OEM SKUs for 3rd party providers.
2. Validated against Canada NAOP production job.
3. ServiceBench BOM setup deprecated.

**Blocked by:** F1 | **ADO Story ID:** _(pending)_

---

#### US-3.2 — Part Substitution Rules Owned in DAX

> **Ref ID:** US-3.2 | **Legacy ID:** EP1B-S2

**As a** MDM / Tomlin
**I want** the substitution matrix owned and maintained in DAX
**So that** substitution rules are in SSOT, not siloed in ServiceBench

**Acceptance criteria:**
1. Substitution matrix migrated to MDM/DAX.
2. Owner confirmed (H4).
3. Rose, Robbie Carter, Tomlin aligned.

**Blocked by:** H4, I3 | **ADO Story ID:** _(pending)_

---

#### US-3.3 — OEM Equipment Type for Pricing and Charging

> **Ref ID:** US-3.3 | **Legacy ID:** EP1B-S3

**As a** MDM team
**I want** OEM equipment type confirmed for pricing/charging logic
**So that** OEM SKUs are priced correctly in D365

**Acceptance criteria:**
1. OEM equipment type definition confirmed (A3).
2. Pricing/charging logic handles OEM correctly.

**Blocked by:** A3 | **ADO Story ID:** _(pending)_

---

### F-4: Soft Reservations at Booking Time

| Field | Value |
|-------|-------|
| **Goal** | Close the 1–5 min availability gap by implementing IVS soft reservations at lead placement. Depends on US-2.4 (Reservation API). |

| **Ref ID** | F-4 |
| **Linked FRs** | FR-10 |
| **ADO Feature(s)** | _(pending — confirm with Michelle Bowersox [H8])_ |
| **Quarter** | Q2 _(pending H8 scope confirmation)_ |
| **Status** | Discovery |
| **Architecture blockers** | C1, C4, C5 |

#### Grooming callouts

> ⚠️ **Entire feature on hold — do not discuss in this grooming session.**
> No ADO feature created. OQ H8 (soft reservations in scope?) must be answered by Bryant/Michelle first.
> Action: PM to schedule H8 decision with Bryant before next grooming session.

#### US-4.1 — Soft Reservation Created at Lead Placement

> **Ref ID:** US-4.1 | **Legacy ID:** EP1C-S1

**As a** ServiceBench (booking)
**I want** IVS to create a soft reservation when a lead is placed
**So that** available inventory decrements immediately, preventing overcommitment during the booking window

**Acceptance criteria:**
1. Soft reservation created in IVS at lead placement.
2. Available quantity decrements.
3. Soft reservation ID returned to SB.

**Blocked by:** C1, C4 | **ADO Story ID:** _(pending)_

---

#### US-4.2 — Soft Reservation Reconciled with Store Confirmation

> **Ref ID:** US-4.2 | **Legacy ID:** EP1C-S2

**As a** ServiceBench (reservation)
**I want** a soft reservation to reconcile with the final store reservation
**So that** there is no double-deduction when the store confirms the repair

**Acceptance criteria:**
1. Final reservation replaces soft reservation (no double-deduction).
2. If soft reservation expires or is cancelled, inventory is restored.

**Blocked by:** C5 | **ADO Story ID:** _(pending)_

---

#### US-4.3 — Soft Reservation Auto-Expiration Handling

> **Ref ID:** US-4.3 | **Legacy ID:** EP1C-S3

**As a** DAX / IVS
**I want** a defined soft reservation expiration model
**So that** uncommitted soft reservations don't block inventory indefinitely

**Acceptance criteria:**
1. Expiration model confirmed (auto-expire after X min OR store acknowledgment).
2. Expired soft reservations auto-release inventory.

**Blocked by:** C4 | **ADO Story ID:** _(pending)_

---

### F-5: AOP Provider Inventory Migration to D365

| Field | Value |
|-------|-------|
| **Goal** | Migrate full inventory lifecycle for 9 AOP service providers (~100 locations) from ServiceBench to DAX/D365. |

| **Ref ID** | F-5 |
| **Linked FRs** | FR-5, FR-12 |
| **ADO Feature(s)** | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) |
| **Quarter** | Q3 |
| **Status** | Discovery |
| **Architecture blockers** | G1, G2, H15, H16 — stories `[BLOCKED]` until resolved |

#### US-5.1 — Full Inventory Lifecycle in D365 for AOP Providers

> **Ref ID:** US-5.1 | **Legacy ID:** EP2-S1

**As a** 3rd party AOP provider
**I want** inventory orders, transfers, receiving, RMA, and cycle count managed in D365
**So that** I no longer use ServiceBench for Asurion inventory lifecycle

**Acceptance criteria:**
1. All lifecycle actions available in D365 (orders, transfers, receiving, RMA, cycle count).
2. No ServiceBench dependency for AOP inventory.
3. **Warehouse setup:** each technician location provisioned as a separate warehouse in D365; warehouse creation triggered upon technician onboarding (Plus One certification process is a candidate trigger).
4. **WMA cycle count tool evaluation (HLE 2026-03-25):** UBIF received a new AWS-based cycle count tool built in ServiceBench — team has recording and code repository access. Evaluate whether this tool covers AOP cycle count needs or if additional development is required before scoping this story's AC for cycle count.
5. AOP providers access D365/WMA via native app; not direct DAX UI (legal constraint — same restriction as ISP; WMA gap analysis required to confirm sufficient field exposure without excess data visibility).

**Blocked by:** G1 | **ADO Story ID:** _(pending)_

---

#### US-5.2 — AOP Inventory Management via Native WMA App

> **Ref ID:** US-5.2 | **Legacy ID:** EP2-S2

**As a** 3rd party AOP provider
**I want** access to DAX inventory management via the **native WMA app**, accessible from a link in Prism
**So that** I can manage inventory in a single system without needing ServiceBench

> **Note (2026-03-18):** Web-based WMA (portal-embedded wrapper) was evaluated and ruled out — certification burden, performance concerns, user management complexity. Native WMA app confirmed. Whether 3rd party AOP locations need WMA UI at all vs. systematic API-only must be confirmed (H15) before this story is fully scoped.

**Acceptance criteria:**
1. Native WMA app is accessible via Prism link; provider can complete full AOP lifecycle (orders, receiving, transfers, RMA, cycle count).
2. Web-based WMA is not used; all AOP inventory management is in native WMA.
3. Phase 2 path (Prism Single Pane of Glass) scoped separately; not a blocker for this story.
4. Identity and access model confirmed (G2, H16).
5. _If H15 resolves as API-only: this story is rescoped or removed._

**Blocked by:** G1 (EA sign-off on native WMA), H15 (WMA UI vs API-only) | **ADO Story ID:** _(pending)_

---

#### US-5.3 — AOP Provider Identity and Access via Hydra and Prism

> **Ref ID:** US-5.3 | **Legacy ID:** EP2-S3

**As a** AOP provider (identity)
**I want** to log into Prism Elite using Hydra credentials
**So that** I don't need a separate Asurion account for inventory management

**Acceptance criteria:**
1. Hydra guest account provisioned for AOP providers.
2. Email structure confirmed.
3. Identity flow tested for all 9 providers.

**Blocked by:** G2, H16 | **ADO Story ID:** _(pending)_

---

#### US-5.4 — Automated SKU and MDM Setup in DAX for AOP

> **Ref ID:** US-5.4 | **Legacy ID:** EP2-S4

**As a** MDM / Robbie Carter
**I want** automated SKU/MDM setup in DAX with no manual ServiceBench replication
**So that** setup is single-touch with no swivel-chair

**Acceptance criteria:**
1. New part created in MDM → automatically available in D365 for AOP.
2. ServiceBench manual setup step eliminated.

**Blocked by:** F1, F2 | **ADO Story ID:** _(pending)_

---

#### US-1.3 — 3rd Party Price on Job/Claim

> **Ref ID:** US-1.3 | **Legacy ID:** EP0-S3 | **Moved from F-1 to F-5** (3rd party price belongs with AOP inventory lifecycle, not UBIF pricing)

**As a** claims / finance user
**I want** 3rd party (AOP/NAOP) price consistently set on Job/Claim
**So that** reimbursement and reconciliation are accurate for all SUR providers, not just UBIF

**Acceptance criteria:** _(TBD — pending OQ H1 resolution)_
- AOP: confirm whether zero / consigned pricing continues or requires transactional price in D365
- NAOP Mobile Klinik: SKU-level price management model TBD
- NAOP Mexico: pricing in consumption messages TBD (possibly BAU — no dev needed)

**Blocked by:** H1 | **Work Type:** BUS | **ADO Story ID:** _(pending H1)_

---

### F-6: NAOP Partner Feed Migration — Canada and Mexico

| Field | Value |
|-------|-------|
| **Goal** | Repoint TELUS/Mobile Clinic and ATT Mexico/Telcel feeds from RTI Webservice to DAX IVS API. |

| **Ref ID** | F-6 |
| **Linked FRs** | FR-4 |
| **ADO Feature(s)** | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) |
| **Quarter** | Q4 _(deferred — TELUS + Mexico partner decisions needed)_ |
| **Status** | Discovery |
| **Architecture blockers** | B1, B2, B4, C6 |

#### US-6.1 — TELUS Mobile Clinic Feed Migration to DAX IVS

> **Ref ID:** US-6.1 | **Legacy ID:** EP3-S1

**As a** TELUS / Mobile Clinic provider
**I want** my inventory feed repointed to the DAX IVS API (AWS/JSON)
**So that** SUR availability is consistent with DAX/SSOT

**Acceptance criteria:**
1. RTI Webservice fully replaced by DAX IVS API for TELUS.
2. All LCM perils available in feed.
3. 30-day rollback validated.

**Blocked by:** B1 (Plan A vs B decision) | **ADO Story ID:** _(pending)_

---

#### US-6.2 — Full Inventory Coverage — All Repair Types (Plan A Preferred)

> **Ref ID:** US-6.2 | **Legacy ID:** EP3-S2a

**As a** TELUS / Mobile Clinic provider
**I want** a full inventory feed for all perils (battery, camera, charging port, LCM)
**So that** no bypass exceptions are needed and SSOT is clean

**Acceptance criteria:**
1. All peril types in DAX feed for TELUS.
2. No fake SKUs.
3. Bypass flag not required.

**Blocked by:** B1 | **ADO Story ID:** _(pending)_

---

#### US-6.3 — LCM-Only Inventory with Bypass Flag — Plan B Fallback

> **Ref ID:** US-6.3 | **Legacy ID:** EP3-S2b

**As a** TELUS / Mobile Clinic provider
**I want** DAX to return a peril+client bypass flag for non-LCM perils
**So that** non-LCM jobs proceed without an inventory check (technology concession)

**Acceptance criteria:**
1. DAX BOM response includes bypass flag per peril+client config.
2. ServiceBench honors bypass flag.
3. LCM availability check still runs.

**Blocked by:** B1, B2 | **ADO Story ID:** _(pending)_

---

#### US-6.4 — ATT Mexico / Telcel Feed Migration to DAX IVS

> **Ref ID:** US-6.4 | **Legacy ID:** EP3-S3

**As a** ATT Mexico / Telcel provider
**I want** the RTI Webservice repointed to DAX IVS API (AWS/JSON, direct)
**So that** the Mexico feed migrates off RTI on the same pattern as TELUS

**Acceptance criteria:**
1. Direct DAX IVS API integration (not via L7).
2. SB Eng team owns web service post-migration.
3. Warehouse ID format standardized.

**Blocked by:** B4, E1 | **ADO Story ID:** _(pending)_

---

### F-7: Phased Rollout and Rollback Framework

| Field | Value |
|-------|-------|
| **Goal** | Controlled pilot-and-expand rollout with 30-day rollback for non-AOP cohorts. Applies across all phases. |

| **Ref ID** | F-7 |
| **Linked FRs** | FR-7 |
| **ADO Feature(s)** | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) |
| **Quarter** | Cross-cutting |
| **Status** | Discovery |
| **Architecture blockers** | D6 |

#### Grooming callouts

> ⚠️ **Scope misalignment in ADO:** [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) "On Demand Ordering Configuration" contains 7 WMA mobile stories — this is AOP/Q3 scope (F-5), not the F-7 rollout flag framework.
> - Action: Confirm with BeyondX team and move 679641 stories under F-5 (Q3)
> - Action: Create a **new ADO Feature** for the per-location feature flag rollout framework under F-7 — assign to BeyondX
> - US-7.2 BUS: D6 (on-demand ordering scope for 3rd party) is the decision gate before any dev work

#### US-7.1 — Feature Flag Rollout Control per Location and Provider

> **Ref ID:** US-7.1 | **Legacy ID:** EP4-S1

**As a** Engineering / Ops
**I want** a feature flag per location/provider for the DAX availability API
**So that** we can pilot with one store before broad rollout

**Acceptance criteria:**
1. Flag toggleable per location.
2. Fallback reverts to ServiceBench local data.
3. 30-day rollback tested for UBIF.

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### US-7.2 — On-Demand Ordering Scope for Third-Party Providers

> **Ref ID:** US-7.2 | **Legacy ID:** EP4-S2

**As a** Planning / Michelle
**I want** on-demand ordering confirmed for non-AOP 3rd party providers
**So that** the rollout plan is accurate

**Acceptance criteria:**
1. On-demand ordering scope confirmed (D6).
2. Included or excluded in rollout plan.

**Blocked by:** D6 | **ADO Story ID:** _(pending)_

---

## 11. Open Questions (Technical)

Technical design questions only. Product/business questions are in **PRD §12**. `[ARCH]` items here are mirrored from the PRD for TRD traceability — single owner assigned.

> Full detail and resolution history: [01-discovery/open-questions.md](../01-discovery/open-questions.md)

| # | Question | Owner | Status | Blocks |
|---|----------|-------|--------|--------|
| A1 | Peril-to-part-type: **ServiceBench** owns mapping; DAX consumes part types | Ankit / DAX Arch | **Resolved** | — |
| A2 [ARCH] | Bypass config (TELUS/non-LCM): ties to **B1/B2**; generic DAX vs SB TBD | Ankit / DAX Arch | Open | EP1-S1 |
| A4 | Job-type exclusions: **SKU-level** in DAX; Robbie security on existing form | Robbie Carter / DAX | **Resolved** | — |
| B1 [ARCH] | TELUS: Plan A (full perils) vs Plan B (LCM-only + bypass)? | Ankit / TELUS rel. | Open | EP3-S1, EP3-S2a, EP3-S2b |
| B2 [ARCH] | Bypass flag: DAX BOM response or SB client config? | DAX Arch | Open | EP3-S2b |
| C1 [ARCH] | Soft reservation lifecycle ownership end-to-end | DAX / SB Arch | Open | EP4-S1 |
| C4 [ARCH] | Soft reservation expiration model | DAX Arch | Open | EP4-S1, EP4-S3 |
| C5 [ARCH] | Double-deduction prevention: soft + hard reservation state | DAX Arch | Open | EP4-S2 |
| C6 [ARCH] | UBIF Legacy reservation: not-reservable response vs SB always reserves? | DAX / SB | **Deferred** — H6 resolved; Legacy not in Q2; revisit if Plan B confirmed | EP3-S1 |
| D1 [ARCH] | Availability API: separate flags for in-stock and JIT per part line? | DAX Arch | **Resolved** (2026-03-25) — `qty` + `allowJustInTime` confirmed separate fields | — |
| D2 | Shipping days out in availability API response? | DAX Arch | **Resolved** | — |
| D3 | Job-type exclusion: **returned in response** (post-filter) | DAX Arch | **Resolved** | — |
| D4 | Reservation + JIT order: **two separate APIs** — availability is read-only; reservation is writable | DAX Arch | **Resolved** (2026-03-26) | — |
| E1 [ARCH] | Warehouse ID format standardization for 3rd party providers | DAX / SB Eng | Open | EP3-S3 |
| E2 | ISP vs SUR: **LOB** routing (WLI vs WCF); internal UBIF vs America's IVS = DAX PBI | DAX / SB Eng | **Resolved** (SB contract) | — |
| G1 [ARCH] | MFE vs WMA for AOP: WMA Phase 1 confirmed | DAX / Prism | **Resolved** (2026-03-26) — WMA confirmed via DDD-SUR architecture; G1 [ARCH] tag cleared | — |
| G2 [ARCH] | Identity for AOP providers in Prism Elite (Hydra structure) | Sandeep / Corey Street | **Near resolution** — Azure AD guest accounts direction confirmed; H15/H16 + identity design session still needed | EP5-S3 |
| I1 [ARCH] | BOM lookup: embed in EIAA or separate BOM service? Combined design confirmed 2026-03-25; Prism peril-change sub-question (I4) open | Ankit / DAPI / Integration | **Near resolution** | EP1-S1 |
| I2 | AOP JIT reservation required when availability = false? | Avengers / DAX Arch | **Resolved** | — |
| I3 [ARCH] | Substitution matrix: reuse Replacement Matrix vs new F&O entity? | Avengers / Robbie Carter / Rose | Open | EP6-S2 |
| I4 | Prism peril-change scenario: Option 1A (reuse combined API, ignore qty) vs Option 1B (separate BOM lookup for peril changes) | BeyondX / DAPI / Michelle | Open | EP1-S1 (peril-change flow) |
| B5 | NAOP inventory feed frequency: Mobile Klinik + Mexico cadence must be defined to maintain accuracy KPIs | SB Eng / Integration | Open | EP3-S1, EP3-S2a |

---

## 12. FR Coverage Audit

> Cross-reference: every FR from the PRD §7 mapped to the stories that implement it. When a FR changes in the PRD, find it here and review each linked story. Update AC or add stories as needed before pushing to Notion.

| FR | Requirement (summary) | Covered by | Status |
|----|-----------------------|------------|--------|
| FR-1 | Single availability + reservation API | EP1-S1, EP1-S4 | Draft — blocked A2 [ARCH], I1 (near-resolution) _(D1 resolved · D4 resolved)_ |
| FR-2 | UBIF orchestration API (distro, routing, deprecate feeds) | EP1-S2, EP1-S3 | EP1-S3 **Grooming Ready**; EP1-S2 **Grooming Ready** _(D1 resolved 2026-03-25)_ |
| FR-3 | Part price on Job/Claim (UBIF only) | EP0-S1 (Done), EP0-S2 (Active) | S2 Done · S1 Active · 3rd party scope → FR-12 |
| FR-4 | NAOP migration — Mobile Clinic + Mexico | EP3-S1, EP3-S2a, EP3-S2b, EP3-S3 | Draft — Q4; blocked B1 B2 B4 |
| FR-5 | AOP migration — 3rd party Asurion-owned parts | EP2-S1, EP2-S2, EP2-S3, EP2-S4 | Draft — blocked G1 G2 F1 F2 |
| FR-12 | 3rd party price on Job/Claim (AOP/NAOP) | EP0-S3 (US-1.3) | Draft — blocked H1 |
| FR-6 | UBIF Next Gen orchestration | EP1-S1, EP1-S2 | EP1-S3 ready; EP1-S1/S2 Draft — blocked A2 D1 I1 |
| FR-7 | Phased rollout + rollback | EP4-S1, EP4-S2 | Draft — EP4-S2 blocked D6 |
| FR-8 | JIT — availability API + configuration | EP1-S1 (flag + days out), EP1-S5 (exclusions), EP1-S6 (order creation) | EP1-S5 **Grooming Ready**; remainder Draft — blocked D4 D5 I1 |
| FR-9 | BOM + substitution matrix | EP1B-S1, EP1B-S2, EP1B-S3 | Draft — Q2; blocked F1 H4 A3 |
| FR-10 | Soft reservations via IVS | EP1C-S1, EP1C-S2, EP1C-S3 | Draft — Q2 pending H8; blocked C1 C4 C5 |
| FR-11 | SKU / MDM setup migration | EP1B-S1, EP2-S4 | Draft — Q2/Q3; blocked F1 F2 |

> **Sync rule:** When a FR is updated in the PRD §7, find it in the FR column above and review each linked story. Update AC or add stories as needed before pushing to Notion.

---

## 13. ADO Connection

| Field | Value |
|-------|-------|
| **Organization** | axasurion |
| **Project** | AX7 Core |
| **Area path** | AX7 Core\Global\Supply Chain\Client and New Channel |
| **Parent Epic** | [676287 — Inventory SSOT for SUR](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676287) |
| **Teams** | Client and New Channel · The Avengers · BeyondX |

### Existing ADO Features (under Epic 676287)

> **Work Type legend:** `Dev` = engineering deliverable requiring sprint capacity. `BA/KT` = PM/BA-owned coordination, knowledge transfer, or requirements work — no dev sprint needed. This flag is maintained in this TRD (not in ADO).

| ADO ID | Feature title | Assigned To | Team | State | Work Type | Maps to |
|--------|--------------|-------------|------|-------|-----------|---------|
| [676288](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676288) | AVENGERS: Discussions, KT sessions, and Design | M. Bowersox | The Avengers | In Progress | **BA/KT** | Discovery coordination — no dev deliverable |
| [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | AVENGERS: UBIF inventory availability lookup NextGen | — _(team)_ | The Avengers | In Progress | **Dev** | **F-2** — US-2.1, US-2.2, US-2.3 |
| [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) | AVENGERS: JIT Transfer orders | A. Hickman | The Avengers | In Progress | **Dev** | **F-2** — US-2.5, US-2.6 (JIT) |
| [681046](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681046) | AVENGERS: Part Substitution Matrix _(created Mar 24)_ | M. Bowersox _(coord.)_ | The Avengers | New | **Dev** | **F-3** — US-3.2; includes design PBI 681047 + sprint PBIs 681155, 681160 |
| [681055](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681055) | AVENGERS: JIT ordering from Distro _(created Mar 24)_ | M. Bowersox _(coord.)_ | The Avengers | New | **Dev** | **F-2 JIT** — US-2.5, US-2.6; includes whitelist research 681062 + lead-time PBI 681073 ⚠️ |
| [679639](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679639) | BeyondX: SUR SSOT — KT and Requirements gathering | — _(team)_ | BeyondX | In Progress | **BA/KT** | Discovery coordination — no dev deliverable |
| [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | BeyondX: SUR SSOT Configurations and Mappings | — _(team)_ | BeyondX | New | **Dev** | **F-3** (BOM/MDM configs) |
| [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) | BeyondX: SUR SSOT — On Demand Ordering | — _(team)_ | BeyondX | New | **Dev** | **F-7** — US-7.2 (rollout) |
| [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) | SUR SSOT: 3rd Party NAOP inventory availability lookup | — | Client & New Channel | New | **Dev** | **F-6** |
| [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) | SUR SSOT: 3rd Party AOP Migration | — | Client & New Channel | New | **Dev** | **F-5** |
| [677454](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677454) | AVENGERS: UBIF inventory availability lookup Legacy Portal | — | The Avengers | New _(Hold)_ | **Dev** | **F-8** (UBIF Legacy deferred) — ⚠️ possibly out of scope [OQ: H6] |

> ⚠️ 681055 contains PBI **681073** (JIT lead time: battery = 7 days, non-battery = 3 days) which has no corresponding PRD story. Needs FR-8 update or new US before grooming.
> M. Bowersox _(coord.)_ = Michelle created and is coordinating this feature; dev work is delivered by the Avengers engineering team. Not a BA-only feature.

### ADO Features pending confirmation — Michelle Bowersox

| TRD Epic | Description | Question for Michelle | Create when |
|----------|-------------|----------------------|-------------|
| EP-2 | Part price on Job/Claim | [H7] Standalone epic or covered under ADO 677038 (UBIF Next Gen)? | Michelle confirms in scope + FR-3 unblocked |
| EP-4 | Soft reservations via IVS | [H8] In scope for this project or a separate initiative? | Michelle confirms in scope + OQ C1, C4, C5 resolved |

### Sync rules

- **Hierarchy:** Epic 676287 → Feature → User Story → Task
- **When a story moves to Grooming Ready:** create it in ADO; fill the ADO ID column in the master backlog table
- **Status sync:** when ADO Feature or Story moves, update the Status column in the master backlog table
- **Source of truth order:** Meeting notes → Open Questions → PRD §7 → this TRD §10 → ADO. Changes flow downward only.
- **Future:** Convert master backlog to a 3-table Notion relational database (FRs ↔ Epics ↔ Stories) when grooming begins — see `PROJECT-CONTEXT.md` Phase gates.

---

*AC stubs — expand during architecture working sessions and grooming. Stories cannot move to Grooming Ready while any referenced blocker is Open in `open-questions.md`.*

---

## 14. ADO Work Item Hierarchy (Ref IDs)

> Reference labels (EP-1, F-1…F-8, US-1.1…US-7.2) are manual identifiers used for cross-referencing in planning and grooming. ADO IDs are separate — see the **ADO ID** column. Legacy IDs preserve the original TRD story/epic numbering.
>
> Parent column: Features point to **EP-1**. User Stories point to their **Feature Ref ID**.

| Work Item Type | Ref ID | ADO Title | Legacy ID | Parent | FR | Target Quarter | Priority | Team | Work Type | Suggested State | ADO ID | Blocked By |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Epic | EP-1 | Inventory Transformation — SSOT | — | — | All | Q1–Q4 2026 | — | Multiple | Dev | New | [676287](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676287) | — |
| Feature | F-1 | Part Price on Job/Claim | EP-0 | EP-1 | FR-3 | Q1 | — | BeyondX | Dev | New | _(pending)_ | — |
| User Story | US-1.1 | Transactional Part Pricing — S2 UBIF Providers | EP0-S1 | F-1 | FR-3 | Q1 | P0 | BeyondX | Dev | Closed | _(pending)_ | — |
| User Story | US-1.2 | Transactional Part Pricing — S1 Providers (Apexia Pending) | EP0-S2 | F-1 | FR-3 | Q1 | P0 | BeyondX | Dev | Active | _(pending)_ | — |
| User Story | US-1.3 | 3rd Party Price on Job/Claim | EP0-S3 | F-5 | FR-12 | Q3 | TBD | BeyondX | BUS | New | _(pending)_ | H1 |
| Feature | F-2 | SUR Real-Time Availability API and UBIF Next Gen Orchestration | EP-1 | EP-1 | FR-1, FR-2, FR-6, FR-8 | Q2 | — | Avengers | Dev | New | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) · [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) | A2, D1, I1 |
| User Story | US-2.1 | SUR Part Availability API Endpoint (Read-Only) | EP1-S1 | F-2 | FR-1, FR-8 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | A2, D1, I1 |
| User Story | US-2.2 | Distro Availability Indicator in Single API Response | EP1-S2 | F-2 | FR-2 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | D1 |
| User Story | US-2.3 | ISP vs SUR Routing for Shared UBIF Store IDs | EP1-S3 | F-2 | FR-6 | Q2 | P0 | Avengers + BeyondX | Dev | New | _(pending)_ | — |
| User Story | US-2.4 | Reservation API — Reservation ID on All Orders | EP1-S4 | F-2 | FR-1 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | — |
| User Story | US-2.5 | Job Type Restrictions Configuration in DAX | EP1-S5 | F-2 | FR-8 | Q2 | P1 | Avengers | Dev | New | _(pending)_ | — |
| User Story | US-2.6 | JIT Order Creation and Eligibility Logic | EP1-S6 | F-2 | FR-8 | Q2 | P1 | Avengers | Dev | New | _(pending)_ | D5 |
| Feature | F-3 | BOM Automation and Substitution Matrix | EP-1B | EP-1 | FR-9, FR-11 | Q2 | — | Avengers | Dev | New | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | F1, H4 |
| User Story | US-3.1 | Single-Touch BOM Setup in DAX (Asurion and OEM Parts) | EP1B-S1 | F-3 | FR-9, FR-11 | Q2 | P1 | Avengers | Dev | New | _(pending)_ | F1 |
| User Story | US-3.2 | Part Substitution Rules Owned in DAX | EP1B-S2 | F-3 | FR-9 | Q2 | P2 | Avengers | Dev | New | _(pending)_ | H4, I3 |
| User Story | US-3.3 | OEM Equipment Type for Pricing and Charging | EP1B-S3 | F-3 | FR-9 | Q2 | P1 | Avengers | Dev | New | _(pending)_ | A3 |
| Feature | F-4 | Soft Reservations at Booking Time | EP-1C | EP-1 | FR-10 | Q2 _(pending H8)_ | — | Avengers | Dev | New | _(pending — confirm H8)_ | C1, C4, C5 |
| User Story | US-4.1 | Soft Reservation Created at Lead Placement | EP1C-S1 | F-4 | FR-10 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | C1, C4 |
| User Story | US-4.2 | Soft Reservation Reconciled with Store Confirmation | EP1C-S2 | F-4 | FR-10 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | C5 |
| User Story | US-4.3 | Soft Reservation Auto-Expiration Handling | EP1C-S3 | F-4 | FR-10 | Q2 | P0 | Avengers | Dev | New | _(pending)_ | C4 |
| Feature | F-5 | AOP Provider Inventory Migration to D365 | EP-2 | EP-1 | FR-5 | Q3 | — | Avengers | Dev | New | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) | G1, G2, H15, H16 |
| User Story | US-5.1 | Full Inventory Lifecycle in D365 for AOP Providers | EP2-S1 | F-5 | FR-5 | Q3 | P1 | Avengers | Dev | New | _(pending)_ | G1 |
| User Story | US-5.2 | AOP Inventory Management via Native WMA App | EP2-S2 | F-5 | FR-5 | Q3 | P1 | Avengers | Dev | New | _(pending)_ | G1, H15 |
| User Story | US-5.3 | AOP Provider Identity and Access via Hydra and Prism | EP2-S3 | F-5 | FR-5 | Q3 | P1 | Avengers | Dev | New | _(pending)_ | G2, H16 |
| User Story | US-5.4 | Automated SKU and MDM Setup in DAX for AOP | EP2-S4 | F-5 | FR-11 | Q3 | P1 | Avengers | Dev | New | _(pending)_ | F1, F2 |
| Feature | F-6 | NAOP Partner Feed Migration — Canada and Mexico | EP-3 | EP-1 | FR-4 | Q4 | — | Integration | Dev | New | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) | B1, B2, B4 |
| User Story | US-6.1 | TELUS Mobile Clinic Feed Migration to DAX IVS | EP3-S1 | F-6 | FR-4 | Q4 | P1 | Integration | Dev | New | _(pending)_ | B1 |
| User Story | US-6.2 | Full Inventory Coverage — All Repair Types (Plan A Preferred) | EP3-S2a | F-6 | FR-4 | Q4 | P1 | Integration | Dev | New | _(pending)_ | B1 |
| User Story | US-6.3 | LCM-Only Inventory with Bypass Flag — Plan B Fallback | EP3-S2b | F-6 | FR-4 | Q4 | P1 | Integration | Dev | New | _(pending)_ | B1, B2 |
| User Story | US-6.4 | ATT Mexico / Telcel Feed Migration to DAX IVS | EP3-S3 | F-6 | FR-4 | Q4 | P1 | Integration | Dev | New | _(pending)_ | B4, E1 |
| Feature | F-7 | Phased Rollout and Rollback Framework | EP-4 | EP-1 | FR-7 | Cross-cutting | — | BeyondX | Dev | New | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) | D6 |
| User Story | US-7.1 | Feature Flag Rollout Control per Location and Provider | EP4-S1 | F-7 | FR-7 | Cross-cutting | P0 | BeyondX | Dev | New | _(pending)_ | — |
| User Story | US-7.2 | On-Demand Ordering Scope for Third-Party Providers | EP4-S2 | F-7 | FR-7 | Cross-cutting | P1 | BeyondX | Dev | New | _(pending)_ | D6 |
| Feature | F-8 | UBIF Legacy Availability — Deferred | EP-5 (deferred) | EP-1 | FR-2 | Q3+ | — | Avengers | Dev | New | [677454](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677454) | H6 |
| Feature | — | AVENGERS: Discussions, KT sessions, Design | 676288 | EP-1 | — | Ongoing | — | Avengers | **BA/KT** | In Progress | [676288](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676288) | — |
| Feature | — | BeyondX: KT and Requirements gathering | 679639 | EP-1 | — | Ongoing | — | BeyondX | **BA/KT** | In Progress | [679639](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679639) | — |

---

## 15. Grooming Readiness & ADO Gap Assessment

> **Purpose:** Pre-grooming review for technology teams. Audits every PRD story against its ADO work item, identifies stories ready to groom vs. blocked, and surfaces mismatches between the PRD and ADO that must be resolved before sprint planning.
>
> **Last reviewed:** 2026-03-26

---

### Story Readiness by Feature and Quarter

> **Legend:** ✅ YES = story can be presented in a grooming session now · ❌ NO = blocked, do not groom · ⛔ HOLD = feature-level hold, no stories until gate clears · _(create)_ = ADO work item does not exist yet — PM action required

| Feature | PRD Story | FR | ADO Feature | ADO Story | PRD Status | Groom Ready? | Blockers | Team |
|---------|-----------|----|-----------|-----------|---------|----|------|------|
| **F-1 · Q1** | US-1.1 | FR-3 | _(pending — retrieve)_ | _(pending — retrieve)_ | Done ✅ | N/A | — | BeyondX |
| | US-1.2 | FR-3 | _(pending — retrieve)_ | _(pending — retrieve)_ | Active | N/A | — | BeyondX |
| **F-2 · Q2** | US-2.1 | FR-1, FR-8 | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | [677037](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677037) | Draft | ❌ NO | A2 [ARCH], I1 (near-res) | Avengers |
| | US-2.2 | FR-2 | 677038 | **_(create)_** | **Grooming Ready** | ✅ YES | — | Avengers |
| | US-2.3 | FR-6 | 677038 | **_(create)_** | **Grooming Ready** | ✅ YES | — | Avengers + BeyondX |
| | US-2.4 | FR-1 | 677038 | **_(create)_** | Draft | ✅ YES | — _(D4 resolved 03/26)_ | Avengers |
| | US-2.5 | FR-8 | [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) | **_(create)_** | **Grooming Ready** | ✅ YES | — | Avengers |
| | US-2.6 | FR-8 | 679502 | **_(create)_** | Draft | ❌ NO | D5 | Avengers |
| **F-3 · Q2** | US-3.1 | FR-9, FR-11 | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | **_(create)_** | Draft | ❌ NO | F1 | Avengers |
| | US-3.2 | FR-9 | [681046](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681046) | **_(create)_** | Draft | ❌ NO | I3 [ARCH], H4 | Avengers |
| | US-3.3 | FR-9 | 679640 | **_(create)_** | Draft (BUS) | ❌ NO | A3 | Avengers |
| **F-4 · Q2 ⚠️** | US-4.1 | FR-10 | _(pending H8)_ | _(pending)_ | Draft | ⛔ HOLD | H8 (scope); C1, C4 | Avengers |
| | US-4.2 | FR-10 | _(pending H8)_ | _(pending)_ | Draft | ⛔ HOLD | H8 (scope); C5 | Avengers |
| | US-4.3 | FR-10 | _(pending H8)_ | _(pending)_ | Draft | ⛔ HOLD | H8 (scope); C4 | Avengers |
| **F-7 · Cross** | US-7.1 | FR-7 | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) ⚠️ | **_(create)_** | Draft | ✅ YES | — | BeyondX |
| | US-7.2 | FR-7 | 679641 ⚠️ | **_(create)_** | Draft (BUS) | ❌ NO | D6 | BeyondX |
| **F-5 · Q3** | US-5.1 | FR-5 | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) | **_(create)_** | Draft | ❌ NO | G2, H15, H17 | Avengers |
| | US-5.2 | FR-5 | 677040 | **_(create)_** | Draft | ❌ NO | G2, H15, H16 | Avengers |
| | US-5.3 | FR-5 | 677040 | **_(create)_** | Draft | ❌ NO | G2, H16 | Avengers |
| | US-5.4 | FR-11 | 677040 | **_(create)_** | Draft | ❌ NO | F1, F2 | Avengers |
| | US-1.3 | FR-12 | _(pending)_ | **_(create)_** | Draft (BUS) | ❌ NO | H1 | BeyondX |
| **F-6 · Q4** | US-6.1 | FR-4 | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) | **_(create)_** | Draft | ❌ NO | B1 [ARCH] | Integration |
| | US-6.2 | FR-4 | 677039 | **_(create)_** | Draft | ❌ NO | B1 [ARCH] | Integration |
| | US-6.3 | FR-4 | 677039 | **_(create)_** | Draft | ❌ NO | B1 [ARCH], B2 [ARCH] | Integration |
| | US-6.4 | FR-4 | 677039 | **_(create)_** | Draft | ❌ NO | B4, E1 [ARCH] | Integration |

> **Stories ready to create in ADO now (Grooming Ready, no ADO story):** US-2.2 · US-2.3 · US-2.4 · US-2.5 · US-7.1

---

### Gap A — PRD Story Has No ADO Work Item

> Stories in the PRD backlog not yet created as ADO work items. Sorted by urgency.

| # | Severity | PRD Story | FR | Quarter | Reason not created | Action | Owner |
|---|----------|-----------|----|---------|--------------------|--------|-------|
| G-1 | 🔴 Critical | US-2.2 | FR-2 | Q2 | Grooming Ready; no blockers | **Create ADO User Story** under [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | PM |
| G-2 | 🔴 Critical | US-2.3 | FR-6 | Q2 | Grooming Ready; no blockers | **Create ADO User Story** under [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | PM |
| G-3 | 🔴 Critical | US-2.4 | FR-1 | Q2 | D4 resolved 03/26 — Reservation API unblocked | **Create ADO User Story** under [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | PM |
| G-4 | 🔴 Critical | US-2.5 | FR-8 | Q2 | Grooming Ready; no blockers | **Create ADO User Story** under [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) | PM |
| G-5 | 🟡 Medium | US-7.1 | FR-7 | Cross | Grooming Ready; ADO Feature 679641 misaligned (see Gap B-5) | Create after B-5 ADO Feature split | PM |
| G-6 | 🟡 Medium | US-2.6 | FR-8 | Q2 | Blocked D5 (JIT record ownership — partial) | Create after D5 confirmed | PM |
| G-7 | 🟡 Medium | US-3.1 | FR-9, FR-11 | Q2 | Blocked F1 (SB field documentation — Raghu/SCM) | Create after F1 delivered | PM |
| G-8 | 🟡 Medium | US-1.1, US-1.2 | FR-3 | Q1 | ADO story IDs exist but not filled in TRD §14 | Retrieve from ADO (search Epic 676287) and fill `_(pending)_` cells | PM |
| G-9 | 🟢 Low | US-3.2 | FR-9 | Q2 | Blocked I3 [ARCH] (sub matrix scope), H4 (ownership) | Create after I3 + H4 resolved | PM |
| G-10 | 🟢 Low | US-3.3 | FR-9 | Q2 | BUS — blocked A3 (OEM equipment type owner TBD) | PM to confirm A3 owner before dev | PM |
| G-11 | 🟢 Low | US-5.1–5.4 | FR-5, FR-11 | Q3 | Blocked G2, H15, H16, H17 | Create once identity + UI path resolved | PM |
| G-12 | 🟢 Low | US-6.1–6.4 | FR-4 | Q4 | Blocked B1 [ARCH], B2 [ARCH], B4, E1 [ARCH] | Create after TELUS architecture decisions | PM |
| G-13 | 🟢 Low | US-1.3 | FR-12 | Q3 | Blocked H1 (3rd party pricing scope) | Create after H1 scoped by Bryant | PM |
| G-14 | ⛔ HOLD | US-4.1–4.3 | FR-10 | Q2 | H8 not answered; C1/C4/C5 open | **Do not create** until Bryant/Michelle confirm H8 | Bryant |

---

### Gap B — ADO Work Item Has No PRD Story Mapping

> ADO items that don't correspond to a named PRD User Story. Needs mapping, AC update, or a new PRD story.

| # | Severity | ADO ID | ADO Title | Tagged FR | Quarter | Gap | Action |
|---|----------|--------|-----------|-----------|---------|-----|--------|
| B-1 | 🔴 Critical | [679882](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679882) | New config: Peril → Equipment Type Mapping | FR-9 | Q2 | BUS — "For Biz confirmation" tag; A3 open; no decision made | PM to confirm A3 owner; schedule decision. [679886] dev blocked until resolved |
| B-2 | 🔴 Critical | [679886](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679886) | Validate Peril → Equipment Type Mapping | FR-9 | Q2 | Dev blocked on B-1 BUS decision | Dependent on B-1 |
| B-3 | 🔴 Critical | [680934](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680934) | JIT flag management — 3rd Party AOP | FR-5 | Q2 ⚠️ | AOP scope (Q3) filed as Q2; no PRD story | Confirm with Avengers: move to F-5 Q3 or retain Q2? Update ADO quarter |
| B-4 | 🔴 Critical | [681066](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681066) | JIT flag indicator for AOP SKUs | FR-5 | Q2 ⚠️ | Same scope concern as B-3 | Same action as B-3 |
| B-5 | 🔴 Critical | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) | "On Demand Ordering" — rollout framework + AOP ordering mixed | FR-7, FR-5 | Q2/Q3 | ADO Feature conflates rollout flag framework (FR-7) and AOP on-demand ordering (FR-5) | **Split:** create new ADO Feature for F-7 per-location rollout; move WMA on-demand stories ([681260–81267](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681260)) under F-5 (677040) |
| B-6 | 🟡 Medium | [680113](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680113) | UBIF Enable IVS for F&O Data | FR-1 | Q2 | Done ✅ — may close OQ K3 (Q2 technical prerequisite) | Confirm with Matt Bertrand: does this close K3? If yes → mark K3 Resolved |
| B-7 | 🟡 Medium | [680122](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680122) | UBIF NG Part SKU → Asurion SKU Mapping Design | FR-1 | Q2 | Committed 🔵 — design gate for US-2.1 AC; no PRD story | Use output to finalize US-2.1 AC before US-2.1 enters sprint |
| B-8 | 🟡 Medium | [679505](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679505) | Design contract changes for JIT parts TO | FR-8 | Q2 | Committed 🔵 — design gate for US-2.6 AC; no PRD story | Use output to finalize US-2.6 AC before it enters sprint |
| B-9 | 🟡 Medium | [681047](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681047) | Part Sub Matrix — R&D & Design | FR-9 | Q2 | R&D gate for US-3.2; must complete before 681155/681160 | Ensure 681047 is scheduled; gates US-3.2 grooming |
| B-10 | 🟡 Medium | [681155](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681155) | Availability API Logic — Part Sub Matrix Sprint 271 | FR-9 | Q2 | No PRD story; placeholder sprint PBI; I3 open | Do not sprint until I3 resolved and US-3.2 is groomed; map to US-3.2 |
| B-11 | 🟡 Medium | [681160](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681160) | Availability API Logic — Part Sub Matrix Sprint 272 | FR-9 | Q2 | Same as B-10 | Same as B-10 |
| B-12 | 🟡 Medium | [681166](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681166) | Part Sub Matrix config SB1/UAT/Testing | FR-9 | Q2 | Validation PBI; no PRD story | Map to US-3.2 testing AC |
| B-13 | 🟡 Medium | 681073 _(in [681055](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681055))_ | JIT lead time: battery=7d, non-battery=3d | FR-8 | Q2 | No PRD story; no corresponding AC in US-2.6 | **Add to US-2.6 AC** (D2 confirmed; SCM-configurable) before 681073 enters sprint |
| B-14 | 🟡 Medium | [681260–681267](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681260) | WMA On Demand Ordering (7 stories) | FR-5 | Q3 | No PRD stories map to them; under wrong ADO Feature | Confirm D6/H14; create **US-5.5 WMA On-Demand Ordering** if in scope; move under F-5 (677040) |

---

### Gap C — Timing & Sprint Risks

| # | Severity | Item | Risk | Action | Owner |
|---|----------|------|------|--------|-------|
| C-1 | 🔴 Critical | F-3a / [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | Target date **2026-03-30 has passed** — BeyondX SUR SSOT Configs & Mappings shows no progress | Immediate escalation: discuss with BeyondX this week; confirm blocked by A3/F1 or under-prioritized | PM |
| C-2 | 🟡 Medium | US-2.1 / [677037](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677037) | In ADO as "New" — unassigned; A2 + I1 still open; [680122] design in sprint | Do not assign to sprint until A2 resolved; confirm 677037 is correctly structured vs design stories | Avengers |
| C-3 | 🟡 Medium | K3 / [680113](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680113) | "UBIF Enable IVS for F&O Data" Done ✅ — may close Q2 prerequisite OQ K3 | Confirm with Matt Bertrand; if resolved → mark K3 Resolved, remove from Q2 risk list | PM |
| C-4 | 🟡 Medium | 681073 JIT lead time | No PRD story or AC captures battery=7d/non-battery=3d; 681073 may enter sprint without it | Add to US-2.6 AC before 681073 is scheduled | PM |
| C-5 | 🟢 Low | US-1.1 + US-1.2 ADO IDs | ADO story IDs for Done/Active Q1 stories not filled in TRD §14 | Retrieve from ADO and fill `_(pending)_` in §14 | PM |

---

### Pre-Grooming Actions Summary

| Priority | Action | Owner | Target |
|----------|--------|-------|--------|
| 🔴 Immediate | **Create ADO User Stories** for US-2.2, US-2.3, US-2.4, US-2.5 (all Grooming Ready; sprint planning blocked without them) | PM | Before next sprint planning |
| 🔴 Immediate | **Escalate F-3a / [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640)** — 2026-03-30 deadline passed with no progress | PM | This week |
| 🔴 Immediate | **Resolve Q2 vs Q3 for [680934](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680934) + [681066](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/681066)** — AOP JIT flag stories in wrong quarter | PM + Avengers | This sprint |
| 🔴 Immediate | **Split ADO Feature [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641)** — create new F-7 rollout ADO feature; move WMA stories to F-5 (677040) | PM + BeyondX | Before Q2 grooming |
| 🟡 This sprint | **Confirm K3 with Matt Bertrand** — does [680113](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/680113) Done close OQ K3? | PM | This sprint |
| 🟡 This sprint | **Resolve OQ A3** — confirm OEM equipment type owner; unblocks [679882] BUS + [679886] dev | PM | This sprint |
| 🟡 This sprint | **Add JIT lead time to US-2.6 AC** — battery=7d, non-battery=3d (D2 confirmed; 681073) | PM | Before 681073 sprints |
| 🟡 This sprint | **Retrieve US-1.1 + US-1.2 ADO IDs** and fill TRD §14 | PM | This sprint |
| 🟡 Grooming prep | **Create ADO User Story for US-7.1** after ADO Feature 679641 is split | PM | Before rollout planning |
| 🟡 Grooming prep | **Schedule H8 decision with Bryant/Michelle** — F-4 Soft Reservations scope gate; entire feature on hold | PM | Before Q2 grooming |
| 🟢 Q3 prep | **Confirm D6 + H14** scope; create US-5.5 WMA On-Demand Ordering story if in scope; move [681260–81267] to F-5 | PM | Q2 planning cycle |
