# PRD: Functional Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Product owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Last updated:** 2026-03-23 (Tech Sync 2026-03-20 + **Job Type / Eligibility Logic 2026-03-23**: DAX-owned job type exclusions in availability response; SB adjudicates; **A5** client/market/model + audit; C2 partial from Tech Sync; **no meeting dated Fri 2026-03-21** in SSOT Meetings DB)  
**Status:** Draft  
**Related brief:** [Product Brief SUR SSOT](https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b)  
**Related TRD:** [TRD — Technical Requirements SUR SSOT](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f)  
**Synced with TRD:** 2026-03-23

> **Purpose:** This document defines the business context, product requirements, functional requirements, and user/process flows for SUR SSOT. Architecture, technical design, engineering backlog, and implementation details are documented in the TRD.

---

## 1. Overview

SUR SSOT extends Asurion's DAX platform inventory single source of truth — proven for DSE/NDES with significant shrink reductions — to Same Unit Repair. The initiative replaces fragmented, replication-based inventory data across ServiceBench, UBIF, and multiple vendor systems with a single real-time DAX/D365 source of record. Aligns to Fulfillment 2026 Objective 2: unified fulfillment ecosystem with a single, accurate system of record for inventory.

**Success metrics (summary):** $250k YoY shrink reduction (Q2) · $600k YTD YoY (Q3) · All SUR inventory inquiries and AOP lifecycle management in D365.

---

## 2. Stakeholders and RACI

> Six user groups benefit from this project: store/portal users (real-time availability + reservations), ServiceBench consumers (UBIF orchestration), claims/finance users (transactional part pricing), 3rd party NAOP providers (DAX IVS feeds), 3rd party AOP providers (full inventory lifecycle in D365), and operators (accurate JIT/appointment availability). Each is covered by the functional requirements in §7.

| Name | Role / Team | Area of ownership | RACI |
|------|-------------|-------------------|------|
| Bryant Mayne | Sr. Director, Software Engineering | Executive sponsor; accountable across all workstreams | A |
| Thays Pritchard | Product Manager (Fulfillment) | PRD authoring, stakeholder coordination, ADO backlog management | R |
| Marion James Pilande | Technical Project Manager | Technical coordination, sprint planning, engineering delivery tracking | R |
| Ankit | Enterprise Architecture | Peril mapping, bypass config, routing and JIT design decisions (A1, A2, B2, D1–D4, E2) | C |
| Tim Clemens | Enterprise Architecture | EA co-owner; architecture sign-off | C |
| DAPI Team | DAX API Engineering | EIAA (Early Inventory Availability API) — central orchestration, location/warehouse mapping, reservation/hold capability (DDD features 5–11) | R |
| Integration Team | DAX / Platform Engineering | NAOP Tyk API gateway integration; BOM API / PRISM BOM decision (DDD features 1–4); new Part Master Config Module | R |
| BeyondX Team | ServiceBench / Consumer Engineering | ServiceBench consumer integration: real-time availability call, Job/Claim price model, part line updates (DDD features 12–18) | R |
| Avengers Team | D365 / F&O Engineering | AOP full inventory lifecycle in D365 (orders, transfers, receiving, RMA, cycle count); WMA Phase 1 UI; part substitution matrix (DDD features 19–30, 34) | R |
| ETL Team | Data / Integration Engineering | Master data sync: locations, warehouses, inventory to DAX/IVS; data entity migration (DDD features 32–33) | R |
| Robbie Carter | MDM / Supply Chain | BOM and SKU setup migration; DAX MDM config (FR-9, FR-11) | C |
| Rose | MDM / Supply Chain | Substitution matrix requirements and DAX config (FR-9, H4) | C |
| Amir | UBIF SME | Current-state flow validation; Parts Management Flows working sessions | C |
| Raghu | Supply Chain (SCM) | ServiceBench field documentation for migration (F1); parts walkthrough lead | C |
| Kelly Shaw / Pat Clark | UBIF / Operations | JIT "quantity one" record ownership and distro config (FR-8, D5) | C |
| Michelle Bowersox | Planning / Program Management | On-demand ordering scope; epic prioritization gate (D6) | C |
| Sandeep / Corey Street | Prism / Identity | Identity model for 3rd party AOP providers in Prism Elite (FR-5, G2) | C |
| TELUS / Mobile Clinic | External partner | Plan A vs Plan B inventory decision; CRM migration timing (B1, B3) | C |
| UBIF Distro | Operations | Distro migration workstream; JIT eligibility records | I |

> **RACI key:** R = Responsible (drives the work) · A = Accountable (owns the outcome) · C = Consulted (input required before decisions) · I = Informed (kept updated on outcomes)

---

## 3. Business Problem

ServiceBench today depends on replicated inventory data from UBIF, 3rd party NAOP vendors, and AOP providers. This replication introduces 1–5 minute latency, inconsistencies between systems, and manual multi-system data setup. Key pain points:

- **Stale availability** causes broken appointments and incorrect booking decisions for both store technicians and Horizon consumers.
- **No soft reservation** creates a 1–5 minute window where the same part can be booked twice, leading to overcommitment.
- **Replicated pricing** from UBIF leads to inaccurate Franchise Co. reconciliation when invoice prices differ from master prices.
- **3rd party vendor feeds** (NAOP: TELUS, Mexico) run over a legacy RTI Webservice not aligned to the DAX integration standard.
- **AOP inventory lifecycle** (orders, receiving, transfers, RMA, cycle counts for 9 AOP providers) is fully managed in ServiceBench, which cannot be retired until this lifecycle moves to D365.
- **Manual SKU/BOM setup** requires Robbie Carter to replicate DAX MDM configuration to ServiceBench by hand — every new part requires two-system swivel-chair setup.

