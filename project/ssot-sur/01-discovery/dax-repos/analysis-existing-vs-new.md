# DAX Repo Analysis — Existing vs. New Builds
## Source: `dax-daxapi` (GitHub read access) + 03/23 meeting notes + Confluence API docs
## Compiled: 2026-03-24 · Author: Thays Pritchard

**Purpose:** Discovery and grooming reference for SSOT-SUR. Use this to understand what DAX already has (reusable) vs. what is net-new (needs to be built), and to prepare accurate grooming questions and acceptance criteria.

> **Methodology:** Everything here is sourced directly from (a) `dax-daxapi` source code, (b) Confluence DDD API docs, (c) 03/23 meeting transcript. Nothing is invented. Gaps are explicitly flagged as unknown until confirmed by the DAX team.

---

## Key Decision from 03/23 Meeting (Matt / Michelle / Thays)

> *"Building new API with unique contract rather than reusing existing schema due to complexity and server-specific fields."*  
> *"Availability and reservation will be two separate APIs — availability is read-only query, reservation is writable."*  
> *"API will be under DAX IVS umbrella, wrapped as backend API."*

This means: the DAX team is not simply calling existing endpoints from a new wrapper. They are **writing new Azure Functions** with new contracts inside `dax-daxapi` (or a sister repo). What exists today provides the infrastructure patterns and some reusable fields — but the SUR Availability and Reservation contracts are new.

---

## Part 1 — What Already Exists in DAX Today

### ✅ F-1: Part Price on Job/Claim (Q1 — Mostly Complete)

**Status in code:** Fully delivered. The write-path repo `sbx-operations-servicejobmanagement-daxintegration` (TypeScript/NestJS) handles all S2 provider part price recording to DAX.

| What exists | Source | Confirmed fields |
|---|---|---|
| Sales Order Create/Update/Cancel event handlers | `sbx-operations-servicejobmanagement-daxintegration` | `client`, `region`, `lineOfBusiness`, `fulfillmentType`, `serviceOrderId`, `serviceJobId`, `paymentMode`, `vendorAccount`, `currency` |
| Parts Consumption records | Same repo, `dax.request.consumption.payload.ts` | `itemId`, `partCost`, `partSerialId`, `qty`, `wmsLocationId`, `serviceOrderId`, `serviceJobId`, `dispatchParts[]` |
| L7 gateway auth pattern | `daxService.js`, `daxService.ts` | `Asurion-apikey`, Basic auth, `l7-dax365.endpoint.host` |
| Retry processor | `sbx-partmanagement-ordering-daxrequestprocessor` | Part order receive/pickup/return retries |

**What's not confirmed:** S1 provider (Apexia) status. Meeting confirmed S2 providers are live; Apexia confirmation is pending.

---

### ✅ On-Hand Availability Infrastructure (Used by Future F-2 Basis)

The `GetInventoryOnHand` function in `dax-daxapi/inventoryFn` is a mature, live endpoint. It already supports:

| Capability | Confirmed |
|---|---|
| Multi-item, multi-warehouse on-hand query | ✅ |
| LFL (like-for-like) substitution | ✅ (`lfl` param → `IncludeLflReplacements`) |
| NLFL substitution | ✅ (`nlfl` param → `IncludeNlflReplacements`) |
| Substitution rollup into parent SKU | ✅ (`rollup` param) |
| Exclude substitutions flag | ✅ (`excludesubs` param) |
| First-only and all-warehouses filtering | ✅ (`firstonly`, `allwarehouses` params) |
| Minimalized response (ItemId, Warehouse, AvailableQty only) | ✅ (`minimalize` param) |
| ReplacementType and Priority in full response | ✅ |

**What it does NOT have (confirmed gap):**
- `AllowJustInTime` — not in `InventoryOnHandLine`. Only confirmed in Confluence `/parts/onhand` endpoint.
- `LeadTimeInDays` — same; not in this function's response schema.
- `partTypes` filtering — not a parameter in `GetInventoryOnHand`. Present in Confluence `/parts/onhand` as a mandatory param.

