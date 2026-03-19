# PRD: Functional Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Product owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Last updated:** 2026-03-18 (WMA ISP / 3rd Party meeting incorporated)  
**Status:** Draft  
**Related brief:** [Product Brief SUR SSOT](https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b)

---

## 1. Overview and goals

SUR SSOT extends Asurion's DAX platform inventory SSOT—proven for DSE/NDES with significant shrink reductions—to Same Unit Repair. **Goals:** (1) Single API for SUR inventory availability and reservations (DES/ISP pattern). (2) Replace UBIF→ServiceBench replication with real-time orchestration; part price on Job/Claim. (3) Migrate 3rd party NAOP and AOP to DAX IVS/D365. (4) Eliminate replication risks (inconsistency, latency, scalability). Aligns to Fulfillment 2026 Objective 2: unified fulfillment ecosystem with a single, accurate system of record for inventory.

**Success metrics:** $250k YoY shrink (Q2) · $600k YTD YoY (Q3) · All SUR inventory inquiries and AOP management in D365.

---

## 2. Stakeholders and RACI

> Six user groups benefit from this project: store/portal users (real-time availability + reservations), ServiceBench consumers (UBIF orchestration), claims/finance users (transactional part pricing), 3rd party NAOP providers (DAX IVS feeds), 3rd party AOP providers (full inventory lifecycle in D365), and operators (accurate JIT/appointment availability). Each is covered by the functional requirements in §3.

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

## 2a. Architecture: current state vs. future state

> **Process flows (reference):** Parts Management Flows (Figma)—Flow 1 (AOP), 2A/2B (NAOP), 3/5 (UBIF), 4 (BOM Setup). Current state mapping in progress via working sessions; future state defined once current state is validated and architecture decisions are resolved.
>
> Flows are grouped into four categories: **RT** (Runtime Transaction), **INT** (Integration/Feed), **IL** (Inventory Lifecycle), **CF** (Configuration).

### RT — Runtime Transaction flows (job creation / availability check)

One row per scenario. These flows execute at every service job creation event.

| Flow | ID | Current state | Future state | Gap / pain point | Open Qs |
|------|----|---------------|--------------|------------------|---------|
| UBIF Next Gen availability | RT-1 | ServiceBench stores replicated availability locally (1–5 min latency). Events-only feed from UBIF. | ServiceBench → EIAA → DAX Americas Availability Service → real-time response. Distro Vendor indicator returned in same call. JSON replication feed deprecated. | Stale availability causes broken appointments and incorrect decisions. | E2 [ARCH] |
| UBIF Legacy availability | RT-2 | ServiceBench receives events + APIs. Three replicated datasets: availability, distro catalog, part price. | EIAA orchestration replaces all three feeds. Reservable vs non-reservable flag per location. Part price returned transactionally on Job/Claim. | Highest-risk dataset; temporary bridge until full Next Gen migration (Q3). | C6 [ARCH], H1 |
| NAOP availability (Canada / Mexico) | RT-3 | RTI Webservice → ServiceBench. LCM-only feed; non-LCM perils have no BOM or availability check. | ServiceBench → EIAA → Tyk API Connect → vendor feed. Plan A: full inventory all perils. Plan B: LCM-only + bypass flag. RTI deprecated. | TELUS unwilling to provide full inventory; exception-handling logic is a technology concession. | B1 [ARCH], B2 [ARCH], B3, B4 |
| BOM lookup at job creation | RT-4 | ServiceBench local BOM; Asurion SKUs only. Manual multi-system setup per BOM entry. | EIAA returns BOM with Asurion + OEM SKUs per part line. Option 1: separate BOM API call from SB first. Option 2: embedded inside EIAA (single call). Decision pending. | Multiple manual touchpoints; OEM SKU type unconfirmed for pricing logic. | I1 [ARCH], A3 |
| Soft reservation at lead placement | RT-5 | No soft reservation — 1–5 min gap between availability check and final reservation. | ServiceBench calls IVS reservation API at lead placement; IVS reconciles with store-created final reservation; prevents double-deduction. | Overcommitment window at booking; risk of inventory sold twice. | C1 [ARCH], C4 [ARCH], C5 [ARCH], I2 [ARCH] |
| JIT availability + order | RT-6 | ServiceBench checks "quantity one" at distro + shipping days out from SKU config. No inventory decrement on JIT orders. | EIAA returns JIT flag + shipping days out per part line. Reservation + JIT order: single vs separate API call TBD. US only; OSR and CSS. | Job-type exclusion model (SKU vs equipment-type level) not yet decided. | A4 [ARCH], D3 [ARCH], D4 [ARCH], D5 |

