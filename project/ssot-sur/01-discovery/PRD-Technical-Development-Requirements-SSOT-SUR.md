# TRD: Technical Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Tech lead / architect:** Ankit / Tim Clemens (Enterprise Architecture)  
**Last updated:** 2026-03-18  
**Status:** Draft — evolves as architecture decisions are finalized  
**Related PRD:** [PRD — Functional Requirements SUR SSOT](https://www.notion.so/3259532a1f8680b08cc4ebb72fe7b535)  
**Notion TRD page:** https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f  
**Synced with PRD:** 2026-03-18  
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

> **Status:** Being finalized through architecture working sessions. EA review scheduled week of 2026-03-24. [ARCH] blockers A1, A2, D1–D4, E2 must resolve before detailed design can be completed.

**External references (authoritative):**
- Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) — Flow 1 (AOP), 2A/2B (NAOP), 3/5 (UBIF), 4 (BOM Setup)
- DDD Feature Breakdown (architecture working session artifacts — will be linked from Confluence once MCP is connected)
- SUR SSOT Inventory Availability Orchestration diagrams (Confluence — pending link)

_This section will expand with high-level component diagram, system boundaries, and major integration patterns once architecture working sessions complete._

---

## 3. System Interactions

> **Status:** Pending architecture decisions. Flow IDs below correspond to PRD §9 flows. This section will expand with interaction patterns, sequence diagrams, and ownership per flow once [ARCH] blockers are resolved.

| Flow ID | Flow name | Systems involved | Key open question |
|---------|-----------|-----------------|-------------------|
| RT-1 | UBIF Next Gen availability | SB → EIAA → DAX Americas Availability Service | E2 [ARCH] — ISP vs SUR routing |
| RT-2 | UBIF Legacy availability | SB → EIAA → UBIF Current State | C6 [ARCH] — reservable vs not-reservable |
| RT-3 | NAOP availability (Canada / Mexico) | SB → EIAA → Tyk API Connect → vendor | B1 [ARCH] — Plan A vs B; B2 [ARCH] — bypass flag location |
| RT-4 | BOM lookup at job creation | SB → EIAA or separate BOM API | I1 [ARCH] — embed in EIAA vs separate BOM service |
| RT-5 | Soft reservation at lead placement | SB → IVS → store confirmation | C1 [ARCH] — lifecycle ownership; C4 [ARCH] — expiration; C5 [ARCH] — double-deduction |
| RT-6 | JIT availability + order | SB → EIAA (JIT flag) → order creation | A4 [ARCH] — job-type exclusion level; D3/D4 [ARCH] — single vs separate call |
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
| EIAA availability endpoint | FR-1, FR-8 | SB → DAX | Single endpoint per part line; returns availability flag, JIT flag, shipping days out, bypass flag, Asurion + OEM SKUs. Aligned to DES/ISP pattern. |
| EIAA / IVS reservation endpoint | FR-1 | SB → IVS | Creates and returns Reservation ID. Single vs combined JIT call TBD (D4). |
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

**Rollback:** 30-day rollback for non-AOP cohorts via per-location feature flags (EP7-S1). AOP rollback approach TBD.

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

> Epic rows show ADO Feature ID(s). Story rows show ADO User Story ID once created. FR refs trace each row back to the PRD §7.

