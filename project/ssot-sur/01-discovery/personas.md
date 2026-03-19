# SSOT-SUR Personas

**Last updated:** 2026-03-18 (WMA ISP / 3rd Party meeting incorporated)  
**Status:** Draft — current/future state tables; identity and UI path decisions partially resolved.

> Personas map operational users to flows and open questions. They are not marketing personas — they describe who interacts with the system, what they need, and what blocks us from designing for them.

---

## Persona index

| ID | Name | System today | System future | Phase | Key open Qs |
|----|------|-------------|---------------|-------|-------------|
| P1 | AOP Provider | ServiceBench | Native WMA app (Phase 1 confirmed; web-based WMA ruled out) | Q3 | G1, G2, H15, H16, I2 |
| P2 | Store / Portal Technician (UBIF) | Horizon → ServiceBench | Horizon → ServiceBench → EIAA (real-time) | Q1 | A1, A2, D1–D4 |
| P3 | NAOP Vendor (Canada / Mexico / others) | RTI Webservice → ServiceBench | Tyk API Connect → DAX IVS | Q2 | B1, B2, B4, H9 |
| P4 | Claims / Finance User | ServiceBench (replicated part price) | ServiceBench (transactional price on Job/Claim) | Q1/Q2 | H1 |
| P5 | MDM / Supply Chain Operator | DAX MDM + manual ServiceBench replication | DAX MDM only (single setup) | Q3/Q4 | F1, F2, H4, I3 |
| P6 | Operations / Dispatch | ServiceBench JIT config (quantity-one records) | D365 / DAX JIT config | Q1 | D5, A4 |
| P7 | Service Job Consumer (Horizon) | Horizon triggers SB availability check (local replica) | Horizon triggers SB → EIAA → real-time availability | Q1 | — |

---

## P1 — AOP Provider

**3rd party Asurion-owned parts provider · ~9 US stores · ~100 locations · Remote tech only**

|| | Current state | Future state |
||-|---------------|--------------|
|| **System used** | ServiceBench.com + ServiceBench mobile app for job updates (not Field App) | **Native WMA app (Phase 1 confirmed)**. Web-based WMA (portal-embedded wrapper) evaluated and **ruled out 2026-03-18** — certification burden, performance issues for chatty operations, user management complexity. WMA accessed via link in Prism. Optional Prism Single Pane of Glass Phase 2 (not committed). |
|| **Job to be done** | Order parts (replenishment, restock, on-demand, SURJIT), receive inventory, transfer between locations, perform cycle counts, process RMAs | Same functions — all in DAX/D365 via native WMA. Whether full WMA UI is needed or systematic API-only TBD (H15). |
|| **How they access inventory** | ServiceBench login; all AOP lifecycle functions in SB UI | Link in Prism → native WMA; no ServiceBench login required. Access model TBD pending Prism UI access confirmation (H16). |
|| **Identity** | ServiceBench account | TBD — Hydra guest accounts (existing UBIF model), or dollar sign users / non-Asurion tenant users. High turnover + multiple workers/location complicates Hydra model. Identity design blocked on H16. (G2) |
|| **User management** | ServiceBench manages accounts per store | High turnover + multiple workers/location confirmed 2026-03-18. Need: # users across 9 stores, turnover rate, who manages 3rd party providers (equivalent to Renee for CA, Alex for MX). |
|| **Pain point today** | Must use ServiceBench as primary system; SB being decommissioned end of year; MDM data replicated manually | Single system (native WMA) for all AOP lifecycle functions; no swivel-chair replication |
|| **Flows** | IL-1 (replenishment), IL-2 (restock), IL-3 (on-demand), IL-4 (SURJIT), IL-5 (receiving), IL-6 (transfers), IL-7 (RMA), IL-8 (cycle counting) |
|| **Phase** | Q3 |
|| **Open Qs** | G1 (native WMA confirmed; web-based ruled out 2026-03-18), G2 (identity model — blocked on H16), H15 (WMA UI vs API-only), H16 (Prism UI access confirmation), I2 (AOP JIT reservation when availability = false) |