### Availability + reservation API comparison

| | Current state | Future state |
|-|---------------|--------------|
| **Trigger** | Horizon → ServiceBench checks local replicated data | Horizon → ServiceBench → EIAA (real-time orchestration) |
| **Availability data** | Stale UBIF replication (1–5 min) | Real-time via UBIF Next Gen / Americas Availability Service |
| **BOM lookup** | ServiceBench local; Asurion SKUs only | EIAA or separate BOM API; returns Asurion + OEM SKUs (I1 pending) |
| **JIT eligibility** | ServiceBench checks "quantity one" at distro | EIAA returns JIT flag + shipping days out per part line |
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
| AOP — SURJIT order (auto) | IL-4 | ServiceBench. JIT orders auto-triggered for SUR-specific JIT parts. | D365 / DAX. AOP JIT reservation: required when availability = false? Pending. | I2 [ARCH] |
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

## 3. Functional requirements

> Items in the **Open Qs** column reference `01-discovery/open-questions.md`. `[ARCH]` items are blockers — resolve before grooming. **Who needs this** anchors each requirement to the primary persona(s) from `01-discovery/personas.md`.

### Availability & Reservation API · EP-1

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-1 | **Single availability and reservation API** | As a **ServiceBench consumer** (P2, P7), I need one real-time endpoint per part line so I get accurate availability without replication lag. | One endpoint (DES/ISP pattern) for all SUR inventory availability and reservations. Per-part-line response: availability flag, JIT flag, shipping days out, peril+client bypass flag, Asurion+OEM SKUs in BOM. Reservation ID returned in orders to UBIF and DAX. Supports AOP and NAOP part lines. | A1 [ARCH], A2 [ARCH], D1 [ARCH], D2 [ARCH], D3 [ARCH] | EP-1 (EP1-S1, EP1-S4) |
| FR-2 | **UBIF orchestration API** | As a **UBIF store technician** (P2), I need real-time orchestration to UBIF so distro availability is in the same response as inventory availability. | Global orchestration calls UBIF Current State and Next Gen in real time for availability and quantity; returns Distro Vendor indicator in same response. Deprecates inventory, distro, and price replication feeds from UBIF to ServiceBench. Routing must distinguish ISP vs SUR for same UBIF store ID. | E2 [ARCH] | EP-1 (EP1-S2, EP1-S3) |
| FR-6 | **UBIF Next Gen orchestration** | As a **UBIF Next Gen store** (P2), I need the JSON replication feed replaced by real-time orchestration so I’m never working from stale data. | Replace UBIF→ServiceBench JSON feed with real-time DAX orchestration. Include Distro Part Availability in same API. Deprecate all three replication datasets (availability, distro catalog, part price) from UBIF to ServiceBench. | — | EP-1 (EP1-S1, EP1-S2) |
| FR-8 | **JIT — availability API and configuration** | As an **operations dispatcher** (P6), I need JIT eligibility and shipping days out returned per part line so technicians can set customer expectations at booking. | Shipping days out returned per part line in availability response. Job-type exclusions applied at SKU level to parent and substitute SKUs. JIT flag returned per part line; included at line level in sales order. JIT eligibility driven by distro "quantity one" record; owner TBD. No inventory decrement at warehouse for JIT orders. Reservation + JIT order creation: single vs separate API call TBD. US clients only; OSR and CSS. | A4 [ARCH], D1 [ARCH], D2 [ARCH], D3 [ARCH], D4 [ARCH], D5 | EP-1 (EP1-S1, EP1-S5, EP1-S6) |

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
| FR-10 | **Soft reservations via IVS** | As a **Horizon consumer** (P7), I need inventory held at lead placement so the part I’m booking is still available when the store confirms — eliminating post-booking failures. | IVS creates soft reservation at lead placement; decrements available inventory immediately to close 1–5 min gap. Reconciles with store-created final reservation to prevent double deduction. Expiration model (auto-expire vs store acknowledgment) TBD. Applies to select providers only. | C1 [ARCH], C2, C3, C4 [ARCH], C5 [ARCH] | EP-4 (EP4-S1, EP4-S2, EP4-S3) |