The initiative eliminates all replication by routing real-time inventory requests through DAX orchestration (EIAA) and migrating all inventory lifecycle management to D365.

---

## 4. Goals

| # | Goal | How it is measured |
|---|------|--------------------|
| G-1 | Single real-time API for SUR inventory availability and reservations (DES/ISP pattern) | UBIF inventory inquiries routed through DAX; replication feed deprecated |
| G-2 | Replace UBIF→ServiceBench replication with real-time orchestration; transactional part price on Job/Claim | Three replication feeds deprecated; price replication deprecated |
| G-3 | Migrate 3rd party NAOP and AOP inventory to DAX IVS / D365 | RTI Webservice deprecated; all AOP lifecycle in D365 |
| G-4 | Eliminate replication risks: inconsistency, latency, scalability | $250k YTD YoY shrink (Q2) · $600k YTD YoY (Q3) |

---

## 5. Scope

**In scope:**
- Single real-time availability + reservation API (EIAA / DAX orchestration) for UBIF Next Gen and Legacy, NAOP, and AOP
- Transactional part price on Job/Claim (UBIF Current State + Next Gen)
- NAOP migration: TELUS/Mobile Clinic + ATT Mexico/Telcel (RTI → Tyk API Connect → DAX IVS)
- AOP full inventory lifecycle in D365 (9 providers, ~100 locations): orders, transfers, receiving, RMA, cycle count
- JIT availability flag and shipping days out per part line; JIT order creation logic
- IVS soft reservations at lead placement (UBIF scale)
- BOM + OEM SKU setup; substitution matrix migration to DAX
- Phased rollout framework with per-location feature flags and 30-day rollback
- AgioTech / TechPeople NAOP integration _(pending confirmation — H9)_
- On-demand ordering for 3rd party providers _(pending confirmation — D6)_

**Out of scope (confirmed):**
- BAU Portal feed migration (TBD, separate workstream)
- Parts Portal
- Microsoft IVS for UBIF inventory
- Improve-replication-only approach
- ATT Tech Express (removed from scope)
- Web-based WMA (portal-embedded wrapper) — evaluated and ruled out 2026-03-18
- EU vendors (AsurionEU / Tesco / VirginMobile) — pending confirmation H10

---

## 6. Dependencies

| Dependency | Owner | Notes |
|------------|-------|-------|
| Next Gen Portal | UBIF Portal team | 100% UBIF store migration by end of Q2 2026. SSOT orchestration and D365 migration depend on this timeline. Nine AOP stores (~100 locations) block full legacy retirement until Prism is ready. |
| DAX / IVS / D365 (F&R, FF&C, IS, F&FS) | DAPI / Avengers / Integration Teams | Must deliver all infrastructure before Prism can provide 3rd party vendor solution. Build and operate orchestration API, IVS integration, NAOP/AOP migration. |
| ServiceBench / Prism | BeyondX Team | Consumer changes; Prism replaces ServiceBench for Asurion programs; 3rd party price scope TBD. |
| MDM / Robbie Carter | MDM Team | BOM and repair asset setup in DAX (Flow 4 working sessions); ServiceBench field documentation for migration. |
| TELUS / Mobile Clinic | Ankit / Business | Plan A vs Plan B decision required early; engage via Ankit. TELUS CRM migration timing may affect integration path. |
| Enterprise Architecture (Ankit / Tim Clemens) | Ankit / Tim Clemens | Confirmed engaged as of 2026-03-18. Ankit attending EA Support sessions and formally reviewing architecture proposal; feedback expected 2026-03-19. Tim Clemens named co-owner. Architecture review meeting being scheduled for week of 2026-03-24. **[OQ: H3 Resolved]** |
| UBIF Distro | Operations | Distro migration is a parallel workstream (DAX/UBIF); viable Distro Migration Plan in scope. |

---

## 7. Product Requirements and Functional Requirements

> Items in the **Open Qs** column reference `01-discovery/open-questions.md`. `[ARCH]` items are blockers — resolve before grooming. **Who needs this** anchors each requirement to the primary persona(s) from `01-discovery/personas.md`. Each FR maps to technical implementation in the TRD (see TRD §10 Engineering Backlog and §12 FR Coverage Audit).

