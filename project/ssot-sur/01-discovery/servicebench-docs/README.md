# ServiceBench — Field reference (SSOT-SUR)

**Status:** Partial — full Part Master Maintenance field table is **pending OQ F1** (Raghu / SCM).  
**Last updated:** 2026-03-20

This folder holds ServiceBench field documentation for data mapping and acceptance criteria. It is intentionally asymmetric with [`../dax-repos/`](../dax-repos/README.md): DAX read/write paths are confirmed from Confluence + GitHub; ServiceBench’s authoritative field list is still being delivered.

---

## Asymmetry: DAX vs ServiceBench

| Side | Status | Source |
|------|--------|--------|
| DAX read path (availability, parts, warehouse) | Confirmed | [`../dax-repos/inventory-api.md`](../dax-repos/inventory-api.md) |
| DAX write path (fulfillment, consumption DTOs) | Confirmed | [`../dax-repos/github-repos.md`](../dax-repos/github-repos.md) |
| ServiceBench Part Master Maintenance (full field table) | **Pending F1** | This folder — [`field-table.md`](field-table.md) (stub until Raghu delivers) |

---

## What is known today (from OQ F1 notes and Parts Walkthrough)

Extracted from `01-discovery/open-questions.md` (F1) and related meetings — **not** a substitute for Raghu’s comprehensive table:

- Shipping Days Out
- Retailer linkage (e.g., AT&T, Verizon) per BOM item
- Job type eligibility toggles (“job types not offered” / exclusion model)
- Part prioritization priority (1–3)
- JIT flag; lead time (e.g., batteries vs non-batteries — direction moving to DAX product master)
- Client-specific prioritization exceptions

SB setup today: file import or Part Master Maintenance UI; future state = MDM single setup in DAX (DES/NDS precedent) per F2.

---

## What is blocked

| Blocker | Owner | Impact |
|---------|-------|--------|
| Full field table: name, definition, options, mandatory/optional | Raghu / SCM (OQ F1) | TRD §4 Data Mapping cannot be completed |
| Formal SB → DAX/F&O mapping per field | Architecture / MDM after F1 | EP5-S4, EP6-S1 AC cannot be fully specified |

---

## Stories / sections blocked until F1 resolves

- **TRD §4** — Data Mapping (placeholder until F1)
- **EP5-S4** — Automated SKU/MDM setup (`Blocked by: F1, F2`)
- **EP6-S1** — Single-touch BOM setup (`Blocked by: F1`)

---

## Cross-references

- **DAX validation:** [`../dax-repos/README.md`](../dax-repos/README.md)
- **Open question F1:** `01-discovery/open-questions.md` — section F · SKU / MDM Setup
- **TRD:** `01-discovery/PRD-Technical-Development-Requirements-SSOT-SUR.md` — §4 Data Mapping

When Raghu delivers the full field table, use **`Ingest document: @servicebench-docs/[file]`** (see [`../../COMMANDS.md`](../../COMMANDS.md)) to populate `field-table.md`, then cascade updates to TRD §4 and story blockers.
