# DAX API Source Repo — `dax-daxapi`
## Repo: `asurion-private/dax-daxapi` · Analyzed: 2026-03-24 · Author: Thays Pritchard

**Description:** The primary, cloud-based API for Dynamics AX/365 integration.  
**Language:** C# · **Default branch:** `master` · **Visibility:** Internal · **Last updated:** 2026-03-18  
**Topics:** `dax`

**Purpose:** Discovery and grooming reference for SSOT-SUR. All field contracts and function signatures documented here are confirmed from direct source code inspection and are used for writing accurate acceptance criteria and preparing grooming questions for the DAX team.

> All fields and behaviors documented here are sourced directly from the `.cs` files in the repo. Nothing is inferred or invented.

---

## Repo structure (top-level modules)

| Directory | Role |
|---|---|
| `inventoryFn` | **Primary inventory Azure Function app** — on-hand queries, IVS reservation read/write, item availability, warehouse inventory |
| `inventoryInternalFn` | Internal inventory functions — Advanced Exchange (AE) feedback processing |
| `dapi.data` | Core data utilities library (caching, IoC, serialization, extensions) |
| `dapi.data.queries` | Data query layer — IVS, D365 AOS, Dataverse, Nexus, payment, SCM reporting |
| `dapi.data.sync` | Data sync utilities |
| `dapi.shipping` | Shipping-related functions |
| `fulfillmentFn` | Fulfillment Azure Functions |
| `procurementFn` | Procurement Azure Functions |
| `http` / `http.functions.core` | HTTP middleware / function framework base |
| `azi.abstractions` / `azi.asurion` | Core abstractions and Asurion platform libraries |

---

## `inventoryFn` — Confirmed Functions

### Function inventory

| Function name | HTTP method | Route (inferred) | Role |
|---|---|---|---|
| `GetInventoryOnHand` | GET | `/v1/inventory/reservations/onhand` | On-hand availability with LFL/NLFL substitution support |
| `GetWarehouseInventory` | GET | `/v1/inventory/reservations/warehouse` | IVS warehouse-level inventory breakdown |
| `GetItemAvailability` | GET | `/v1/inventory/reservations/...` | Single-item availability with warehouse selector |
| `PostInventoryReservation` | POST | `/v1/inventory/reservations/...` | Reserve or unreserve items in IVS |
| `PostInventoryAdvReserv` | POST | `/v1/inventory/reservations/...` | Advanced Exchange (AE) reservation / unreservation |
| `GetInventoryAdvReserv` | GET | `/v1/inventory/reservations/...` | GET AE reservation details (by source + refs) |
| `GetFGPlanTransferOrder` | GET | — | FG Plan Transfer Order query |
| `GetInventoryContainersLines` | GET | — | Inventory container lines |
| `GetInventorySerialsExpect` | GET | — | Inventory serial expectations |
| `GetLoanItem` | GET | — | Loan item query |
| `ClearExpiredInventReservationsTask` | Timer | 30-min schedule | Auto-clears expired IVS reservations per TTL config |
| `PostClearExpiredInventReservations` | POST | — | Manual trigger to clear IVS reservations at or before a given datetime |

---

## Confirmed Field Contracts (from source code)

### `GetInventoryOnHand` — Request parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `items` | string (comma-delimited) | required | SKU / product IDs to query |
| `warehouses` | string (comma-delimited) | required | Warehouse codes |
| `minimalize` | bool | false | Return only ItemId, Warehouse, AvailableQty |
| `lfl` | bool | false | Include like-for-like replacements |
| `nlfl` | bool | false | Include non-like-for-like replacements |
| `firstonly` | bool | true | Return only first result with available qty per item |
| `allwarehouses` | bool | true | When firstonly=true, return first per warehouse+item |
| `excludesubs` | bool | false | Exclude substitution SKUs from LFL/NLFL results |
| `rollup` | bool | false | Roll sub inventory into substituted SKU; overrides excludeSubs |

