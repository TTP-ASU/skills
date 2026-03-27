# Project Latest Update — Week of March 27, 2026

**Audience:** Upper leadership · **Project:** APC-2299 SUR SSOT · **Post to:** [APC-2299 project page](https://www.notion.so/3179532a1f8680daad25f1f0a0215679) (append this section; do not replace prior history)

---

## Progress

| Area | Status |
|------|--------|
| Q1 F-1 (transactional part price on Job/Claim) | In delivery; unblocked |
| Q2 F-2 (availability + orchestration + JIT) | Combined BOM/availability API design confirmed; reservation/JIT **separate APIs** decided; remaining Q2 architecture items: bypass logic (**A2**), formal **I1** sign-off, **I4** peril-change sub-path, **A5** job-type nomenclature |
| Q2 F-3 (BOM/MDM + substitution) | Blocked on **F1** (ServiceBench field table) and **I3/H4** (substitution matrix approach + ownership) |
| F-4 soft reservations | **On hold** until **H8** scope confirmation; **[ARCH]** C1/C4/C5 if in scope |
| Q3 AOP / WMA | WMA path confirmed (G1 resolved); identity (**G2**) and UI vs API (**H15/H16**) still open; **[WMA–SB Cycle Count Tool Gap Analysis](https://www.notion.so/asurionproduct/WMA-SB-Cycle-Count-Tool-Gap-Analysis-32f9532a1f868024b736fa8dfabf21ea)** added as pre-Q3 input for flow review |
| Operational risk | **L1** repair funnel reporting degraded post-Prism migration — baseline measurement at risk; **L2** SUR volume decline — root cause TBD before attributing SSOT outcomes |

---

## Proposed roadmap and SUR job impact (after each phase, pending rollout)

Percentages are **share of US SUR jobs** (SCM channel mix — simple average ATT + Verizon FY 2026), not absolute counts. **No production store cutover in Q2**; UBIF benefits realize as stores enable in **Q3** per rollout plan (**Assumption A** = all UBIF Next Gen enabled by end of Q3). Absolute job volumes depend on finalized rollout schedule and baseline job counts — **TBD with ops**.

| Quarter | Milestone (end of development) | Approx. share of SUR jobs touched when rollout complete for that phase | Notes |
|---------|----------------------------------|------------------------------------------------------------------------|-------|
| **Q1 2026** | Transactional part price on Job/Claim (UBIF Current State + Next Gen) | **~96%** (all UBIF in-store + UBIF remote tech — **pricing** on claims) | Does not change real-time inventory path yet |
| **Q2 2026** | DAX availability + reservation + JIT APIs built and validated; BOM/substitution work advanced | **0%** on new inventory orchestration at stores (build/test only) | **Readiness** for ~**96%** of SUR jobs once Q3 store enablement executes; soft reservations only if **H8** confirms F-4 in scope |
| **Q3 2026** | AOP inventory lifecycle in D365 + UBIF store enablement on DAX orchestration (rollout) | **~96%** UBIF + **~3.5%** 3rd-party remote tech (AOP) ≈ **~99.5%** of US mix excl. depot (~1%) and **NAOP (TBD)** | Shrink / savings milestones per PRD; **H1** pricing scope for 3rd party still open |
| **Q4 2026** | NAOP (Canada / Mexico) on DAX IVS pattern | **NAOP share TBD** (not in ATT/Verizon US mix slide); depot ~**1%** scope **TBD** (**K1**) | TELUS **B1/B2** and Mexico routing **J3** gate design |

---

## Focus next week

- Open questions session: close **A3**, **A5**, **F1** scheduling, **H8**, **I1/I4**, **K3** prerequisite, **L1/L2** ownership
- WMA / cycle count: user-flow workshops informed by gap analysis page
- BeyondX / F-3a: confirm priority vs **A3/F1** blockers (per TRD gap assessment)

---

## Decisions needed (leadership level)

| Decision | Why it matters |
|----------|----------------|
| **H8** — Is soft reservation (F-4) in this program or a follow-on? | Unblocks or defers major IVS reservation architecture (**C1/C4/C5**) |
| **L1** — Who funds/owns repair funnel reporting fix? | SSOT success metrics require a credible baseline |
| **L2** — Accept investigation of SUR volume decline before locking SSOT attribution? | Avoid misreading launch outcomes |

---

## Risks

| Risk | Mitigation |
|------|------------|
| F-3a / config mappings lagging vs dated targets | PM escalation with BeyondX; align to **F1/A3** |
| Q2 ADO hygiene (missing stories, Feature 679641 split) | PM + leads: create grooming-ready stories; split rollout vs AOP ordering features |
| AOP count **H17** (8 vs 9 companies) | Confirm before warehouse and identity sizing |

---

*Source: PRD §11 roadmap, open-questions.md, Strategy Discussion 2026-03-26, TRD grooming readiness §15. Local draft — sync to Notion on approval.*