### Availability & Reservation API · EP-1

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-1 | **Single availability and reservation API** | As a **ServiceBench consumer** (P2, P7), I need one real-time endpoint per part line so I get accurate availability without replication lag. | One endpoint (DES/ISP pattern) for all SUR inventory availability and reservations. Per-part-line response: availability flag, JIT flag, shipping days out, peril+client bypass flag, Asurion+OEM SKUs in BOM; **job type exclusions** returned as **excluded** job types for the part/context (DAX source of truth; SB applies offer logic — Job Type / Eligibility 2026-03-23). Reservation ID returned in orders to UBIF and DAX. Supports AOP and NAOP part lines. | A2 [ARCH], D1 [ARCH], D4 [ARCH], A5 | EP-1 (EP1-S1, EP1-S4) |
| FR-2 | **UBIF orchestration API** | As a **UBIF store technician** (P2), I need real-time orchestration to UBIF so distro availability is in the same response as inventory availability. | Global orchestration calls UBIF Current State and Next Gen in real time for availability and quantity; returns Distro Vendor indicator in same response. Deprecates inventory, distro, and price replication feeds from UBIF to ServiceBench. **ISP vs SUR** for the same ServiceBench store ID: **line of business** partitions repair (SUR → WLI) vs replace (ISP → WCF); internal **UBIF IVS vs America's IVS** routing is a DAX-side PBI (Tech Sync 2026-03-20). | — | EP-1 (EP1-S2, EP1-S3) |
| FR-6 | **UBIF Next Gen orchestration** | As a **UBIF Next Gen store** (P2), I need the JSON replication feed replaced by real-time orchestration so I'm never working from stale data. | Replace UBIF→ServiceBench JSON feed with real-time DAX orchestration. Include Distro Part Availability in same API. Deprecate all three replication datasets (availability, distro catalog, part price) from UBIF to ServiceBench. | — | EP-1 (EP1-S1, EP1-S2) |
| FR-8 | **JIT — availability API and configuration** | As an **operations dispatcher** (P6), I need JIT eligibility and shipping days out returned per part line so technicians can set customer expectations at booking. | Shipping days out returned per part line in availability response. **Job-type exclusions:** SKU-level in DAX; **excluded** job types in availability response; SB decides what to offer (A4 resolved; Job Type / Eligibility 2026-03-23). JIT flag returned per part line; included at line level in sales order. JIT eligibility driven by distro "quantity one" record; owner TBD. No inventory decrement at warehouse for JIT orders. Reservation + JIT order creation: single vs separate API call TBD. US clients only; OSR and CSS. | A5, D1 [ARCH], D4 [ARCH], D5 | EP-1 (EP1-S1, EP1-S5, EP1-S6) |

### Part Price on Job/Claim · EP-2

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-3 | **Part price on Job/Claim** | As a **claims/finance user** (P4), I need transactional partner invoice price on every Job/Claim so Franchise Co. reconciliation is accurate. | Partner invoice price set transactionally on Job/Claim in ServiceBench. Both UBIF Current State and Next Gen support this; price replication from UBIF deprecated for UBIF claims. Scope of ServiceBench local price copy for 3rd party claims: TBD. | H1 | EP-2 (EP2-S1, EP2-S2, EP2-S3) |

### NAOP Migration · EP-3

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-4 | **NAOP migration — Mobile Clinic and Mexico** | As a **NAOP vendor** (P3) and **store technician** (P2), I need NAOP inventory feeds moved off RTI Webservice to the standardized DAX IVS API so all vendors are on one integration pattern. | Repoint inventory feeds from RTI Webservice to DAX IVS API (AWS/JSON). Plan A: TELUS/Mobile Clinic provides full inventory for all perils (preferred). Plan B: LCM-only feed + peril+client bypass flag for non-LCM perils (fallback; fake SKUs ruled out). Mexico same pattern; SB team takes over web service. UBIF Legacy: reservable vs non-reservable by location. | B1 [ARCH], B2 [ARCH], B3, B4, C6 [ARCH], C7 | EP-3 (EP3-S1, EP3-S2a, EP3-S2b, EP3-S3) |

### Soft Reservations via IVS · EP-4

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-10 | **Soft reservations via IVS** | As a **Horizon consumer** (P7), I need inventory held at lead placement so the part I'm booking is still available when the store confirms — eliminating post-booking failures. | IVS creates soft reservation at lead placement; decrements available inventory immediately to close 1–5 min gap. Reconciles with store-created final reservation to prevent double deduction. Expiration model (auto-expire vs store acknowledgment) TBD. Applies to select providers only. | C1 [ARCH], C2, C3, C4 [ARCH], C5 [ARCH] | EP-4 (EP4-S1, EP4-S2, EP4-S3) |

### AOP Migration · EP-5

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-5 | **AOP migration — 3rd party Asurion-owned parts** | As an **AOP provider** (P1), I need all inventory lifecycle functions (orders, transfers, receiving, RMA, cycle counts) to move from ServiceBench to DAX/D365 so I have one system when SB is decommissioned. | Migrate full inventory lifecycle from ServiceBench to DAX/D365. UI via **native WMA app (Phase 1 — web-based WMA ruled out 2026-03-18)**; 3rd party providers access WMA via link in Prism. ISP picking/return screens will be first-class in UBIF Next Gen Portal (separate track). Whether 3rd party AOP locations need WMA UI or only systematic API integration: TBD (H15). Whether they will have Prism UI access: TBD (H16). Identity via Hydra; structure TBD (G2). | G1 [ARCH], G2 [ARCH], H15, H16 | EP-5 (EP5-S1, EP5-S2, EP5-S3, EP5-S4) |

### BOM / MDM / Substitution Matrix · EP-6

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-9 | **BOM and substitution matrix** | As an **MDM operator** (P5) and **store technician** (P2), I need BOM to return both Asurion and OEM SKUs and substitution rules to live in DAX so there's no manual multi-system replication. | BOM returns both Asurion and OEM SKUs for 3rd party providers (validated in production Canada NAOP job). OEM equipment type must be confirmed for pricing/charging logic. Substitution matrix owned by MDM/Tomlin; coordination with Robbie Carter, Rose. | A3, H4 | EP-6 (EP6-S1, EP6-S2, EP6-S3) |
| FR-11 | **SKU / MDM setup migration** | As an **MDM operator** (P5), I need a single DAX setup to replace manual ServiceBench replication so every BOM update isn't a two-system swivel-chair task. | ServiceBench part setup deprecated (precedent: DES/NDS). MDM owns single setup in DAX. Full ServiceBench field documentation (definition, options, mandatory/optional) required before migration to avoid breaking existing functionality. | F1, F2 | EP-6 (EP6-S1), EP-5 (EP5-S4) |