### AOP Migration · EP-5

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-5 | **AOP migration — 3rd party Asurion-owned parts** | As an **AOP provider** (P1), I need all inventory lifecycle functions (orders, transfers, receiving, RMA, cycle counts) to move from ServiceBench to DAX/D365 so I have one system when SB is decommissioned. | Migrate full inventory lifecycle from ServiceBench to DAX/D365. UI via **native WMA app (Phase 1 — web-based WMA ruled out 2026-03-18)**; 3rd party providers access WMA via link in Prism. ISP picking/return screens will be first-class in UBIF Next Gen Portal (separate track). Whether 3rd party AOP locations need WMA UI or only systematic API integration: TBD (H15). Whether they will have Prism UI access: TBD (H16). Identity via Hydra; structure TBD (G2). | G1 [ARCH], G2 [ARCH], H15, H16 | EP-5 (EP5-S1, EP5-S2, EP5-S3, EP5-S4) |

### BOM / MDM / Substitution Matrix · EP-6

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-9 | **BOM and substitution matrix** | As an **MDM operator** (P5) and **store technician** (P2), I need BOM to return both Asurion and OEM SKUs and substitution rules to live in DAX so there’s no manual multi-system replication. | BOM returns both Asurion and OEM SKUs for 3rd party providers (validated in production Canada NAOP job). OEM equipment type must be confirmed for pricing/charging logic. Substitution matrix owned by MDM/Tomlin; coordination with Robbie Carter, Rose. | A3, H4 | EP-6 (EP6-S1, EP6-S2, EP6-S3) |
| FR-11 | **SKU / MDM setup migration** | As an **MDM operator** (P5), I need a single DAX setup to replace manual ServiceBench replication so every BOM update isn’t a two-system swivel-chair task. | ServiceBench part setup deprecated (precedent: DES/NDS). MDM owns single setup in DAX. Full ServiceBench field documentation (definition, options, mandatory/optional) required before migration to avoid breaking existing functionality. | F1, F2 | EP-6 (EP6-S1), EP-5 (EP5-S4) |

### Phased Rollout & Rollback · EP-7

| # | Requirement | Who needs this | What it means | Open Qs | Covered by |
|---|-------------|----------------|---------------|---------|------------|
| FR-7 | **Phased rollout and rollback** | As a **program manager** (all personas), I need each migration phase to be independently deployable per location/provider so we can roll back without affecting other phases. | Rollout order: (1) UBIF Next Gen + NAOP, (2) 3rd party NAOP (Canada/Mexico), (3) 3rd party AOP. Pilot by location/provider; 30-day rollback for non-AOP. On-demand ordering for 3rd party providers in scope (planning confirmation needed). | D6 | EP-7 (EP7-S1, EP7-S2) |
---

## 4. Non-functional requirements

| # | Requirement | Notes | Open Qs |
|---|-------------|-------|---------|
| NFR-1 | Orchestration API response time sufficient for real-time availability and JIT | Must match or exceed current ServiceBench local-lookup performance | — |
| NFR-2 | IVS soft reservation supports UBIF scale (~800 locations) without over-committing inventory | Scalability analysis required before design is finalized | H5 |
| NFR-3 | Reservation lifecycle prevents double deduction across soft and hard reservations | State reconciliation logic must be designed explicitly | C5 [ARCH] |
| NFR-4 | 3rd party (CAN, LatAm) feed repoint with minimal disruption; 30-day rollback for non-AOP; warehouse ID format standardized | Format standardization needed to match UBIF JSON format | E1 |

---

## 5. Dependencies

| Dependency | Notes |
|------------|-------|
| Next Gen Portal | 100% UBIF store migration by end of Q2 2026. SSOT orchestration and D365 migration depend on this timeline. Nine AOP stores (~100 locations) block full legacy retirement until Prism is ready. |
| DAX / IVS / D365 (F&R, FF&C, IS, F&FS) | Must deliver all infrastructure before Prism can provide 3rd party vendor solution. Build and operate orchestration API, IVS integration, NAOP/AOP migration. |
| ServiceBench / Prism | Consumer changes; Prism replaces ServiceBench for Asurion programs; 3rd party price scope TBD. |
| MDM / Robbie Carter | BOM and repair asset setup in DAX (Flow 4 working sessions); ServiceBench field documentation for migration. |
| TELUS / Mobile Clinic | Plan A vs Plan B decision required early; engage via Ankit. TELUS CRM migration timing may affect integration path. |
| Enterprise Architecture (Ankit / Tim Clemens) | Confirmed engaged as of 2026-03-18. Ankit attending EA Support sessions and formally reviewing architecture proposal; feedback expected 2026-03-19. Tim Clemens named co-owner. Architecture review meeting being scheduled for week of 2026-03-24. **[OQ: H3 Resolved]** |
| UBIF Distro | Distro migration is a parallel workstream (DAX/UBIF); viable Distro Migration Plan in scope. |

