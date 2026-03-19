# Open questions – SSOT-SUR

Track open questions here. When a question is answered, update **Status** to Resolved, fill **Answer** and **Date**, then update the relevant section in the Brief or PRD.

Grouped by theme. **Architecture questions** (from design/engineering sessions) are flagged with `[ARCH]` and must be resolved before the relevant functional requirement can be fully specified.

---

## A. Peril Mapping & Equipment Type

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| A1 | **[ARCH]** Who owns peril-to-equipment-type translation: DAX or ServiceBench? Whoever owns this also owns the configuration flag that drives inventory lookup bypass. | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | Matt (DAX) proposed DAX takes ownership — consolidating peril determination, replacement matrices, and substitution logic into a unified API. Ankit reviewing; EA feedback expected 2026-03-19. Full decision at architecture review (est. week of 2026-03-24). | |
| A2 | **[ARCH]** Should the "bypass inventory check" logic be driven by peril + client configuration in DAX (recommended), or should ServiceBench own the client-level config to proceed without a BOM? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | Matt's proposal aligns with the existing recommendation: peril + client config in DAX. Ankit reviewing; pending EA confirmation at architecture review (est. week of 2026-03-24). Per SSOT EA Support (1), 2026-03-18. | |
| A3 | OEM parts equipment type: what is the correct type for pricing/charging logic? Needs verification before BOM can return OEM SKUs. | Meeting: DAX-SB Integration (Mar 6) | MDM / SCM | Open | | |
| A4 | **[ARCH]** Can job type exclusions (currently at SKU level in ServiceBench) be modeled at equipment-type level in F&O/D365 instead, or must they remain SKU-level? Job type concept doesn't currently exist in F&O. | Meeting: JIT (Mar 6) | Robbie Carter / DAX | Open | | |

---

## B. TELUS / Mobile Clinic (Canada) Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| B1 | **[ARCH]** TELUS/Mobile Clinic only provides LCM inventory. For non-LCM perils (battery, charging port, camera), no BOM/availability check happens today, and jobs are created without part lines. Plan A: push TELUS to provide full inventory for all part types. Plan B: return a "bypass inventory check" flag per peril+client. Which path? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX / TELUS rel. | Open | | |
| B2 | **[ARCH]** Should the "bypass inventory" flag live in DAX's BOM response or in ServiceBench's client-level config? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | | |
| B3 | What is the timing of TELUS CRM project migration, and does that change the preferred path for inventory integration? | Meeting: DAX-SB Integration (Mar 6) | Business / TELUS rel. | Open | | |
| B4 | Mexico/Mobile Clinic: currently use RTI webservice (web service calls, not file-based). Will they switch to AWS/JSON as part of this project? Who takes over the web service when feeds move to DAX? | Meeting: DAX-SB Integration (Mar 6) | SB Eng / DAX | Open | | |

---

## C. Reservation Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| C1 | **[ARCH]** Who owns the reservation lifecycle end-to-end? ServiceBench initiates soft reservation via IVS; store creates final reservation. Ownership of state transitions must be defined. | Meeting: Reservations Design (Mar 4) | DAX / SB Arch | Open | | |
| C2 | **[ARCH]** Is the 1–5 minute timing gap between availability check and real reservation creation materially impacting business outcomes today? Is soft reservation a near-term necessity or a longer-term optimization? | Meeting: Reservations Design (Mar 4) | Bryant / Ops | Open | | |
| C3 | Should soft reservations apply to all providers or only select ones? | Meeting: Reservations Design (Mar 4) | DAX / SB Arch | Open | | |
| C4 | **[ARCH]** Expiration model for soft reservations: auto-expire after X minutes, or confirmed only by store acknowledgment? What's the rollback if a reservation isn't converted? | Meeting: Reservations Design (Mar 4) | DAX Arch | Open | | |
| C5 | **[ARCH]** How do we prevent double-deduction during reconciliation when soft reservation is followed by store reservation event? | Meeting: Reservations Design (Mar 4) | DAX Arch | Open | | |
| C6 | **[ARCH]** UBIF Legacy: reservation concept is difficult to implement. Option A: return "not-reservable" response for legacy providers. Option B: ServiceBench always reserves, DAX overrides for legacy providers via backend. Which is preferred? | Meeting: DAX-SB Integration (Mar 6) | DAX / SB | Open | | |
| C7 | Mobile Clinic: not tracking reservations today. Is it worth adding reservation tracking in the future state, or leave as not-reservable? | Meeting: DAX-SB Integration (Mar 6) | DAX / SB | Open | | |

