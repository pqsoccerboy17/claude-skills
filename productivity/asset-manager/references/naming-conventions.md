# Asset Naming Conventions

## Organizational Hierarchy

```
Entity (Business)
└── Treehouse LLC
    │
    ├── Properties
    │   ├── Dallas Property (DAL)
    │   └── Austin Property
    │       ├── Main Unit A (ATX-A)
    │       ├── ADU Unit B (ATX-B)
    │       └── ADU Unit C (ATX-C) - coming soon
    │
    └── Assets
        └── Individual items at each property
```

This hierarchy allows tracking assets across multiple properties while maintaining clear ownership under a single business entity.

## Asset ID Format

```
{PROPERTY}-{CATEGORY}-{SEQUENCE}
```

### Property Codes

| Code | Property | Description |
|------|----------|-------------|
| `DAL` | Dallas | Dallas property assets |
| `ATX-A` | Austin Main Unit A | Austin main house assets |
| `ATX-B` | Austin ADU Unit B | Austin ADU B assets |
| `ATX-C` | Austin ADU Unit C | Austin ADU C assets (coming soon) |

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

- Start at `01` for each property-category combination
- Increment sequentially: `01`, `02`, `03`...
- If you reach `99`, consider if category is too broad

## Examples

| Asset ID | Meaning |
|----------|---------|
| `DAL-HVAC-01` | Dallas property, first HVAC unit |
| `DAL-HVAC-02` | Dallas property, second HVAC unit |
| `DAL-APPL-01` | Dallas property, first appliance (e.g., refrigerator) |
| `DAL-APPL-02` | Dallas property, second appliance (e.g., dishwasher) |
| `DAL-PLMB-01` | Dallas property, first plumbing item (e.g., water heater) |
| `ATX-A-HVAC-01` | Austin Main Unit A, first HVAC unit |
| `ATX-A-APPL-01` | Austin Main Unit A, first appliance |
| `ATX-A-APPL-02` | Austin Main Unit A, second appliance |
| `ATX-B-HVAC-01` | Austin ADU Unit B, first HVAC unit |
| `ATX-B-APPL-01` | Austin ADU Unit B, first appliance |
| `ATX-C-HVAC-01` | Austin ADU Unit C, first HVAC unit (future) |

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
DAL-HVAC-01_manual_2024-01-15.pdf
DAL-HVAC-01_warranty_2024-01-15.pdf
DAL-HVAC-01_receipt_2024-01-15.pdf
DAL-HVAC-01_invoice_2024-06-15.pdf   (service invoice)
DAL-HVAC-01_photo_2024-01-15.jpg
ATX-A-APPL-01_manual_2023-08-20.pdf
ATX-B-HVAC-01_receipt_2024-03-10.pdf
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
5. **No spaces in IDs** - Use hyphens: `DAL-HVAC-01` not `DAL HVAC 01`
6. **Lowercase for files** - `dal-hvac-01_manual_2024-01-15.pdf`
7. **Uppercase for IDs** - `DAL-HVAC-01` in database records
8. **Property consistency** - Each asset belongs to exactly one property