### Phased Rollout & Rollback · EP-7

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-7 | **Phased rollout and rollback** | As a **program manager** (all personas), I need each migration phase to be independently deployable per location/provider so we can roll back without affecting other phases. | Rollout order: (1) UBIF Next Gen + NAOP, (2) 3rd party NAOP (Canada/Mexico), (3) 3rd party AOP. Pilot by location/provider; 30-day rollback for non-AOP. On-demand ordering for 3rd party providers in scope (planning confirmation needed). | D6 | EP-7 (EP7-S1, EP7-S2) |

---

## 8. Non-Functional Requirements

| # | Requirement | Notes | Open Qs |
|---|-------------|-------|---------|
| NFR-1 | Orchestration API response time sufficient for real-time availability and JIT | Must match or exceed current ServiceBench local-lookup performance | — |
| NFR-2 | IVS soft reservation supports UBIF scale (~800 locations) without over-committing inventory | Scalability analysis required before design is finalized | H5 |
| NFR-3 | Reservation lifecycle prevents double deduction across soft and hard reservations | State reconciliation logic must be designed explicitly | C5 [ARCH] |
| NFR-4 | 3rd party (CAN, LatAm) feed repoint with minimal disruption; 30-day rollback for non-AOP; warehouse ID format standardized | Format standardization needed to match UBIF JSON format | E1 |

---

## 9. User / Process Flows

> Flows describe end-to-end business and operational behavior. Focus on logic, user actions, triggers, and outcomes. Technical realization details — system interactions, API contracts, data mapping — are in the TRD. Flow IDs used here match the TRD.
>
> **Process flows (reference):** Parts Management Flows (Figma)—Flow 1 (AOP), 2A/2B (NAOP), 3/5 (UBIF), 4 (BOM Setup). Current state mapping in progress via working sessions; future state defined once current state is validated and architecture decisions are resolved.
>
> Flows are grouped into four categories: **RT** (Runtime Transaction), **INT** (Integration/Feed), **IL** (Inventory Lifecycle), **CF** (Configuration).

### RT — Runtime Transaction flows (job creation / availability check)

One row per scenario. These flows execute at every service job creation event.

| Flow | ID | Current state | Future state | Gap / pain point | Open Qs |
|------|----|---------------|--------------|------------------|---------|
| UBIF Next Gen availability | RT-1 | ServiceBench stores replicated availability locally (1–5 min latency). Events-only feed from UBIF. | ServiceBench → EIAA → DAX Americas Availability Service → real-time response. Distro Vendor indicator returned in same call. JSON replication feed deprecated. | Stale availability causes broken appointments and incorrect decisions. | E2 (resolved); A5 |
| UBIF Legacy availability | RT-2 | ServiceBench receives events + APIs. Three replicated datasets: availability, distro catalog, part price. | EIAA orchestration replaces all three feeds. Reservable vs non-reservable flag per location. Part price returned transactionally on Job/Claim. | Highest-risk dataset; temporary bridge until full Next Gen migration (Q3). | C6 [ARCH], H1 |
| NAOP availability (Canada / Mexico) | RT-3 | RTI Webservice → ServiceBench. LCM-only feed; non-LCM perils have no BOM or availability check. | ServiceBench → EIAA → Tyk API Connect → vendor feed. Plan A: full inventory all perils. Plan B: LCM-only + bypass flag. RTI deprecated. | TELUS unwilling to provide full inventory; exception-handling logic is a technology concession. | B1 [ARCH], B2 [ARCH], B3, B4 |
| BOM lookup at job creation | RT-4 | ServiceBench local BOM; Asurion SKUs only. Manual multi-system setup per BOM entry. | EIAA returns BOM with Asurion + OEM SKUs per part line. Option 1: separate BOM API call from SB first. Option 2: embedded inside EIAA (single call). Decision pending. | Multiple manual touchpoints; OEM SKU type unconfirmed for pricing logic. | I1 [ARCH], A3 |
| Soft reservation at lead placement | RT-5 | No soft reservation — 1–5 min gap between availability check and final reservation. | ServiceBench calls IVS reservation API at lead placement; IVS reconciles with store-created final reservation; prevents double-deduction. | Overcommitment window at booking; risk of inventory sold twice. | C1 [ARCH], C4 [ARCH], C5 [ARCH] |
| JIT availability + order | RT-6 | ServiceBench checks "quantity one" at distro + shipping days out from SKU config. No inventory decrement on JIT orders. | EIAA returns JIT flag + shipping days out per part line; job-type exclusions as **excluded** types in response. Reservation + JIT order: single vs separate API call TBD. US only; OSR and CSS. | SKU-level exclusions in DAX (A4 resolved); API dimensions **A5**. | D4 [ARCH], D5, A5 |

### Availability + reservation API comparison

| | Current state | Future state |
|-|---------------|--------------|
| **Trigger** | Horizon → ServiceBench checks local replicated data | Horizon → ServiceBench → EIAA (real-time orchestration) |
| **Availability data** | Stale UBIF replication (1–5 min) | Real-time via UBIF Next Gen / Americas Availability Service |
| **BOM lookup** | ServiceBench local; Asurion SKUs only | EIAA or separate BOM API; returns Asurion + OEM SKUs (I1 pending) |
| **JIT eligibility** | ServiceBench checks "quantity one" at distro | EIAA returns JIT flag + shipping days out per part line |
| **Job type exclusions** | ServiceBench Part Master per-SKU toggles | DAX holds exclusions; response lists **excluded** job types; SB adjudicates offers (A5 pending contract) |
| **Bypass flag** | ServiceBench client-level config | DAX returns peril+client bypass flag in availability response (A2 pending) |
| **Soft reservation** | None | ServiceBench calls IVS at lead placement; IVS reconciles with final reservation |
| **Reservation ID** | Not passed to UBIF or DAX | Reservation ID included in orders to UBIF and DAX |
| **Part price** | Replicated master price from UBIF | Transactional price set on Job/Claim in ServiceBench |

