# Open questions – SSOT-SUR

Track open questions here. When a question is answered, update **Status** to Resolved, fill **Answer** and **Date**, then update the relevant section in the Brief or PRD.

Grouped by theme. **Architecture questions** (from design/engineering sessions) are flagged with `[ARCH]` and must be resolved before the relevant functional requirement can be fully specified.

---

## A. Peril Mapping & Equipment Type

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| A1 | **[ARCH]** Who owns peril-to-equipment-type translation: DAX or ServiceBench? Whoever owns this also owns the configuration flag that drives inventory lookup bypass. | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | | |
| A2 | **[ARCH]** Should the "bypass inventory check" logic be driven by peril + client configuration in DAX (recommended), or should ServiceBench own the client-level config to proceed without a BOM? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | Recommendation: peril + client config, not fake SKUs | |
| A3 | OEM parts equipment type: what is the correct type for pricing/charging logic? Needs verification before BOM can return OEM SKUs. | Meeting: DAX-SB Integration (Mar 6) | MDM / SCM | Open | | |
| A4 | **[ARCH]** Can job type exclusions (currently at SKU level in ServiceBench) be modeled at equipment-type level in F&O/D365 instead, or must they remain SKU-level? Job type concept doesn't currently exist in F&O. | Meeting: JIT (Mar 6) | Robbie Carter / DAX | Open | | |

---

## B. TELUS / Mobile Clinic (Canada) Architecture

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| B1 | **[ARCH]** TELUS/Mobile Clinic only provides LCM inventory. For non-LCM perils (battery, charging port, camera), no BOM/availability check happens today, and jobs are created without part lines. Plan A: push TELUS to provide full inventory for all part types. Plan B: return a "bypass inventory check" flag per peril+client. Which path? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX / TELUS rel. | Open | | |
| B2 | Should the "bypass inventory" flag live in DAX's BOM response or in ServiceBench's client-level config? | Meeting: DAX-SB Integration (Mar 6) | Ankit / DAX Arch | Open | | |
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
| C6 | UBIF Legacy: reservation concept is difficult to implement. Option A: return "not-reservable" response for legacy providers. Option B: ServiceBench always reserves, DAX overrides for legacy providers via backend. Which is preferred? | Meeting: DAX-SB Integration (Mar 6) | DAX / SB | Open | | |
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
| F1 | What ServiceBench part setup fields must be replicated in DAX/F&O? (Need complete table: field name, definition, options, mandatory/optional.) Created Mar 16 action item: Amir to send recording; Raghu to present comprehensive field table. | Meeting: Parts Walkthrough (Mar 16) | Raghu / SCM | Open | | |
| F2 | MDM setup process in DAX: is it manual (import or UI) or can it be automated? Who owns MDM setup in the future state? | Meeting: Parts Walkthrough (Mar 16) | MDM Team | Open | | |
| F3 | Is the "magic tool" (single-touch SKU creation across DAX, ServiceBench, UBIF Portal) still a viable concept from the Kaizen event? Who owns it? | Meeting: Parts Walkthrough (Mar 16) | MDM / SCM / Ops | Open | | |

---

## G. Identity & UI for 3rd Party AOP

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| G1 | **[ARCH]** DAX MFE in Prism Elite (TypeScript React) vs WMA: which path for rollout to 3rd party AOP providers? | Meeting: JIT (Mar 6); PRD | DAX / Prism | Open | | |
| G2 | **[ARCH]** Identity management for 3rd party providers in Prism Elite: UBIF uses @ubifipx.com with Hydra guest accounts into Asurion tenant. What email/identity structure do 3rd party AOP providers use? Should Corey Street be brought in for Hydra guest account design? | Meeting: JIT (Mar 6) | Sandeep / Corey Street | Open | | |

---

## H. Scope / Product

| # | Question | Source | Owner | Status | Answer | Date |
|---|----------|--------|-------|--------|--------|------|
| H1 | ServiceBench local price copy for 3rd party claims—in scope for this project? | PRD §3 | TBD | Open | | |
| H2 | BAU Portal feed migration—when/if in scope? | Brief §5 | TBD | Open | Out of scope until explicitly confirmed. | |
| H3 | Enterprise architecture assignment: is Ankit / Tim Clemens formally on the project? Leadership has not confirmed EA involvement yet. | Meeting: Parts Walkthrough (Mar 16) | Bryant / Leadership | Open | | |
| H4 | Substitution matrix: Tomlin + Robbie Carter + Rose—who owns requirements and configuration in DAX? Meeting to be scheduled upon Tomlin's return. | Meeting: DAX-SB Integration (Mar 6) | SCM / MDM | Open | | |
| H5 | Scalability implications for IVS with soft reservations at UBIF scale (~800 locations)? | Meeting: Reservations Design (Mar 4) | DAX Arch | Open | | |

---

**How to use with Cursor**

- Say "capture the answer: [question ID] was resolved: [answer]" and the agent will update the row and suggest edits to the PRD/Brief.
- Questions tagged `[ARCH]` block the relevant FR from being finalized. Resolve architecture decisions before grooming stories.
