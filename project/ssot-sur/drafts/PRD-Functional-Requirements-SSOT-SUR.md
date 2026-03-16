# PRD: Functional Requirements — SUR SSOT (Same Unit Repair · Single Source of Truth)

**Product owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Last updated:** 2026-03-16  
**Status:** Draft  
**Related brief:** [Product Brief SUR SSOT](https://www.notion.so/asurionproduct/Product-Brief-SUR-SSOT-3259532a1f8680538478fe482766eb7b)

---

## 1. Overview and goals

SUR SSOT extends Asurion's DAX platform inventory SSOT—proven for DSE/NDES with significant shrink reductions—to Same Unit Repair. **Goals:** (1) Single API for SUR inventory availability and reservations (DES/ISP pattern). (2) Replace UBIF→ServiceBench replication with real-time orchestration; part price on Job/Claim. (3) Migrate 3rd party NAOP and AOP to DAX IVS/D365. (4) Eliminate replication risks (inconsistency, latency, scalability). Aligns to Fulfillment 2026 Objective 2: unified fulfillment ecosystem with a single, accurate system of record for inventory.

**Success metrics:** $250k YoY shrink (Q2) · $600k YTD YoY (Q3) · All SUR inventory inquiries and AOP management in D365.

---

## 2. User stories

| ID | As a… | I want… | So that… | Priority |
|----|-------|---------|----------|----------|
| US-1 | Store / portal user | One API to check SUR part availability and reserve parts | I get accurate, real-time data without replication lag | P0 |
| US-2 | ServiceBench consumer | Call the orchestration API for UBIF availability and distro | I no longer depend on replicated UBIF feeds | P0 |
| US-3 | Claims / finance user | Part price set on the Job/Claim | Reconciliation with UBIF Franchise Co. uses transactional price, not replicated master | P0 |
| US-4 | 3rd party NAOP provider (TELUS, Mobile Klinik, Mexico) | Inventory feed and reservation strategy in DAX IVS | SUR availability is consistent with DES/NDES | P1 |
| US-5 | 3rd party AOP location | Inventory management in D365 (WMA or DAX MFE) | Asurion-owned parts are tracked in the enterprise SOR | P1 |
| US-6 | Operator | JIT and availability based on real-time orchestration | Appointments and repair vs. replacement decisions are accurate | P0 |

**Process flows (reference):** Parts Management Flows (Figma)—Flow 1 (AOP), 2A/2B (NAOP), 3/5 (UBIF), 4 (BOM Setup). Current state mapping in progress via working sessions; future state defined once current state is validated and architecture decisions are resolved.

---

## 2a. Architecture: current state vs. future state

One row per flow. Columns show the key shift from current to future state and which architecture questions remain open.

| Flow | Vendor | Current state | Future state | Gap / pain point | Open Qs |
|------|--------|---------------|--------------|------------------|---------|
| **1 – AOP** | 3rd party Asurion-owned parts (9 service providers, ~100 locations; remote tech only) | ServiceBench manages full inventory lifecycle (orders, transfers, receiving, RMA, cycle count). MDM sets up in DAX → Robbie Carter manually replicates to ServiceBench ("swivel chair"). | DAX/D365 owns full inventory lifecycle. UI via DAX MFE embedded in Prism Elite (TypeScript React) or WMA. Prism replaces ServiceBench for Asurion programs. ServiceBench setup deprecated (precedent: DES/NDS). | Manual multi-system setup; no SSOT; 9 stores blocking full Prism migration | G1 (MFE vs WMA), G2 (Hydra identity), F1 (SB field documentation) |
| **2A – NAOP Mobile Clinic** | TELUS / Mobile Klinik (Canada) | RTI Webservice → ServiceBench. LCM inventory feed only. Battery, camera, charging port treated as "small parts" — no BOM or availability check. Jobs created without part lines for non-LCM perils. | Repoint RTI → DAX IVS API (AWS/JSON). **Plan A (preferred):** full inventory for all perils. **Plan B (fallback):** LCM-only + DAX returns peril+client bypass flag for non-LCM. Fake SKUs ruled out. | TELUS unwilling to provide full inventory; exception-handling logic is a technology concession for one client | B1 (Plan A vs B), B2 (bypass flag owner), B3 (TELUS CRM timing), B4 (web service ownership) |
| **2B – NAOP Mexico** | ATT Mexico / Telcel | RTI Webservice (direct, not via L7) → ServiceBench. Same LCM feed pattern as 2A. | Same as 2A. Direct AWS/JSON integration. ServiceBench team takes over web service. | Feed ownership and format unclear post-RTI migration | B4, E1 (warehouse ID format) |
| **3 – UBIF Next Gen** | UBIF Next Gen stores | Events only → ServiceBench. ServiceBench stores replicated availability locally. Latency 1–5 min. | ServiceBench calls DAX Availability API in real time. JSON inventory feed deprecated. Same API returns Distro Vendor indicator. | Stale availability leads to broken appointments and incorrect repair/replacement decisions | E2 (ISP vs SUR routing for same UBIF store ID) |
| **5 – UBIF Legacy** | UBIF Legacy stores (migrating to Next Gen by Q3) | Events + APIs → ServiceBench. Three replicated datasets: transactional availability, distro catalog, part price. | Orchestration API replaces all three replication feeds. Reservable vs non-reservable flag by location. Part price set transactionally on Job/Claim. | Highest risk dataset (transactional availability); price replication also deprecated | C6 (UBIF Legacy reservation approach), H1 (3rd party price scope) |
| **4 – BOM / MDM Setup** | All repair types | MDM sets up in DAX → Robbie Carter manually sets up in ServiceBench → Portal may need separate setup. BOM contains Asurion SKUs only. | MDM single setup in DAX. ServiceBench setup deprecated. BOM returns Asurion and OEM SKUs for 3rd party providers. Substitution matrix in MDM/Tomlin. | Multiple manual touch points for same BOM; OEM SKU type unconfirmed for pricing logic | A3 (OEM equipment type), F1 (SB field docs), F2 (MDM automation), H4 (substitution matrix ownership) |

### Availability and reservation flow comparison

| | Current state | Future state |
|-|---------------|--------------|
| **Trigger** | Horizon → ServiceBench checks local replicated data | Horizon → ServiceBench → DAX Availability API (real-time) |
| **Availability data** | Stale copy from UBIF replication (1–5 min latency) | Real-time from UBIF Current State / Next Gen via orchestration |
| **BOM lookup** | ServiceBench local; Asurion SKUs only | DAX; returns Asurion + OEM SKUs |
| **JIT eligibility** | ServiceBench checks "quantity one" at distro + shipping days out from SKU config | DAX returns JIT flag + shipping days out per part line in availability response |
| **Bypass (no inventory)** | ServiceBench client-level config (e.g., TELUS non-LCM) | DAX returns peril+client bypass flag in BOM/availability response |
| **Soft reservation** | None — 1–5 min gap between check and reservation | ServiceBench calls IVS to soft-reserve at lead placement; IVS reconciles when store creates final reservation |
| **Reservation ID** | Not passed to UBIF or DAX | Reservation ID included in orders to UBIF and DAX |
| **Part price** | Replicated master price from UBIF | Transactional price set on Job/Claim in ServiceBench |

### JIT mechanics

| | Current state | Future state |
|-|---------------|--------------|
| **Orderability signal** | "Quantity one" at distro location (not true inventory; counts never decremented on JIT order) | DAX returns JIT flag per part line; shipping days out in availability response |
| **Job-type exclusions** | Maintained at SKU level in ServiceBench (apply to parent + substitute SKUs) | To be determined: SKU level in F&O or equipment-type level? **[OQ: A4, D3]** |
| **Receiving** | Marks serials as reserved (not in-stock); nightly job converts unused reserved serials >30 days back to in-stock | Same model expected; design TBD |
| **Scope** | US clients only; OSR and CSS job types; store-level config drives eligibility | Same scope |

---

## 3. Functional requirements

> Items in the **Open Qs** column reference `docs/open-questions.md`. `[ARCH]` items are blockers — resolve before grooming.

| # | Requirement | What it means | Open Qs |
|---|-------------|---------------|---------|
| FR-1 | **Single availability and reservation API** | One endpoint (DES/ISP pattern) for all SUR inventory availability and reservations. Per-part-line response: availability flag, JIT flag, shipping days out, peril+client bypass flag, Asurion+OEM SKUs in BOM. Reservation ID returned in orders to UBIF and DAX. Supports AOP and NAOP part lines. | A1 [ARCH], A2 [ARCH], D1 [ARCH], D2 [ARCH], D3 [ARCH] |
| FR-2 | **UBIF orchestration API** | Global orchestration calls UBIF Current State and Next Gen in real time for availability and quantity; returns Distro Vendor indicator (distro part availability) in same response. Deprecates inventory, distro, and price replication feeds from UBIF to ServiceBench. Routing must distinguish ISP vs SUR for same UBIF store ID. | E2 [ARCH] |
| FR-3 | **Part price on Job/Claim** | Partner invoice price set transactionally on Job/Claim in ServiceBench. Both UBIF Current State and Next Gen support this; price replication from UBIF deprecated for UBIF claims. Scope of ServiceBench local price copy for 3rd party claims: TBD. | H1 |
| FR-4 | **NAOP migration — Mobile Clinic and Mexico** | Repoint inventory feeds from RTI Webservice to DAX IVS API (AWS/JSON). Plan A: TELUS/Mobile Clinic provides full inventory for all perils (preferred). Plan B: LCM-only feed + peril+client bypass flag for non-LCM perils (fallback; fake SKUs ruled out). Mexico same pattern; SB team takes over web service. UBIF Legacy: reservable vs non-reservable by location. | B1 [ARCH], B2 [ARCH], B3, B4, C6 [ARCH], C7 |
| FR-5 | **AOP migration — 3rd party Asurion-owned parts** | Migrate full inventory lifecycle from ServiceBench to DAX/D365. UI via DAX MFE in Prism Elite (TypeScript React) or WMA. 3rd party providers access DAX via Prism (single system experience). Identity via Hydra; structure TBD. | G1 [ARCH], G2 [ARCH] |
| FR-6 | **UBIF Next Gen orchestration** | Replace UBIF→ServiceBench JSON feed with real-time DAX orchestration. Include Distro Part Availability in same API. Deprecate all three replication datasets (availability, distro catalog, part price) from UBIF to ServiceBench. | — |
| FR-7 | **Phased rollout and rollback** | Rollout order: (1) UBIF Next Gen + NAOP, (2) 3rd party NAOP (Canada/Mexico), (3) 3rd party AOP. Pilot by location/provider; 30-day rollback for non-AOP. On-demand ordering for 3rd party providers in scope (planning confirmation needed). | D6 |
| FR-8 | **JIT — availability API and configuration** | Shipping days out returned per part line in availability response (e.g., 3 days non-battery, 7 days battery). Job-type exclusions applied at SKU level to parent and substitute SKUs. JIT flag returned per part line; included at line level in sales order. JIT eligibility driven by distro "quantity one" record; owner TBD. No inventory decrement at warehouse for JIT orders. Reservation + JIT order creation: single vs separate API call TBD. US clients only; OSR and CSS. | A4 [ARCH], D1 [ARCH], D2 [ARCH], D3 [ARCH], D4 [ARCH], D5 |
| FR-9 | **BOM and substitution matrix** | BOM returns both Asurion and OEM SKUs for 3rd party providers (validated in production Canada NAOP job). OEM equipment type must be confirmed for pricing/charging logic. Substitution matrix owned by MDM/Tomlin; coordination with Robbie Carter, Rose. | A3, H4 |
| FR-10 | **Soft reservations via IVS** | IVS creates soft reservation at lead placement; decrements available inventory immediately to close 1–5 min gap. Reconciles with store-created final reservation to prevent double deduction. Expiration model (auto-expire vs store acknowledgment) TBD. Applies to select providers only. | C1 [ARCH], C2, C3, C4 [ARCH], C5 [ARCH] |
| FR-11 | **SKU / MDM setup migration** | ServiceBench part setup deprecated (precedent: DES/NDS). MDM owns single setup in DAX. Full ServiceBench field documentation (definition, options, mandatory/optional) required before migration to avoid breaking existing functionality. | F1, F2 |

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
| Enterprise Architecture (Ankit / Tim Clemens) | Not yet confirmed by leadership. Required for peril mapping, routing, and reservation architecture decisions. **[OQ: H3]** |
| UBIF Distro | Distro migration is a parallel workstream (DAX/UBIF); viable Distro Migration Plan in scope. |

---

## 6. Success metrics and acceptance criteria

| Release | Story | Acceptance criteria |
|---------|-------|---------------------|
| Q1 | US-1, US-2 | ServiceBench calls single DAX API for SUR availability; real-time response from UBIF via orchestration; no replication. UBIF inventory inquiries migrated to D365. *(At risk — track closely.)* |
| Q2 | US-3, US-4 | Part price set transactionally on Job/Claim; price replication deprecated. 3rd party NAOP migrated to D365; $250k savings YTD YoY. |
| Q3 | US-5, US-6 | AOP inventory management in D365 (WMA or MFE); no SUR inventory management in Prism. $600k savings YTD YoY. |

---

## 7. Open questions

Full detail in **[docs/open-questions.md](../docs/open-questions.md)**. Items tagged `[ARCH]` are blockers — must resolve before grooming.

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| A1 [ARCH] | Who owns peril-to-equipment-type translation: DAX or ServiceBench? Determines who owns the bypass config flag. | Ankit / DAX Arch | Open | |
| A2 [ARCH] | Should "bypass inventory check" be driven by peril+client config in DAX or ServiceBench client-level config? | Ankit / DAX Arch | Open | |
| A4 [ARCH] | Can job-type exclusions (currently SKU-level in SB) be modeled at equipment-type level in F&O, or must they stay SKU-level? | Robbie Carter / DAX | Open | |
| B1 [ARCH] | TELUS/Mobile Clinic: Plan A (full inventory for all perils) vs Plan B (LCM-only + bypass flag)? | Ankit / TELUS rel. | Open | |
| B2 [ARCH] | Should the bypass flag live in DAX's BOM response or in ServiceBench's client config? | DAX Arch | Open | |
| B3 | TELUS CRM migration timing — does it affect the preferred integration path? | Business / TELUS rel. | Open | |
| B4 | Mexico/Mobile Clinic feed: who takes over the RTI web service when it moves to AWS/JSON? | SB Eng / DAX | Open | |
| C1 [ARCH] | Who owns the soft reservation lifecycle end-to-end? (SB initiates, store confirms, IVS manages state) | DAX / SB Arch | Open | |
| C4 [ARCH] | Expiration model for soft reservations: auto-expire after X minutes or confirmed by store acknowledgment? | DAX Arch | Open | |
| C5 [ARCH] | How do we prevent double-deduction when soft reservation is followed by store reservation event? | DAX Arch | Open | |
| C6 [ARCH] | UBIF Legacy reservation: return "not-reservable" response, or ServiceBench always reserves + DAX overrides backend? | DAX / SB | Open | |
| D1 [ARCH] | Should availability API return in-stock status and JIT eligibility as separate flags per part line? | DAX Arch | Open | |
| D2 [ARCH] | Should shipping days out be included in the availability API response (for Horizon/SB appointment scheduling)? | DAX Arch | Open | |
| D3 [ARCH] | Should job-type exclusion info be evaluated before the availability check or returned in the response? | DAX Arch | Open | |
| D4 [ARCH] | Should reservation and JIT order creation be a single combined API call or separate calls? | DAX Arch | Open | |
| D5 | Who maintains the "quantity one" records (distro/WLI JIT) in ServiceBench? Kelly Shaw or Pat Clark? | Kelly Shaw / Pat Clark | Open | |
| D6 | On-demand ordering for non-AOP providers: confirmed in scope? | Planning / Michelle | Open | |
| E1 | Warehouse identifier format for 3rd party providers in DAX IVS — standardization needed to match UBIF JSON format. | DAX / SB Eng | Open | |
| E2 [ARCH] | Same UBIF store has same SB ID for ISP and SUR. What routing logic distinguishes them? | DAX / SB Eng | Open | |
| G1 [ARCH] | DAX MFE in Prism Elite (TypeScript React) vs WMA for 3rd party AOP rollout — which path? | DAX / Prism | Open | |
| G2 [ARCH] | Identity for 3rd party AOP providers in Prism Elite: Hydra guest accounts? Email structure TBD. | Sandeep / Corey Street | Open | |
| H1 | ServiceBench local price copy for 3rd party claims — in scope for this project? | TBD | Open | |
| H3 | EA assignment: is Ankit / Tim Clemens formally on the project? Leadership has not confirmed EA involvement. | Bryant / Leadership | Open | |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose — who owns requirements and config in DAX? | SCM / MDM | Open | |
| H5 | Scalability implications for IVS soft reservations at UBIF scale (~800 locations)? | DAX Arch | Open | |
| — | Microsoft IVS for UBIF inventory | — | **Closed** | Not in scope. |

Full question detail, source references, and answer history: [docs/open-questions.md](../docs/open-questions.md).

---

## 8. Roadmap 2026

> Sequencing logic: architecture blockers must clear before engineering can groom. Build in the order of broadest impact → most complex migration, so each phase proves the infrastructure the next phase depends on.

| Quarter | Milestone | Why this order | FRs | Key dependencies | Target |
|---------|-----------|---------------|-----|-----------------|--------|
| **Now → Q1** | Complete discovery: resolve all `[ARCH]` blockers, finish current-state flow validation, confirm EA engagement | 15 `[ARCH]` questions block every FR from grooming. Engineering cannot start detailed design until peril mapping, reservation lifecycle, routing, and TELUS plan decisions are made. | All | Peril mapping meeting (A1, A2); TELUS Plan A/B (B1, B2); EA confirmation (H3) | 0 open `[ARCH]` blockers; current-state validated across all 5 flows |
| **Q1** | DAX availability API + UBIF Next Gen orchestration | Highest-volume impact (~800 stores, highest availability call frequency). Next Gen Portal migration completes Q2 — the availability API must be proven before that cutover window. Q1 KR at risk if delayed. | FR-1, FR-2, FR-6 | EA decisions; UBIF ISP/SUR routing (E2); Next Gen Portal timeline | UBIF inquiries migrated to D365; real-time availability live; Q1 KR met |
| **Q1/Q2** | Part price on Job/Claim | Relatively self-contained API + ServiceBench model change; high financial impact (Franchise Co. reconciliation fixed). Ship before NAOP adds new complexity. | FR-3 | UBIF Current State + Next Gen API changes; SB Job/Claim model update | Price replication deprecated; transactional price on all UBIF claims |
| **Q2** | NAOP migration — Mobile Clinic + Mexico | Removes RTI Webservice dependency; aligns TELUS/Mexico to the DAX pattern. TELUS Plan A/B must be decided in Q1 to be implementation-ready by Q2. | FR-4 | TELUS decision (B1); warehouse ID standardization (E1); web service handoff (B4) | $250k YTD YoY savings; 3rd party NAOP feeds in D365 |
| **Q2/Q3** | Soft reservations via IVS | Closes the 1–5 min availability gap that causes overcommitment at booking. Must be proven at UBIF scale (~800 locations) before AOP adds more reservation volume. | FR-10 | Reservation lifecycle design (C1, C4, C5); double-deduction prevention (C5) | Zero overcommit incidents at UBIF scale; soft reservation live |
| **Q3** | AOP migration — 3rd party Asurion-owned parts | Most complex: full inventory lifecycle change, UI path (MFE vs WMA), identity management (Hydra). Goes last so DAX/IVS infrastructure is fully proven and all prior architecture decisions are stable. | FR-5 | MFE vs WMA decision (G1); Hydra identity (G2); DAX infrastructure complete; Prism ready for 9 AOP stores | AOP inventory in D365; $600k YTD YoY savings; Prism legacy retirement unblocked |
| **Q3/Q4** | BOM/MDM automation + substitution matrix | Reduces manual swivel-chair setup. Does not block availability or reservations — schedule parallel to or following AOP migration. | FR-9, FR-11 | MDM automation design (F2); substitution matrix owner confirmed (H4) | Single-touch SKU setup in DAX; ServiceBench part setup deprecated |

> **Prerequisite gate:** No engineering sprint for Q1 milestones should be groomed until `[ARCH]` blockers A1, A2, D1, D2, D3, D4, and E2 are resolved. Target: architecture working sessions complete by end of March 2026.

**Technical Development Requirements (Epics + Engineering Stories):** See [`docs/PRD-Technical-Development-Requirements-SSOT-SUR.md`](../docs/PRD-Technical-Development-Requirements-SSOT-SUR.md) and [Notion TDR page](https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f). Contains Azure DevOps-ready Epics and User Stories with acceptance criteria. This PRD remains the stable functional alignment reference.

---

## 9. Appendix

**Out of scope (confirmed):** BAU Portal feed migration (TBD); Parts Portal; Microsoft IVS for UBIF inventory; improve-replication-only approach.

**References:** (PRD) Inventory Single Source of Truth for SUR · APC-2299 Project Brief · Parts Management Flows (Figma: `kRrljWUXdow6bg7KBHkkx7`) · SURInventory workflow · PROJECT-CONTEXT.md.

**Risks:** Q1 at risk; TELUS Plan B is a technology concession for one client; AOP UI path must be decided before grooming; EA engagement not confirmed.

---

*Questions tagged `[ARCH]` in open-questions.md block FR finalization. Resolve before grooming.*