This means the SUR Availability API (F-2) **cannot reuse `GetInventoryOnHand` directly** — it requires a new contract that includes JIT and lead time fields.

---

### ✅ Simple IVS Reservation Infrastructure (Basis for F-4)

`PostInventoryReservation` and `IvsReservationManager` are live today. This is the existing reservation plumbing:

| What exists | Details |
|---|---|
| IVS reserve / unreserve | `PostInventoryReservation` — POST with `itemId`, `qty`, `warehouse`, `reservationId` for unreservations |
| Dataverse-backed reservation storage | `is_reservation` table. Columns: `is_productid`, `is_quantity`, `is_dimensions`, `is_organizationid`, `is_recid` |
| TTL-based expiry cleanup | `ClearExpiredInventReservationsTaskFunc` — 30-min timer, reads `IvsReservationTtlHours` config |
| Manual reservation clear | `PostClearExpiredInventReservations` — HTTP-triggered with `modifiedAtOrBefore` datetime |
| Reservation ID returned on reserve | `ReservationId` in response — confirmed field |

**What it does NOT have (confirmed gap):**
- `source` attribution (which portal triggered the reservation) — not a field in `PostInventoryReservation` (it IS a field in `PostInventoryAdvReserv`). New SUR contract will need to carry source/portal context.
- No expiry time on the reservation itself — expiry is system-wide config, not per-reservation.
- No direct link from IVS reservation ID to UBIF portal job ID — this link needs to be designed as part of the new Reservation API contract.

---

### ✅ Advanced Exchange Reservation Pattern (Mature Reference for F-4)

`PostInventoryAdvReserv` and `GetInventoryAdvReserv` are a more mature version of the reservation pattern that includes the source attribution and reference fields the new SUR Reservation API will also need:

| AE pattern field | Maps to SUR need |
|---|---|
| `source` | Which system originated the reservation (UBIF portal, SB, etc.) |
| `reference1 / reference2 / reference3` | Order ID / job ID / claim ID linkage |
| `customer` | Customer account context |
| `reservationId` for unreservation | Already the pattern for release on job close |
| `isPrimary` on items | Primary vs. secondary item reservation (relevant for substitution reservations) |

> **Implication:** The DAX team has already built the reference-field and source-attribution pattern for AE. The SUR Soft Reservations API (F-4) will likely follow the same pattern. This reduces new design work.

---

### ✅ IVS Auth Pattern (New APIs Will Reuse This)

The `InventoryVisibilitySvc` in `dapi.data.queries` confirms the AAD-based auth pattern for IVS:
- AAD client credentials flow (`IVSAppClientId` / `IVSAppClientSecret`)
- Security Service token exchange for D365 IVS access
- Environment-scoped (`IVSEnvironmentId`)
- Token caching with policy (`CacheItemPolicy`)

> **Implication:** New SUR Availability and Reservation APIs will use the same `InventoryVisibilitySvc` and the same AAD credentials — no new auth infrastructure required beyond what already exists.

---

## Part 2 — What Is New (Being Built by DAX)

Based on the 03/23 meeting and source analysis, the following are **net-new builds** inside `dax-daxapi` or a related repo.

### 🆕 F-2: SUR Availability API (Q2 — New Contract)

**What is new:**
- A completely new Azure Function (likely `GetSurInventoryAvailabilityFunc` or similar) with a new contract
- New request fields not in any existing function:
  - `partTypes` — mandatory filter (`BAT`, `LCM`, `FRONTGLASS`, `BACKGLASS`) — confirmed only in Confluence `/parts/onhand`, not in `GetInventoryOnHand`
  - UBIF JIT flag — referenced in meeting ("includes JIT flags and UBIF JIT flag") but **not found in any current repo file** — this is a new field DAX needs to build