---

## D. JIT Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| D1 | **[ARCH]** Should the availability API return both in-stock status and JIT eligibility as separate flags per part line, or a single combined response? | Meeting: JIT (Mar 6) | DAX Arch | Open | | |
| D2 | **[ARCH]** Should shipping days out be included in the availability API response (for appointment scheduling by Horizon/ServiceBench)? | Meeting: JIT (Mar 6) | DAX Arch | Open | | |
| D3 | **[ARCH]** Should job type exclusion information be evaluated before the availability check (in the request) or returned in the response for the consumer to act on? | Meeting: JIT (Mar 6) | DAX Arch | Open | | |
| D4 | **[ARCH]** Should reservation and JIT order creation be a single combined call or kept as separate API calls? | Meeting: JIT (Mar 6) | DAX Arch | Open | | |
| D5 | Who maintains the "quantity one" records in ServiceBench for distro and WLI JIT (signals orderability, not true inventory)? Kelly Shaw or Pat Clark? Needs owner before migration. | Meeting: JIT (Mar 6) | Pat Clark / Kelly Shaw | Open | | |
| D6 | On-demand ordering for non-AOP providers: is this in scope? Needs confirmation from planning team. | Meeting: JIT (Mar 6) | Planning / Michelle | Open | | |

---

## E. Warehouse & Routing Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| E1 | **[ARCH]** How will vendors identify warehouses in the future-state DAX IVS API? Format standardization needed to match UBIF JSON format. | Meeting: DAX-SB Integration (Mar 6) | DAX / SB Eng | Open | | |
| E2 | **[ARCH]** Same UBIF store has same ServiceBench ID for both ISP and SUR. What routing logic will distinguish ISP vs SUR requests? (DES uses SB account + pipe-delimited part location; ISP uses SB ID.) | Meeting: DAX-SB Integration (Mar 6) | DAX / SB Eng | Open | | |

---

## F. SKU / MDM Setup

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| F1 | What ServiceBench part setup fields must be replicated in DAX/F&O? (Need complete table: field name, definition, options, mandatory/optional.) Created Mar 16 action item: Amir to send recording; Raghu to present comprehensive field table. | Meeting: Parts Walkthrough (Mar 16) | Raghu / SCM | Open | Parts Walkthrough confirmed: SB setup is done via file import or Part Master Maintenance UI. Each BOM item linked to specific retailers (AT&T, Verizon, etc.). Fields include Shipping Days Out and retailer linkage. Raghu's action item to create full field table is still pending as of 2026-03-16. | |
| F2 | MDM setup process in DAX: is it manual (import or UI) or can it be automated? Who owns MDM setup in the future state? | Meeting: Parts Walkthrough (Mar 16) | MDM Team | Open | Parts Walkthrough confirmed: current SB setup can be done via file import or UI. Future state = MDM owns single setup in DAX (DES/NDS precedent confirmed). MDM team follow-up still required on automation path. | |
| F3 | Is the "magic tool" (single-touch SKU creation across DAX, ServiceBench, UBIF Portal) still a viable concept from the Kaizen event? Who owns it? | Meeting: Parts Walkthrough (Mar 16) | MDM / SCM / Ops | Open | | |

---

## G. Identity & UI for 3rd Party AOP

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| G1 | **[ARCH]** DAX MFE in Prism Elite (TypeScript React) vs WMA: which path for rollout to 3rd party AOP providers? | Meeting: JIT (Mar 6); PRD | DAX / Prism | Open | WMA Phase 1 confirmed for AOP back-of-house inventory (DDD features 25–30, architecture diagram). **Web-based WMA explicitly ruled out** 2026-03-18 — certification burden, performance concerns for chatty operations (inventory counting), and user management complexity. Native WMA app continues for back-of-house. ISP picking/return screens will be first-class in UBIF Next Gen Portal (separate track, not WMA — action item for ISP team). Phase 2 Single Pane of Glass optional, not committed. New open: whether AOP 3rd party locations need WMA UI at all or only systematic API (H15). Per WMA ISP / 3rd Party meeting 2026-03-18. | |
| G2 | **[ARCH]** Identity management for 3rd party providers in Prism Elite: UBIF uses @ubifipx.com with Hydra guest accounts into Asurion tenant. What email/identity structure do 3rd party AOP providers use? Should Corey Street be brought in for Hydra guest account design? | Meeting: JIT (Mar 6) | Sandeep / Corey Street | Open | User management challenges confirmed 2026-03-18: high turnover, multiple workers per location across 9 AOP stores. Alternative noted: dollar sign users or non-Asurion tenant users instead of Hydra guest accounts. UBIF guesting process exists (Brent Moore creates user/worker records). Prereq: determine # of users + turnover rate + who manages 3rd party AOP providers (equivalent to Renee for CA, Alex for MX). Clarify Prism UI access (H16) before designing identity model. | |