---

## P2 — Store / Portal Technician (UBIF)

**UBIF Next Gen and Legacy store technicians · ~800 locations · Appointment-driven repair + ISP pickup**

|| | Current state | Future state |
||-|---------------|--------------|
|| **System used** | Horizon → ServiceBench (availability check using local replica). ISP technicians also use WMA app for picking operations during in-store pickup. | Horizon → ServiceBench → EIAA → real-time DAX availability. **ISP picking and return screens built natively in UBIF Next Gen Portal** (confirmed 2026-03-18 — not WMA). |
|| **Job to be done** | Check part availability before booking; confirm JIT eligibility; place parts order. ISP technicians additionally perform picking and return operations during customer pickup. | Same — availability is real-time, JIT flag returned per part line. ISP: picking/return natively in Next Gen Portal with no app-switching. |
|| **How they experience the change** | SB local data; can be stale by 1–5 min. ISP requires switching between Next Gen Portal and WMA during pickup (friction). | Real-time EIAA response; no local replica; part price on Job/Claim. ISP: no more app-switching — first-class picking/return UI in portal. |
|| **Pain point today** | Stale availability leads to incorrect decisions and broken appointments. ISP technicians must context-switch between Next Gen Portal and WMA during pickup. | Eliminated: single real-time call replaces three replication feeds. ISP friction removed with native picking/return UI. |
|| **Flows** | RT-1 (UBIF Next Gen availability), RT-2 (UBIF Legacy availability), RT-6 (JIT) |
|| **Phase** | Q1 (availability API). ISP picking UI: separate epic, timeline TBD. |
|| **Open Qs** | A1 (peril mapping owner), A2 (bypass flag owner), D1–D4 (API response design), E2 (ISP vs SUR routing) |

---

## P3 — NAOP Vendor (Canada / Mexico / others)

**3rd party Non-Asurion-Owned Parts vendors · TELUS/Mobile Klinik (CA), ATT Mexico/Telcel (MX), others**

| | Current state | Future state |
|-|---------------|--------------|
| **System used** | RTI Webservice → ServiceBench (feed-based, LCM only for CA/MX) | Tyk API Connect → DAX Americas Availability Service (AWS/JSON) |
| **Job to be done** | Provide inventory availability data to Asurion for service job creation | Same — via standardized Tyk API contract |
| **How they experience the change** | RTI Webservice feed (legacy integration); LCM perils only for TELUS; non-LCM jobs created without part lines | Repointed feed; Plan A (full inventory all perils, preferred) or Plan B (LCM-only + bypass flag, fallback for TELUS) |
| **Pain point today** | RTI is a legacy integration; TELUS unwilling to provide full inventory creates exception-handling complexity | Standardized API contract via Tyk; same pattern for all NAOP vendors |
| **Flows** | INT-1 (Canada), INT-2 (Mexico), INT-3 (other NAOP vendors), RT-3 (NAOP availability at job creation) |
| **Phase** | Q2 |
| **Open Qs** | B1 (TELUS Plan A vs B), B2 (bypass flag owner), B3 (TELUS CRM timing), B4 (web service ownership), H9 (AgioTech/TechPeople scope), H10 (EU vendors scope) |

---

## P4 — Claims / Finance User

**Internal finance and franchise reconciliation users · Job/Claim pricing accuracy**

| | Current state | Future state |
|-|---------------|--------------|
| **System used** | ServiceBench (replicated master price from UBIF) | ServiceBench (transactional partner invoice price on Job/Claim) |
| **Job to be done** | Reconcile part costs on claims; validate pricing for Franchise Co. billing | Same — with accurate transactional price instead of replicated master price |
| **Pain point today** | Replicated master price can differ from actual invoice price; Franchise Co. reconciliation errors | Transactional price eliminates reconciliation delta; price replication from UBIF deprecated |
| **Flows** | RT-2 (part price on Job/Claim via UBIF Legacy orchestration) |
| **Phase** | Q1/Q2 |
| **Open Qs** | H1 (ServiceBench local price copy for 3rd party claims — in scope?) |