### `GetInventoryOnHand` — Response (`InventoryOnHandLine[]`)

| Field | Type | Minimalized | Description |
|---|---|---|---|
| `ItemId` | string | ✅ always | SKU / product identifier |
| `Warehouse` | string | ✅ always | Warehouse code |
| `AvailableQty` | decimal | ✅ always | Available quantity |
| `ReplacementType` | string | ❌ nulled when minimalized | LFL / NLFL / none |
| `Priority` | int? | ❌ nulled when minimalized | Substitution priority order |

> **Note:** `AllowJustInTime` and `LeadTimeInDays` are **NOT** in this response. Those fields are only confirmed in the Confluence `/parts/onhand` endpoint (`inventory-api.md`). This endpoint is a different, SUR-specific endpoint.

---

### `GetItemAvailability` — Request parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ItemId` | string | required | SKU / product ID |
| `client` | header/context | required | Asurion client (via RequestContext) |
| `region` | header/context | required | Geographic region (via RequestContext) |

### `GetItemAvailability` — Response (`GetItemAvailabilityResult`)

| Field | Type | Description |
|---|---|---|
| `ItemId` | string | The queried SKU |
| `InventorySummary` | object (nullable) | Summary object, null if no availability found |
| `InventorySummary.Warehouse` | string | Warehouse code |
| `InventorySummary.QtyAvailableInDAX` | decimal | `AvailPhysical` from D365 |
| `InventorySummary.QtyAvailableToOrder` | decimal | Available minus reserved |
| `InventorySummary.QtyReservedInDAX` | decimal | `OnOrder` from D365 |
| `InventorySummary.QtyReservedInQueue` | decimal | In-queue reservations |
| `InventorySummary.Size` | string? | Optional — nullable |
| `InventorySummary.Configuration` | string? | Optional — nullable |
| `InventorySummary.Color` | string? | Optional — nullable |

---

### `PostInventoryReservation` — Request schema

| Field | Type | Required | Description |
|---|---|---|---|
| `client` | string | — | Asurion client |
| `region` | string | — | Geographic region |
| `lineOfBusiness` | string | — | Line of business |
| `company` | string | — | D365 company |
| `unreserve` | bool? | — | If true, performs unreservation |
| `items[].itemId` | string | ✅ | SKU to reserve |
| `items[].qty` | decimal | ✅ | Quantity to reserve |
| `items[].warehouse` | string | ✅ | Target warehouse |
| `items[].reservationId` | string | — | Required when unreserving |

### `PostInventoryReservation` — Response

| Field | Type | Description |
|---|---|---|
| `RequestStatus` | string | Overall status of the reservation request |
| `Reservations[].Status` | string | Per-item reservation status |
| `Reservations[].ReservationId` | string | Assigned reservation ID |
| `Reservations[].Warehouse` | string | Warehouse where reserved |
| `Reservations[].ItemId` | string | Reserved SKU |
| `Reversals[].Status` | string | (Unreserve only) Per-item reversal status |
| `Reversals[].ReservationId` | string | (Unreserve only) The cleared reservation ID |
| `Reversals[].Warehouse` | string | (Unreserve only) |
| `Reversals[].ItemId` | string | (Unreserve only) |

---

### `PostInventoryAdvReserv` — Request schema (Advanced Exchange)

| Field | Type | Required | Description |
|---|---|---|---|
| `client` | string | — | Asurion client |
| `region` | string | — | Geographic region |
| `lineOfBusiness` | string | — | Line of business |
| `company` | string | — | D365 company |
| `warehouse` | string | — | Target warehouse |
| `source` | string | — | Source system identifier |
| `reference1` | string | — | Reference 1 (order / job / claim ID) |
| `reference2` | string | — | Reference 2 |
| `reference3` | string | — | Reference 3 |
| `customer` | string | — | Customer account |
| `unreserve` | bool? | — | If true, performs unreservation |
| `reservationId` | string | Required if unreserve=true | Existing reservation ID to release |
| `items[].itemId` | string | ✅ (reserve only) | SKU to reserve |
| `items[].qty` | decimal | ✅ (reserve only) | Quantity |
| `items[].isPrimary` | bool? | — | Whether this is the primary item |