---

## H. Scope / Product

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| H1 | ServiceBench local price copy for 3rd party claims—in scope for this project? | PRD §3 | Bryant Mayne | Open | Tied to FR-3. UBIF claims move to transactional price via EP2-S1/S2 (unblocked). 3rd party (NAOP/AOP) local price copy is a separate question — scope not confirmed. EP2-S3 is blocked pending this answer. | |
| H2 | BAU Portal feed migration—when/if in scope? | Brief §5 | Bryant Mayne | Open | Out of scope until explicitly confirmed. Referenced in PRD §9 Appendix (out of scope list). | |
| H3 | Enterprise architecture assignment: is Ankit / Tim Clemens formally on the project? Leadership has not confirmed EA involvement yet. | Meeting: Parts Walkthrough (Mar 16) | Bryant / Leadership | Resolved | Ankit confirmed engaged: attended SSOT EA Support (1) meeting 2026-03-18, formally reviewing architecture proposal, EA feedback expected 2026-03-19. Tim Clemens named EA co-owner. Bryant scheduling broader architecture review for week of 2026-03-24. | 2026-03-18 |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose—who owns requirements and configuration in DAX? Meeting to be scheduled upon Tomlin's return. | Meeting: DAX-SB Integration (Mar 6) | SCM / MDM | Open | Blocks EP6-S2. I3 is the related architecture question (Replacement Matrix reuse vs new entity). Both H4 and I3 must resolve before EP6-S2 can be groomed. | |
| H5 | Scalability implications for IVS with soft reservations at UBIF scale (~800 locations)? | Meeting: Reservations Design (Mar 4) | DAX Arch | Open | NFR-2 depends on this. EP4 (soft reservations) cannot finalize design without a scalability analysis. Needed before EP4 stories move from Draft. | |
| H6 | **UBIF Legacy scope:** Do we need to solution for Legacy UBIF at all, given that all stores are expected to fully migrate to Next Gen by Q3? If yes, is the Legacy solution a temporary bridge only, or full parity with Next Gen? ADO Feature 677454 may be out of scope. | PRD review (Mar 16) | Bryant / Michelle Bowersox | Open | ADO Feature 677454 flagged ⚠️ in TDR as potentially out of scope. If Legacy scope is removed, RT-2 (UBIF Legacy availability flow) and EP3-S3 reservation approach become moot. Confirm before Q1 grooming. | |
| H7 | **EP-2 needed?** Is "Part price on Job/Claim" in scope for this project as a standalone epic, or is it already covered under the UBIF orchestration feature (677038)? Placeholder only — confirm before grooming. | PRD review (Mar 16) | Michelle Bowersox | Open | EP2-S1 and EP2-S2 are unblocked and could be groomed as soon as epic scope is confirmed. If EP-2 merges into EP-1 (677038), the stories still exist — just the epic boundary changes. | |
| H8 | **EP-4 needed?** Is "Soft reservations via IVS" in scope for this project, or is it a separate enhancement initiative? Placeholder only — confirm before grooming. | PRD review (Mar 16) | Michelle Bowersox | Open | If EP-4 is confirmed in scope, it is blocked by C1, C4, C5, I2 — all [ARCH] open. If it is a separate initiative, EP4 stories should be removed from this TDR. Confirm before Q2 planning. | |
| H9 | AgioTech / TechPeople (NAOP) — confirmed in scope? Same Tyk API contract as other NAOP vendors? | Parts Mgmt Flows PDF | Bryant / Amir | Open | Appears in Parts Mgmt Flows diagram as a NAOP vendor. If confirmed, they would follow the INT-3 (other NAOP) flow and the same Tyk API contract as INT-1/INT-2. | |
| H10 | EU vendors (AsurionEU / Tesco / VirginMobile) — in scope for this project? Same RTI → Tyk repoint pattern as CA/LATAM? | Parts Mgmt Flows PDF | Bryant / Leadership | Open | Appears in Parts Mgmt Flows diagram. If in scope, pattern is the same RTI → Tyk repoint. No separate architecture needed — confirm scope only. | |
| H12 | US NEW (ATTRepair / Verizon clients) — what is this new client group shown in Parts Mgmt Flows? Scope and timeline for inclusion? | Parts Mgmt Flows PDF | Bryant | Open | Appears as "US NEW" in Parts Mgmt Flows diagram alongside existing US UBIF clients. Unclear if this is a new channel, a rebrand, or a future-state group. Needs clarification before any INT flow can be scoped for them. | |
| H14 | Order types in scope: Replenishment (auto), Restock (manual), SURJIT (auto) — confirmed in scope alongside On-demand (D6)? Or are only some order types migrating to DAX? | Parts Mgmt Flows PDF | Bryant / Michelle Bowersox | Open | Parts Mgmt Flows PDF and SSOT Parts Mgmt Walkthrough confirmed 4 order types for AOP: Replenishment (auto), Restock (manual), On-demand (manual), SURJIT (auto). On-demand is tracked separately as D6. This question confirms whether all 4 migrate or only a subset. Replenishment, Restock, and SURJIT appear confirmed in DDD features 19–24. | |
| H15 | Do 3rd party AOP locations need a WMA inventory management UI, or only systematic API/RTI integration (no UI needed)? | WMA ISP / 3rd Party meeting 2026-03-18 | Bryant / Avengers | Open | Per meeting: 9 US AOP stores currently use ServiceBench mobile app for job updates (not Field App). Web-based WMA ruled out. If AOP locations only need API-level inventory sync with no user-facing UI, EP5-S2 scope changes significantly. Thays to gather work instructions from 3rd party providers on current inventory processes. | |
| H16 | Will 3rd party AOP locations have Prism UI access? | WMA ISP / 3rd Party meeting 2026-03-18 | Bryant / SB Team | Open | Action item from 2026-03-18 WMA meeting: clarify with ServiceBench/Prism team. Impacts G2 (identity/access model) and EP5-S3 (Hydra identity story). Must be answered before identity design can proceed. | |

