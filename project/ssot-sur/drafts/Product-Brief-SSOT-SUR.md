# Product Brief: SUR SSOT (Same Unit Repair – Single Source of Truth)

**Owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Date:** 2026-03-16  
**Status:** Draft  

---

## 1. Problem / opportunity

SUR (Same Unit Repair) inventory is not served by a single source of truth. Availability, JIT scheduling, and claims pricing depend on data replicated from UBIF (Current State and Next Gen) into ServiceBench, which creates **data inconsistency, latency, and scalability risks**. Transactional part availability/quantity can be wrong, leading to stores unable to honor appointments, incorrect repair vs. replacement decisions, and missed revenue. There is no single API for SUR inventory availability and reservations across repair channels. Extending the proven DAX SSOT pattern (already used for DSE/NDES with significant shrink reductions) to SUR will reduce shrink, unify availability under one API, and support Fulfillment 2026 Objective 2: a unified fulfillment ecosystem with a single, accurate system of record for inventory.

## 2. Proposed solution (summary)

Deliver a **single API** for SUR inventory availability and reservations (DES/ISP pattern). Replace UBIF→ServiceBench replication with a **real-time orchestration API** for part availability, quantity, and distro; set **part price transactionally on Job/Claim** in ServiceBench. **Migrate** 3rd party NAOP and AOP inventory feeds/management from ServiceBench to DAX IVS/D365. UBIF store-level availability remains owned by UBIF; consumers (ServiceBench, portals) call the single API instead of relying on replicated data.

## 3. Users and impact

- **UBIF (stores and distro):** Inventory exposed via orchestration API; part price on claim; deprecation of outbound feeds to ServiceBench.
- **ServiceBench/Prism:** Consumer of orchestration API for UBIF availability; part price on Job/Claim; 3rd party SUR until migrated; Prism replaces ServiceBench for Asurion programs; SUR inventory management in DAX (IVS), not Prism.
- **DAX/Engineering (F&R, FF&C, IS, F&FS):** Build and operate orchestration API, IVS/D365 integration, NAOP/AOP migration.
- **3rd party repair (NAOP/AOP):** Feeds and reservation strategy move to DAX; AOP inventory management moves to DAX.
- **Store Ops / Remote Tech:** SUR availability and JIT behavior change with single API and real-time data.
- **Claims/Finance:** Part price on claim affects Asurion–UBIF Franchise Co. reconciliation.

**Cohorts (rollout):** (1) UBIF Next Gen, (2) UBIF Legacy, (3) 3rd party AOP, (4) 3rd party NAOP (Mexico/Canada), (5) Remote tech. Project is on roadmaps (Camille, Dax) through year-end. **Prism dependency:** Nine AOP stores (~100 locations) block full legacy retirement until Prism migration completes.

## 4. Success metrics

- All SUR inventory inquiries and reservations handled by D365; all inventory management of AOP in D365; alignment to DES/NDES pattern.
- **$250k YoY** shrink reduction (Q2); **$600k Savings YTD YoY** (Q3); contributes to enterprise **$2.32M** shrink reduction.
- 100% UBIF store migration to Next Gen Portal by end of Q2 2026 (dependency).

## 5. Scope

**In scope:**  
- Single API for SUR inventory (availability + reservations).  
- Global orchestration API for UBIF (replace replication); part price on Job/Claim; deprecate UBIF→ServiceBench inventory/distro/price feeds.  
- Migrate 3rd party NAOP to DAX IVS; migrate 3rd party AOP inventory management to DAX (IVS).  
- UBIF Next Gen: ServiceBench calls DAX availability (no UBIF→ServiceBench replication).  
- Distro Part Availability in same API; approved Distro Migration Plan (viable plan in scope).

**Out of scope:**  
- BAU Portal feed migration (timing/scope TBD; never assume in scope without explicit confirmation).  
- Parts Portal (explicitly out of scope per Prism).  
- Microsoft IVS for UBIF inventory (not recommended for this scope).  
- “Improve replication only” (orchestration required).

## 6. Dependencies and risks

- **Dependency:** Next Gen Portal store migration (Q2 2026); SUR SSOT UBIF orchestration aligns to that timeline. Nine AOP stores (~100 locations) depend on Prism before full legacy retirement.
- **Risks:** Q1 key results at risk; 3rd party (CAN/LatAm) may need to repoint feeds; Prism/ServiceBench transition and DAX MFE vs WMA for AOP affect UX and rollout.
- **Mitigation:** Phased rollout by location/provider; 30-day rollback for non-AOP; working sessions to validate current state (Parts Management Flows) before future state. **Enterprise architecture:** Ankit / Tim Clemens engaged for architecture alignment.

## 7. Open questions

Open questions are maintained in **[project/ssot-sur/docs/open-questions.md](../docs/open-questions.md)** (template: Question | Source | Owner | Status | Answer | Date). Key items: ServiceBench 3rd party price scope; BAU Portal feed scope; DAX MFE vs WMA for AOP; EA assignment; JIT quantity-one ownership; TELUS/Mobile Clinic full-inventory vs Plan B; substitution matrix ownership; peril-to-equipment-type ownership.

## 8. Next steps / approval

- Finalize PRD from this brief and existing (PRD) Inventory SSOT for SUR doc.  
- Complete current-state mapping (Parts Management Flows) with Amir, Raghu, UBIF SMEs, MDM. **Discovery:** Thays leading.  
- Q1: Migrate UBIF inventory inquiries to D365; Q2: Migrate 3rd party NAOP to D365; Q3: Migrate 3rd party AOP to D365.  
- Technology labor estimate: $50K–$100K (APC-2299).