### `PostInventoryAdvReserv` — Response

| Field | Type | Description |
|---|---|---|
| `RequestStatus` | string | Overall status |
| `ReservationId` | string | Assigned reservation ID |
| `Warehouse` | string | Warehouse where reserved |
| `Reservations[].Status` | string | Per-item status |
| `Reservations[].ItemId` | string | Reserved SKU |
| `Reservations[].Quantity` | decimal | Reserved quantity |
| `ErrorMessage` | string? | Set only on failure |

---

### `GetInventoryAdvReserv` — Request (AE reservation lookup)

| Parameter | Source | Description |
|---|---|---|
| `source` | header/context | Source system (AssertSource required) |
| `reference1` | header/context | Reference 1 |
| `reference2` | header/context | Reference 2 |
| `reference3` | header/context | Reference 3 |
| `includeHistory` | query string | Whether to include full reservation history |

---

## IVS Reservation Infrastructure (Domain Layer)

### `IvsReservation` domain model

| Property | Type | Description |
|---|---|---|
| `Company` | string | D365 Dynamics company |
| `Reservation` | string | Reservation identifier (IVS-assigned) |
| `Qty` | decimal | Reserved quantity |
| `ProductId` | string | Reserved SKU |
| `Dimensions` | string | JSON dimensions string (includes `locationid`) |
| `Warehouse` | string | Extracted from Dimensions.locationid |

### `IvsReservationManager` — Dataverse backend

Manages IVS reservations stored in **Microsoft Dataverse** (`is_reservation` table):

| Dataverse column | Description |
|---|---|
| `is_organizationid` | D365 organization / company |
| `is_quantitydatasource` | Quantity data source |
| `is_quantity` | Reserved quantity |
| `is_recid` | Record ID |
| `is_productid` | Product / SKU ID |
| `is_dimensions` | JSON dimensions (warehouse, location) |
| `modifiedon` | Last modified timestamp (used for TTL cleanup) |

**Key capabilities:**
- `ClearReservationsAsync(modifiedAtOrBefore?)` — batch-clear all or TTL-expired IVS reservations
- `ClearAdvancedExchangeReservationsAsync(modifiedAtOrBefore?)` — clear AE-specific reservations and mark `is_reservation` rows as inactive
- Automatic 30-minute timer (`ClearExpiredInventReservationsTaskFunc`) runs TTL cleanup with `IvsReservationTtlHours` config
- `EnableAdvancedExchangeProcesses` feature flag gates AE reservation processing

---

## `InventoryVisibilitySvc` — IVS Authentication

Auth for the Inventory Visibility Service uses **AAD token + Security Service** pattern — different from the L7 gateway used by write-path repos:

| Config key | Description |
|---|---|
| `IVSAppTenantId` | AAD tenant ID |
| `IVSAppClientId` | AAD application client ID |
| `IVSAppClientSecret` | AAD client secret (from key vault) |
| `IVSAadTokenScope` | AAD token scope for IVS |
| `IVSSecurityServiceScope` | D365 Security Service scope |
| `IVSEnvironmentId` | Dynamics environment ID |
| `IVSUrl` | IVS base URL |

> **Implication for SSOT-SUR:** New Availability and Reservation APIs will use this same AAD/IVS auth pattern — not the L7 gateway. This is a different credential set than what `sbx-operations-servicejobmanagement-daxintegration` uses.

---

## `inventoryInternalFn` — Advanced Exchange Internal Functions

| Function | Type | Role |
|---|---|---|
| `AdvExchangeFeedbackTaskFunc` | Timer | Scheduled AE feedback processing |
| `PostRunAdvExchangeFeedbackFunc` | POST | Manual trigger for AE feedback run |

These are internal-only functions that process AE outcomes back into the system.
