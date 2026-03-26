# DAX Repos — Discovery & Grooming Reference
## Project: SSOT-SUR · Compiled: 2026-03-20 · Updated: 2026-03-24 · Author: Thays Pritchard

**Purpose:** This folder is a PM research reference for the SSOT-SUR discovery and grooming phase. It documents DAX API field contracts, function behavior, and existing capabilities sourced from the DAX GitHub repos and Confluence. Use it to:
- Write accurate acceptance criteria using real DAX field names
- Identify what DAX already has vs. what needs to be built
- Ask informed questions during architecture and grooming sessions
- Avoid inventing field names or API shapes that don't match reality

**Source:** `asurion-private` GitHub org (read access confirmed 2026-03-24). ADO connection will be established when code reaches QA for validation.

---

## Files in this folder

| File | Contents | Use for |
|---|---|---|
| `README.md` | This file — cross-validation summary and overall findings | Start here |
| `inventory-api.md` | DAX Inventory API endpoints (from Confluence `DDD` space) — confirmed read-path schema | F-2 Availability AC |
| `github-repos.md` | Write-path repos under `asurion-private` — confirmed DTOs and event types | F-1 Part Price AC, F-5/F-7 migration context |
| `dax-daxapi.md` | Source analysis of `dax-daxapi` — all confirmed functions, field contracts, domain objects, IVS auth | F-2/F-4 grooming, architecture questions |
| `analysis-existing-vs-new.md` | What already exists in DAX vs. what DAX will build new — per 03/23 roadmap discussion | Scoping grooming sessions, identifying gaps |

---

## Cross-Validation: GitHub Repos vs. DAX Inventory API

The GitHub repos represent the **write path** (ServiceBench → DAX: orders, consumption, fulfillment).  
The Confluence API pages represent the **read path** (DAX IVS → inventory availability queries).  
Together they form the complete DAX data model for the SSOT-SUR project.

### ✅ Validated (consistent between both sources)

| Concept | GitHub (write-path) | Confluence API (read-path) | Notes |
|---|---|---|---|
| **Client** | `client: string` in `DaxRequestFulfillmentPayload` | `client=Sprint` (mandatory param) | Same field, same purpose |
| **Region** | `region: string` in DTOs; `REGION: "US"` in enums | `region=US` (mandatory param) | Confirmed US = Americas scope |
| **Line of Business** | `lineOfBusiness: string`; `LINE_OF_BUSINESS: "ApplianceRepair"` in enums | `lob=REPAIR` | Same concept, different value format — see conflicts below |
| **Warehouse / Location** | `wmsLocationId` in `DaxRequestConsumptionPayload` | `warehouses=TLC,LKY` (mandatory param) | Same warehouse identifier concept; external format `<account>\|<location>` confirmed in both |
| **Item / Part ID** | `itemId` in `DaxRequestConsumptionPayload` | `items=S300-0411-IPH135G128RED` param; `ItemId` in response | Same concept — SKU/part identifier |
| **Auth: L7 Gateway** | `l7-dax365.endpoint.host`, `Asurion-apikey`, Basic auth in `daxService.js` | "Base Path — Layer 7" on all endpoints | Same L7 gateway architecture for all existing DAX calls |
| **API versioning** | `/dax/v1/assets/products`, `/dax/v1/procurement/purchase/orders` in enums | `/v1/inventory/reservations/...` | Consistent `/v1/` versioning across read and write paths |
| **Americas scope** | `REGION: "US"`, handles MA / SUR / HomeFusion job types | `/parts/onhand` combines "Americas and UBIF instances of DAX" | Confirms Americas is the primary scope; UBIF is additive |
| **Parts substitution / LFL** | `dispatchParts[]` in consumption payload handles part variants | `lfl`, `nlfl`, `rollup`, `excludesubs` flags in `/parts/onhand` | Write path processes substituted parts; read path queries them |

---

### Expected Gaps (read-path only — not in write-path repos)

