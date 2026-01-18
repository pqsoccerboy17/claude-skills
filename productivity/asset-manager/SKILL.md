---
name: asset-manager
description: "QR-code-based asset tracking with maintenance scheduling and depreciation. Use when: (1) adding new equipment/assets, (2) logging maintenance, (3) generating QR codes, (4) tracking depreciation, (5) checking what maintenance is due. Triggers: asset, equipment, inventory, maintenance, QR code, depreciation."
license: Proprietary
---

# Asset Manager

Manage physical assets with QR code tracking, maintenance scheduling, and tax depreciation calculations.

## Quick Start

```bash
# Create a new asset
python3 ~/claude-skills/productivity/asset-manager/scripts/asset_crud.py create \
  --id "DAL-HVAC-01" \
  --name "Primary AC Unit" \
  --category "HVAC" \
  --location "Dallas Property" \
  --cost 3500 \
  --purchase-date "2024-01-15" \
  --warranty-years 5 \
  --service-interval 90

# Generate QR code for an asset
python3 ~/claude-skills/productivity/asset-manager/scripts/qr_generator.py \
  --asset-id "DAL-HVAC-01" \
  --notion-url "https://notion.so/page-id"

# Log maintenance
python3 ~/claude-skills/productivity/asset-manager/scripts/maintenance.py log \
  --asset-id "DAL-HVAC-01" \
  --type "Preventive" \
  --description "Replaced air filter" \
  --cost 25

# Check what's due
python3 ~/claude-skills/productivity/asset-manager/scripts/maintenance.py due

# Calculate depreciation
python3 ~/claude-skills/productivity/asset-manager/scripts/depreciation.py \
  --asset-id "DAL-HVAC-01" \
  --tax-year 2024
```

## Organizational Hierarchy

```
Entity: Treehouse LLC (the business)
    │
    └── Properties
        ├── DAL     = Dallas property
        ├── ATX-A   = Austin Main Unit A
        ├── ATX-B   = Austin ADU Unit B
        └── ATX-C   = Austin ADU Unit C (coming soon)
            │
            └── Assets: Individual items at each property
```

## Naming Convention

```
{PROPERTY}-{CATEGORY}-{SEQUENCE}

PROPERTY:
  DAL   = Dallas property
  ATX-A = Austin Main Unit A
  ATX-B = Austin ADU Unit B
  ATX-C = Austin ADU Unit C (coming soon)

CATEGORY:
  HVAC   = Heating/cooling systems
  APPL   = Appliances (refrigerator, dishwasher, etc.)
  PLMB   = Plumbing fixtures
  ELEC   = Electrical systems
  TOOL   = Tools
  TECH   = Technology/computers
  FURN   = Furniture
  LAND   = Landscaping equipment
  SAFE   = Safety equipment (smoke detectors, etc.)
  MISC   = Miscellaneous

SEQUENCE: 01, 02, 03...

Examples:
  DAL-HVAC-01    = Dallas, first HVAC unit
  DAL-APPL-01    = Dallas, first appliance
  ATX-A-HVAC-01  = Austin Main Unit A, first HVAC unit
  ATX-A-APPL-01  = Austin Main Unit A, first appliance
  ATX-B-APPL-01  = Austin ADU Unit B, first appliance
  ATX-C-HVAC-01  = Austin ADU Unit C, first HVAC unit (future)
```

## Asset Categories & Depreciation

| Category | Typical Items | IRS Life | Method |
|----------|--------------|----------|--------|
| HVAC | AC units, furnaces, heat pumps | 27.5 years | Straight-line (residential) |
| APPL | Refrigerator, dishwasher, washer/dryer | 5 years | MACRS |
| PLMB | Water heater, fixtures | 27.5 years | Straight-line (residential) |
| ELEC | Electrical panel, wiring upgrades | 27.5 years | Straight-line (residential) |
| TOOL | Power tools, equipment | 5-7 years | MACRS |
| TECH | Computers, monitors, phones | 5 years | MACRS |
| FURN | Furniture, fixtures | 7 years | MACRS |
| LAND | Mowers, trimmers | 7 years | MACRS |

**Note:** Items that are part of the building structure (HVAC, plumbing, electrical) use the building's 27.5-year depreciation for residential rental property. Separate personal property uses MACRS.

