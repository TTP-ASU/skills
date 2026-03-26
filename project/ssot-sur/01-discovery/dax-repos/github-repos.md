# DAX GitHub Repositories — Americas Write Path
## Source: asurion-private · Researched: 2026-03-20

**Purpose:** Discovery and grooming reference for SSOT-SUR. Field names and DTO contracts here are confirmed from source code and used for writing accurate acceptance criteria. Source access: GitHub (`asurion-private` org, read access confirmed 2026-03-24).

These repos handle the **write path**: ServiceBench triggers events → these services process them → DAX receives orders, consumption records, and fulfillment updates.

Org: `asurion-private` · Scope: Americas only (APAC, SKT, and Japan repos excluded)

---

## Primary Repos

### 1. `sbx-operations-servicejobmanagement-daxintegration` ⭐

**Role:** Active event-driven DAX integration. Consumes SQS messages from SBX service job management and sends Sales Order headers and Parts Consumption records to DAX.

| Field | Value |
|---|---|
| Language | TypeScript (NestJS) |
| Last commit | Mar 13, 2026 |
| Default branch | `main` |
| Open PRs | 1 — [#416 "Added functionalCapability field"](https://github.com/asurion-private/sbx-operations-servicejobmanagement-daxintegration/pull/416) (`feature/FSET-510`, stale since Oct 2025) |
| Topics | `iso27001`, `sb-sbx`, `sbx-service-updates` |

**Architecture:**

| Layer | Key files | Role |
|---|---|---|
| Consumer | `src/consumer.service.ts` | Reads from SQS queue `sbx-us-east-1-xxx-servicejobmanagement-daxIntegration` |
| Handler | `src/handler/` | Chain of responsibility routing by job type: MA, SUR, HomeFusion |
| Adapter | `src/adapter/` | Transforms SBX job format → DAX request format |
| Publisher | `src/publisher.service.ts` | POSTs to DAX via L7 gateway |
| Repository | `src/repository.ts` (62KB) | TypeORM entity mapping against legacy DB model |
| DTOs | `src/dto/` | All DAX request/response shapes |
| Tax API | `src/tax.api/` | SOAP client for New Corp tax data (missing invoice case) |

**Job event types (confirmed from `src/dto/service.job.event.type.ts`):**

| Event type constant | Value | Maps to |
|---|---|---|
| `FULFILLMENT_ORDER_CREATE_MA` | `FulfillmentOrderCreate_MA` | DAX Sales Order Create |
| `FULFILLMENT_ORDER_UPDATE_MA` | `FulfillmentOrderUpdate_MA` | DAX Sales Order Update |
| `FULFILLMENT_ORDER_CANCEL_MA` | `FulfillmentOrderCancel_MA` | DAX Sales Order Cancel |
| `FULFILLMENT_ORDER_REJECT_MA` | `FulfillmentOrderReject_MA` | — |
| `CONSUMPTION_MA` | `Consumption_MA` | Parts Consumption |
| `HORIZON_CREATE_REPAIR` | `HORIZON_CREATE_REPAIR` | Horizon repair job |
| `HORIZON_CANCEL_SALES_ORDER` | `HORIZON_CANCEL_SALES_ORDER` | Horizon cancel |
| `DAX_PARTS_CONSUMPTION` | `DAX_PARTS_CONSUMPTION` | Parts consumption (direct) |
| `DAX_RENOTIFY_REQUEST` | `DAX_RENOTIFY_REQUEST` | Retry notification |

**Confirmed DTO fields — Fulfillment Order (`src/dto/dax.request.fullfilment.order.payload.ts`):**

```typescript
client: string
region: string
lineOfBusiness: string
fulfillmentType: string
serviceOrderId: string
serviceJobId: string
serviceRequestType: string
serviceLocation: string
paymentMode: string
customerAccount: string
invoiceAccount: string
vendorAccount: string
currency: string
correlation: string
source: string
reference1-4: string
isDeliveryInfoUpdate: boolean
enrollmentData: { enrolledItemId: string }
deliveryInfo: {
  deliveryAddressFirstName, deliveryAddressLastName,
  deliveryAddressLine1, deliveryAddressLine2,
  deliveryAddressCity, deliveryAddressZip,
  deliveryAddressState, deliveryAddressCountry,
  deliveryAddressBusiness
}
```

**Confirmed DTO fields — Parts Consumption (`src/dto/dax.request.consumption.payload.ts`):**

```typescript
itemId: string
partCost: string
partSerialId: string
partUsed: string[]
qty: number
wmsLocationId: string           // maps to `warehouses` in read-path API
serviceOrderId: string
serviceJobId: string
serviceType: string
serviceLocation: string
dispatchStatus: string
resolutionCode: string
serviceJobOutcome: string
serviceExplanation: string
serviceDateActual, serviceDateScheduled, serviceDateCompleted: string
serviceAccount: string
serviceDispatchPartStatus: string
enrolledItemId: string
client: string
clientProgramId: string
region: string
lineOfBusiness: string
ref1, ref2, ref3: string
addressCity, addressStreet, addressZipCodeId, addressStateId, addressCountryRegionId: string
servicerAddress*: string        // servicer location fields
dispatchParts: DaxRequestConsumptionPart[]
```

---

### 2. `sbx-partmanagement-ordering-daxrequestprocessor`

**Role:** Scheduled retry processor. Cron job that retries failed DAX calls for US part orders (receive, pickup, return). Catches failures from the main integration.

| Field | Value |
|---|---|
| Language | JavaScript (Node.js, Express) |
| Last commit | Mar 20, 2026 (today — Dependabot security fix) |
| Default branch | `main` |
| Open PRs | 1 — [#299 Dependabot `path-to-regexp` + `express` bump](https://github.com/asurion-private/sbx-partmanagement-ordering-daxrequestprocessor/pull/299) (stale since Dec 2024) |
| Topics | `iso27001`, `sb-sbx`, `sbx-parts` |
| Database | Oracle `SERVICEBENCHV5.AT_ORDER_EVENT_SBX` |

**Key DAX call patterns (`lib/daxService/daxService.js`):**

| Function | Method | Route | Auth |
|---|---|---|---|
| `notifyDax()` | POST | L7 gateway (`l7-dax365.endpoint.host`) | `Asurion-apikey` + Basic auth |
| `notifyDaxCloudHost()` | POST | Direct `dax.cloudhost` | `x-api-key` + Basic auth |
| `callDax()` | GET | L7 gateway (availability lookup) | `Asurion-apikey` + Basic auth |

`notifyDaxCloudHost()` is used only for `CancelOrderDax` events.

**Confirmed event types and API paths (`lib/enums.js`):**

| Event | Path |
|---|---|
| `CREATE_DAX_SKU` | `/dax/v1/assets/products` |
| `CHECK_DAX_SKU` | `/dax/v1/assets/products` |
| `CreateDaxPoD2C` | `/dax/v1/procurement/purchase/orders` |
| `LSPO_DAX_INVOICE` | Invoice update flow |
| `LSPO_DAX_CREDIT` | Credit flow |

**Constants:**

```javascript
REGION: "US"
LINE_OF_BUSINESS: "ApplianceRepair"
SOURCE: "ServiceBench"
```

---

## Supporting Repos (DAX-adjacent, Americas)

| Repo | DAX touchpoint | Notes |
|---|---|---|
| `sbx-operations-servicescheduling-common` | `src/models/DaxGateway.ts` | Shared DAX gateway model for SBX scheduling |
| `sbx-operations-administration-oem` | `apps/daxvendorcreation/app.js` | OEM vendor creation in DAX |
| `techworks-api` | `services/dax/bom.js` | BOM via DAX — may contain `partTypes` mapping |
| `metis-backend` | `db/diagnostic_dax_insert.js` | Diagnostic DAX inserts |
| `metis-backend--integration-api` | `src/db/acyan_dax_result_group.rs` | Acyan DAX result grouping (Rust) |

---

## Auth Pattern (confirmed across all repos)

All DAX calls go through the **Layer 7 gateway** using:

```
Headers:
  Asurion-apikey: <from config l7-gateway.headers.Asurion-apikey>
  Asurion-client: "SBX"
  Asurion-channel: "SBX-Node"
  Asurion-correlationid: <correlationId>
  Authorization: Basic <base64 from config>
  Content-Type: application/json

Endpoint:
  host: <from config l7-dax365.endpoint.host>
  port: <from config l7-dax365.endpoint.port>
```

This is the **same auth pattern** the `dax-ivs-mcp` read-path will use — no new credentials required for the MCP build.