---

## 6. Success metrics and acceptance criteria

| Release | Requirements | Acceptance criteria |
|---------|--------------|---------------------|
| Q1 | FR-1, FR-2, FR-6, FR-8 | ServiceBench calls single DAX API for SUR availability; real-time response from UBIF via orchestration; no replication. JIT flag and shipping days out returned per part line. UBIF inventory inquiries migrated to D365. *(At risk — track closely.)* |
| Q2 | FR-3, FR-4 | Part price set transactionally on Job/Claim; price replication deprecated. 3rd party NAOP migrated to D365; $250k savings YTD YoY. |
| Q3 | FR-5, FR-10 | AOP inventory management in D365 (WMA or MFE); no SUR inventory management in Prism. Soft reservations live at UBIF scale; zero overcommit incidents. $600k savings YTD YoY. |

---

## 7. Open questions

Full detail in **[01-discovery/open-questions.md](../01-discovery/open-questions.md)**. Items tagged `[ARCH]` are blockers — must resolve before grooming.

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| A1 [ARCH] | Who owns peril-to-equipment-type translation: DAX or ServiceBench? Determines who owns the bypass config flag. | Ankit / DAX Arch | Open | |
| A2 [ARCH] | Should "bypass inventory check" be driven by peril+client config in DAX or ServiceBench client-level config? | Ankit / DAX Arch | Open | |
| A3 | OEM parts equipment type: what is the correct type for pricing/charging logic? Required before BOM can return OEM SKUs for 3rd party providers. | MDM / SCM | Open | |
| A4 [ARCH] | Can job-type exclusions (currently SKU-level in SB) be modeled at equipment-type level in F&O, or must they stay SKU-level? | Robbie Carter / DAX | Open | |
| B1 [ARCH] | TELUS/Mobile Clinic: Plan A (full inventory for all perils) vs Plan B (LCM-only + bypass flag)? | Ankit / TELUS rel. | Open | |
| B2 [ARCH] | Should the bypass flag live in DAX's BOM response or in ServiceBench's client config? | DAX Arch | Open | |
| B3 | TELUS CRM migration timing — does it affect the preferred integration path? | Business / TELUS rel. | Open | |
| B4 | Mexico/Mobile Clinic feed: who takes over the RTI web service when it moves to AWS/JSON? | SB Eng / DAX | Open | |
| C1 [ARCH] | Who owns the soft reservation lifecycle end-to-end? (SB initiates, store confirms, IVS manages state) | DAX / SB Arch | Open | |
| C2 [ARCH] | Is the 1–5 min timing gap between availability check and reservation creation materially impacting business outcomes? Is soft reservation near-term or longer-term? | Bryant / Ops | Open | |
| C3 | Should soft reservations apply to all providers or only select ones? | DAX / SB Arch | Open | |
| C4 [ARCH] | Expiration model for soft reservations: auto-expire after X minutes or confirmed by store acknowledgment? | DAX Arch | Open | |
| C5 [ARCH] | How do we prevent double-deduction when soft reservation is followed by store reservation event? | DAX Arch | Open | |
| C6 [ARCH] | UBIF Legacy reservation: return "not-reservable" response, or ServiceBench always reserves + DAX overrides backend? | DAX / SB | Open | |
| D1 [ARCH] | Should availability API return in-stock status and JIT eligibility as separate flags per part line? | DAX Arch | Open | |
| D2 [ARCH] | Should shipping days out be included in the availability API response (for Horizon/SB appointment scheduling)? | DAX Arch | Open | |
| D3 [ARCH] | Should job-type exclusion info be evaluated before the availability check or returned in the response? | DAX Arch | Open | |
| D4 [ARCH] | Should reservation and JIT order creation be a single combined API call or separate calls? | DAX Arch | Open | |
| D5 | Who maintains the "quantity one" records (distro/WLI JIT) in ServiceBench? Kelly Shaw or Pat Clark? | Kelly Shaw / Pat Clark | Open | |
| D6 | On-demand ordering for non-AOP providers: confirmed in scope? | Planning / Michelle | Open | |
| E1 [ARCH] | Warehouse identifier format for 3rd party providers in DAX IVS — standardization needed to match UBIF JSON format. | DAX / SB Eng | Open | |
| E2 [ARCH] | Same UBIF store has same SB ID for ISP and SUR. What routing logic distinguishes them? | DAX / SB Eng | Open | |
| F1 | What ServiceBench part setup fields must be replicated in DAX/F&O? Full field table (name, definition, options, mandatory/optional) required before migration. | Raghu / SCM | Open | |
| F2 | MDM setup process in DAX: manual (import or UI) or automated? Who owns MDM setup in future state? | MDM Team | Open | |
| F3 | Is the "magic tool" (single-touch SKU creation across DAX, ServiceBench, UBIF Portal) still viable from the Kaizen event? Who owns it? | MDM / SCM / Ops | Open | |
| G1 [ARCH] | DAX MFE in Prism Elite (TypeScript React) vs WMA for 3rd party AOP rollout — which path? | DAX / Prism | Open | WMA Phase 1 confirmed (DDD, architecture diagram). Phase 2 = Single Pane of Glass. Prism MFE optional, not committed. EA sign-off pending. |
| G2 [ARCH] | Identity for 3rd party AOP providers in Prism Elite: Hydra guest accounts? Email structure TBD. | Sandeep / Corey Street | Open | |
| H1 | ServiceBench local price copy for 3rd party claims — in scope for this project? | Bryant Mayne | Open | |
| H3 | EA assignment: is Ankit / Tim Clemens formally on the project? | Bryant / Leadership | **Resolved** | Ankit confirmed engaged (attended 2026-03-18 EA Support session, formally reviewing proposal). Tim Clemens co-owner. Bryant scheduling architecture review for week of 2026-03-24. |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose — who owns requirements and config in DAX? | SCM / MDM | Open | |
| H5 | Scalability implications for IVS soft reservations at UBIF scale (~800 locations)? | DAX Arch | Open | |
| H6 | UBIF Legacy scope: do we need to solution for Legacy UBIF given full migration to Next Gen by Q3? Temporary bridge only or full parity? ADO Feature 677454 may be out of scope. | Bryant / Michelle Bowersox | Open | |
| H7 | EP-2 scope: is "Part price on Job/Claim" a standalone epic or covered under UBIF Next Gen orchestration (ADO 677038)? Confirm before grooming. | Michelle Bowersox | Open | |
| H8 | EP-4 scope: is "Soft reservations via IVS" in scope for this project or a separate enhancement initiative? Confirm before grooming. | Michelle Bowersox | Open | |
| H9 | AgioTech / TechPeople (NAOP) — confirmed in scope? Same Tyk API contract? | Bryant / Amir | Open | |
| H10 | EU vendors (AsurionEU / Tesco / VirginMobile) — in scope? Same RTI → Tyk repoint pattern? | Bryant / Leadership | Open | |
| H12 | US NEW client group (ATTRepair / Verizon) — scope and timeline? | Bryant | Open | |
| H14 | Order types in scope: Replenishment (auto), Restock (manual), SURJIT (auto) — confirmed in scope alongside On-demand (D6)? | Bryant / Michelle Bowersox | Open | |
| I1 [ARCH] | BOM Lookup architecture: embed BOM lookup inside EIAA (single call) — OR — separate BOM service that ServiceBench calls first? Shown as "PRISM BOM?" open question in architecture diagram. | Ankit / DAPI Team / Integration Team | Open | |
| I2 [ARCH] | AOP JIT reservation: is a reservation required when inventory availability is false for AOP JIT scenarios? | Avengers / DAX Arch | Open | |
| I3 [ARCH] | Part Substitution Matrix: reuse existing Replacement Matrix (modified) — OR — build new F&O menu/form/table/data entity? | Avengers / Robbie Carter / Rose | Open | |
| — | Microsoft IVS for UBIF inventory | — | **Closed** | Not in scope. |