### INT — Integration / Feed flows (vendor connectivity)

These flows govern how 3rd party vendor inventory data reaches the EIAA/DAX layer.

| Flow | ID | Vendor | Current integration | Future integration | Key change | Open Qs |
|------|----|--------|--------------------|--------------------|------------|---------|
| NAOP — Canada (Mobile Clinic / TELUS) | INT-1 | TELUS / Mobile Klinik | RTI Webservice → ServiceBench (LCM only) | Tyk API Connect → DAX Americas Availability Service (AWS/JSON) | RTI deprecated; Plan A/B decision pending for peril coverage | B1 [ARCH], B2 [ARCH], B3, B4 |
| NAOP — Mexico (ATT Mexico / Telcel) | INT-2 | ATT Mexico / Telcel | RTI Webservice direct (not via L7) → ServiceBench | Tyk API Connect → DAX Americas Availability Service. SB team takes over web service. | Same pattern as INT-1; feed ownership change | B4, E1 [ARCH] |
| NAOP — CA/LATAM others | INT-3 | AgioTech / TechPeople / others | Varies (RTI or legacy) | Tyk API Connect → standard NAOP feed contract | Standardize all NAOP feeds through Tyk; same API contract | H9 |
| UBIF Next Gen feed deprecation | INT-4 | UBIF Next Gen | JSON inventory events → ServiceBench replication | Real-time EIAA call replaces feed; no replication | Three replicated datasets deprecated | E2 [ARCH] |

### IL — Inventory Lifecycle flows (AOP full lifecycle in D365)

These flows apply to the 9 AOP service providers (~100 locations, remote tech only).

| Flow | ID | Current state | Future state | Open Qs |
|------|----|---------------|--------------|---------|
| AOP — Replenishment order (auto) | IL-1 | ServiceBench manages replenishment (auto-triggered by min/max). Robbie Carter manually replicates DAX MDM setup to ServiceBench. | D365 / DAX owns replenishment. WMA Phase 1 UI. ServiceBench setup deprecated. | G1, G2 [ARCH] |
| AOP — Restock order (manual) | IL-2 | ServiceBench manages manual restock (provider-initiated). | D365 / DAX owns restock. | G1, G2 [ARCH] |
| AOP — On-demand order | IL-3 | ServiceBench. On-demand (provider-specific manual orders). | D365 / DAX. Scope confirmation pending (D6). | D6, G1 |
| AOP — SURJIT order (auto) | IL-4 | ServiceBench. JIT orders auto-triggered for SUR-specific JIT parts. | D365 / DAX. **I2 resolved 2026-03-19:** no reservation for OOS JIT-enabled parts. | — |
| AOP — Receiving | IL-5 | ServiceBench. Marks serials as reserved (not in-stock); nightly job converts unused >30 days. | D365 / DAX. Same model expected; design TBD. | G2 [ARCH] |
| AOP — Transfers | IL-6 | ServiceBench. Manual inter-location transfer. | D365 / DAX via WMA. | G1 |
| AOP — RMA | IL-7 | ServiceBench. Return Merchandise Authorization. | D365 / DAX via WMA. | G1 |
| AOP — Cycle counting | IL-8 | ServiceBench. Manual cycle count. | D365 / DAX via WMA. | G1 |

### CF — Configuration flows (BOM, MDM, Part Master)

These flows govern how parts data, substitution rules, and configuration are set up and maintained.

| Flow | ID | Current state | Future state | Open Qs |
|------|----|---------------|--------------|---------|
| SKU / MDM setup | CF-1 | MDM sets up in DAX → Robbie Carter manually sets up in ServiceBench → Portal may also need separate setup. | MDM single setup in DAX. ServiceBench setup deprecated (precedent: DES/NDS). | F1, F2 |
| BOM / OEM SKU setup | CF-2 | BOM contains Asurion SKUs only. Robbie Carter manual replication. | BOM contains Asurion + OEM SKUs. ServiceBench BOM deprecated. OEM equipment type for pricing TBD. | A3, F1 |
| Part substitution matrix | CF-3 | Managed in Tomlin with Robbie Carter + Rose. Manual reconciliation. | New substitution matrix in F&O: reuse Replacement Matrix (modified) OR new menu/form/table/data entity. | I3 [ARCH], H4 |
| New Part Master Config Module | CF-4 | Not present. | New module: List Types, Part Groupings, Substitution Rules — feeds EIAA for substitution and bypass logic. Integration Team owns. | I1 [ARCH], I3 [ARCH] |

---

## 10. Success Metrics and Acceptance Criteria

| Release | Requirements | Acceptance criteria |
|---------|--------------|---------------------|
| Q1 | FR-1, FR-2, FR-6, FR-8 | ServiceBench calls single DAX API for SUR availability; real-time response from UBIF via orchestration; no replication. JIT flag and shipping days out returned per part line. UBIF inventory inquiries migrated to D365. *(At risk — track closely.)* |
| Q2 | FR-3, FR-4 | Part price set transactionally on Job/Claim; price replication deprecated. 3rd party NAOP migrated to D365; $250k savings YTD YoY. |
| Q3 | FR-5, FR-10 | AOP inventory management in D365 (WMA or MFE); no SUR inventory management in Prism. Soft reservations live at UBIF scale; zero overcommit incidents. $600k savings YTD YoY. |

---

## 11. Roadmap 2026

