# Product Brief: SUR SSOT (Same Unit Repair – Single Source of Truth)

**Owner:** Bryant Mayne (Sr. Director, Software Engineering)
**Date:** 2026-03-25
**Status:** Draft

---

## 1. Problem / opportunity

SUR (Same Unit Repair) inventory today is not served from a single source of truth. Availability data, JIT scheduling, and claims pricing all depend on information replicated from UBIF into ServiceBench — creating **data inconsistency, latency, and scalability risks** across repair channels. Part availability can be stale by 1–5 minutes, leading to broken store appointments, incorrect repair-vs-replacement decisions, and missed revenue. There is no mechanism to hold a part at booking, so the same part can be committed to two jobs before either is confirmed. Extending the proven DAX SSOT pattern — already live for DSE/NDES with significant shrink reductions — to SUR will eliminate these gaps and support Fulfillment 2026 Objective 2: a unified fulfillment ecosystem with a single, accurate system of record for inventory.

## 2. Proposed solution

Replace UBIF→ServiceBench replication with a **single real-time inventory API** that gives ServiceBench accurate, live data for every SUR part request — availability, JIT eligibility, lead times, substitute parts, and job type restrictions, all in one call. Alongside that, set **part price transactionally on every repair Job/Claim** (eliminating reconciliation errors with UBIF Franchise Co.), and **migrate all 3rd party NAOP and AOP inventory management** from ServiceBench into DAX/D365 — the same platform already used for DSE/NDES. This removes all replication, consolidates every inventory system of record into one, and enables ServiceBench's eventual retirement from inventory management.

## 3. Users and impact

- **Store technicians (UBIF):** Real-time part availability replaces stale replicated data; accurate JIT scheduling; fewer broken appointments.
- **Repair coordinators / Horizon:** Part held at booking time — eliminating the window where a part can be double-committed.
- **Claims and Finance:** Part price set directly on each Job/Claim; no more reconciliation errors between UBIF master pricing and ServiceBench.
- **3rd party repair partners (NAOP — Canada and Mexico):** Vendor feeds migrated to the standard DAX integration pattern; legacy RTI Webservice retired.
- **3rd party AOP providers (9 companies, 103 Asurion Network locations, 100–200 users, ~6,000 jobs/month):** Full inventory lifecycle — replenishment (min-max at SKU level, monthly refresh + weekly adjustments, Mon/Wed/Fri release schedule), transfers, receiving, returns, cycle counts — moves to D365; ServiceBench retired for these providers.
- **Ops and MDM teams:** Single part setup in DAX eliminates manual two-system replication for every new SKU.

**Rollout (agreed March 2026):**
- Q1 — Accurate part pricing on every repair Job/Claim (ready to build now)
- Q2 — API built and validated; **end of Q2 = store migration begins** for UBIF Next-Gen stores; BOM/part setup automated; soft reservations (scope confirmation pending). Legacy not part of Q2 build.
- Q3 — AOP provider inventory migrated to D365 ($600k savings milestone)
- Q4 — Canadian and Mexico partner feed migration (deferred from Q2 due to TELUS partner complexity; $250k savings milestone)

Nine AOP stores (~100 locations) cannot fully retire ServiceBench until the Prism migration is complete.

## 4. Success metrics

- All SUR inventory inquiries and reservations handled through D365; full AOP inventory lifecycle in D365; alignment to the DSE/NDES pattern.
- **$600k savings YTD YoY** (Q3) · **$250k YoY** shrink reduction (Q4 — NAOP); contributes to enterprise **$2.32M** shrink reduction goal.
- **Channel coverage:** ~96% of SUR jobs (UBIF In-Store ~62% + UBIF Remote Tech ~34%) addressed in Q2–Q3; ~3.5% (AOP / 3rd Party Remote Tech) in Q3; ~1% (Depot / Mail-in = NAOP) in Q4. Source: SCM channel mix avg ATT + Verizon FY 2026.
- 100% UBIF Next-Gen store migration by end of Q3 2026 (Assumption A; see PRD §11 for Assumption B gap scenario).

## 5. Scope