| Type | ID | Summary | FR | Quarter | Priority | Status | ADO ID | Blocked by |
|------|----|---------|----|---------|----|--------|--------|-----------|
| **Epic** | EP-1 | DAX availability API + UBIF orchestration | FR-1, FR-2, FR-6, FR-8 | Q1 | — | Discovery | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) · [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) · [677454](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677454) ⚠️ | A1 A2 D1–D5 E2 |
| Story | EP1-S1 | Real-time availability endpoint | FR-1, FR-8 | Q1 | P0 | Draft | _(pending)_ | A1, A2, D1, D2, I1 |
| Story | EP1-S2 | Distro Vendor indicator in availability response | FR-2 | Q1 | P0 | Draft | _(pending)_ | D1 |
| Story | EP1-S3 | ISP vs SUR routing for shared UBIF store ID | FR-6 | Q1 | P0 | Draft | _(pending)_ | E2 |
| Story | EP1-S4 | Reservation ID on UBIF and DAX orders | FR-1 | Q1 | P0 | Draft | _(pending)_ | D4 |
| Story | EP1-S5 | JIT job-type exclusion configuration | FR-8 | Q1 | P1 | Draft | _(pending)_ | A4, D3 |
| Story | EP1-S6 | JIT order creation and eligibility logic | FR-8 | Q1 | P1 | Draft | _(pending)_ | D4, D5 |
| **Epic** | EP-2 | Part price on Job/Claim | FR-3 | Q1/Q2 | — | Discovery | _(pending — confirm [H7])_ | — |
| Story | EP2-S1 | Price on Job/Claim — UBIF Current State | FR-3 | Q1 | P0 | Draft | _(pending)_ | — |
| Story | EP2-S2 | Price on Job/Claim — UBIF Next Gen | FR-3 | Q1 | P0 | Draft | _(pending)_ | — |
| Story | EP2-S3 | 3rd party price on Job/Claim _(TBD)_ | FR-3 | Q1/Q2 | TBD | Draft | _(pending)_ | H1 |
| **Epic** | EP-3 | NAOP migration — Mobile Clinic + Mexico | FR-4 | Q2 | — | Discovery | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) | B1 B2 B4 C6 |
| Story | EP3-S1 | TELUS feed repointed to DAX IVS API | FR-4 | Q2 | P1 | Draft | _(pending)_ | B1 |
| Story | EP3-S2a | Full inventory for all perils — Plan A (preferred) | FR-4 | Q2 | P1 | Draft | _(pending)_ | B1 |
| Story | EP3-S2b | LCM-only + bypass flag — Plan B (fallback) | FR-4 | Q2 | P1 | Draft | _(pending)_ | B1, B2 |
| Story | EP3-S3 | ATT Mexico / Telcel feed repointed to DAX IVS API | FR-4 | Q2 | P1 | Draft | _(pending)_ | B4, E1 |
| **Epic** | EP-4 | Soft reservations via IVS | FR-10 | Q2/Q3 | — | Discovery | _(pending — confirm [H8])_ | C1 C4 C5 |
| Story | EP4-S1 | Soft reservation created at lead placement | FR-10 | Q2/Q3 | P0 | Draft | _(pending)_ | C1, C4, I2 |
| Story | EP4-S2 | Soft reservation reconciles with final store reservation | FR-10 | Q2/Q3 | P0 | Draft | _(pending)_ | C5, I2 |
| Story | EP4-S3 | Soft reservation expiration model | FR-10 | Q2/Q3 | P0 | Draft | _(pending)_ | C4 |
| **Epic** | EP-5 | AOP migration — 3rd party Asurion-owned parts | FR-5 | Q3 | — | Discovery | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) | G1 G2 H15 H16 |
| Story | EP5-S1 | Full inventory lifecycle in D365 for AOP | FR-5 | Q3 | P1 | Draft | _(pending)_ | G1, I2 |
| Story | EP5-S2 | AOP inventory UI via native WMA (Phase 1 — web-based WMA ruled out) | FR-5 | Q3 | P1 | Draft | _(pending)_ | G1, H15 |
| Story | EP5-S3 | Hydra identity for AOP providers in Prism | FR-5 | Q3 | P1 | Draft | _(pending)_ | G2, H16 |
| Story | EP5-S4 | Automated SKU/MDM setup in DAX (no SB replication) | FR-5 | Q3 | P1 | Draft | _(pending)_ | F1, F2 |
| **Epic** | EP-6 | BOM/MDM automation + substitution matrix | FR-9, FR-11 | Q3/Q4 | — | Discovery | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | A3 F1 F2 H4 |
| Story | EP6-S1 | Single-touch BOM setup in DAX (Asurion + OEM SKUs) | FR-9, FR-11 | Q3/Q4 | P1 | Draft | _(pending)_ | F1 |
| Story | EP6-S2 | Substitution matrix owned in DAX / MDM | FR-9 | Q3/Q4 | P2 | Draft | _(pending)_ | H4, I3 |
| Story | EP6-S3 | OEM equipment type confirmed for pricing logic | FR-9 | Q3/Q4 | P1 | Draft | _(pending)_ | A3 |
| **Epic** | EP-7 | Phased rollout + rollback framework | FR-7 | Cross-cutting | — | Discovery | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) | D6 |
| Story | EP7-S1 | Feature flag per location/provider for DAX API | FR-7 | Cross-cutting | P0 | Draft | _(pending)_ | — |
| Story | EP7-S2 | On-demand ordering scope confirmed for non-AOP | FR-7 | Cross-cutting | P1 | Draft | _(pending)_ | D6 |