---

## I. API Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| I1 | **[ARCH]** BOM Lookup architecture: embed BOM lookup inside the EIAA (Early Inventory Availability API) as a single orchestrated call (DDD Option 2 / feature 3) — OR — expose as a separate BOM service that ServiceBench calls first (DDD Option 1 / feature 1)? Shown as "PRISM BOM?" open red question in architecture diagram. Impact: 1 vs 2 API calls at job creation. | DDD Feature 32; SSOT EA Support 2026-03-18; Architecture diagram | Ankit / DAPI Team / Integration Team | Open | | |
| I2 | AOP JIT reservation: is a reservation required for AOP JIT scenarios when inventory availability is false? DDD open item 33 leans toward no reservation in that case. Decision needed before EP-4/EP-5 stories can be groomed. | DDD Feature 33 | Avengers / DAX Arch | Open | DDD open item 33 direction: no reservation required when availability = false for AOP JIT. If confirmed, EP4-S1 and EP5-S1 blockers on I2 can be cleared. Decision must come from Avengers team + DAX Arch before grooming. | |
| I3 | Part Substitution Matrix vs Replacement Matrix: reuse existing Replacement Matrix with modified unique index/validation rules — OR — build a new F&O menu/form/table/data entity for part substitution? | DDD Feature 34 | Avengers / Robbie Carter / Rose | Open | DDD open item 34: leading option is reuse of Replacement Matrix with modified validation. New entity is the fallback if Replacement Matrix constraints are incompatible. Rose and Robbie Carter to confirm. Blocks EP6-S2 alongside H4. | |

---

**How to use with Cursor**

- Say "capture the answer: [question ID] was resolved: [answer]" and the agent will update the row and suggest edits to the PRD/Brief.
- Questions tagged `[ARCH]` block the relevant FR from being finalized. Resolve architecture decisions before grooming stories.