**In scope:**
- Single real-time inventory API for SUR: availability, JIT eligibility and lead times, substitute parts, and job type restrictions per part — all returned in one call to ServiceBench.
- Transactional part price on every Job/Claim (UBIF Current State and Next Gen); all UBIF→ServiceBench replication feeds retired.
- Migration of Canadian (TELUS/Mobile Clinic) and Mexican partner inventory feeds to the DAX standard integration pattern (Q4).
- Full AOP inventory lifecycle — replenishment (min-max per SKU per location, monthly bulk refresh, Mon/Wed/Fri scheduled release), receiving, transfers, returns, cycle counts — migrated from ServiceBench to D365 for 9 US providers (103 locations, 100–200 users) (Q3).
- Soft reservation at booking time: holding inventory from the moment a repair is scheduled until the store confirms (scope confirmation required before build begins — see §7).
- Automated part/BOM setup in DAX; ServiceBench part setup retired.
- Phased deployment with per-location controls and a 30-day rollback capability for each phase.

**Out of scope (confirmed):**
- **UBIF Legacy inventory integration (Q2)** — Not part of Q2 build scope. Legacy stores continue on existing replication feeds until they migrate to Next-Gen. If Next-Gen migration is not 100% by end of Q2, a Plan B for Legacy jobs in DAX is TBD (last priority for the team).
- BAU Portal feed migration (separate workstream, timeline TBD).
- Parts Portal.
- EU vendors (AsurionEU / Tesco / VirginMobile) — separate decision required.

## 6. Dependencies and risks

| Item | Detail |
|------|--------|
| **UBIF Next Gen Portal migration** | 100% UBIF store migration to Next Gen Portal required by end of Q2 2026. SUR availability API go-live depends on this cutover. |
| **TELUS / Mobile Clinic partner decision** | TELUS must confirm whether they will provide full inventory data for all repair types (preferred) or a limited feed requiring fallback handling. Decision needed to finalize Q4 NAOP scope. Deferring to Q4 adds risk to the $250k savings milestone — previously targeted for Q2. |
| **Prism readiness** | 103 AOP locations (9 companies) cannot fully retire ServiceBench until the Prism migration is complete. |
| **Enterprise Architecture** | Ankit and Tim Clemens (EA) are formally engaged as co-owners of the architecture design. Combined BOM + Availability API architecture confirmed in architecture workshop 2026-03-25; HLE sizing in progress. D1 resolved (separate qty + JIT flags confirmed 2026-03-25). Remaining [ARCH] blockers for Q2: A2, D4, I1 (HLE pending), A5 (job type nomenclature — Raghu/Amir action item). |

**Key risks:**
- Q1 part price delivery is the critical path — any delay puts Q1 key results at risk.
- NAOP deferral to Q4 shifts the $250k savings milestone by approximately two quarters versus the original plan.
- Phased rollout with 30-day rollback is the primary risk mitigation; each phase deploys independently by location or provider.

## 7. Decisions needed from leadership

| Decision | Owner | Needed by |
|----------|-------|-----------|
| Confirm whether soft reservations (holding a part at booking) are in scope for this project or a separate initiative | Bryant Mayne / Michelle Bowersox | Before Q2 planning |
| TELUS: provide full inventory for all repair types, or limited feed with fallback handling? | Business / Partner relations | Before Q4 NAOP design begins |
| AOP providers: use D365 WMA inventory app directly, or API-only integration with no UI? | Bryant Mayne | Before Q3 AOP design begins |
| On-demand ordering for 3rd party providers — confirmed in scope? | Michelle Bowersox | Before Q2 planning |
| Approve technology labor estimate: **$50K–$100K** (APC-2299) | Bryant Mayne / Finance | Now |

## 8. Next steps

- **Q1 (now):** Engineering starts part price on Job/Claim — no blockers; ready to build.
- **Q2:** API built and validated; **end of Q2 = UBIF Next-Gen store migration begins**; BOM/part setup automated in DAX; soft reservations if confirmed in scope. Legacy not part of Q2 build — Plan B for Legacy jobs TBD (last priority). Architecture design completing week of March 24. Two volume scenarios: Assumption A (100% Next-Gen by Q3) vs Assumption B (partial migration; Legacy gap remains until Plan B confirmed).
- **Q3:** AOP provider inventory fully migrated to D365 (103 locations, ~6,000 jobs/month); ServiceBench retired for AOP. $600k savings milestone.
- **Q4:** Canadian and Mexico partner feeds migrated to DAX. $250k savings milestone.
- Discovery lead: Thays Pritchard. Full technical and functional requirements: [PRD — SUR SSOT](https://www.notion.so/asurionproduct/3259532a1f8680b08cc4ebb72fe7b535).