> ⚠️ ADO Feature 677454 (UBIF Legacy Portal) may be out of scope — see OQ H6.

---

### Story details

> Full user story and acceptance criteria per story. AC stubs — expand during architecture working sessions and grooming.

---

### EP-1: DAX Availability API + UBIF Orchestration

| Field | Value |
|-------|-------|
| **Goal** | Replace UBIF→ServiceBench replication with a single real-time availability and reservation API. Includes JIT flag, job-type exclusion config, and order creation logic. |
| **Linked FRs** | FR-1, FR-2, FR-6, FR-8 |
| **ADO Feature(s)** | [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) · [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) |
| **Quarter** | Q1 |
| **Status** | Discovery |
| **Architecture blockers** | A1, A2, D1–D5, E2 — all stories `[BLOCKED]` until resolved |

#### EP1-S1 — Real-time availability endpoint

**As a** ServiceBench consumer
**I want** a single DAX endpoint to check SUR part availability per part line
**So that** I get real-time data without replication lag

**Acceptance criteria:**
1. API returns availability flag, JIT flag, shipping days out, bypass flag, Asurion + OEM SKUs per part line.
2. Response time ≤ SB local-lookup baseline.
3. Existing UBIF replication feed is deprecated for migrated stores.

**Blocked by:** A1, A2, D1, D2 | **ADO Story ID:** _(pending)_

---

#### EP1-S2 — Distro Vendor indicator in availability response

**As a** ServiceBench consumer
**I want** the Distro Vendor indicator returned in the same availability API response
**So that** I don't need a separate distro catalog feed

**Acceptance criteria:**
1. Distro Vendor flag included per part line in same response as availability.
2. Distro replication feed deprecated.

**Blocked by:** D1 | **ADO Story ID:** _(pending)_

---

#### EP1-S3 — ISP vs SUR routing logic

**As a** DAX / ServiceBench routing layer
**I want** logic to distinguish ISP vs SUR for stores that share the same ServiceBench ID
**So that** ISP availability calls don't mix with SUR availability calls

**Acceptance criteria:**
1. Routing correctly separates ISP and SUR calls for same UBIF store ID in all test cases.

**Blocked by:** E2 | **ADO Story ID:** _(pending)_

---

#### EP1-S4 — Reservation ID on all orders

**As a** store / portal user
**I want** a Reservation ID included in orders sent to UBIF and DAX
**So that** reservations are traceable end-to-end

**Acceptance criteria:**
1. Reservation ID present in all UBIF and DAX order payloads.
2. ID can be used to look up reservation state.

**Blocked by:** D4 | **ADO Story ID:** _(pending)_

---

#### EP1-S5 — JIT job-type exclusion configuration

**As a** DAX / F&O configuration owner
**I want** job-type exclusions modeled at the correct level (SKU or equipment type) in D365
**So that** JIT-ineligible job types (e.g., non-OSR/CSS) are correctly excluded from JIT availability

**Acceptance criteria:**
1. Job-type exclusion level confirmed: SKU-level in F&O or equipment-type level (OQ A4 resolved).
2. Exclusions apply to both parent and substitute SKUs.
3. ServiceBench SKU-level exclusion config deprecated for migrated stores.

**Blocked by:** A4, D3 | **ADO Story ID:** _(pending)_

---

#### EP1-S6 — JIT order creation and eligibility logic

**As a** ServiceBench / orchestration consumer
**I want** JIT order creation behavior and eligibility logic defined and implemented
**So that** JIT orders are created correctly without incorrectly decrementing warehouse inventory

**Acceptance criteria:**
1. JIT eligibility driven by distro "quantity one" record; owner confirmed (D5).
2. No inventory decrement at warehouse for JIT orders.
3. Reservation + JIT order creation confirmed: single API call or separate calls (OQ D4 resolved).
4. JIT flag included at line level in sales order.

**Blocked by:** D4, D5 | **ADO Story ID:** _(pending)_

---

### EP-2: Part Price on Job/Claim

