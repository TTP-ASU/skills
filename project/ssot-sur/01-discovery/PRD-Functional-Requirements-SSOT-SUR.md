# PRD: Functional Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Product owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Last updated:** 2026-03-27 (**WMA–SB Cycle Count Tool Gap Analysis** linked in §6 and §13 — pre-meeting analysis for Q3 WMA/user-flow review; **PRD health / OQ review prep** · **§12 D4 reconciled** to Resolved (matches open-questions + 2026-03-26 decision) · Prior: **SUR SSOT Strategy Discussion 2026-03-26**: Distro Migration to D365 F&O ERP added as §6 dependency; repair funnel risk L1 + SUR volume decline L2 opened; 3rd party AOP shrink context captured · **Deep dive BOM/Availability API contracts 2026-03-25**: I4 opened — Prism peril-change sub-question 1A vs 1B; B5 opened — NAOP feed frequency; C3 NAOP reservation note added · **Stale [ARCH] tags cleared**: D1 removed from FR-1/FR-8; G1 removed from FR-5; D4 removed from RT-6 flow and Q2 roadmap row · **HLE Discussion 2026-03-25**: dev sizing confirmed — Part Availability API = 2 sprints, Reservation API = 1–2 sprints, Sub Matrix UI = 1 sprint + API = 1 sprint, JIT Config = 1 sprint; flip-and-fold dual-BAT edge case identified; reservation must support multi-part requests with individual IDs; ~3 min cancellation queue latency; composite + granular API decision · **BOM/Availability API Contract Workshop 2026-03-25**: combined API design confirmed; PRISM location IDs = existing SB numeric values · **3rd Party AOP walkthrough 2026-03-24**: 103 AOP locations confirmed; ~500 total SB locations across 9 companies (updated from ~400); 100–200 users; 6,000 jobs/month · **Replenishments/MIN-MAX 2026-03-24**: AOP min-max and JIT flag requirements for D365 captured · Tech Sync 2026-03-20 · EA Support (2) 2026-03-20 · Job Type / Eligibility Logic 2026-03-23 · Roadmap alignment with Michelle/Matt 2026-03-23: Q1 = Part Price (F-1), Q2 = Availability+BOM+Soft Reservations, Q3 = AOP, Q4 = NAOP)  
**Status:** Draft  
**Related brief:** [Product Brief SUR SSOT](https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b)  
**Related TRD:** [TRD — Technical Requirements SUR SSOT](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f)  
**Synced with TRD:** 2026-03-27

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
- AOP full inventory lifecycle in D365 (9 providers, ~100 locations): orders, transfers, receiving, RMA, cycle count _(WMA vs ServiceBench cycle-count UX gap analysis — [WMA–SB Cycle Count Tool Gap Analysis](https://www.notion.so/asurionproduct/WMA-SB-Cycle-Count-Tool-Gap-Analysis-32f9532a1f868024b736fa8dfabf21ea) — informs Q3 planning; meetings week of 2026-03-31)_
- JIT availability flag and shipping days out per part line; JIT order creation logic
- IVS soft reservations at lead placement (UBIF scale)
- BOM + OEM SKU setup; substitution matrix migration to DAX
- Phased rollout framework with per-location feature flags and 30-day rollback
- AgioTech / TechPeople NAOP integration _(pending confirmation — H9)_
- On-demand ordering for 3rd party providers _(pending confirmation — D6)_

**Out of scope (confirmed):**
- **Peril to Part Type Configuration** (e.g., CrackedFrontGlass → FrontGlass) — remains in Prism/ServiceBench; not migrating to D365 (DDD-SUR architecture confirmed). Any "repair eligibility/decision impacting" business logic on part data stays exclusively in Prism.
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
| Distro Migration to D365 F&O ERP | Bryant / UBIF Operations | **Distro Migration to D365 F&O ERP is a separate program scheduled for next year (2027).** This migration improves Distro traceability, visibility, and standardization across the enterprise. SSOT and Distro Migration are co-dependencies — both programs need to deliver for full inventory ecosystem benefit. Strategy Discussion 2026-03-26. |
| **WMA–SB Cycle Count Tool Gap Analysis** (Notion) | PM / Avengers / BeyondX | **[WMA–SB Cycle Count Tool Gap Analysis](https://www.notion.so/asurionproduct/WMA-SB-Cycle-Count-Tool-Gap-Analysis-32f9532a1f868024b736fa8dfabf21ea)** — analysis ahead of meetings (target: week of 2026-03-31) to review user flows and functionality gaps between WMA and ServiceBench for cycle count and related inventory tasks. **Not a committed scope cut** until sessions conclude; **informs Q3 F-5 / WMA** planning and any supplemental stories. |

---

## 7. Product Requirements and Functional Requirements

> Items in the **Open Qs** column reference `01-discovery/open-questions.md`. `[ARCH]` items are blockers — resolve before grooming. **Who needs this** anchors each requirement to the primary persona(s) from `01-discovery/personas.md`. Each FR maps to technical implementation in the TRD (see TRD §10 Engineering Backlog and §12 FR Coverage Audit).

### Availability & Reservation API · F-2

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-1 | **Single availability and reservation API** | As a **ServiceBench consumer** (P2, P7), I need one real-time endpoint per part line so I get accurate availability without replication lag. | One endpoint (DES/ISP pattern) for all SUR inventory availability and reservations. **Combined BOM + Substitution Matrix + Job Type Exclusions + Product Equipment Type API confirmed (2026-03-25 architecture workshop).** Input: `client`, `region`, `lob`, `deviceSku` (enrolled device — not a part SKU), `serviceBenchLocationIdentifiers` (existing SB numeric IDs / PRISM location numbers), `partTypes` (e.g., LCM, BAT — Prism maps peril → part type). Logic: no "best part / best location" business logic; return all requested locations and all potential parts per BOM + Substitution Matrix, filtered by part type only. Output per part per location: `prismLocationId`, `asurionPartSku`, `productEquipmentType`, `qty`, `priority` (substitution matrix rank — all priorities returned, no filtering), `allowJustInTime`, `leadTimeInDays`, `jobTypeExclusions` (array, e.g., `RemoteTech`, `CarryInStore`). Each substitute part carries its own exclusion record. DAX provides data; Prism adjudicates repair correctness and offer logic. Reservation ID returned in orders to UBIF and DAX. Supports AOP and NAOP part lines. Audit trail via transaction logging (Job Type / Eligibility 2026-03-23). **Note — schema evolution:** current deployed API (`/v1/orcas/inventory/availability`, QA L7 endpoint) takes `skus` (SB part SKUs) + `locations` as input and returns `instock` + `allowJIT` per SKU/location. The confirmed 2026-03-25 design replaces `skus` input with `deviceSku` (enrolled device) and enriches the response with `priority`, `productEquipmentType`, `leadTimeInDays`, `jobTypeExclusions` — a significant schema evolution. Foundation DDD features: F.3 (BOM lookup filtered by part type), F.5 (substitution priority logic), F.6 (core orchestration layer), F.7 (consolidated response), F.8 (AOP/NAOP use cases). **Flip-and-fold device edge case (2026-03-25):** Devices like flip and fold phones require two batteries (primary + secondary); both are tagged as `BAT` part type but are not separately identified in the BOM. API must handle returning multiple parts of the same part type for a single device. **API granularity (HLE 2026-03-25):** Both a composite API (BOM + substitution + availability in one call) and granular APIs (separate calls) will be offered — composite for consumer convenience; granular for flexibility and performance optimization. | A2 [ARCH], A5 | F-2 (US-2.1, US-2.4) |
| FR-2 | **UBIF orchestration API** | As a **UBIF store technician** (P2), I need real-time orchestration to UBIF so distro availability is in the same response as inventory availability. | Real-time orchestration for UBIF availability and quantity; Distro Vendor indicator returned in same response. Deprecates inventory, distro, and price replication feeds from UBIF to ServiceBench. **Q2 scope: UBIF Next-Gen only** — UBIF Legacy is not in scope (H6 resolved 2026-03-25; Legacy stores in run-off migrating to Next Gen). **ISP vs SUR** for the same ServiceBench store ID: **line of business** partitions repair (SUR → WLI) vs replace (ISP → WCF); internal **UBIF IVS vs America's IVS** routing is a DAX-side PBI (Tech Sync 2026-03-20). | — | F-2 (US-2.2, US-2.3) |
| FR-6 | **UBIF Next Gen orchestration** | As a **UBIF Next Gen store** (P2), I need the JSON replication feed replaced by real-time orchestration so I'm never working from stale data. | Replace UBIF→ServiceBench JSON feed with real-time DAX orchestration. Include Distro Part Availability in same API. Deprecate all three replication datasets (availability, distro catalog, part price) from UBIF to ServiceBench. | — | F-2 (US-2.1, US-2.2) |
| FR-8 | **JIT — availability API and configuration** | As an **operations dispatcher** (P6), I need JIT eligibility and shipping days out returned per part line so technicians can set customer expectations at booking. | Shipping days out returned per part line in availability response. **Job-type exclusions:** SKU-level in DAX; **excluded** job types in availability response; SB decides what to offer (A4 resolved; Job Type / Eligibility 2026-03-23). JIT flag set at part/SKU level; returned per part line and included at line level in sales order. **If one or more parts in the job require JIT, the entire job is treated as a JIT job (confirmed 2026-03-25).** JIT availability = part is orderable but not immediately in stock at the location. No inventory decrement at warehouse for JIT orders. Transfer order created for JIT items on the sales order. **JIT auto-transfer order scope (DDD Feature 11.5):** When SB sends a JIT flag on a fulfillment order line, a transfer order is automatically created from WLI to the service provider. This feature is **scoped for AOP providers using real inventory SKUs only** — not applicable to NAOP orders that use service parts. Reservation API will not throw HTTP error for JIT items but will indicate whether reservation succeeded; Prism confirmed it will only call reservation API for parts that need to be reserved. JIT eligibility driven by distro "quantity one" record at SKU level; master account controls binary JIT on/off across entire Asurion network (confirmed 2026-03-24 Replenishments session). Client-level controls exist separately (Robbie/supply chain). **Reservation and JIT order creation: separate APIs (D4 resolved 2026-03-26)** — Reservation API is a separate writable call from the availability read; JIT order creation is a separate mechanism. US clients only; OSR and CSS. | A5, D5 | F-2 (US-2.1, US-2.5, US-2.6) |

### Part Price on Job/Claim · F-1

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-3 | **Part price on Job/Claim** | As a **claims/finance user** (P4), I need transactional partner invoice price on every Job/Claim so Franchise Co. reconciliation is accurate. | Partner invoice price set transactionally on Job/Claim in ServiceBench. Both UBIF Current State and Next Gen support this; price replication from UBIF deprecated for UBIF claims. **UBIF scope only** — 3rd party price scope moved to FR-12 under F-5. No architecture blockers — **unblocked for Q1.** | — | F-1 (US-1.1, US-1.2) |

### NAOP Migration · F-6

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-4 | **NAOP migration — Mobile Clinic and Mexico** | As a **NAOP vendor** (P3) and **store technician** (P2), I need NAOP inventory feeds moved off RTI Webservice to the standardized DAX IVS API so all vendors are on one integration pattern. | Repoint inventory feeds from RTI Webservice to DAX IVS API (AWS/JSON). Plan A: TELUS/Mobile Clinic provides full inventory for all perils (preferred). Plan B: LCM-only feed + peril+client bypass flag for non-LCM perils (fallback; fake SKUs ruled out). Mexico same pattern; SB team takes over web service. **NAOP job types (per Parts Management Flows):** Mobile Klinik (Canada) = **Depot, Carry-In only** (no Remote Tech); Mexico = **Depot, Carry-In only** (no Remote Tech). NAOP inventory data is needed only for these job types. **SB team handles Tyk/FSG migration** for both Canada and Mexico — routes data to DAX API for IVS ingestion (DDD-SUR architecture). **Deferred to Q4** — TELUS Plan A/B decision (B1/B2) and Mexico routing (B4/J3) require dedicated EA + TELUS sessions. | B1 [ARCH], B2 [ARCH], B3, B4, C6 [ARCH], C7, K2 | F-6 (US-6.1, US-6.2, US-6.3, US-6.4) |

### Soft Reservations via IVS · F-4

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-10 | **Soft reservations via IVS** | As a **Horizon consumer** (P7), I need inventory held at lead placement so the part I'm booking is still available when the store confirms — eliminating post-booking failures. | IVS creates soft reservation at lead placement; decrements available inventory immediately to close 1–5 min gap. Reconciles with store-created final reservation to prevent double deduction. Expiration model (auto-expire vs store acknowledgment) TBD. Applies to select providers only. **Scope confirmation pending (H8)** — if confirmed, blockers are C1, C4, C5 only (I2 resolved). **Multi-part support (HLE 2026-03-25):** Reservation API must support multiple parts in a single request and return an individual reservation ID per part (not a single reservation for the whole job). **Cancellation queue latency (HLE 2026-03-25):** ~3 minutes for reservation to be released after job cancellation (SNS message flow); team consensus is to prioritize inventory integrity over immediate re-availability. **Job reassignment (HLE 2026-03-25):** When a job is reassigned to a different location, the sales order remains as-is — no cancellation triggered by reassignment. | C1 [ARCH], C2, C3, C4 [ARCH], C5 [ARCH] | F-4 (US-4.1, US-4.2, US-4.3) |

### AOP Migration · F-5

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-5 | **AOP migration — 3rd party Asurion-owned parts** | As an **AOP provider** (P1), I need all inventory lifecycle functions (orders, transfers, receiving, RMA, cycle counts) to move from ServiceBench to DAX/D365 so I have one system when SB is decommissioned. | Migrate full inventory lifecycle from ServiceBench to DAX/D365. **Scope confirmed (2026-03-24 sessions):** 9 companies, **103 Asurion Network AOP remote tech locations** (~500 total ServiceBench locations across all 9 companies — updated from prior estimate of ~400), **100–200 users** total, ~6,000 repair jobs/month. UI via **native WMA app (Phase 1 — web-based WMA ruled out 2026-03-18)**; 3rd party providers access WMA via link in Prism. ISP picking/return screens will be first-class in UBIF Next Gen Portal (separate track). **Replenishment / MIN-MAX requirements (confirmed 2026-03-24):** Min-max set at individual SKU level for each location; monthly bulk refresh (mass import + single SKU update) + weekly adjustments to maintain 95% parts availability KPI; scheduled release on Mon/Wed/Fri at 3am ET (configurable for holidays); min-max reads off available quantity (not on-hand); auto-replenishment when available qty drops below minimum threshold — follows DES model. **JIT flag management:** binary on/off at SKU level for entire Asurion network via master account; client-level controls separate (Robbie/supply chain); bulk import capability required for mass JIT flag changes. SUR substitution matrix is effectively one-to-one (no cross-model part substitution possible — each SKU managed independently for min-max). Receiving, cycle counts, on-demand ordering, DOA returns also migrate. Whether 3rd party AOP locations need WMA UI or only systematic API integration: TBD (H15). Whether they will have Prism UI access: TBD (H16). **Identity direction (DDD-SUR + Feature 31.5):** Access controlled via D365 F&O with Azure Identity management; AOP 3rd party workers **guested into Azure tenant** (Entra/Azure AD guest accounts). DDD architecture: "Requires guesting of ServiceBench user into Azure tenant." Feature 31.5 (Avengers): identity guesting + F&O user/worker setup for AOP 3rd party workers. G2 [ARCH] near resolution — see OQ. User provisioning: Plus 1 file import currently provides technician SB logins on Asurion certification — future D365 access model TBD; potential to leverage Plus One certification process as trigger point. **Warehouse setup (HLE 2026-03-25):** each technician location is treated as a separate warehouse in D365; service providers can add technician users at any time without Asurion notification — a process must be defined to trigger warehouse creation when new users are onboarded. **Legal/access constraint (HLE 2026-03-25):** ISP providers currently cannot access DAX UI due to data visibility concerns (seeing too much Asurion data); the same risk applies to AOP 3rd party providers — WMA gap analysis required to confirm whether the WMA tool can expose the necessary inventory fields without exposing excess data. **⚠️ Company count discrepancy:** 3rd Party AOP session (2026-03-24) confirmed 9 companies; HLE session (2026-03-25) noted 8 companies — verify and align before design begins. | G2 [ARCH], H15, H16, H17 | F-5 (US-5.1, US-5.2, US-5.3, US-5.4) |

| FR-12 | **3rd party price on Job/Claim** | As a **claims/finance user** (P4) and **AOP provider** (P1), I need part price set consistently on Job/Claim for 3rd party providers so reimbursement and reconciliation are accurate outside the UBIF channel. | Scope TBD pending H1 resolution. AOP providers currently use zero / consigned part pricing. NAOP (Mobile Klinik, Mexico) pricing model requires separate investigation: Mobile Klinik — SKU-level price management TBD; Mexico — pricing in consumption messages TBD (possibly BAU). Decision required before any dev work begins. | H1 | F-5 (US-1.3) |

### BOM / MDM / Substitution Matrix · F-3

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-9 | **BOM and substitution matrix** | As an **MDM operator** (P5) and **store technician** (P2), I need BOM to return both Asurion and OEM SKUs and substitution rules to live in DAX so there's no manual multi-system replication. | BOM returns both Asurion and OEM SKUs for 3rd party providers (validated in production Canada NAOP job). OEM equipment type must be confirmed for pricing/charging logic. Substitution matrix owned by MDM/Tomlin; coordination with Robbie Carter, Rose. Each substitute part carries its own job-type exclusion record in the API response (Job Type / Eligibility 2026-03-23). | A3, H4 | F-3 (US-3.1, US-3.2, US-3.3) |
| FR-11 | **SKU / MDM setup migration** | As an **MDM operator** (P5), I need a single DAX setup to replace manual ServiceBench replication so every BOM update isn't a two-system swivel-chair task. | ServiceBench part setup deprecated (precedent: DES/NDS). MDM owns single setup in DAX. Full ServiceBench field documentation (definition, options, mandatory/optional) required before migration to avoid breaking existing functionality. | F1, F2 | F-3 (US-3.1), F-5 (US-5.4) |

### Phased Rollout & Rollback · F-7

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-7 | **Phased rollout and rollback** | As a **program manager** (all personas), I need each migration phase to be independently deployable per location/provider so we can roll back without affecting other phases. | **Rollout phases:** (1) Q1 — Part Price; (2) Q2 — API build and validation only; (3) Q3 — UBIF Next Gen store enablement + AOP migration; (4) Q4 — NAOP migration. **Q2 = build phase only** — no stores switch to DAX orchestration during Q2. UBIF Next Gen store enablement can only begin once Q2 deliverables are complete. **Q3 = store enablement phase** — Next Gen stores flip to DAX orchestration via per-store feature flag as enablement progresses; replication feeds remain live as rollback path until the last store is confirmed migrated (feeds are not deprecated at API go-live). **Rollback granularity:** per-store for UBIF (revert feature flag → replication feed); per-provider for AOP (revert to ServiceBench; SB must remain live until last AOP provider migrates); per-vendor for NAOP (RTI Webservice stays live until all vendors confirmed). **Rollback window:** 30 days from each store/provider/vendor cutover date. **Exit criteria per phase:** UBIF — replication feed traffic = 0; AOP — last AOP provider lifecycle confirmed in D365; NAOP — RTI Webservice traffic = 0. On-demand ordering for 3rd party providers: scope confirmation pending (D6). | D6 | F-7 (US-7.1, US-7.2) |

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
| UBIF Legacy availability | RT-2 | ServiceBench receives events + APIs. Three replicated datasets: availability, distro catalog, part price. | **Not part of Q2 build.** Legacy stores continue on existing replication feeds until they migrate to Next-Gen. No new investment in Legacy IVS integration for Q2. In the event Next-Gen migration is not 100% (**Assumption B**), a **Plan B** for addressing Legacy store jobs in DAX is TBD — last priority for the team. C6 [ARCH] (Legacy reservation pattern) deferred pending Plan B confirmation. | — | — |
| NAOP availability (Canada / Mexico) | RT-3 | RTI Webservice → ServiceBench. LCM-only feed; non-LCM perils have no BOM or availability check. **Job types served: Depot, Carry-In only — no Remote Tech for NAOP (per Parts Management Flows 2A/2B).** | ServiceBench → EIAA → Tyk API Connect → vendor feed. Plan A: full inventory all perils. Plan B: LCM-only + bypass flag. RTI deprecated. **SB team handles Tyk/FSG migration**; routes data to DAX API for IVS ingestion (DDD-SUR). Canada: Mobile Klinik moving to new CRM — opportunity to shift from RTI to Tyk → FSG. Mexico: 4 vendors; some open to change, others lack capacity. **Deferred to Q4.** | TELUS unwilling to provide full inventory; Canada/Mexico = Depot/Carry-In only (not Remote Tech) — scopes what inventory data is needed. | B1 [ARCH], B2 [ARCH], B3, B4, K2 |
| BOM lookup at job creation | RT-4 | ServiceBench local BOM; Asurion SKUs only. Manual multi-system setup per BOM entry. | EIAA returns BOM + Substitution Matrix + Job Type Exclusions in a single combined call (I1 near-resolution — confirmed 2026-03-25; HLE sizing pending formal clearance). Asurion + OEM SKUs per part line. ServiceBench BOM deprecated. | Multiple manual touchpoints; OEM SKU type unconfirmed for pricing logic. | I1 [ARCH] (near-resolution), A3 |
| Soft reservation at lead placement | RT-5 | No soft reservation — 1–5 min gap between availability check and final reservation. | ServiceBench calls IVS reservation API at lead placement; IVS reconciles with store-created final reservation; prevents double-deduction. | Overcommitment window at booking; risk of inventory sold twice. | C1 [ARCH], C4 [ARCH], C5 [ARCH] |
| JIT availability + order | RT-6 | ServiceBench checks "quantity one" at distro + shipping days out from SKU config. No inventory decrement on JIT orders. | EIAA returns JIT flag + shipping days out per part line; job-type exclusions as **excluded** types in response. **Reservation + JIT order creation: separate APIs (D4 resolved 2026-03-26).** US only; OSR and CSS. | SKU-level exclusions in DAX (A4 resolved); API dimensions **A5**. | D5, A5 |

### Availability + reservation API comparison

| | Current state | Future state |
|-|---------------|--------------|
| **Trigger** | Horizon → ServiceBench checks local replicated data | Horizon → ServiceBench → EIAA (real-time orchestration) |
| **Availability data** | Stale UBIF replication (1–5 min) | Real-time via UBIF Next Gen / Americas Availability Service |
| **BOM lookup** | ServiceBench local; Asurion SKUs only | EIAA combined call — BOM + substitution matrix + job type exclusions in single response (I1 near-resolution; combined design confirmed 2026-03-25). Asurion + OEM SKUs per part line. |
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
| Q1 | FR-3 | Part price set transactionally on Job/Claim (UBIF Current State + Next Gen only); price replication deprecated for UBIF claims. No architecture blockers — F-1 ready to groom. |
| Q2 | FR-1, FR-2, FR-6, FR-8, FR-9, FR-10 _(pending H8)_ | DAX combined API built, validated, and production-ready — **UBIF Next-Gen only** (Legacy out of scope, H6 resolved). No stores switch to DAX orchestration during Q2 — store enablement is a Q3 activity gated on Q2 completion. JIT flag and shipping days out per part line. Job type exclusions returned per part per client. BOM/MDM single-touch setup in DAX; SB part setup deprecated. Soft reservations designed and ready at UBIF Next-Gen scale if F-4 confirmed in scope. |
| Q3 | FR-5, FR-12 | AOP inventory lifecycle in D365 (native WMA Phase 1); no SUR inventory in ServiceBench. $600k savings YTD YoY. FR-12: 3rd party price on Job/Claim (scope TBD — H1). |
| Q4 | FR-4 | 3rd party NAOP (TELUS + Mexico) migrated from RTI to DAX IVS. $250k savings milestone reached. |

## 11. Roadmap 2026

> Sequencing logic agreed with Michelle and Matt, 2026-03-23. Part price ships Q1 (no blockers); availability + BOM + soft reservations consolidate in Q2 alongside the UBIF Next Gen Portal cutover; AOP in Q3 once DAX/IVS infrastructure is fully proven; NAOP deferred to Q4 given TELUS architecture complexity. **Already delivered:** The DAX SSOT availability/reservation pattern is live for ISP/DES/NDES — SSOT-SUR extends this proven infrastructure.
>
> **Volume / scale context — channel mix (source: SCM, David Tomlin 2026-03-25; avg ATT + Verizon FY 2026):**
>
> | Channel | Avg % of SUR jobs | Phase benefited |
> |---------|-------------------|----------------|
> | UBIF In Store (Carry-in) | **~62%** | Q2 (Next-Gen stores) |
> | UBIF Remote Tech | **~34%** | Q2 (Next-Gen stores) |
> | 3rd Party Remote Tech | **~3.5%** | Q3 (AOP migration) |
> | Depot / Mail-in Repair | **~1%** | Phase TBD — see K1 |
> | NAOP Canada / Mexico | **TBD** | Q4 (NAOP migration) |
> | **Total (excl. NAOP)** | **~100%** | |
>
> **Q2 = API built and validated; end of Q2 = stores begin migrating to new inventory management.** Benefit realization in Q3 at the pace of store migration. Volume impact expressed as % of SUR jobs only — no absolute job counts used for roadmap sizing.
>
> **Roadmap volume assumptions — UBIF Next-Gen migration:**
>
> | | Description | % of SUR jobs benefited |
> |-|-------------|------------------------|
> | **Assumption A** (base case) | UBIF Next-Gen store enablement on DAX orchestration completes across all stores during Q3. | Full ~96% of SUR jobs (UBIF In-Store + UBIF Remote Tech) by Q3 end. |
> | **Assumption B** (gap scenario) | Not all stores are enabled by end of Q3. Enabled stores benefit; remaining stores stay on existing replication feeds (replication feeds not deprecated until last store is confirmed). **Plan B** for any Legacy-only jobs TBD (last priority). | % proportional to stores enabled; gap persists until Plan B confirmed. |
>
> Q2 build scope is **UBIF Next-Gen only under both assumptions. No stores are enabled during Q2 — enablement is a Q3 activity gated on Q2 completion.**
>

| Quarter | Epic | Milestone | Why this order | FRs | Key dependencies | Volume / Scale | Target |
|---------|------|-----------|---------------|-----|-----------------|----------------|--------|
| **Q1** | F-1 | **Part price on Job/Claim** | No architecture blockers; unblocked for immediate grooming. High financial impact (Franchise Co. reconciliation). Deliver first while [ARCH] blockers on F-2 continue to clear. | FR-3 | UBIF Current State + Next Gen API changes; SB Job/Claim model update | **~96% of SUR jobs** (all UBIF In-Store + UBIF Remote Tech claims — price applies across both Next-Gen and Current State). | Price replication deprecated; transactional price on all UBIF claims |
| **Q2** | F-2 | **DAX availability API + UBIF Next Gen orchestration + JIT** (ADO 677038 · 679502) | **Q2 = build and validation only.** API built and validated; no stores switch to DAX orchestration during Q2. Build scope is UBIF Next-Gen only — UBIF Legacy is not part of Q2 build (Plan B for Legacy jobs in DAX is TBD; last priority). JIT flag, shipping days out, job type exclusions per part per client returned in a single call. **UBIF Next Gen store enablement begins Q3**, gated on Q2 completion (see FR-7). | FR-1, FR-2, FR-6, FR-8 | I1 [ARCH] (near-resolution — combined API confirmed 2026-03-25; peril-change sub-question I4 open); A5 (job type nomenclature — Raghu/Amir action item); A2 [ARCH]; D1 resolved; D4 resolved; E2 resolved | **~96% of SUR jobs at full rollout** (UBIF In-Store/Carry-in ~62% + UBIF Remote Tech ~34%, avg ATT + Verizon FY 2026). Full ~96% under Assumption A (Q3 enablement complete). See Assumptions A/B. | API complete and validated end of Q2. **Store enablement begins Q3** (gated on Q2 delivery). Full UBIF benefit by Q3 end (Assumption A) or partial benefit at legacy pace (Assumption B). |
| **Q2** | F-3 | **BOM/MDM automation + substitution matrix** (ADO 679640) | Runs parallel to F-2; shares the same God API contract. Eliminates manual swivel-chair SKU setup. Substitution matrix: each substitute part carries own exclusion record in the response. | FR-9, FR-11 | F1 (Raghu's SB field table); I3 [ARCH] (substitution matrix — Matt mock-up); H4 (ownership — Robbie/Rose) | All SUR BOM SKUs. SUR substitution matrix is 1-to-1 today (confirmed 2026-03-24); new matrix adds priority hierarchy. **Active SKU count: TBD** | Single-touch SKU setup in DAX; SB part setup deprecated; OEM SKUs in BOM |
| **Q2** | F-4 _(pending H8)_ | **Soft reservations via IVS** | Closes the 1–5 min overcommit window at booking. Must be proven at UBIF scale before AOP adds reservation volume. Scope confirmation required before grooming. | FR-10 | C1, C4, C5 [ARCH]; H5 (scalability at ~800 stores); H8 (scope confirm — Bryant/Michelle) | **~96% of SUR jobs** if in scope (UBIF In-Store/Carry-in ~62% + UBIF Remote Tech ~34%); Next-Gen stores only at Q2 go-live | Zero overcommit incidents; soft reservation live at UBIF scale |
| **Q3** | F-5 | **AOP migration — 3rd party Asurion-owned parts** (ADO 677040) | Most complex: full inventory lifecycle, WMA Phase 1 UI, Hydra identity. Goes last so DAX/IVS infrastructure is fully proven. **Q3 runs two tracks in parallel:** (1) UBIF Next Gen store enablement (per-store, gated on Q2 delivery); (2) AOP provider migration to D365 (per-provider/company). | FR-5 | G1 [ARCH] (WMA Phase 1; H15 = UI vs API-only?); G2 [ARCH] (Hydra identity; H16 = Prism access?); F1/F2 (MDM migration) | **~3.5% of SUR jobs** (3rd Party Remote Tech channel, avg ATT + Verizon FY 2026). 103 AOP locations · 9 companies · Mon/Wed/Fri replenishment · 95% availability KPI. | AOP inventory in D365; replenishment + JIT flag in DAX; **$600k YTD YoY savings**; SB inventory lifecycle retired. UBIF Next Gen stores enabled on DAX orchestration throughout Q3 → full ~96% benefit by Q3 end (Assumption A) or partial benefit (Assumption B; see assumptions above). |
| **Q4** | F-6 | **NAOP migration — Mobile Clinic + Mexico** (ADO 677039) | Deferred from Q2: TELUS Plan A/B (B1/B2) and Mexico RTI routing (B4/J3) require dedicated EA + TELUS sessions not completing before Q3. | FR-4 | B1, B2 [ARCH] (TELUS Plan A/B); B3 (TELUS CRM timing); B4/J3 (Mexico RTI routing); E1 [ARCH] (warehouse ID format) | **NAOP volume TBD** (Canada/Mexico not represented in ATT/Verizon US channel mix slides). Depot / Mail-in ~1% of US SUR jobs — scope and phase TBD (see K1). Canada: TELUS/Mobile Klinik. Mexico: ATT MXO/Telcel + 4 vendors. | RTI deprecated; NAOP on DAX IVS pattern; **$250k YoY shrink reduction** |
| Cross-cutting | F-7 | **Phased rollout + rollback framework** (ADO 679641) | Applies to every phase | FR-7 | D6 (on-demand ordering scope) | All phases; per-location feature flag | Feature flag per location/provider; 30-day rollback for non-AOP |

> **Architecture decisions completed (2026-03-19–26):** A1 · A4 · D1 · D2 · D3 · D4 · E2 · I2 resolved. **H6 resolved 2026-03-25:** UBIF Legacy not part of Q2 build — Q2 is UBIF Next-Gen only; Plan B for Legacy jobs in DAX TBD (last priority); C6 [ARCH] deferred. **Remaining [ARCH] for Q2 F-2 grooming:** A2 · I1 (combined API — design confirmed 2026-03-25; formal sign-off / I4 peril-change sub-path still tracked). **A5** (Raghu/Amir job type nomenclature action item) to close. **Q1 F-1 is unblocked** — grooming can start immediately.
>
> **Volume source:** Channel mix % from SCM (David Tomlin 2026-03-25); simple average of ATT and Verizon FY 2026 4+8 Channel Mix slides. Note: Mail-in Repair = Depot = NAOP.

**Technical development details (epics, stories, ADO):** See [TRD — Technical Requirements SUR SSOT](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f) and `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`. This PRD is the stable functional alignment reference.

## 12. Open Questions

Full detail in **[01-discovery/open-questions.md](../01-discovery/open-questions.md)**. Items tagged `[ARCH]` are technical architecture blockers — listed here for PRD traceability, resolved via architecture working sessions (TRD-owned). Untagged items are PRD/business-owned.

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| A1 | Who owns peril-to-part-type translation for DAX calls? (Bypass for TELUS/non-LCM is **B1/B2**.) | Ankit / DAX Arch | **Resolved** | **Tech Sync 2026-03-20:** **ServiceBench** maps peril → part types (LCM, BAT, etc.); Cloud→Prism→DAX handoff for equipment type; DAX filters BOM by part type + job-type exclusion on part. No client on peril map. |
| A2 [ARCH] | Should "bypass inventory check" (when no inventory) be driven in DAX vs ServiceBench? **Peril mapping is not client-scoped** — see A1 answer. **TELUS path:** B1/B2. | Ankit / DAX Arch | Open | **Tech Sync 2026-03-20:** Narrowed — client not in peril row; confirm with **B1/B2** for TELUS. |
| A3 | OEM parts equipment type: what is the correct type for pricing/charging logic? Required before BOM can return OEM SKUs for 3rd party providers. | MDM / SCM | Open | |
| A4 | Job-type exclusions: SKU-level vs equipment-type in F&O? | Robbie Carter / DAX | **Resolved** | **Tech Sync 2026-03-20:** **SKU-level attribute in DAX**; existing form; MDM + **Robbie security** for on-the-fly changes; Michelle tracks in PBI. |
| A5 | Job type exclusion dimensions (client/market/model) + audit expectations for DAX config | DAX / Michelle / Robbie | Open | **Job Type / Eligibility 2026-03-23 confirmed:** Exclusions at **part + client (purchase from / client group)** level — no device model dimension. API lists **excluded** job types per part per client (e.g., "no CSS JIT", "no remote tech"). Each substitute part from the substitution matrix has its own exclusion record. **Audit trail:** transaction logging enabled for exclusion changes. **Client vs market** final dimension deferred to Wed API contract workshop. **BOM/Availability API Contract Workshop 2026-03-25:** `jobTypeExclusions` confirmed as array in response (e.g., `RemoteTech`, `CarryInStore`). Action item: Raghu/Amir to confirm exact job type nomenclature for SUR — two additional job types beyond the initial four reported by Amir still pending. Client vs market: client-level exclusions confirmed (e.g., Verizon carry-in excluded for specific LCM SKUs); market dimension still under discussion. |
| B1 [ARCH] | TELUS/Mobile Clinic: Plan A (full inventory for all perils) vs Plan B (LCM-only + bypass flag)? | Ankit / TELUS rel. | Open | |
| B2 [ARCH] | Should the bypass flag live in DAX's BOM response or in ServiceBench's client config? | DAX Arch | Open | |
| B3 | TELUS CRM migration timing — does it affect the preferred integration path? | Business / TELUS rel. | Open | |
| B4 | Mexico/Mobile Clinic feed: who takes over the RTI web service when it moves to AWS/JSON? | SB Eng / DAX | **Partially resolved** | **DDD-SUR architecture (2026-03-26):** "Any future Tyk/FSG migration where possible will be handled by the Service Bench team. And Service Bench Team will route the data to DAX API for inventory visibility service ingestion." **SB team owns the RTI → Tyk/FSG migration** for both Canada and Mexico vendors. Mexico: 4 vendors; some open to change, others lack capacity. Full routing decision (direct to FSG vs through FSG → DAX) still subject to B1/B2 and J3 architecture decisions. |
| C1 [ARCH] | Who owns the soft reservation lifecycle end-to-end? (SB initiates, store confirms, IVS manages state) | DAX / SB Arch | Open | |
| C2 [ARCH] | Is the 1–5 min timing gap between availability check and reservation creation materially impacting business outcomes? Is soft reservation near-term or longer-term? | Bryant / Ops | Open | **Tech Sync 2026-03-20:** SUR has **no** soft allocation today; fudge factor; cancel metrics — **Raghu** to pull data; follow-up session scheduled. |
| C3 | Should soft reservations apply to all providers or only select ones? | DAX / SB Arch | Open | |
| C4 [ARCH] | Expiration model for soft reservations: auto-expire after X minutes or confirmed by store acknowledgment? | DAX Arch | Open | |
| C5 [ARCH] | How do we prevent double-deduction when soft reservation is followed by store reservation event? | DAX Arch | Open | |
| C6 [ARCH] | UBIF Legacy reservation: return "not-reservable" response, or ServiceBench always reserves + DAX overrides backend? | DAX / SB | **Deferred** | **H6 resolved 2026-03-25** — UBIF Legacy is not part of Q2 build. C6 is deferred; will need resolution if/when Plan B for Legacy jobs in DAX is confirmed. |
| D1 [ARCH] | Should availability API return in-stock status and JIT eligibility as separate flags per part line? | DAX Arch | **Resolved** | **BOM/API Contract Workshop 2026-03-25:** Confirmed as **separate fields** — `qty` (quantity in stock) and `allowJustInTime` (boolean) are distinct response fields per part per location (see FR-1 confirmed output schema). |
| D2 | Should shipping days out be included in the availability API response (for Horizon/SB appointment scheduling)? | DAX Arch | **Resolved** | **EA Support (2) + Part Rel Mgmt 2026-03-19/20:** DAX availability API will include lead times. Specific values: batteries = 7 days, non-batteries = 3 days (configurable by SCM). F&O product master already has lead-time concepts that can be leveraged. |
| D3 | Should job-type exclusion info be evaluated before the availability check or returned in the response? | DAX Arch | **Resolved** | **Tech Sync 2026-03-20:** **Returned in response** (post-filter); SB adjudicates. |
| D4 | Should reservation and JIT order creation be a single combined API call or separate calls? | DAX Arch | **Resolved** | **2026-03-26:** **Separate APIs** — availability read-only; reservation writable; JIT order creation separate. Aligns with BOM/API workshop direction (Prism calls reservation only where needed). |
| D5 | Who maintains the "quantity one" records (distro/WLI JIT) in ServiceBench? Kelly Shaw or Pat Clark? | Kelly Shaw / Pat Clark | **Partially resolved** | **Replenishments/MIN-MAX session 2026-03-24:** For Asurion Network (AOP), **Taylor's team (TLC operations)** manages the binary JIT on/off at SKU level via a master account (single screen, binary toggle); Kelly Shaw involved. Client-level controls separate (Robbie/supply chain). Whether the same ownership applies to UBIF distro "quantity one" records is still TBD — confirm with Kelly Shaw. |
| D6 | On-demand ordering for non-AOP providers: confirmed in scope? | Planning / Michelle | Open | |
| E1 [ARCH] | Warehouse identifier format for 3rd party providers in DAX IVS — standardization needed to match UBIF JSON format. | DAX / SB Eng | Open | |
| E2 | Same UBIF store has same SB ID for ISP and SUR. What routing logic distinguishes them? | DAX / SB Eng | **Resolved** | **Tech Sync 2026-03-20:** **LOB** — repair (SUR) vs replace (ISP); WLI vs WCF; Hawaii example. SB passes ID; **internal DAX PBI** for UBIF vs America's IVS routing. **DDD Feature F.9 (additional detail, 2026-03-26):** Americas WLI has UBIF stores as external warehouses — must be **excluded** from Americas IVS lookups (zero inventory there). UBIF F&O only has UBIF store data. See K4 for outstanding mapping-rules exploration. |
| F1 | What ServiceBench part setup fields must be replicated in DAX/F&O? Full field table (name, definition, options, mandatory/optional) required before migration. | Raghu / SCM | Open | |
| F2 | MDM setup process in DAX: manual (import or UI) or automated? Who owns MDM setup in future state? | MDM Team | Open | |
| F3 | Is the "magic tool" (single-touch SKU creation across DAX, ServiceBench, UBIF Portal) still viable from the Kaizen event? Who owns it? | MDM / SCM / Ops | Open | |
| G1 [ARCH] | DAX MFE in Prism Elite (TypeScript React) vs WMA for 3rd party AOP rollout — which path? | DAX / Prism | **Resolved** | **DDD-SUR architecture (ingested 2026-03-26):** "Migrated to D365 F&O Warehouse Mobile Application; User Access controlled via D365 F&O with Azure Identity management." WMA confirmed. Feature 31.5 (Avengers): "Identity Guesting and F&O user/worker setup for AOP 3rd Party Workers." **Web-based WMA ruled out 2026-03-18**. ISP picking/return to be first-class in UBIF Next Gen Portal (separate track). Whether AOP locations need WMA UI or API-only: H15 (still open). [ARCH] tag cleared. |
| G2 [ARCH] | Identity for 3rd party AOP providers in Prism Elite: Hydra guest accounts? Email structure TBD. | Sandeep / Corey Street | **Near resolution** | **DDD-SUR architecture (2026-03-26):** "Requires guesting of ServiceBench user into Azure tenant." Direction = **Azure AD guest accounts** for AOP 3rd party workers in D365 F&O. Feature 31.5 (Avengers) confirms identity guesting + F&O user/worker setup. H15 (UI vs API-only) and H16 (Prism access) still needed before formal resolution. Identity design session with Sandeep/Corey Street required. |
| H1 | 3rd party price on Job/Claim — what pricing model applies to AOP and NAOP providers in the future state? (Scope now owned by **FR-12** under F-5; UBIF pricing resolved via FR-3.) | Bryant Mayne | Open | **Updated 2026-03-26:** Scope moved from FR-3 to FR-12 / F-5. UBIF pricing live and unblocked (US-1.1 Done, US-1.2 Active). AOP uses zero / consigned pricing today. Open items: (a) AOP — zero/consigned or transactional? (b) Mobile Klinik — SKU-level price management TBD; (c) Mexico — pricing in consumption messages TBD (possibly BAU). US-1.3 Draft; blocked pending this answer. |
| H3 | EA assignment: is Ankit / Tim Clemens formally on the project? | Bryant / Leadership | **Resolved** | Ankit confirmed engaged (attended 2026-03-18 EA Support session, formally reviewing proposal). Tim Clemens co-owner. Bryant scheduling architecture review for week of 2026-03-24. |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose — who owns requirements and config in DAX? | SCM / MDM | Open | |
| H5 | Scalability implications for IVS soft reservations at UBIF scale (~800 locations)? | DAX Arch | Open | |
| H6 | UBIF Legacy scope: do we need to solution for Legacy UBIF given full migration to Next Gen by Q3? Temporary bridge only or full parity? ADO Feature 677454 may be out of scope. | Bryant / Michelle Bowersox | **Resolved** | **2026-03-25:** UBIF Legacy is **not part of Q2 build scope**. Q2 F-2 is UBIF Next-Gen only. In the event Next-Gen migration is not 100% by end of Q2 (**Assumption B**), a **Plan B** for addressing Legacy store jobs in DAX is TBD — confirmed last priority for the team. ADO Feature 677454 not being built in Q2. C6 [ARCH] (Legacy reservation) deferred pending Plan B confirmation. Existing Legacy replication feeds remain in place until stores migrate. |
| H7 | F-1 scope: is "Part price on Job/Claim" a standalone feature or covered under UBIF Next Gen orchestration (ADO 677038)? Confirm before grooming. | Michelle Bowersox | **Resolved** | F-1 is a **standalone feature** (Q1, unblocked). Not covered under ADO 677038 (UBIF Next Gen orchestration). Confirmed in roadmap alignment with Michelle/Matt 2026-03-23. |
| H8 | F-4 scope: is "Soft reservations via IVS" in scope for this project or a separate enhancement initiative? Confirm before grooming. | Michelle Bowersox | Open | **Reconciled with OQ:** If F-4 is in scope, engineering blockers are **C1, C4, C5** only. **I2 resolved** — does not block F-4. If F-4 is out of scope, remove F-4 stories from TRD. |
| H9 | AgioTech / TechPeople (NAOP) — confirmed in scope? Same Tyk API contract? | Bryant / Amir | Open | |
| H10 | EU vendors (AsurionEU / Tesco / VirginMobile) — in scope? Same RTI → Tyk repoint pattern? | Bryant / Leadership | Open | |
| H12 | US NEW client group (ATTRepair / Verizon) — scope and timeline? | Bryant | Open | |
| H14 | Order types in scope: Replenishment (auto), Restock (manual), SURJIT (auto) — confirmed in scope alongside On-demand (D6)? | Bryant / Michelle Bowersox | **Partially resolved** | **SURInventory PDF (Raghu, 2026-03-26):** Four AOP order types confirmed: (1) Replenishment — auto; (2) Restock — manual; (3) On-demand — manual; (4) SURJIT — auto. DDD Feature 26 (BeyondX) confirms On-Demand Ordering is in scope. Formal scope commitment still needs Michelle/Bryant sign-off (see D6 for non-AOP providers). |
| H15 | Do 3rd party AOP locations need WMA inventory management UI, or only systematic API integration (no UI)? | Bryant / Avengers | Open | Per 2026-03-18 WMA meeting: 9 US AOP stores use SB mobile app today (not Field App). If WMA UI needed, US-5.2 stays as-is. If API-only, US-5.2 scope changes. Thays: gather work instructions from 3rd party providers on current inventory processes. |
| H16 | Will 3rd party AOP locations have Prism UI access? | Bryant / SB Team | Open | Action item 2026-03-18 WMA meeting: clarify with ServiceBench/Prism team. Impacts G2 (identity design) and US-5.3 (Hydra identity story). Must answer before identity model can be designed. |
| I1 [ARCH] | BOM Lookup architecture: embed BOM lookup inside EIAA (single call) — OR — separate BOM service that ServiceBench calls first? Shown as "PRISM BOM?" open question in architecture diagram. | Ankit / DAPI Team / Integration Team | Open | **EA Support (2) + Tech Sync 2026-03-20:** DAX owns returning parts list; God API vs split to be finalized at Wed API contract session. **BOM/Availability API Contract Workshop 2026-03-25:** Combined API design confirmed — BOM + Substitution Matrix Priority + Job Type Exclusions + Product Equipment Type returned in a single combined call. Input/output contract agreed (see FR-1 for full field spec). PRISM location IDs = existing SB numeric values. HLE T-shirt sizing session scheduled 2:00–4:00 PM 2026-03-25. Separate session to be scheduled for reverse-lookup substitution API (UBIF-specific). **Formal [ARCH] clearance** upon HLE completion and contract sign-off. |
| I2 | AOP JIT reservation: is a reservation required when inventory availability is false for AOP JIT scenarios? | Avengers / DAX Arch | **Resolved** | **Part Rel Mgmt 2026-03-19:** No reservation needed for out-of-stock JIT-enabled parts. Aligns with DDD open item 33 direction. US-4.1 and US-5.1 blocker on I2 cleared. |
| I3 [ARCH] | Part Substitution Matrix: reuse existing Replacement Matrix (modified) — OR — build new F&O menu/form/table/data entity? | Avengers / Robbie Carter / Rose | Open | **Part Rel Mgmt 2026-03-19:** Explored reuse with market-level defaults + client-level exceptions. Matt action item: create mock-up to verify. New entity remains fallback. **DDD Feature F.34 (Avengers, ADO 681046):** Formally listed as pending decision — three options: (1) Reuse Replacement Matrix (changes to unique indexes/validation); (2) New F&O Menu/Form/Table/Data Entity; (3) Live in BOM if client not required. **DDD Feature F.5:** Regardless of storage decision, substitution priority logic must be added to the central Availability API (expand BOM parts + substitutions with Priority indicator; no Best Version Filter needed). Matt mock-up still pending. |
| J1 [ARCH] | Product 360 / Product Intelligence team (Julian Bankston) building device catalog expanding to phones — potential overlap with DAX part master. Boundary must be defined. | Bryant / Ankit / Mika | Open | **EA Support (2) 2026-03-20:** Won't stall SSOT. Bryant to schedule boundary discussion with Mika, Mark Zoukas, Julian's team. |
| J2 | Remote Tech 3rd party identity: 9 companies, AOP remote tech locations, users, and volume. Future-state authentication approach? | Sandeep / Suman | Open | **Part Rel Mgmt 2026-03-19:** Landscape confirmed. Follow-up with Sandeep/Suman scheduled. Separate from AOP identity (G2/H16). **3rd Party AOP session 2026-03-24 (updated):** 9 companies · **103 Asurion Network AOP remote tech locations** · ~500 total ServiceBench locations across all 9 companies (updated from prior ~400 estimate) · **100–200 users** total · ~6,000 repair jobs/month. Admin can add SB users at any time; technicians onboarded via Plus 1 file import on Asurion Certification. User provisioning path for D365/WMA TBD — may not be a DAX development item. |
| J3 | Mexico/RTI routing: can Mexico vendors move directly to FSG, or must RTI route through FSG to DAX? | SB Eng / Mexico rel. | Open | **Part Rel Mgmt 2026-03-19:** Action item to SB team. No decision yet. See also B4. |
| K1 | Depot / Mail-in Repair (~1% of US SUR jobs per SCM channel mix, avg ATT + Verizon FY 2026): is this channel in scope for SSOT-SUR? If so, which phase/epic covers it? Is it part of NAOP (Q4 F-6), a separate US depot track, or out of scope? Note: this is a US channel — distinct from NAOP Canada/Mexico vendor volume which is TBD. | Bryant / Michelle Bowersox | Open | |
| — | Microsoft IVS for UBIF inventory | — | **Closed** | Not in scope. |
| K2 | NAOP job types — Mobile Klinik (Canada) and Mexico serve Depot/Carry-In only (no Remote Tech) per Parts Management Flows. Does this limit what inventory data is required from NAOP vendors? Does it affect job type exclusion logic for NAOP in FR-4 and RT-3? | Bryant / Amir / Raghu | Open | Source: Parts Management Flows PDF (Flow 2A: Mobile Klinik — "Depot, Carry-In; no Remote Tech"; Flow 2B: Mexico — same). Implication: NAOP inventory check only needed for Depot and Carry-In job types. Remote Tech jobs for Canada/Mexico clients use AOP/UBIF channels, not NAOP. |
| K3 | UBIF IVS instance for F&O is not currently enabled — Feature 13 (DDD Feature Breakdown): "Stand up and enable the UBIF IVS instance for F&O data source (currently not enabled)." What is the timeline and team ownership for enabling UBIF IVS? This is a Q2 technical prerequisite. | DAPI / Integration Team / Ankit | Open | Source: DDD Feature Breakdown F.13 (Configuration). Blocks core orchestration layer (Feature F.6) and UBIF Next-Gen availability (RT-1). |
| K4 | Americas IVS vs UBIF IVS routing/mapping rules — Feature F.9 (DDD Feature Breakdown): DAX API must determine which backend (UBIF IVS vs Americas IVS) for each ServiceBench location. Americas WLI has UBIF stores as external warehouses — must be excluded from Americas IVS lookups (zero inventory there). Feature F.23: technical exploration needed for consolidating mapping rules (Americas company/site/warehouse + UBIF store site/warehouse/company + UBIF Part SKU mapping from Asurion SKU). | DAPI / ETL Team | Open | Source: DDD Feature Breakdown F.9 and F.23. E2 partially covers LOB routing; this is the deeper warehouse/mapping layer. Blocks F.6 (core orchestration). |
| B5 | NAOP vendor inventory feed frequency: Mobile Klinik (Canada) and Mexico vendors push inventory feeds at varying cadences. What is the required frequency to maintain accuracy KPIs? | SB Eng / Integration Team | Open | Feed frequency alignment not yet defined. Establish minimum cadence during NAOP design sessions (Q4 planning). |
| I4 | **Prism peril-change scenario:** When UBIF calls Prism to add or change a peril, should Prism reuse the combined BOM+availability API (ignoring qty) — **Option 1A** — or call the existing BOM lookup separately — **Option 1B (formerly 2)**? | BeyondX / DAPI / Michelle Bowersox | Open | Discussed but not resolved 2026-03-25. Separate session to be scheduled. Does not block Q2 main API build but must resolve before SB peril-change flow is implemented. |
| L1 | **Repair funnel reporting broken:** Funnel reporting has been broken since Prism migration (Ross role eliminated). Who owns fixing it, and what is the risk to SSOT success metric tracking? | Bryant / Rebecca Suttler | Open | No active maintenance underway. Risk: SSOT benefit cannot be measured without a working baseline funnel report. |
| L2 | **SUR job volume decline:** SUR job volume has declined — possibly Prism-related (new status events, reconciliation issues). Root cause must be confirmed before SSOT baseline is set to avoid misattribution of results. | Bryant / Client team | Open | UBIF client team reviews only lagging P&L monthly. Recommended: establish top-of-funnel conversion rate tracking before SSOT baseline is set. |

Full question detail, source references, and answer history: [01-discovery/open-questions.md](../01-discovery/open-questions.md).

---

## 13. Appendix

**References:** (PRD) Inventory Single Source of Truth for SUR · APC-2299 Project Brief · Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) · SURInventory workflow · PROJECT-CONTEXT.md · TRD: [01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md](PRD-Technical-Development-Requirements-SSOT-SUR.md) · **[WMA–SB Cycle Count Tool Gap Analysis](https://www.notion.so/asurionproduct/WMA-SB-Cycle-Count-Tool-Gap-Analysis-32f9532a1f868024b736fa8dfabf21ea)** (Notion — Q3 planning input; user-flow / functionality gap review ahead of engineering)

**Risks:** Q1 at risk; TELUS Plan B is a technology concession for one client; **`[ARCH]` count further reduced** — G1 resolved (WMA confirmed, DDD-SUR 2026-03-26), D1 resolved, D4 resolved (separate APIs 2026-03-26), H6 resolved, G2 near-resolution (Azure AD guest direction confirmed). Remaining [ARCH] for Q2 grooming: **A2 · I1** (near-resolution — combined API confirmed 2026-03-25; peril-change sub-question I4 open). **A5** (job type nomenclature — Raghu/Amir action item); **K3** (UBIF IVS not currently enabled — Q2 technical prerequisite); **K4** (Americas/UBIF IVS routing/mapping exploration); **I3** (substitution matrix decision — Matt mock-up pending, ADO 681046). Product 360 overlap (J1); AOP identity (G2/H15/H16) needs dedicated session; **soft reservation** (C1/C4/C5) scope confirmation still needed (H8). **New risks (Strategy Discussion 2026-03-26):** Repair funnel reporting broken (L1 — Ross role eliminated; risk to baseline metric); SUR job volume decline (L2 — Prism migration-related?); Distro Migration to D365 F&O ERP is a co-dependency for full benefit realization. **Architecture direction:** Horizon → SB → DAX; combined BOM + availability API confirmed 2026-03-25 (I1 near-resolution; I4 peril-change sub-question open). DDD reference sources ingested 2026-03-26: DDD-SUR SSOT document, DDD Feature Breakdown (ADO refs 681046, 681055), DDD Orchestration Schema, Parts Management Flows, SURInventory workflow.

---

*Questions tagged `[ARCH]` in open-questions.md block FR finalization. Resolve before grooming.*