---

## P5 — MDM / Supply Chain Operator

**Robbie Carter + Rose + MDM team · BOM, SKU setup, substitution matrix**

| | Current state | Future state |
|-|---------------|--------------|
| **System used** | DAX MDM (primary setup) + manual ServiceBench replication (swivel chair) | DAX MDM only — ServiceBench setup deprecated |
| **Job to be done** | Create and maintain SKUs, BOM entries, substitution rules; replicate to ServiceBench | Single setup in DAX; BOM returns Asurion + OEM SKUs; substitution matrix in F&O |
| **Pain point today** | Manual multi-system replication; multiple touchpoints for the same BOM entry; OEM equipment type unclear | Single-touch setup in DAX; ServiceBench setup deprecated; substitution matrix owned in F&O |
| **Flows** | CF-1 (SKU/MDM setup), CF-2 (BOM/OEM SKU setup), CF-3 (substitution matrix), CF-4 (New Part Master Config Module) |
| **Phase** | Q3/Q4 |
| **Open Qs** | F1 (SB field documentation required), F2 (MDM automation — manual vs automated), H4 (substitution matrix ownership), I3 (Replacement Matrix reuse vs new entity) |

---

## P6 — Operations / Dispatch

**Kelly Shaw / Pat Clark and UBIF Distro team · JIT eligibility configuration**

| | Current state | Future state |
|-|---------------|--------------|
| **System used** | ServiceBench (maintains "quantity one" records for JIT distro eligibility) | D365 / DAX (JIT config migrated) |
| **Job to be done** | Maintain distro eligibility records that signal JIT orderability per SKU; manage job-type exclusions | Same — in D365/DAX; job-type exclusion model (SKU vs equipment-type level) TBD |
| **Pain point today** | JIT "quantity one" is not true inventory (counts never decremented); config split across ServiceBench SKU-level exclusions | Ownership and model to be determined in architecture sessions |
| **Flows** | RT-6 (JIT availability + order) |
| **Phase** | Q1 |
| **Open Qs** | D5 (who owns "quantity one" records), A4 (job-type exclusion model: SKU vs equipment-type level in F&O) |

---

## P7 — Service Job Consumer (Horizon)

**End-consumer / Horizon platform · Repair booking trigger**

| | Current state | Future state |
|-|---------------|--------------|
| **System used** | Horizon → triggers ServiceBench availability check using local replicated data | Horizon → triggers ServiceBench → EIAA → real-time availability |
| **Job to be done** | Book a repair appointment with confirmed part availability | Same — with real-time availability and accurate JIT/bypass flags |
| **Pain point today** | Stale availability data can cause post-booking failures (part not actually available) | Real-time availability eliminates post-booking failures |
| **Flows** | RT-1 (UBIF Next Gen), RT-3 (NAOP), RT-4 (BOM lookup), RT-5 (soft reservation) |
| **Phase** | Q1 |
| **Open Qs** | — (flows through ServiceBench; no direct system change for consumer) |

---

## Persona × flow coverage matrix

| Persona | RT-1 | RT-2 | RT-3 | RT-4 | RT-5 | RT-6 | INT-1 | INT-2 | INT-3 | IL-1–8 | CF-1–4 |
|---------|------|------|------|------|------|------|-------|-------|-------|--------|--------|
| P1 AOP Provider | | | | | | | | | | X | |
| P2 Store Tech (UBIF) | X | X | | X | | X | | | | | |
| P3 NAOP Vendor | | | X | | | | X | X | X | | |
| P4 Claims/Finance | | X | | | | | | | | | |
| P5 MDM Operator | | | | X | | | | | | | X |
| P6 Ops/Dispatch | | | | | | X | | | | | |
| P7 Horizon Consumer | X | | X | X | X | | | | | | |

---

*Full open question detail: [01-discovery/open-questions.md](open-questions.md)*