| Field | Value |
|-------|-------|
| **Goal** | Set partner invoice price transactionally on the ServiceBench Job/Claim, deprecating the UBIF price replication feed. |
| **Linked FRs** | FR-3 |
| **ADO Feature(s)** | _(pending — confirm with Michelle Bowersox [H7])_ |
| **Quarter** | Q1/Q2 |
| **Status** | Discovery |
| **Architecture blockers** | H1 |

#### EP2-S1 — Part price on Job/Claim (UBIF Current State)

**As a** claims / finance user
**I want** part price set on the ServiceBench Job at the time of transaction (UBIF Current State)
**So that** Franchise Co. reconciliation uses the transactional price, not a replicated master

**Acceptance criteria:**
1. Price is written to Job/Claim at transaction time.
2. Matches UBIF invoice price.
3. UBIF price replication feed deprecated for migrated stores.

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### EP2-S2 — Part price on Job/Claim (UBIF Next Gen)

**As a** claims / finance user
**I want** part price on Job/Claim for UBIF Next Gen stores
**So that** the same reconciliation fix applies to Next Gen stores

**Acceptance criteria:**
1. Same as EP2-S1, scoped to Next Gen stores.
2. No dependency on UBIF Current State price replication.

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### EP2-S3 — 3rd party price on Job/Claim _(scope TBD)_

**As a** claims / finance user
**I want** 3rd party (NAOP/AOP) price consistently set on Job/Claim
**So that** pricing is consistent across all SUR providers

**Acceptance criteria:** _(TBD pending OQ H1 resolution)_

**Blocked by:** H1 | **ADO Story ID:** _(pending)_

---

### EP-3: NAOP Migration — Mobile Clinic + Mexico

| Field | Value |
|-------|-------|
| **Goal** | Repoint TELUS/Mobile Clinic and ATT Mexico/Telcel feeds from RTI Webservice to DAX IVS API. |
| **Linked FRs** | FR-4 |
| **ADO Feature(s)** | [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) |
| **Quarter** | Q2 |
| **Status** | Discovery |
| **Architecture blockers** | B1, B2, B4, C6 |

#### EP3-S1 — TELUS feed repointed to DAX IVS API

**As a** TELUS / Mobile Clinic provider
**I want** my inventory feed repointed to the DAX IVS API (AWS/JSON)
**So that** SUR availability is consistent with DAX/SSOT

**Acceptance criteria:**
1. RTI Webservice fully replaced by DAX IVS API for TELUS.
2. All LCM perils available in feed.
3. 30-day rollback validated.

**Blocked by:** B1 (Plan A vs B decision) | **ADO Story ID:** _(pending)_

---

#### EP3-S2a — Full inventory for all perils (Plan A — preferred)

**As a** TELUS / Mobile Clinic provider
**I want** a full inventory feed for all perils (battery, camera, charging port, LCM)
**So that** no bypass exceptions are needed and SSOT is clean

**Acceptance criteria:**
1. All peril types in DAX feed for TELUS.
2. No fake SKUs.
3. Bypass flag not required.

**Blocked by:** B1 | **ADO Story ID:** _(pending)_

---

#### EP3-S2b — LCM-only + bypass flag (Plan B — fallback)

**As a** TELUS / Mobile Clinic provider
**I want** DAX to return a peril+client bypass flag for non-LCM perils
**So that** non-LCM jobs proceed without an inventory check (technology concession)

**Acceptance criteria:**
1. DAX BOM response includes bypass flag per peril+client config.
2. ServiceBench honors bypass flag.
3. LCM availability check still runs.

**Blocked by:** B1, B2 | **ADO Story ID:** _(pending)_

---

#### EP3-S3 — ATT Mexico / Telcel feed repointed to DAX IVS API

**As a** ATT Mexico / Telcel provider
**I want** the RTI Webservice repointed to DAX IVS API (AWS/JSON, direct)
**So that** the Mexico feed migrates off RTI on the same pattern as TELUS

**Acceptance criteria:**
1. Direct DAX IVS API integration (not via L7).
2. SB Eng team owns web service post-migration.
3. Warehouse ID format standardized.

**Blocked by:** B4, E1 | **ADO Story ID:** _(pending)_

---

### EP-4: Soft Reservations via IVS

