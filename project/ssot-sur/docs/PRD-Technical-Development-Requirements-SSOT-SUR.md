# PRD: Technical Development Requirements — SUR SSOT

**Product owner:** Bryant Mayne (Sr. Director, Software Engineering)  
**Last updated:** 2026-03-16  
**Status:** Draft — evolves as architecture decisions are finalized  
**Related PRD (Functional):** [PRD — Functional Requirements SUR SSOT](https://www.notion.so/3259532a1f8680b08cc4ebb72fe7b535)  
**Notion TDR page:** https://www.notion.so/3259532a1f8680e0946ec9fbb1e85d2f  
**Azure DevOps:** _(To be connected at handoff — see PROJECT-CONTEXT.md)_

---

> **Purpose:** This document is the engineering-facing complement to the PRD. It holds Epics, User Stories with acceptance criteria, and implementation notes structured for Azure DevOps import. The PRD captures the "what and why"; this document captures the "how to build it, in what order."
>
> **Status note:** Architecture has 15 `[ARCH]` open questions (see PRD §7 and `open-questions.md`). Stories marked `[BLOCKED]` cannot be groomed until the corresponding architecture decision is resolved. Unblock in the order defined by the 2026 Roadmap (PRD §8).

---

## Epics

| Epic | Description | Cohort / flow | Roadmap quarter | Status |
|------|-------------|---------------|-----------------|--------|
| EP-1 | DAX availability API + UBIF orchestration | UBIF Next Gen, UBIF Legacy | Q1 | Discovery |
| EP-2 | Part price on Job/Claim | UBIF (all) | Q1/Q2 | Discovery |
| EP-3 | NAOP migration — Mobile Clinic + Mexico | 3rd party NAOP | Q2 | Discovery |
| EP-4 | Soft reservations via IVS | UBIF + select providers | Q2/Q3 | Discovery |
| EP-5 | AOP migration — 3rd party Asurion-owned parts | 3rd party AOP | Q3 | Discovery |
| EP-6 | BOM/MDM automation + substitution matrix | All | Q3/Q4 | Discovery |
| EP-7 | Phased rollout + rollback framework | All cohorts | Cross-cutting | Discovery |

---

## EP-1: DAX Availability API + UBIF Orchestration

**Goal:** Replace UBIF→ServiceBench replication with a single real-time availability and reservation API. ServiceBench calls DAX; UBIF calls are orchestrated live.

**Linked FRs:** FR-1, FR-2, FR-6  
**Architecture blockers:** A1, A2, D1, D2, D3, D4, E2 — `[BLOCKED]` until resolved

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP1-S1 | ServiceBench consumer | A single DAX endpoint to check SUR part availability per part line | I get real-time data without replication lag | (1) API returns availability flag, JIT flag, shipping days out, bypass flag, Asurion+OEM SKUs per part line. (2) Response time ≤ SB local-lookup baseline. (3) Existing UBIF replication feed is deprecated for migrated stores. | P0 | A1, A2, D1, D2 |
| EP1-S2 | ServiceBench consumer | Distro Vendor indicator returned in the same availability API response | I don't need a separate distro catalog feed | (1) Distro Vendor flag included per part line in same response as availability. (2) Distro replication feed deprecated. | P0 | D1 |
| EP1-S3 | DAX / ServiceBench routing | Logic to distinguish ISP vs SUR for stores that share the same ServiceBench ID | ISP availability calls don't mix with SUR availability calls | (1) Routing correctly separates ISP and SUR calls for same UBIF store ID in all test cases. | P0 | E2 |
| EP1-S4 | Store / portal user | Reservation ID included in orders sent to UBIF and DAX | Reservations are traceable end-to-end | (1) Reservation ID present in all UBIF and DAX order payloads. (2) ID can be used to look up reservation state. | P0 | D4 |

---

## EP-2: Part Price on Job/Claim

**Goal:** Set partner invoice price transactionally on the ServiceBench Job/Claim, deprecating the UBIF price replication feed.

**Linked FRs:** FR-3  
**Architecture blockers:** H1 (scope for 3rd party price)

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP2-S1 | Claims / finance user | Part price set on the ServiceBench Job at the time of transaction (UBIF Current State) | Franchise Co. reconciliation uses the transactional price, not replicated master | (1) Price is written to Job/Claim at transaction time. (2) Matches UBIF invoice price. (3) UBIF price replication feed deprecated for migrated stores. | P0 | — |
| EP2-S2 | Claims / finance user | Part price on Job/Claim for UBIF Next Gen | Same reconciliation fix applies to Next Gen stores | Same as EP2-S1, scoped to Next Gen stores. | P0 | — |
| EP2-S3 _(TBD)_ | Claims / finance user | 3rd party (NAOP/AOP) price on Job/Claim | Consistent pricing across all SUR providers | Scope: TBD pending OQ H1 resolution. | TBD | H1 |

---

## EP-3: NAOP Migration — Mobile Clinic + Mexico

**Goal:** Repoint TELUS/Mobile Clinic and ATT Mexico/Telcel inventory feeds from RTI Webservice to DAX IVS API.

**Linked FRs:** FR-4  
**Architecture blockers:** B1, B2, C6 — `[BLOCKED]` until TELUS Plan A/B decision (B1)

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP3-S1 | TELUS / Mobile Clinic provider | Inventory feed repointed to DAX IVS API (AWS/JSON) | SUR availability is consistent with DAX/SSOT | (1) RTI Webservice fully replaced by DAX IVS API for TELUS. (2) All LCM perils available in feed. (3) 30-day rollback validated. | P1 | B1 (Plan A vs B decision) |
| EP3-S2 _(Plan A)_ | TELUS / Mobile Clinic provider | Full inventory feed for all perils (battery, camera, charging port, LCM) | No bypass exceptions needed; clean SSOT | (1) All peril types in DAX feed for TELUS. (2) No fake SKUs. (3) Bypass flag not required. | P1 | B1 |
| EP3-S2 _(Plan B fallback)_ | TELUS / Mobile Clinic provider | DAX returns peril+client bypass flag for non-LCM perils | Non-LCM jobs proceed without inventory check (technology concession) | (1) DAX BOM response includes bypass flag per peril+client config. (2) ServiceBench honors bypass flag. (3) LCM availability check still runs. | P1 | B1, B2 |
| EP3-S3 | ATT Mexico / Telcel provider | RTI Webservice repointed to DAX IVS API (AWS/JSON, direct) | Mexico feed migrates off RTI on same pattern as TELUS | (1) Direct DAX IVS API integration (not via L7). (2) SB Eng team owns web service post-migration. (3) Warehouse ID format standardized. | P1 | B4, E1 |

---

## EP-4: Soft Reservations via IVS

**Goal:** Close the 1–5 min availability gap between check and reservation by implementing IVS soft reservations at lead placement.

**Linked FRs:** FR-10  
**Architecture blockers:** C1, C4, C5 — `[BLOCKED]`

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP4-S1 | ServiceBench (booking) | IVS creates a soft reservation when a lead is placed | Available inventory decrements immediately, preventing overcommitment during the booking window | (1) Soft reservation created in IVS at lead placement. (2) Available quantity decrements. (3) Soft reservation ID returned to SB. | P0 | C1, C4 |
| EP4-S2 | ServiceBench (reservation) | Soft reservation reconciles with final store reservation | No double-deduction when the store confirms the repair | (1) Final reservation replaces soft reservation (no double-deduction). (2) If soft reservation expires or is cancelled, inventory is restored. | P0 | C5 |
| EP4-S3 | DAX / IVS | Soft reservation expiration model | Uncommitted soft reservations don't block inventory indefinitely | (1) Expiration model confirmed (auto-expire after X min OR store acknowledgment). (2) Expired soft reservations auto-release inventory. | P0 | C4 |

---

## EP-5: AOP Migration — 3rd Party Asurion-Owned Parts

**Goal:** Migrate full inventory lifecycle for 9 AOP service providers (~100 locations) from ServiceBench to DAX/D365. UI via Prism Elite (MFE or WMA).

**Linked FRs:** FR-5  
**Architecture blockers:** G1 (MFE vs WMA), G2 (Hydra identity) — `[BLOCKED]`

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP5-S1 | 3rd party AOP provider | Inventory orders, transfers, receiving, RMA, and cycle count in D365 | I no longer use ServiceBench for Asurion inventory lifecycle | (1) All lifecycle actions available in D365. (2) No ServiceBench dependency for AOP inventory. | P1 | G1 |
| EP5-S2 | 3rd party AOP provider | Access D365 inventory UI via Prism Elite (MFE or WMA) | I have a single system experience alongside my other Prism workflows | (1) Prism Elite embeds DAX MFE or WMA. (2) Provider can complete full lifecycle in one UI. (3) UI path confirmed (G1). | P1 | G1 |
| EP5-S3 | AOP provider (identity) | Log into Prism Elite using Hydra credentials | I don't need a separate Asurion account for inventory management | (1) Hydra guest account provisioned for AOP providers. (2) Email structure confirmed. (3) Identity flow tested for all 9 providers. | P1 | G2 |
| EP5-S4 | MDM / Robbie Carter | Automated SKU/MDM setup in DAX (no manual ServiceBench replication) | Setup is single-touch; no swivel-chair | (1) New part created in MDM → automatically available in D365 for AOP. (2) ServiceBench manual setup step eliminated. | P1 | F1, F2 |

---

## EP-6: BOM/MDM Automation + Substitution Matrix

**Goal:** Automate repair asset and BOM setup in DAX; migrate substitution matrix ownership to MDM/Tomlin.

**Linked FRs:** FR-9, FR-11  

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP6-S1 | MDM team | Single-touch BOM setup in DAX (Asurion + OEM SKUs) | No manual steps to replicate to ServiceBench | (1) BOM returns both Asurion and OEM SKUs for 3rd party providers. (2) Validated against Canada NAOP production job. (3) ServiceBench BOM setup deprecated. | P1 | F1 |
| EP6-S2 | MDM / Tomlin | Substitution matrix owned and maintained in DAX | Substitution rules are in SSOT, not siloed in ServiceBench | (1) Substitution matrix migrated to MDM/DAX. (2) Owner confirmed (H4). (3) Rose, Robbie Carter, Tomlin aligned. | P2 | H4 |
| EP6-S3 | MDM team | OEM equipment type confirmed for pricing/charging logic | OEM SKUs are priced correctly in D365 | (1) OEM equipment type definition confirmed (A3). (2) Pricing/charging logic handles OEM correctly. | P1 | A3 |

---

## EP-7: Phased Rollout + Rollback Framework

**Goal:** Deliver a controlled pilot-and-expand rollout strategy with a 30-day rollback capability for non-AOP cohorts.

**Linked FRs:** FR-7  

| Story | As a… | I want… | So that… | Acceptance criteria | Priority | Blocked by |
|-------|-------|---------|----------|---------------------|----------|-----------|
| EP7-S1 | Engineering / Ops | Feature flag per location/provider for DAX availability API | We can pilot with one store before broad rollout | (1) Flag toggleable per location. (2) Fallback reverts to ServiceBench local data. (3) 30-day rollback tested for UBIF. | P0 | — |
| EP7-S2 | Planning / Michelle | On-demand ordering confirmed for non-AOP 3rd party providers | Rollout plan is accurate | (1) On-demand ordering scope confirmed (D6). (2) Included or excluded in rollout plan. | P1 | D6 |

---

## Notes

- Stories marked `[BLOCKED]` require the referenced open question to be resolved before grooming. See `open-questions.md` for owner and status.
- Acceptance criteria are stubs — expand during architecture working sessions and grooming.
- Azure DevOps import: use Epics → Features → User Stories hierarchy. Epic IDs map to EP-1 through EP-7.
- This document is the source of truth for engineering backlog. Keep in sync with PRD FRs — when a FR changes, update the corresponding epic/stories here.
