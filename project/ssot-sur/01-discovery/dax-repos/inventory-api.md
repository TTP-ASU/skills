# DAX Inventory API — Confirmed Endpoints
## Source: Confluence · Space: DDD · Retrieved: 2026-03-20

Americas only. All endpoints use the L7 (Layer 7) gateway. Auth uses `Asurion-apikey` + Basic auth — same pattern as existing integrations in `sbx-operations-servicejobmanagement-daxintegration`.

---

## Environments

| Environment | Base URL |
|---|---|
| **QA (non-prod)** | `https://us-sqa-dax.azure-api.net/` |
| **Prod** | `https://asu-us-prod-dax.azure-api.net/` |

---

## Endpoint 1 — On-Hand Availability by Item

**Most relevant for:** Availability checks, LFL/NLFL substitution queries, rollup scenarios.

```
GET /v1/inventory/reservations/onhand
```

### Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| `client` | Mandatory | Asurion client | `Sprint` |
| `region` | Mandatory | Geographic region | `US` |
| `lob` | Optional | Line of business | `REPAIR` |
| `company` | Optional | DAX company | `WCF` |
| `warehouses` | Mandatory | Comma-delimited list; external format: `<account>\|<location>` | `TLC,LKY,0118491\|303` |
| `items` | Mandatory | Comma-delimited SKU list; use S- SKUs with lfl/nlfl flags | `S300-0411-IPH135G128RED` |
| `lfl` | Optional (default: false) | Include like-for-like replacements from D365 replacement matrix | `true` |
| `nlfl` | Optional (default: false) | Include non-like-for-like replacements | `true` |
| `firstonly` | Optional (default: true) | Return only first item with available qty per requested item | `true` |
| `allwarehouses` | Optional (default: true) | When `firstonly=true`, return first result per warehouse+item | `true` |
| `excludesubs` | Optional (default: false) | Exclude substitution SKUs from LFL/NLFL results | `true` |
| `rollup` | Optional (default: false) | Roll substitution inventory into substituted SKU; overrides `excludesubs` | `true` |
| `minimalize` | Optional (default: false) | Return only `ItemId`, `Warehouse`, `AvailableQty` | `true` |

### Response fields (minimalized)

| Field | Type | Description |
|---|---|---|
| `ItemId` | string | SKU / part number |
| `Warehouse` | string | Warehouse code |
| `AvailableQty` | number | Available on-hand quantity |

### Example

```
GET https://us-sqa-dax.azure-api.net/v1/inventory/reservations/onhand
  ?company=WCF
  &warehouses=0118491|303,TLC,LKY
  &items=4983M,6285D,S300-0411-IPH135G128RED
  &lfl=true
```

---

## Endpoint 2 — Warehouse Inventory from IVS

**Most relevant for:** Full IVS quantity breakdown (physical, posted, reserved) per warehouse.

```
GET /v1/inventory/reservations/warehouse
```

### Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| `client` | Mandatory | Asurion client | `Sprint` |
| `region` | Mandatory | Geographic region | `US` |
| `lob` | Optional | Line of business | `REPAIR` |
| `company` | Optional | DAX company | `WCF` |
| `warehouses` | Mandatory | Comma-delimited list | `TLC` |

### Response (confirmed shape from IVS)

```json
[
  {
    "productId": "UPG744-0420-IPH13MN5G128BLK-B",
    "dimensions": {
      "SiteId": "Site1",
      "LocationId": "UPGRADE"
    },
    "quantities": {
      "fno": {
        "physicalinvent": 1,
        "postedqty": 1,
        "reservphysical": 1
      }
    }
  }
]
```

### Response field reference

| Field | Description | Notes |
|---|---|---|
| `productId` | SKU / part number | Maps to `itemId` in write-path DTOs |
| `dimensions.SiteId` | D365 site identifier | |
| `dimensions.LocationId` | Warehouse / location code | Maps to `wmsLocationId` in write-path |
| `quantities.fno.physicalinvent` | Total physical inventory | |
| `quantities.fno.postedqty` | Posted (committed) quantity | |
| `quantities.fno.reservphysical` | Reserved physical quantity | |
| **Available** | `physicalinvent - reservphysical` | Derived — no direct field |

---

## Endpoint 3 — Parts On-Hand (Americas + UBIF) ⭐ Most Relevant

**Most relevant for:** SSOT-SUR — this endpoint combines Americas and UBIF DAX instances and includes JIT and lead time fields. Use this for availability acceptance criteria.

```
GET /v1/inventory/reservations/parts/onhand
```

### Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| `client` | Mandatory | Asurion client | `Sprint` |
| `region` | Mandatory | Geographic region | `US` |
| `lob` | Optional | Line of business | `REPAIR` |
| `company` | Optional | DAX company | `WCF` |
| `warehouses` | Mandatory | Comma-delimited list | `TLC,LKY` |
| `items` | Mandatory | Comma-delimited S- SKU list | `S300-0411-IPH135G128RED` |
| `partTypes` | Mandatory | Comma-delimited part type filter from BOM | `BAT,LCM,FRONTGLASS,BACKGLASS` |
| `lfl` | Optional (default: false) | Like-for-like replacements | `true` |
| `nlfl` | Optional (default: false) | Non-like-for-like replacements | `true` |
| `firstonly` | Optional (default: true) | First item with available qty per requested item | `true` |
| `allwarehouses` | Optional (default: true) | First result per warehouse+item when `firstonly=true` | `true` |
| `excludesubs` | Optional (default: false) | Exclude substitution SKUs | `true` |
| `rollup` | Optional (default: false) | Roll substitution inventory into substituted SKU | `true` |
| `minimalize` | Optional (default: false) | Return only essential fields (see below) | `true` |

### Response fields (minimalized) — **confirmed field names**

| Field | Type | Description | Proposal placeholder replaced |
|---|---|---|---|
| `ItemId` | string | SKU / part number | — |
| `Warehouse` | string | Warehouse code | — |
| `AvailableQty` | number | Available on-hand quantity | `availabilityFlag` |
| `AllowJustInTime` | boolean | Whether JIT fulfillment is allowed for this item | `jitFlag` |
| `LeadTimeInDays` | number | Lead time in days for this item | `shippingDaysOut` |

### Notes

- This endpoint **combines Americas + UBIF DAX instances** — it is the single source for parts availability across both programs.
- `partTypes` filter maps to BOM part categories: `BAT` (battery), `LCM` (screen), `FRONTGLASS`, `BACKGLASS`.
- With `lfl=true`, if no replacement matrix exists for an item, the original item's on-hand quantity is returned.

---

## Acceptance Criteria — Real Field Example

```
Given warehouse TLC and SKU S300-0411-IPH135G128RED
When GET /v1/inventory/reservations/parts/onhand is called with partTypes=LCM
Then response includes:
  { "ItemId": "S300-0411-IPH135G128RED", "Warehouse": "TLC",
    "AvailableQty": 5, "AllowJustInTime": false, "LeadTimeInDays": 2 }
```