| Field | Value |
|-------|-------|
| **Goal** | Close the 1–5 min availability gap by implementing IVS soft reservations at lead placement. |
| **Linked FRs** | FR-10 |
| **ADO Feature(s)** | _(pending — confirm with Michelle Bowersox [H8])_ |
| **Quarter** | Q2/Q3 |
| **Status** | Discovery |
| **Architecture blockers** | C1, C4, C5 |

#### EP4-S1 — Soft reservation at lead placement

**As a** ServiceBench (booking)
**I want** IVS to create a soft reservation when a lead is placed
**So that** available inventory decrements immediately, preventing overcommitment during the booking window

**Acceptance criteria:**
1. Soft reservation created in IVS at lead placement.
2. Available quantity decrements.
3. Soft reservation ID returned to SB.

**Blocked by:** C1, C4 | **ADO Story ID:** _(pending)_

---

#### EP4-S2 — Soft reservation reconciliation

**As a** ServiceBench (reservation)
**I want** a soft reservation to reconcile with the final store reservation
**So that** there is no double-deduction when the store confirms the repair

**Acceptance criteria:**
1. Final reservation replaces soft reservation (no double-deduction).
2. If soft reservation expires or is cancelled, inventory is restored.

**Blocked by:** C5 | **ADO Story ID:** _(pending)_

---

#### EP4-S3 — Soft reservation expiration model

**As a** DAX / IVS
**I want** a defined soft reservation expiration model
**So that** uncommitted soft reservations don't block inventory indefinitely

**Acceptance criteria:**
1. Expiration model confirmed (auto-expire after X min OR store acknowledgment).
2. Expired soft reservations auto-release inventory.

**Blocked by:** C4 | **ADO Story ID:** _(pending)_

---

### EP-5: AOP Migration — 3rd Party Asurion-Owned Parts

| Field | Value |
|-------|-------|
| **Goal** | Migrate full inventory lifecycle for 9 AOP service providers (~100 locations) from ServiceBench to DAX/D365. |
| **Linked FRs** | FR-5 |
| **ADO Feature(s)** | [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) |
| **Quarter** | Q3 |
| **Status** | Discovery |
| **Architecture blockers** | G1, G2, H15, H16 — stories `[BLOCKED]` until resolved |

#### EP5-S1 — Full inventory lifecycle in D365

**As a** 3rd party AOP provider
**I want** inventory orders, transfers, receiving, RMA, and cycle count managed in D365
**So that** I no longer use ServiceBench for Asurion inventory lifecycle

**Acceptance criteria:**
1. All lifecycle actions available in D365.
2. No ServiceBench dependency for AOP inventory.

**Blocked by:** G1 | **ADO Story ID:** _(pending)_

---

#### EP5-S2 — AOP inventory UI via native WMA (Phase 1 — web-based WMA ruled out)

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

#### EP5-S3 — Hydra identity for AOP providers

**As a** AOP provider (identity)
**I want** to log into Prism Elite using Hydra credentials
**So that** I don't need a separate Asurion account for inventory management

**Acceptance criteria:**
1. Hydra guest account provisioned for AOP providers.
2. Email structure confirmed.
3. Identity flow tested for all 9 providers.

**Blocked by:** G2, H16 | **ADO Story ID:** _(pending)_

---

#### EP5-S4 — Automated SKU/MDM setup in DAX

**As a** MDM / Robbie Carter
**I want** automated SKU/MDM setup in DAX with no manual ServiceBench replication
**So that** setup is single-touch with no swivel-chair

**Acceptance criteria:**
1. New part created in MDM → automatically available in D365 for AOP.
2. ServiceBench manual setup step eliminated.

**Blocked by:** F1, F2 | **ADO Story ID:** _(pending)_

---

### EP-6: BOM/MDM Automation + Substitution Matrix

| Field | Value |
|-------|-------|
| **Goal** | Automate repair asset and BOM setup in DAX; migrate substitution matrix ownership to MDM/Tomlin. |
| **Linked FRs** | FR-9, FR-11 |
| **ADO Feature(s)** | [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) |
| **Quarter** | Q3/Q4 |
| **Status** | Discovery |
| **Architecture blockers** | A3, F1, F2, H4 |

#### EP6-S1 — Single-touch BOM setup in DAX

**As a** MDM team
**I want** single-touch BOM setup in DAX (Asurion + OEM SKUs)
**So that** there are no manual steps to replicate to ServiceBench