## Maintenance Scheduling

### Service Intervals (Common)

| Item | Interval | Notes |
|------|----------|-------|
| HVAC filter | 90 days | More frequent if pets/allergies |
| HVAC service | 365 days | Annual tune-up |
| Water heater flush | 365 days | Annual |
| Smoke detector battery | 180 days | Bi-annual |
| Smoke detector replace | 3650 days | 10 years |
| Refrigerator coils | 365 days | Annual cleaning |
| Dryer vent | 365 days | Annual cleaning |
| Gutter cleaning | 180 days | Bi-annual |

### Maintenance Types

- **Preventive**: Scheduled maintenance (filter changes, tune-ups)
- **Repair**: Fix something broken
- **Inspection**: Periodic check without service
- **Emergency**: Unplanned urgent repair

## QR Code Workflow

1. **Create asset** in Notion database (via script or manually)
2. **Generate QR code** pointing to Notion page URL
3. **Print label** on weatherproof label stock (Brother P-Touch, Avery, etc.)
4. **Affix to asset** in visible location
5. **Scan to access** - phone camera opens Notion page with all details

### Label Recommendations

- **Indoor**: Standard label stock
- **Outdoor/garage**: Weatherproof/laminated labels
- **High-heat areas**: Avoid direct placement on hot surfaces
- **Size**: 1"x1" QR code minimum for reliable scanning

## Environment Variables

Required in `~/scripts/ecosystem.env`:

```bash
# Asset Management (add these)
NOTION_ASSETS_DB_ID=           # Asset Inventory database
NOTION_MAINTENANCE_DB_ID=       # Maintenance Log database
NOTION_DEPRECIATION_DB_ID=      # Depreciation Schedule database
```

## Notion Database Setup

### Asset Inventory Database

Create with these properties:

| Property | Type | Notes |
|----------|------|-------|
| Asset ID | Title | Unique identifier (DAL-HVAC-01, ATX-A-APPL-01) |
| Name | Text | Human-readable name |
| Category | Select | HVAC, APPL, PLMB, ELEC, TOOL, TECH, FURN, LAND, SAFE, MISC |
| Location | Select | Property address or room |
| Status | Select | Active, Needs Service, Retired |
| Purchase Date | Date | When acquired |
| Purchase Cost | Number | Original cost (currency format) |
| Vendor | Text | Where purchased |
| Warranty Expiry | Date | When warranty ends |
| Depreciation Category | Select | 5-year, 7-year, 27.5-year |
| Service Interval | Number | Days between service |
| Last Service | Date | Most recent maintenance |
| Next Service Due | Formula | `dateAdd(prop("Last Service"), prop("Service Interval"), "days")` |
| Documentation | URL | Link to NotebookLM or manual |
| QR Code | Files | Generated QR image |
| Photo | Files | Current photo of asset |
| Notes | Text | Additional information |

### Maintenance Log Database

| Property | Type | Notes |
|----------|------|-------|
| Log ID | Title | ML-2024-001 format |
| Asset | Relation | → Asset Inventory |
| Date | Date | Service date |
| Type | Select | Preventive, Repair, Inspection, Emergency |
| Description | Text | What was done |
| Cost | Number | Service cost |
| Vendor/Tech | Text | Who performed |
| Receipt | Files | Documentation |
| Notes | Text | Additional info |

## Integration with Ecosystem

### Notifications

When maintenance is due, integrates with `notify.py`:

```python
from notify import send_notification

send_notification(
    title="Maintenance Due",
    message="DAL-HVAC-01: Filter change due in 3 days",
    priority=0
)
```

### Ecosystem Status

Add to `ecosystem_status.py` checks:

```python
def check_maintenance_due():
    # Query Notion for assets where Next Service Due <= today + 7 days
    # Return count and list of assets
    pass
```

## File Naming for Documents

```
{ASSET-ID}_{DOCTYPE}_{DATE}.{ext}

Examples:
  DAL-HVAC-01_manual_2024-01-15.pdf
  DAL-HVAC-01_warranty_2024-01-15.pdf
  ATX-A-APPL-01_receipt_2024-01-15.pdf
  ATX-B-HVAC-01_photo_2024-01-15.jpg
```

Upload to NotebookLM for querying, link URL in Notion asset record.