> Sequencing logic: architecture blockers must clear before engineering can groom. Build in the order of broadest impact → most complex migration, so each phase proves the infrastructure the next phase depends on.

| Quarter | Milestone | Why this order | FRs | Key dependencies | Target |
|---------|-----------|---------------|-----|-----------------|--------|
| **Now → Q1** | Complete discovery: resolve all `[ARCH]` blockers, finish current-state flow validation, confirm EA engagement | 15 `[ARCH]` questions block every FR from grooming. Engineering cannot start detailed design until peril mapping, reservation lifecycle, routing, and TELUS plan decisions are made. | All | Peril mapping meeting (A1, A2); TELUS Plan A/B (B1, B2); EA confirmation (H3) | 0 open `[ARCH]` blockers; current-state validated across all 5 flows |
| **Q1** | DAX availability API + UBIF Next Gen orchestration + JIT | Highest-volume impact (~800 stores, highest availability call frequency). Next Gen Portal migration completes Q2 — the availability API must be proven before that cutover window. JIT flag and shipping days out included in same API. Q1 KR at risk if delayed. | FR-1, FR-2, FR-6, FR-8 | **E2 resolved**; I1/A5/D1/D4; JIT **D4–D5** (D3 resolved); Next Gen Portal timeline | UBIF inquiries migrated to D365; real-time availability live; JIT flag and days-out per part line; Q1 KR met |
| **Q1/Q2** | Part price on Job/Claim | Relatively self-contained API + ServiceBench model change; high financial impact (Franchise Co. reconciliation fixed). Ship before NAOP adds new complexity. | FR-3 | UBIF Current State + Next Gen API changes; SB Job/Claim model update | Price replication deprecated; transactional price on all UBIF claims |
| **Q2** | NAOP migration — Mobile Clinic + Mexico | Removes RTI Webservice dependency; aligns TELUS/Mexico to the DAX pattern. TELUS Plan A/B must be decided in Q1 to be implementation-ready by Q2. | FR-4 | TELUS decision (B1); warehouse ID standardization (E1); web service handoff (B4) | $250k YTD YoY savings; 3rd party NAOP feeds in D365 |
| **Q2/Q3** | Soft reservations via IVS | Closes the 1–5 min availability gap that causes overcommitment at booking. Must be proven at UBIF scale (~800 locations) before AOP adds more reservation volume. | FR-10 | Reservation lifecycle design (C1, C4, C5); double-deduction prevention (C5) | Zero overcommit incidents at UBIF scale; soft reservation live |
| **Q3** | AOP migration — 3rd party Asurion-owned parts | Most complex: full inventory lifecycle change, UI path (MFE vs WMA), identity management (Hydra). Goes last so DAX/IVS infrastructure is fully proven and all prior architecture decisions are stable. | FR-5 | MFE vs WMA decision (G1); Hydra identity (G2); DAX infrastructure complete; Prism ready for 9 AOP stores | AOP inventory in D365; $600k YTD YoY savings; Prism legacy retirement unblocked |
| **Q3/Q4** | BOM/MDM automation + substitution matrix | Reduces manual swivel-chair setup. Does not block availability or reservations — schedule parallel to or following AOP migration. | FR-9, FR-11 | MDM automation design (F2); substitution matrix owner confirmed (H4) | Single-touch SKU setup in DAX; ServiceBench part setup deprecated |

> **Prerequisite gate:** **A1, E2, D2, A4, D3** resolved (2026-03-19–20). Remaining `[ARCH]` for Q1 grooming include **A2, D1, D4**, plus **I1** (API contract). **A5** (exclusion dimensions / audit) to close in same contract cycle where possible. Target: architecture working sessions **week of 2026-03-24**.

**Technical development details (epics, stories, ADO):** See [TRD — Technical Requirements SUR SSOT](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f) and `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`. This PRD is the stable functional alignment reference.

---

## 12. Open Questions