Full question detail, source references, and answer history: [01-discovery/open-questions.md](../01-discovery/open-questions.md).

---

## 8. Roadmap 2026

> Sequencing logic: architecture blockers must clear before engineering can groom. Build in the order of broadest impact → most complex migration, so each phase proves the infrastructure the next phase depends on.

| Quarter | Milestone | Why this order | FRs | Key dependencies | Target |
|---------|-----------|---------------|-----|-----------------|--------|
| **Now → Q1** | Complete discovery: resolve all `[ARCH]` blockers, finish current-state flow validation, confirm EA engagement | 15 `[ARCH]` questions block every FR from grooming. Engineering cannot start detailed design until peril mapping, reservation lifecycle, routing, and TELUS plan decisions are made. | All | Peril mapping meeting (A1, A2); TELUS Plan A/B (B1, B2); EA confirmation (H3) | 0 open `[ARCH]` blockers; current-state validated across all 5 flows |
| **Q1** | DAX availability API + UBIF Next Gen orchestration + JIT | Highest-volume impact (~800 stores, highest availability call frequency). Next Gen Portal migration completes Q2 — the availability API must be proven before that cutover window. JIT flag and shipping days out included in same API. Q1 KR at risk if delayed. | FR-1, FR-2, FR-6, FR-8 | EA decisions; UBIF ISP/SUR routing (E2); JIT blockers A4, D3–D5; Next Gen Portal timeline | UBIF inquiries migrated to D365; real-time availability live; JIT flag and days-out per part line; Q1 KR met |
| **Q1/Q2** | Part price on Job/Claim | Relatively self-contained API + ServiceBench model change; high financial impact (Franchise Co. reconciliation fixed). Ship before NAOP adds new complexity. | FR-3 | UBIF Current State + Next Gen API changes; SB Job/Claim model update | Price replication deprecated; transactional price on all UBIF claims |
| **Q2** | NAOP migration — Mobile Clinic + Mexico | Removes RTI Webservice dependency; aligns TELUS/Mexico to the DAX pattern. TELUS Plan A/B must be decided in Q1 to be implementation-ready by Q2. | FR-4 | TELUS decision (B1); warehouse ID standardization (E1); web service handoff (B4) | $250k YTD YoY savings; 3rd party NAOP feeds in D365 |
| **Q2/Q3** | Soft reservations via IVS | Closes the 1–5 min availability gap that causes overcommitment at booking. Must be proven at UBIF scale (~800 locations) before AOP adds more reservation volume. | FR-10 | Reservation lifecycle design (C1, C4, C5); double-deduction prevention (C5) | Zero overcommit incidents at UBIF scale; soft reservation live |
| **Q3** | AOP migration — 3rd party Asurion-owned parts | Most complex: full inventory lifecycle change, UI path (MFE vs WMA), identity management (Hydra). Goes last so DAX/IVS infrastructure is fully proven and all prior architecture decisions are stable. | FR-5 | MFE vs WMA decision (G1); Hydra identity (G2); DAX infrastructure complete; Prism ready for 9 AOP stores | AOP inventory in D365; $600k YTD YoY savings; Prism legacy retirement unblocked |
| **Q3/Q4** | BOM/MDM automation + substitution matrix | Reduces manual swivel-chair setup. Does not block availability or reservations — schedule parallel to or following AOP migration. | FR-9, FR-11 | MDM automation design (F2); substitution matrix owner confirmed (H4) | Single-touch SKU setup in DAX; ServiceBench part setup deprecated |

> **Prerequisite gate:** No engineering sprint for Q1 milestones should be groomed until `[ARCH]` blockers A1, A2, D1, D2, D3, D4, and E2 are resolved. Target: architecture working sessions complete by end of March 2026.

**Technical Development Requirements (Epics + Engineering Stories):** See [`01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md`](PRD-Technical-Development-Requirements-SSOT-SUR.md) and [Notion TDR page](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f). Contains Azure DevOps-ready Epics and User Stories with acceptance criteria. This PRD remains the stable functional alignment reference.

---

## 9. Appendix

**Out of scope (confirmed):** BAU Portal feed migration (TBD); Parts Portal; Microsoft IVS for UBIF inventory; improve-replication-only approach.

**References:** (PRD) Inventory Single Source of Truth for SUR · APC-2299 Project Brief · Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) · SURInventory workflow · PROJECT-CONTEXT.md.

**Risks:** Q1 at risk; TELUS Plan B is a technology concession for one client; AOP UI path (MFE vs WMA) must be decided before grooming; 15 `[ARCH]` blockers remain open pending architecture review (est. week of 2026-03-24).

---

*Questions tagged `[ARCH]` in open-questions.md block FR finalization. Resolve before grooming.*
