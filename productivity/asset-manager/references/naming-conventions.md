# Asset Naming Conventions

## Asset ID Format

```
{ENTITY}-{CATEGORY}-{SEQUENCE}
```

### Entity Codes (2 characters)

| Code | Entity | Description |
|------|--------|-------------|
| `TH` | Treehouse LLC | Rental property assets |
| `CO` | Consulting | Consulting business assets |
| `TP` | Tap | Startup assets |
| `PR` | Personal | Personal assets (not business) |

### Category Codes (Variable length)

| Code | Category | Typical Items |
|------|----------|---------------|
| `HVAC` | Heating/Cooling | AC units, furnaces, heat pumps, thermostats |
| `APPL` | Appliances | Refrigerator, dishwasher, washer, dryer, microwave |
| `PLMB` | Plumbing | Water heater, toilets, faucets, garbage disposal |
| `ELEC` | Electrical | Panels, outlets, light fixtures, ceiling fans |
| `TOOL` | Tools | Power tools, hand tools, ladders |
| `TECH` | Technology | Computers, monitors, phones, networking equipment |
| `FURN` | Furniture | Desks, chairs, tables, beds, sofas |
| `LAND` | Landscaping | Mowers, trimmers, blowers, irrigation |
| `SAFE` | Safety | Smoke detectors, CO detectors, fire extinguishers |
| `MISC` | Miscellaneous | Anything that doesn't fit other categories |

### Sequence (2 digits)

- Start at `01` for each entity-category combination
- Increment sequentially: `01`, `02`, `03`...
- If you reach `99`, consider if category is too broad

## Examples

| Asset ID | Meaning |
|----------|---------|
| `TH-HVAC-01` | Treehouse, first HVAC unit |
| `TH-HVAC-02` | Treehouse, second HVAC unit (if multi-unit) |
| `TH-APPL-01` | Treehouse, first appliance (e.g., refrigerator) |
| `TH-APPL-02` | Treehouse, second appliance (e.g., dishwasher) |
| `TH-APPL-03` | Treehouse, third appliance (e.g., washer) |
| `TH-PLMB-01` | Treehouse, first plumbing item (e.g., water heater) |
| `TH-SAFE-01` | Treehouse, first safety item (e.g., smoke detector) |
| `CO-TECH-01` | Consulting, first tech item (e.g., laptop) |
| `CO-TECH-02` | Consulting, second tech item (e.g., monitor) |
| `TP-TECH-01` | Tap startup, first tech item |
| `PR-TOOL-01` | Personal, first tool |

## Document Naming

For documents related to an asset:

```
{ASSET-ID}_{DOCTYPE}_{DATE}.{ext}
```

### Document Types

| Code | Type | Description |
|------|------|-------------|
| `manual` | User Manual | Operating instructions, specifications |
| `warranty` | Warranty | Warranty card, certificate, terms |
| `receipt` | Purchase Receipt | Proof of purchase |
| `invoice` | Service Invoice | Maintenance/repair invoices |
| `photo` | Photograph | Current photo of asset |
| `inspect` | Inspection | Inspection reports |

### Examples

```
TH-HVAC-01_manual_2024-01-15.pdf
TH-HVAC-01_warranty_2024-01-15.pdf
TH-HVAC-01_receipt_2024-01-15.pdf
TH-HVAC-01_invoice_2024-06-15.pdf   (service invoice)
TH-HVAC-01_photo_2024-01-15.jpg
TH-APPL-01_manual_2023-08-20.pdf
```

## Maintenance Log IDs

```
ML-{YEAR}-{SEQUENCE}
```

### Examples

| Log ID | Meaning |
|--------|---------|
| `ML-2024-001` | First maintenance log entry of 2024 |
| `ML-2024-002` | Second maintenance log entry of 2024 |
| `ML-2025-001` | First maintenance log entry of 2025 |

## Location Naming

For the Location field in Notion:

### Property-Level

```
{Street Number} {Street Name}
```

Examples:
- `123 Main St`
- `456 Oak Ave`

### Room-Level (if needed)

```
{Property} - {Room}
```

Examples:
- `123 Main St - Kitchen`
- `123 Main St - Master Bath`
- `123 Main St - Garage`
- `123 Main St - Exterior`

## Best Practices

1. **Be consistent** - Once you pick a convention, stick with it
2. **Don't overthink** - The goal is findability, not perfection
3. **Use leading zeros** - `01` not `1` for proper sorting
4. **Date format** - Always `YYYY-MM-DD` for sorting
5. **No spaces in IDs** - Use hyphens: `TH-HVAC-01` not `TH HVAC 01`
6. **Lowercase for files** - `th-hvac-01_manual_2024-01-15.pdf`
7. **Uppercase for IDs** - `TH-HVAC-01` in database records