Full detail in **[01-discovery/open-questions.md](../01-discovery/open-questions.md)**. Items tagged `[ARCH]` are technical architecture blockers — listed here for PRD traceability, resolved via architecture working sessions (TRD-owned). Untagged items are PRD/business-owned.

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| A1 | Who owns peril-to-part-type translation for DAX calls? (Bypass for TELUS/non-LCM is **B1/B2**.) | Ankit / DAX Arch | **Resolved** | **Tech Sync 2026-03-20:** **ServiceBench** maps peril → part types (LCM, BAT, etc.); Cloud→Prism→DAX handoff for equipment type; DAX filters BOM by part type + job-type exclusion on part. No client on peril map. |
| A2 [ARCH] | Should "bypass inventory check" (when no inventory) be driven in DAX vs ServiceBench? **Peril mapping is not client-scoped** — see A1 answer. **TELUS path:** B1/B2. | Ankit / DAX Arch | Open | **Tech Sync 2026-03-20:** Narrowed — client not in peril row; confirm with **B1/B2** for TELUS. |
| A3 | OEM parts equipment type: what is the correct type for pricing/charging logic? Required before BOM can return OEM SKUs for 3rd party providers. | MDM / SCM | Open | |
| A4 | Job-type exclusions: SKU-level vs equipment-type in F&O? | Robbie Carter / DAX | **Resolved** | **Tech Sync 2026-03-20:** **SKU-level attribute in DAX**; existing form; MDM + **Robbie security** for on-the-fly changes; Michelle tracks in PBI. |
| A5 | Job type exclusion dimensions (client/market/model) + audit expectations for DAX config | DAX / Michelle / Robbie | Open | **EA Support (2) 2026-03-20** + **Job Type / Eligibility 2026-03-23:** DAX holds exclusion data; API returns **excluded** job types; **SB adjudicates** offers. **D3 resolved** — exclusions in response. No model in today’s SB exclusion UI; **client vs market** TBD in API workshop (week of 2026-03-24). |
| B1 [ARCH] | TELUS/Mobile Clinic: Plan A (full inventory for all perils) vs Plan B (LCM-only + bypass flag)? | Ankit / TELUS rel. | Open | |
| B2 [ARCH] | Should the bypass flag live in DAX's BOM response or in ServiceBench's client config? | DAX Arch | Open | |
| B3 | TELUS CRM migration timing — does it affect the preferred integration path? | Business / TELUS rel. | Open | |
| B4 | Mexico/Mobile Clinic feed: who takes over the RTI web service when it moves to AWS/JSON? | SB Eng / DAX | Open | |
| C1 [ARCH] | Who owns the soft reservation lifecycle end-to-end? (SB initiates, store confirms, IVS manages state) | DAX / SB Arch | Open | |
| C2 [ARCH] | Is the 1–5 min timing gap between availability check and reservation creation materially impacting business outcomes? Is soft reservation near-term or longer-term? | Bryant / Ops | Open | **Tech Sync 2026-03-20:** SUR has **no** soft allocation today; fudge factor; cancel metrics — **Raghu** to pull data; follow-up session scheduled. |
| C3 | Should soft reservations apply to all providers or only select ones? | DAX / SB Arch | Open | |
| C4 [ARCH] | Expiration model for soft reservations: auto-expire after X minutes or confirmed by store acknowledgment? | DAX Arch | Open | |
| C5 [ARCH] | How do we prevent double-deduction when soft reservation is followed by store reservation event? | DAX Arch | Open | |
| C6 [ARCH] | UBIF Legacy reservation: return "not-reservable" response, or ServiceBench always reserves + DAX overrides backend? | DAX / SB | Open | |
| D1 [ARCH] | Should availability API return in-stock status and JIT eligibility as separate flags per part line? | DAX Arch | Open | |
| D2 | Should shipping days out be included in the availability API response (for Horizon/SB appointment scheduling)? | DAX Arch | **Resolved** | **EA Support (2) + Part Rel Mgmt 2026-03-19/20:** DAX availability API will include lead times. Specific values: batteries = 7 days, non-batteries = 3 days (configurable by SCM). F&O product master already has lead-time concepts that can be leveraged. |
| D3 | Should job-type exclusion info be evaluated before the availability check or returned in the response? | DAX Arch | **Resolved** | **Tech Sync 2026-03-20:** **Returned in response** (post-filter); SB adjudicates. |
| D4 [ARCH] | Should reservation and JIT order creation be a single combined API call or separate calls? | DAX Arch | Open | |
| D5 | Who maintains the "quantity one" records (distro/WLI JIT) in ServiceBench? Kelly Shaw or Pat Clark? | Kelly Shaw / Pat Clark | Open | |
| D6 | On-demand ordering for non-AOP providers: confirmed in scope? | Planning / Michelle | Open | |
| E1 [ARCH] | Warehouse identifier format for 3rd party providers in DAX IVS — standardization needed to match UBIF JSON format. | DAX / SB Eng | Open | |
| E2 | Same UBIF store has same SB ID for ISP and SUR. What routing logic distinguishes them? | DAX / SB Eng | **Resolved** | **Tech Sync 2026-03-20:** **LOB** — repair (SUR) vs replace (ISP); WLI vs WCF; Hawaii example. SB passes ID; **internal DAX PBI** for UBIF vs America's IVS routing. |
| F1 | What ServiceBench part setup fields must be replicated in DAX/F&O? Full field table (name, definition, options, mandatory/optional) required before migration. | Raghu / SCM | Open | |
| F2 | MDM setup process in DAX: manual (import or UI) or automated? Who owns MDM setup in future state? | MDM Team | Open | |
| F3 | Is the "magic tool" (single-touch SKU creation across DAX, ServiceBench, UBIF Portal) still viable from the Kaizen event? Who owns it? | MDM / SCM / Ops | Open | |
| G1 [ARCH] | DAX MFE in Prism Elite (TypeScript React) vs WMA for 3rd party AOP rollout — which path? | DAX / Prism | Open | WMA Phase 1 confirmed for AOP back-of-house (DDD). **Web-based WMA ruled out 2026-03-18** — certification burden, performance, user management complexity. ISP picking/return to be first-class in UBIF Next Gen Portal (separate track). New open: do AOP 3rd party locations need WMA UI or only API? (H15) |
| G2 [ARCH] | Identity for 3rd party AOP providers in Prism Elite: Hydra guest accounts? Email structure TBD. | Sandeep / Corey Street | Open | High turnover + multiple workers/location confirmed 2026-03-18. Alternative: dollar sign users or non-Asurion tenant users. Prereq: confirm Prism UI access (H16) + determine # users + identify 3rd party manager (equivalent to Renee for CA / Alex for MX). |
| H1 | ServiceBench local price copy for 3rd party claims — in scope for this project? | Bryant Mayne | Open | |
| H3 | EA assignment: is Ankit / Tim Clemens formally on the project? | Bryant / Leadership | **Resolved** | Ankit confirmed engaged (attended 2026-03-18 EA Support session, formally reviewing proposal). Tim Clemens co-owner. Bryant scheduling architecture review for week of 2026-03-24. |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose — who owns requirements and config in DAX? | SCM / MDM | Open | |
| H5 | Scalability implications for IVS soft reservations at UBIF scale (~800 locations)? | DAX Arch | Open | |
| H6 | UBIF Legacy scope: do we need to solution for Legacy UBIF given full migration to Next Gen by Q3? Temporary bridge only or full parity? ADO Feature 677454 may be out of scope. | Bryant / Michelle Bowersox | Open | |
| H7 | EP-2 scope: is "Part price on Job/Claim" a standalone epic or covered under UBIF Next Gen orchestration (ADO 677038)? Confirm before grooming. | Michelle Bowersox | Open | |
| H8 | EP-4 scope: is "Soft reservations via IVS" in scope for this project or a separate enhancement initiative? Confirm before grooming. | Michelle Bowersox | Open | **Reconciled with OQ:** If EP-4 is in scope, engineering blockers are **C1, C4, C5** only. **I2 resolved** — does not block EP-4. If EP-4 is out of scope, remove EP4 stories from TRD. |
| H9 | AgioTech / TechPeople (NAOP) — confirmed in scope? Same Tyk API contract? | Bryant / Amir | Open | |
| H10 | EU vendors (AsurionEU / Tesco / VirginMobile) — in scope? Same RTI → Tyk repoint pattern? | Bryant / Leadership | Open | |
| H12 | US NEW client group (ATTRepair / Verizon) — scope and timeline? | Bryant | Open | |
| H14 | Order types in scope: Replenishment (auto), Restock (manual), SURJIT (auto) — confirmed in scope alongside On-demand (D6)? | Bryant / Michelle Bowersox | Open | |
| H15 | Do 3rd party AOP locations need WMA inventory management UI, or only systematic API integration (no UI)? | Bryant / Avengers | Open | Per 2026-03-18 WMA meeting: 9 US AOP stores use SB mobile app today (not Field App). If WMA UI needed, EP5-S2 stays as-is. If API-only, EP5-S2 scope changes. Thays: gather work instructions from 3rd party providers on current inventory processes. |
| H16 | Will 3rd party AOP locations have Prism UI access? | Bryant / SB Team | Open | Action item 2026-03-18 WMA meeting: clarify with ServiceBench/Prism team. Impacts G2 (identity design) and EP5-S3 (Hydra identity story). Must answer before identity model can be designed. |
| I1 [ARCH] | BOM Lookup architecture: embed BOM lookup inside EIAA (single call) — OR — separate BOM service that ServiceBench calls first? Shown as "PRISM BOM?" open question in architecture diagram. | Ankit / DAPI Team / Integration Team | Open | **EA Support (2) + Tech Sync 2026-03-20:** DAX owns returning parts list; **God API vs split** still finalized **Wed** API contract session; **Michelle** line-by-line doc (MA-style). **Formal [ARCH] clearance** when contract agreed. |
| I2 | AOP JIT reservation: is a reservation required when inventory availability is false for AOP JIT scenarios? | Avengers / DAX Arch | **Resolved** | **Part Rel Mgmt 2026-03-19:** No reservation needed for out-of-stock JIT-enabled parts. Aligns with DDD open item 33 direction. EP4-S1 and EP5-S1 blocker on I2 cleared. |
| I3 [ARCH] | Part Substitution Matrix: reuse existing Replacement Matrix (modified) — OR — build new F&O menu/form/table/data entity? | Avengers / Robbie Carter / Rose | Open | **Part Rel Mgmt 2026-03-19:** Explored reuse with market-level defaults + client-level exceptions. Matt action item: create mock-up to verify. New entity remains fallback. |
| J1 [ARCH] | Product 360 / Product Intelligence team (Julian Bankston) building device catalog expanding to phones — potential overlap with DAX part master. Boundary must be defined. | Bryant / Ankit / Mika | Open | **EA Support (2) 2026-03-20:** Won't stall SSOT. Bryant to schedule boundary discussion with Mika, Mark Zoukas, Julian's team. |
| J2 | Remote Tech 3rd party identity: 9 companies, ~100 locations, ~500+ techs, ~6,000 OSR jobs/month. Future-state authentication approach? | Sandeep / Suman | Open | **Part Rel Mgmt 2026-03-19:** Landscape confirmed. Follow-up with Sandeep/Suman scheduled. Separate from AOP identity (G2/H16). |
| J3 | Mexico/RTI routing: can Mexico vendors move directly to FSG, or must RTI route through FSG to DAX? | SB Eng / Mexico rel. | Open | **Part Rel Mgmt 2026-03-19:** Action item to SB team. No decision yet. See also B4. |
| — | Microsoft IVS for UBIF inventory | — | **Closed** | Not in scope. |

Full question detail, source references, and answer history: [01-discovery/open-questions.md](../01-discovery/open-questions.md).

---

## 13. Appendix

**References:** (PRD) Inventory Single Source of Truth for SUR · APC-2299 Project Brief · Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) · SURInventory workflow · PROJECT-CONTEXT.md · TRD: [01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md](PRD-Technical-Development-Requirements-SSOT-SUR.md)

**Risks:** Q1 at risk; TELUS Plan B is a technology concession for one client; AOP UI path (MFE vs WMA) must be decided before grooming; **`[ARCH]` count reduced** after Tech Sync 2026-03-20 (A1, A4, D3, E2, D2 resolved in OQ; **I1** pending API contract); **Job Type / Eligibility 2026-03-23** reinforced DAX-as-source for exclusions and SB-as-adjudicator — **A5** must close with Michelle’s line-by-line contract work; Product 360 overlap (J1); Remote Tech (J2); **soft reservation** (C1/C4/C5) needs dedicated session (**C2** partial). **Architecture direction:** Horizon → SB → DAX; combined BOM + availability ("God API") still **pending formal contract** (I1).

---

*Questions tagged `[ARCH]` in open-questions.md block FR finalization. Resolve before grooming.*