- New response fields not in any existing function:
  - `AllowJustInTime` — confirmed in Confluence `/parts/onhand` but **absent from `InventoryOnHandLine` in the repo**
  - `LeadTimeInDays` — same; only in Confluence docs
- New contract naming still to be ratified (per 03/23 meeting: "11am Wednesday meeting scheduled")

**What can be reused from existing code:**
- `GetInventoryOnHand` provides the LFL/NLFL/rollup/substitution logic as a direct reuse pattern
- `InventoryVisibilitySvc` auth — no new credentials needed
- `IReservations.GetOnHandAsync()` — the underlying query method is already abstracted; the new function can call it with new parameters

**What is confirmed unknown (do not write AC until resolved):**
- Exact name and contract of the new Availability endpoint — pending ratification
- "UBIF JIT flag" — what exactly this field is, what it represents, and how DAX computes it — **not found in any source reviewed**
- Whether `partTypes` parameter will be implemented as a filter in the new function or via a new IVS query path

---

### 🆕 F-3: BOM / Substitution Matrix (Q2)

**What exists:**
- `lfl` and `nlfl` flags in `GetInventoryOnHand` expose the substitution matrix data
- `techworks-api/services/dax/bom.js` (confirmed in `github-repos.md`) — BOM lookup via DAX

**What is new:**
- A structured BOM API that ServiceBench / UBIF can query to get the full BOM for a device (list of parts by type)
- This is separate from availability — it's a product catalog query, not an inventory state query
- No BOM function was found in `inventoryFn` — it's either in `fulfillmentFn` or a new function to be built
- The `partTypes` param in the Availability API depends on the BOM API being available upstream (caller needs to know which partTypes to request)

**What is confirmed unknown:**
- Whether `techworks-api/bom.js` is the canonical BOM implementation or a reference only
- Whether DAX is building a new `GetBomFunc` or adapting an existing one

---

### 🆕 F-4: Soft Reservations / Reservation API (Q2)

**What exists (reusable):**
- `PostInventoryReservation` — core IVS reserve/unreserve pattern
- `IvsReservationManager` — Dataverse storage, TTL management, batch clear
- `PostInventoryAdvReserv` — source + reference attribution pattern
- `ClearExpiredInventReservationsTaskFunc` — existing TTL cleanup can be extended for SUR reservations

**What is new:**
- New SUR-specific reservation contract (per meeting: "new API with unique contract")
- Source attribution: which portal/system created the reservation (UBIF NextGen vs. SB)
- Reservation ID needs to flow into the UBIF portal job record AND the DAX fulfillment order
- Expiry behavior: TTL per-reservation or system-wide config — not yet determined
- Soft reservation window: "close the 1–5 min overcommit window" — requires near-real-time reservation creation and release, which is new behavior on top of the existing batch-clear model

**Key dependency (from meeting):** EP1S4 (US-2.4) — Reservation ID on UBIF and DAX orders — must be delivered before Soft Reservations can go live. The `ReservationId` field already exists in the response of `PostInventoryReservation`, but the UBIF side needs to store and send it in subsequent DAX order calls.

---

### 🆕 F-5 / F-7: AOP and NAOP Migration (Q3 / Q4)

**What exists:**
- `sbx-operations-servicejobmanagement-daxintegration` handles SUR job types today via ServiceBench SQS events
- The handler routing (`src/handler/`) already distinguishes MA, SUR, HomeFusion job types

**What is new:**
- AOP migration: Moving AOP (Asurion-Operated Providers) from ServiceBench-fed inventory to DAX-direct availability queries via the new Availability API
- NAOP migration: Moving NAOP (Non-AOP) — larger in scope, includes TELUS (Plan B: LCM-only + bypass flag)
- Both require the new Availability and Reservation APIs (F-2, F-4) to be live first
- TELUS-specific: Plan B = LCM-only coverage + bypass flag — a conditional path in the new Availability API, not a new endpoint