**Acceptance criteria:**
1. BOM returns both Asurion and OEM SKUs for 3rd party providers.
2. Validated against Canada NAOP production job.
3. ServiceBench BOM setup deprecated.

**Blocked by:** F1 | **ADO Story ID:** _(pending)_

---

#### EP6-S2 — Substitution matrix in DAX / MDM

**As a** MDM / Tomlin
**I want** the substitution matrix owned and maintained in DAX
**So that** substitution rules are in SSOT, not siloed in ServiceBench

**Acceptance criteria:**
1. Substitution matrix migrated to MDM/DAX.
2. Owner confirmed (H4).
3. Rose, Robbie Carter, Tomlin aligned.

**Blocked by:** H4, I3 | **ADO Story ID:** _(pending)_

---

#### EP6-S3 — OEM equipment type for pricing/charging

**As a** MDM team
**I want** OEM equipment type confirmed for pricing/charging logic
**So that** OEM SKUs are priced correctly in D365

**Acceptance criteria:**
1. OEM equipment type definition confirmed (A3).
2. Pricing/charging logic handles OEM correctly.

**Blocked by:** A3 | **ADO Story ID:** _(pending)_

---

### EP-7: Phased Rollout + Rollback Framework

| Field | Value |
|-------|-------|
| **Goal** | Controlled pilot-and-expand rollout with 30-day rollback for non-AOP cohorts. |
| **Linked FRs** | FR-7 |
| **ADO Feature(s)** | [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) |
| **Quarter** | Cross-cutting |
| **Status** | Discovery |
| **Architecture blockers** | D6 |

#### EP7-S1 — Feature flag per location / provider

**As a** Engineering / Ops
**I want** a feature flag per location/provider for the DAX availability API
**So that** we can pilot with one store before broad rollout

**Acceptance criteria:**
1. Flag toggleable per location.
2. Fallback reverts to ServiceBench local data.
3. 30-day rollback tested for UBIF.

**Blocked by:** — | **ADO Story ID:** _(pending)_

---

#### EP7-S2 — On-demand ordering scope confirmed

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
| A1 [ARCH] | Peril-to-equipment-type translation: DAX or ServiceBench? | Ankit / DAX Arch | Open | EP1-S1 |
| A2 [ARCH] | Bypass config: DAX peril+client vs SB client-level? | Ankit / DAX Arch | Open | EP1-S1 |
| A4 [ARCH] | Job-type exclusions: SKU-level or equipment-type level in F&O? | Robbie Carter / DAX | Open | EP1-S5 |
| B1 [ARCH] | TELUS: Plan A (full perils) vs Plan B (LCM-only + bypass)? | Ankit / TELUS rel. | Open | EP3-S1, EP3-S2a, EP3-S2b |
| B2 [ARCH] | Bypass flag: DAX BOM response or SB client config? | DAX Arch | Open | EP3-S2b |
| C1 [ARCH] | Soft reservation lifecycle ownership end-to-end | DAX / SB Arch | Open | EP4-S1 |
| C4 [ARCH] | Soft reservation expiration model | DAX Arch | Open | EP4-S1, EP4-S3 |
| C5 [ARCH] | Double-deduction prevention: soft + hard reservation state | DAX Arch | Open | EP4-S2 |
| C6 [ARCH] | UBIF Legacy reservation: not-reservable response vs SB always reserves? | DAX / SB | Open | EP3-S1 |
| D1 [ARCH] | Availability API: separate flags for in-stock and JIT per part line? | DAX Arch | Open | EP1-S1, EP1-S2 |
| D2 [ARCH] | Shipping days out in availability API response? | DAX Arch | Open | EP1-S1 |
| D3 [ARCH] | Job-type exclusion: pre-check or returned in response? | DAX Arch | Open | EP1-S5 |
| D4 [ARCH] | Reservation + JIT order: single combined call or separate? | DAX Arch | Open | EP1-S4, EP1-S6 |
| E1 [ARCH] | Warehouse ID format standardization for 3rd party providers | DAX / SB Eng | Open | EP3-S3 |
| E2 [ARCH] | ISP vs SUR routing logic for shared UBIF store ID | DAX / SB Eng | Open | EP1-S3 |
| G1 [ARCH] | MFE vs WMA for AOP: WMA Phase 1 confirmed; EA sign-off needed | DAX / Prism | Open | EP5-S1, EP5-S2 |
| G2 [ARCH] | Identity for AOP providers in Prism Elite (Hydra structure) | Sandeep / Corey Street | Open | EP5-S3 |
| I1 [ARCH] | BOM lookup: embed in EIAA or separate BOM service? | Ankit / DAPI / Integration | Open | EP1-S1 |
| I2 [ARCH] | AOP JIT reservation required when availability = false? | Avengers / DAX Arch | Open | EP4-S1, EP5-S1 |
| I3 [ARCH] | Substitution matrix: reuse Replacement Matrix vs new F&O entity? | Avengers / Robbie Carter / Rose | Open | EP6-S2 |

