# ServiceBench Part Master — Field table

**[STUB — pending OQ F1 completion]**  
Raghu / SCM to deliver the authoritative table (field name, definition, options, mandatory/optional). Replace stub rows; remove this banner when F1 is resolved.

**Owner:** Raghu / SCM · **OQ:** F1 in `01-discovery/open-questions.md`

---

## Expected column shape (target schema)

| Field name | Definition | Options / values | Mandatory? | Maps to DAX/F&O field | Notes |
|------------|------------|--------------------|------------|------------------------|-------|
| _(pending)_ | | | | | |

---

## Partial fields (from OQ F1 Answer / Parts Walkthrough — pre–full table)

These rows are **provisional** until the comprehensive SB field documentation arrives.

| Field name | Definition | Options / values | Mandatory? | Maps to DAX/F&O field | Notes |
|------------|------------|--------------------|------------|------------------------|-------|
| Shipping Days Out | Lead time / days-out signal for scheduling | TBD per SCM (legacy: batteries vs non-batteries in SB) | TBD | F&O product master lead time (direction per EA / Part Rel Mgmt) | Confirmed as concept; exact SB field name TBD |
| Retailer linkage | BOM item linked to retailers (e.g., AT&T, Verizon) | Per retailer | TBD | TBD | Parts Walkthrough |
| Job type eligibility | Exclusions for which job types a part supports | Toggle / “job types not offered” | TBD | Part attribute in DAX (data layer; SB adjudicates — A4 direction) | SB SKU-level today |
| Part prioritization priority | Substitution / priority rank | 1–3 typical | TBD | Replacement matrix / EIAA (I1, I3) | Aligns with “God API” discussion |
| JIT flag | Orderability when not in stock | TBD | TBD | `AllowJustInTime` / availability API (see `dax-repos/inventory-api.md`) | Cross-check DAX |
| Lead time | Days out for JIT / scheduling | e.g., batteries 7d, non-batteries 3d (configurable SCM) | TBD | `LeadTimeInDays` in DAX API | D2 resolved for DAX side |
| Client-specific prioritization exceptions | Exceptions to default prioritization | Per client | TBD | TBD | Part Rel Mgmt notes |

---

## How to complete this document

1. Ingest Raghu’s delivered file: `Ingest document: @servicebench-docs/<file>` (see [`../../COMMANDS.md`](../../COMMANDS.md)).
2. Update `01-discovery/open-questions.md` — F1 → Resolved with source and date.
3. Fill TRD §4 Data Mapping in `PRD-Technical-Development-Requirements-SSOT-SUR.md`.
4. Re-evaluate `Blocked by: F1` on EP5-S4, EP6-S1; promote to **Grooming Ready** when F1 and F2 (as applicable) are clear.
