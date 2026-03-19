# MCP Integration Proposal: DAX and ServiceBench
## Project: SSOT-SUR · Author: Thays Pritchard · Date: 2026-03-16

---

## Why connect DAX and ServiceBench via MCP?

Right now, writing user stories and test requirements requires manually looking up:
- ServiceBench field definitions, job types, and part configuration (resolves OQ F1 directly)
- DAX IVS API response schema, inventory unit structure, and JIT flags
- Real test data (part numbers, location IDs, SKUs) to write meaningful acceptance criteria

Connecting both systems via MCP lets Cursor read this context directly — so user stories reference real field names, acceptance criteria match actual API shapes, and test cases use real data rather than placeholders.

---

## Proposal

### Tier 1 — Quick wins (use existing tools, no custom MCP needed)

| Connection | Method | What it unlocks |
|------------|--------|-----------------|
| **D365 / DAX OData metadata** | Generic HTTP MCP (`mcp-fetch`) calling `https://<dax-env>/data/$metadata` | Full entity model: field names, types, relationships for IVS, inventory units, BOM, JIT — paste directly into acceptance criteria |
| **ServiceBench API docs** | Generic HTTP MCP fetching the SB API spec (Swagger/WSDL endpoint or static spec file) | SB field definitions, mandatory/optional flags, job type codes — directly answers OQ F1 |
| **DAX IVS OpenAPI spec** | HTTP MCP or fetch the spec from the DAX API gateway (Azure APIM if available) | Exact request/response shapes for availability API, reservation API, JIT flags — write stories that reference real field names |

**Setup:** Add `mcp-fetch` or equivalent to `~/.cursor/mcp.json`. No auth needed for metadata endpoints; use a service account PAT for protected endpoints.

---

### Tier 2 — Custom MCP servers (2–4 weeks, high PM value)

#### `servicebench-mcp`

**Purpose:** Read-only access to ServiceBench configuration and field definitions.

**Capabilities:**
- `sb_get_field_definitions(entity)` — returns all fields for a given SB entity (Job, Part, Work Order) with name, type, mandatory flag, allowed values
- `sb_get_job_types()` — returns all job type codes and their configuration (OSR, CSS, etc.)
- `sb_get_part_config(sku)` — returns part-level JIT config, job-type exclusions, substitution rules
- `sb_get_location(location_id)` — returns location config (reservable flag, client, distro settings)

**Unlocks:**
- OQ F1 resolved automatically — pull the full field list instead of scheduling a working session
- User stories reference real SB field names (e.g., `Job.PartPrice`, `WorkOrder.ReservationId`)
- Test cases can specify exact field values and expected states

**Auth:** ServiceBench API key (internal integration credential, not user token)

---

#### `dax-ivs-mcp`

**Purpose:** Read-only access to DAX IVS / D365 inventory schema and test data.

**Capabilities:**
- `dax_get_availability(location_id, sku_list)` — calls the DAX availability API and returns real response shape
- `dax_get_item(item_id)` — returns item record: SKU, equipment type, JIT flag, BOM links
- `dax_get_location(location_id)` — returns warehouse/location config, reservation eligibility
- `dax_get_bom(model_id)` — returns BOM for a device model: Asurion SKUs + OEM SKUs
- `dax_get_inventory_unit(serial)` — returns IVS unit state (reserved, available, in-transit)

**Unlocks:**
- Write acceptance criteria using real response field names (`availabilityFlag`, `jitFlag`, `shippingDaysOut`)
- Test cases reference real SKUs, location IDs, and expected states from non-prod
- Validates architecture decisions (e.g., confirm what D365 actually returns for bypass peril config)
- Directly informs [ARCH] questions A1, A2, D1, D2 by showing what the API currently does vs. what it needs to do

**Auth:** D365 service principal (same pattern as existing DAX integrations; use a non-prod environment)

---

### Tier 3 — Bidirectional sync (post-architecture, pre-sprint)

Once architecture is finalized and stories are being actively groomed:

| Integration | What it enables |
|-------------|-----------------|
| **ADO ↔ Notion sync** | Already connected (ADO MCP live). Use to create User Stories in ADO directly from TDR stories, fill in acceptance criteria, and update status. |
| **ServiceBench test env** | Create/update test work orders via `sb_create_job()` to run acceptance test scenarios end-to-end |
| **DAX sandbox** | POST availability requests to non-prod DAX to validate response shapes before writing final AC |

---

## Recommended setup order

| Priority | Action | Owner | Effort |
|----------|--------|-------|--------|
| 1 | Add `mcp-fetch` to `~/.cursor/mcp.json`; point at D365 `$metadata` endpoint (non-prod) | Thays + DAX team | 1 hour |
| 2 | Get ServiceBench API spec (Swagger/WSDL) from SB Eng team; add as a fetchable resource | Thays + SB Eng | 1 day |
| 3 | Build `servicebench-mcp` (read-only, field defs + job types) | DAX/SB Eng | 1–2 weeks |
| 4 | Build `dax-ivs-mcp` (read-only, availability + item + BOM) | DAX team | 2–3 weeks |
| 5 | Connect Tier 3 bidirectional flows | Engineering | Post-architecture |

---

## Impact on user stories and test requirements

### Before (current state)
- Acceptance criteria use placeholder field names: "the API returns an availability flag"
- Test cases require manual lookup of real part numbers and location IDs
- OQ F1 (SB field documentation) blocks FR-11 migration planning

### After (with DAX + SB MCP)
- Acceptance criteria reference real fields: "API returns `{ availabilityFlag: true, jitFlag: false, shippingDaysOut: 3 }` for SKU `ASU-LCM-001` at location `WH-US-001`"
- Test cases include real non-prod data seeded from the MCP query
- OQ F1 is self-resolving: `sb_get_field_definitions('Part')` returns the complete field list including definition, mandatory flag, and allowed values
- Architecture questions D1–D4 can be answered by querying what the DAX API currently returns — no working session needed for the factual questions

---

## Next steps

1. **Thays to confirm:** Is there a non-prod D365/DAX endpoint accessible with a service account? (Required for Tier 1 immediate setup)
2. **Thays to ask SB Eng:** Does ServiceBench have a Swagger/OpenAPI spec or WSDL available internally?
3. **Share this proposal with Bryant / DAX Arch** to prioritize `dax-ivs-mcp` and `servicebench-mcp` as part of the SSOT discovery workstream — both directly reduce architecture working session load.