---

## 12. FR Coverage Audit

> Cross-reference: every FR from the PRD §7 mapped to the stories that implement it. When a FR changes in the PRD, find it here and review each linked story. Update AC or add stories as needed before pushing to Notion.

| FR | Requirement (summary) | Covered by | Status |
|----|-----------------------|------------|--------|
| FR-1 | Single availability + reservation API | EP1-S1, EP1-S4 | Draft — blocked A1 A2 D1 D2 D4 |
| FR-2 | UBIF orchestration API (distro, routing, deprecate feeds) | EP1-S2, EP1-S3 | Draft — blocked D1, E2 |
| FR-3 | Part price on Job/Claim | EP2-S1, EP2-S2, EP2-S3 | Draft — EP2-S3 blocked H1 |
| FR-4 | NAOP migration — Mobile Clinic + Mexico | EP3-S1, EP3-S2a, EP3-S2b, EP3-S3 | Draft — blocked B1 B2 B4 |
| FR-5 | AOP migration — 3rd party Asurion-owned parts | EP5-S1, EP5-S2, EP5-S3, EP5-S4 | Draft — blocked G1 G2 F1 F2 |
| FR-6 | UBIF Next Gen orchestration | EP1-S1, EP1-S2 | Draft — blocked A1 A2 D1 |
| FR-7 | Phased rollout + rollback | EP7-S1, EP7-S2 | Draft — EP7-S2 blocked D6 |
| FR-8 | JIT — availability API + configuration | EP1-S1 (flag + days out), EP1-S5 (exclusions), EP1-S6 (order creation) | Draft — blocked A4 D3 D4 D5 |
| FR-9 | BOM + substitution matrix | EP6-S1, EP6-S2, EP6-S3 | Draft — blocked F1 H4 A3 |
| FR-10 | Soft reservations via IVS | EP4-S1, EP4-S2, EP4-S3 | Draft — blocked C1 C4 C5 |
| FR-11 | SKU / MDM setup migration | EP6-S1, EP5-S4 | Draft — blocked F1 F2 |

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

| ADO ID | Feature title | Team | State | Maps to |
|--------|--------------|------|-------|---------|
| [676288](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/676288) | SUR SSOT: Discussions, KT sessions, and Design | The Avengers | In Progress | Discovery / EP-1 prereq |
| [677038](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677038) | SUR SSOT: UBIF inventory availability lookup NextGen | Client & New Channel | New | **EP-1** |
| [677454](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677454) | SUR SSOT: UBIF inventory availability lookup Legacy Portal | Client & New Channel | New | **EP-1** (legacy) — ⚠️ possibly out of scope [OQ: H6] |
| [677039](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677039) | SUR SSOT: 3rd Party NAOP inventory availability lookup | Client & New Channel | New | **EP-3** |
| [677040](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/677040) | SUR SSOT: 3rd Party AOP Migration | Client & New Channel | New | **EP-5** |
| [679502](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679502) | SUR SSOT: JIT Transfer orders | The Avengers | New | **EP-1** (JIT) |
| [679639](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679639) | BeyondX: SUR SSOT — KT and Requirements gathering | BeyondX | New | Discovery |
| [679640](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679640) | BeyondX: SUR SSOT Configurations and Mappings | BeyondX | New | **EP-6** (BOM/MDM) |
| [679641](https://axasurion.visualstudio.com/AX7%20Core/_workitems/edit/679641) | BeyondX: SUR SSOT — On Demand Ordering | BeyondX | New | **EP-7** (rollout) |

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