These fields exist in the Confluence API but are not in the GitHub write-path DTOs. This is **correct and expected** — the write path sends orders to DAX; it does not need to read availability state back.

| Field | Where | Why not in write-path repos |
|---|---|---|
| `AllowJustInTime` | `/parts/onhand` response | JIT flag is checked *before* ordering (read-path decision), not sent in the order itself |
| `LeadTimeInDays` | `/parts/onhand` response | Lead time is an availability attribute, not an order attribute |
| `physicalinvent`, `postedqty`, `reservphysical` | `/warehouse` response | IVS quantity breakdown — read only, never written |
| `AvailableQty` | `/onhand` + `/parts/onhand` response | Derived value from IVS — not in write path |

---

### Conflicts Worth Clarifying in Architecture Sessions

| Concept | GitHub value | Confluence value | Question |
|---|---|---|---|
| **Line of business value** | `"ApplianceRepair"` (enums.js) | `lob=REPAIR` | Are these the same program? Is `REPAIR` an abbreviation or a different LOB code? |
| **Company param** | `Asurion-client: "SBX"` (HTTP header) | `company=WCF` (query param) | Different placement (header vs param) and different values — intentional read/write split or a discrepancy? |
| **`partTypes` in write path** | `dispatchParts[]` array (untyped) | `partTypes=BAT,LCM,FRONTGLASS,BACKGLASS` (mandatory) | The write path doesn't explicitly type parts by BAT/LCM/etc. — does it need to? Relevant for F-3. |

---

## Overall Verdict

**The repos and Confluence API pages are consistent and complementary.** No fundamental conflicts found. The write-path repos confirm the same gateway, client/region/warehouse/item model as the read-path API. The read-path fields needed for acceptance criteria (`AllowJustInTime`, `LeadTimeInDays`, `AvailableQty`) are correctly absent from write-path repos — they belong to the new Availability API.

### What to use for each feature

| Use | Confirmed source |
|---|---|
| F-1 Part Price — AC field names for consumption/fulfillment | `github-repos.md` — confirmed DTO fields |
| F-2 Availability — base on-hand, LFL/NLFL, substitution params | `dax-daxapi.md` §GetInventoryOnHand |
| F-2 Availability — JIT and lead time fields (new contract) | `inventory-api.md` §parts/onhand + `analysis-existing-vs-new.md` |
| F-3 BOM — substitution matrix patterns | `inventory-api.md` §parts/onhand (lfl/nlfl flags) |
| F-4 Reservation — reserve/unreserve fields | `dax-daxapi.md` §PostInventoryReservation |
| F-4 Reservation — source attribution pattern | `dax-daxapi.md` §PostInventoryAdvReserv (AE pattern) |
| F-5 / F-7 AOP/NAOP migration — existing write-path event types | `github-repos.md` §job event types |
| Architecture Q: what DAX returns today | `inventory-api.md` — `AllowJustInTime` + `LeadTimeInDays` confirmed live |
| Architecture Q: what is net-new vs. reused | `analysis-existing-vs-new.md` |
| Architecture Q: auth for new APIs | `dax-daxapi.md` §InventoryVisibilitySvc (AAD, not L7) |

### Key findings from 2026-03-24 repo analysis

- **`GetInventoryOnHand` does not include `AllowJustInTime` or `LeadTimeInDays`** — those only appear in the Confluence `/parts/onhand` endpoint. The new SUR Availability API (F-2) requires a net-new contract.
- **Reservation infrastructure already exists** (`PostInventoryReservation`, Dataverse-backed `IvsReservationManager`, 30-min TTL timer) — F-4 reuses this plumbing but needs a new contract and source attribution.
- **Advanced Exchange pattern** (`source`, `reference1/2/3`) is the confirmed model for source attribution — relevant for how UBIF portal identifies itself on reservation calls.
- **New APIs use AAD auth, not L7** — `InventoryVisibilitySvc` uses client credentials + Security Service token. Different from the L7 gateway used by existing write-path repos.