---

## Part 3 — Gap Summary (No Fabrication)

These are real gaps identified from source inspection. Do not write acceptance criteria for these until resolved.

| Gap | What we know | What we don't know | Blocking |
|---|---|---|---|
| UBIF JIT flag | Referenced in 03/23 meeting; JIT behavior exists in Confluence `/parts/onhand` | Exact field name in new contract, how DAX computes it, whether it differs from `AllowJustInTime` | F-2 AC |
| New Availability API contract | Decision made to build new contract; will be under DAX IVS umbrella | Endpoint path, all request/response fields, naming (pending 03/23 "11am Wednesday" ratification session) | F-2 stories |
| `partTypes` implementation | Confirmed as mandatory in Confluence `/parts/onhand`; absent from `GetInventoryOnHand` | Whether it is in a new function or being added to existing; internal IVS query path used | F-2, F-3 AC |
| Soft reservation TTL design | Existing timer clears all expired reservations on 30-min schedule | Per-reservation TTL vs. system TTL for SUR; whether the 1–5 min window requires a shorter timer or on-demand cancel | F-4 design |
| Reservation ID on UBIF orders | `ReservationId` exists in `PostInventoryReservation` response | How UBIF portal stores and passes it back on order creation; DAX-side contract for receiving it | US-2.4 / F-4 gate |
| BOM API canonical source | `techworks-api/bom.js` exists; `partTypes` is a concept in Availability API | Whether DAX builds a new BOM function, and what the contract looks like | F-3 stories |
| TELUS Plan B bypass flag | Plan B confirmed (LCM-only + bypass flag for NAOP) | Exact field name in Availability API request/response for TELUS bypass | F-7 stories |

---

## Part 4 — Confirmed Reuse Map for AC Writing

Use these confirmed fields in acceptance criteria **right now** (no open questions blocking them):

| Story | Field/behavior | Source |
|---|---|---|
| F-1 part price write | `partCost`, `itemId`, `qty`, `wmsLocationId`, `serviceOrderId`, `serviceJobId`, `dispatchParts[]` in consumption payload | `github-repos.md` |
| F-2 availability (base availability) | `items`, `warehouses`, `lfl`, `nlfl`, `firstonly`, `rollup`, `excludesubs`, `minimalize` params; `ItemId`, `Warehouse`, `AvailableQty`, `ReplacementType`, `Priority` in response | `dax-daxapi` source |
| F-2 availability (JIT + LeadTime) | `AllowJustInTime`, `LeadTimeInDays` as confirmed response fields | Confluence `/parts/onhand` (`inventory-api.md`) — **use `[pending contract ratification]` in AC until new endpoint is named** |
| F-4 reservation request | `itemId`, `qty`, `warehouse` (required); `client`, `region`, `lineOfBusiness`, `company` (optional but expected) | `dax-daxapi` `PostInventoryReservationSchema` |
| F-4 reservation response | `ReservationId`, `Status`, `Warehouse`, `ItemId` per reservation | `dax-daxapi` `InventoryReservationResult` |
| F-4 reservation release | `unreserve: true` + `reservationId` in items array | `dax-daxapi` `PostInventoryReservationSchema` |
| F-4 source attribution | `source`, `reference1/2/3` pattern confirmed for AE | `dax-daxapi` `PostInventoryAdvReservSchema` — **confirm with DAX whether SUR uses same pattern** |
| F-4 TTL cleanup | 30-min timer, `IvsReservationTtlHours` config, `modifiedAtOrBefore` parameter | `dax-daxapi` `ClearExpiredInventReservationsTaskFunc` |
| Auth (all new APIs) | AAD client credentials, `IVSAppClientId/Secret`, `IVSEnvironmentId`, Security Service token exchange | `dapi.data.queries/InventoryVisibilitySvc.cs` |
