# Implementation Checklist: Unified System Build

> **Ethos:** Ralph Wiggum Plugin - Chip away. Each checkbox is progress. Don't try to do it all at once. Small focused changes, clear success criteria, test before commit.
>
> *Reference: [Ralph-Wiggum Repository](https://github.com/pqsoccerboy17/Ralph-Wiggum)*

---

## Properties Overview

| Code | Property | Status |
|------|----------|--------|
| `DAL` | Dallas | Active |
| `ATX-A` | Austin Main Unit A | Active |
| `ATX-B` | Austin ADU Unit B | Active |
| `ATX-C` | Austin ADU Unit C | Coming Soon |

---

## Phase 0: Foundation ✅ COMPLETE

### Prerequisites
- [x] Verify Notion API token is valid in `ecosystem.env`
- [x] Test Pushover notifications are working
- [x] Verify Python environment has required packages

### Documentation
- [x] Review UNIFIED-SYSTEM-PLAN.md
- [x] Locate Ralph Wiggum plugin original reference
- [x] Document Ralph Wiggum philosophy in planning docs

---

## Phase 1: Asset Database ✅ SKILL COMPLETE

### Skill: asset-manager ✅ BUILT
- [x] Create directory: `productivity/asset-manager/`
- [x] Create SKILL.md with frontmatter
- [x] Create `scripts/` directory
- [x] Build `asset_crud.py` with all CRUD functions
- [x] Build `qr_generator.py` with batch support
- [x] Build `maintenance.py` with logging and due checking
- [x] Build `depreciation.py` with MACRS and straight-line
- [x] Create `references/naming-conventions.md` (updated for 4 properties)
- [x] Create `references/notebooklm-guide.md`

### Notion Setup (User Action Required)
- [ ] Create `Asset Inventory` database with all properties:
  - [ ] Asset ID (Title) - Format: `DAL-HVAC-01`, `ATX-A-APPL-01`
  - [ ] Name (Text)
  - [ ] Category (Select: HVAC, APPL, PLMB, ELEC, TOOL, TECH, FURN, LAND, SAFE, MISC)
  - [ ] Location (Select: Dallas, Austin-A, Austin-B, Austin-C)
  - [ ] Status (Select: Active, Needs Service, Retired)
  - [ ] Purchase Date (Date)
  - [ ] Purchase Cost (Number, currency)
  - [ ] Vendor (Text)
  - [ ] Warranty Expiry (Date)
  - [ ] Depreciation Category (Select: 5-year, 7-year, 27.5-year)
  - [ ] Service Interval (Number, days)
  - [ ] Last Service (Date)
  - [ ] Next Service Due (Formula: `Last Service + Service Interval`)
  - [ ] Documentation (URL) - Link to NotebookLM
  - [ ] QR Code (Files)
  - [ ] Photo (Files)
  - [ ] Notes (Text)

- [ ] Create `Maintenance Log` database:
  - [ ] Log ID (Title) - Format: `ML-2026-001`
  - [ ] Asset (Relation → Asset Inventory)
  - [ ] Date (Date)
  - [ ] Type (Select: Preventive, Repair, Inspection, Emergency)
  - [ ] Description (Text)
  - [ ] Cost (Number, currency)
  - [ ] Vendor/Tech (Text)
  - [ ] Receipt (Files)
  - [ ] Notes (Text)

- [ ] Create `Depreciation Schedule` database (optional):
  - [ ] Asset (Relation → Asset Inventory)
  - [ ] Tax Year (Select)
  - [ ] Beginning Value (Number)
  - [ ] Depreciation Amount (Number)
  - [ ] Ending Value (Formula)
  - [ ] Method (Text)

- [ ] Get database IDs and add to `~/scripts/ecosystem.env`:
  ```bash
  NOTION_ASSETS_DB_ID=your-database-id
  NOTION_MAINTENANCE_DB_ID=your-database-id
  NOTION_DEPRECIATION_DB_ID=your-database-id  # optional
  ```

### Initial Data Entry (Per Property)
**Dallas (DAL)**
- [ ] DAL-HVAC-01: ____________________
- [ ] DAL-APPL-01: ____________________
- [ ] DAL-APPL-02: ____________________

**Austin Main (ATX-A)**
- [ ] ATX-A-HVAC-01: ____________________
- [ ] ATX-A-APPL-01: ____________________
- [ ] ATX-A-APPL-02: ____________________

**Austin ADU B (ATX-B)**
- [ ] ATX-B-HVAC-01: ____________________
- [ ] ATX-B-APPL-01: ____________________

**Austin ADU C (ATX-C)** - Coming Soon
- [ ] (Add when property is ready)

---

## Phase 2: ecosystem-mcp-server Integration

### Add Asset Tools to MCP Server
Reference: MCP integration plan created during this session

- [ ] Add environment variable handling:
  - [ ] `NOTION_ASSETS_DB_ID`
  - [ ] `NOTION_MAINTENANCE_DB_ID`
  - [ ] `ASSET_SCRIPTS_PATH` configuration

- [ ] Implement MCP tools in `server.py`:
  - [ ] `get_maintenance_due(days, property)` - Query due maintenance
  - [ ] `create_asset(...)` - Create new asset
  - [ ] `log_maintenance(...)` - Log maintenance entry
  - [ ] `get_property_assets(property)` - List assets by property
  - [ ] `get_depreciation_report(tax_year, property)` - Generate tax report
  - [ ] `generate_asset_qr(asset_id)` - Generate QR code

### Daily Briefing Integration
- [ ] Add `get_asset_maintenance_status()` to `daily_briefing.py`
- [ ] Update `generate_briefing()` to include assets
- [ ] Add maintenance section to `format_briefing_text()`

### Notion Automation Queue
- [ ] Add command handlers to `notion_control.py`:
  - [ ] `maintenance-check` command
  - [ ] `maintenance-log` command
  - [ ] `depreciation-report` command

### Testing
- [ ] Test: `get_maintenance_due()` returns correct assets
- [ ] Test: `create_asset()` creates in Notion
- [ ] Test: Daily briefing shows maintenance status
- [ ] Test: Automation queue processes asset commands

---

## Phase 3: NotebookLM Setup

Reference: `productivity/asset-manager/references/notebooklm-guide.md`

### Create Property Notebooks
- [ ] **Dallas Property**
  - [ ] Create notebook in NotebookLM
  - [ ] Upload: Lease agreement
  - [ ] Upload: HVAC manual + warranty
  - [ ] Upload: Appliance manuals
  - [ ] Upload: Property inspection report

- [ ] **Austin Main (Unit A)**
  - [ ] Create notebook in NotebookLM
  - [ ] Upload: Lease agreement
  - [ ] Upload: HVAC manual + warranty
  - [ ] Upload: Appliance manuals

- [ ] **Austin ADU B**
  - [ ] Create notebook in NotebookLM
  - [ ] Upload: Lease agreement
  - [ ] Upload: Mini-split/HVAC manual
  - [ ] Upload: Appliance manuals

- [ ] **Austin ADU C** (when ready)
  - [ ] Create notebook in NotebookLM
  - [ ] Upload documents as acquired

- [ ] **Treehouse General**
  - [ ] Create notebook in NotebookLM
  - [ ] Upload: Insurance policies
  - [ ] Upload: LLC operating agreement
  - [ ] Upload: Multi-property documents

### Create Consulting Notebooks
- [ ] **Methodologies**
  - [ ] Create notebook
  - [ ] Upload: Your frameworks and templates

- [ ] **Per-Client** (as needed)
  - [ ] Create notebook for active clients
  - [ ] Upload: Discovery notes, proposals, meeting notes

### Test Queries
- [ ] Property: "What's the warranty on the Dallas HVAC?"
- [ ] Lease: "What's the notice period for Austin A?"
- [ ] Troubleshooting: "What does error code E4 mean?"

---

## Phase 4: Full Integration

### Link Notion ↔ NotebookLM
- [ ] For each asset in Notion:
  - [ ] Ensure docs are in NotebookLM
  - [ ] Add notebook reference URL to Documentation field

### Generate QR Codes
- [ ] Generate QR codes for all entered assets
- [ ] Print on weatherproof labels
- [ ] Affix to physical assets

### Create Notion Dashboard
- [ ] Dashboard page with:
  - [ ] Asset count by property (DAL, ATX-A, ATX-B, ATX-C)
  - [ ] Maintenance due this week
  - [ ] Recent maintenance log
  - [ ] Total asset value by property

### End-to-End Testing
- [ ] Workflow: Create asset → Generate QR → Print label
- [ ] Workflow: Log maintenance → Next due updates automatically
- [ ] Workflow: Query NotebookLM → Get answer with source
- [ ] Workflow: Generate depreciation report → Export CSV
- [ ] Workflow: Ask Claude "What maintenance is due?" → Get MCP response

---

## Phase 5: Ongoing Operations

### Weekly Check (5 min)
- [ ] Check: Any maintenance due this week?
- [ ] Check: Any overdue maintenance?
- [ ] Action: Log any completed maintenance

### Monthly Review (15 min)
- [ ] Review: Asset inventory accuracy
- [ ] Review: Maintenance log completeness
- [ ] Upload: Any new manuals/warranties to NotebookLM

### Annual Tasks (January)
- [ ] Generate depreciation report for previous year
- [ ] Export CSV for accountant
- [ ] Review asset values and update if needed
- [ ] Archive retired assets

---

## Quick Wins (Start Here)

Small tasks that prove the system works:

- [ ] Create 1 NotebookLM notebook (Dallas Property)
- [ ] Upload 1 manual (HVAC is a good start)
- [ ] Query: "What's the warranty period?" - feel the magic
- [ ] Create Notion Asset Inventory database
- [ ] Enter 1 asset (your most expensive one)
- [ ] Generate 1 QR code and affix it

---

## Blocked / Waiting

| Item | Waiting On | Date Added |
|------|------------|------------|
| Notion databases | User to create in Notion | 2026-01-18 |
| ecosystem-mcp-server integration | Notion DBs must exist first | 2026-01-18 |
| Austin ADU C assets | Property not ready | 2026-01-18 |

---

## ✅ Completed Archive

### Session: 2026-01-18

**Planning & Design**
- [x] Create UNIFIED-SYSTEM-PLAN.md
- [x] Create IMPLEMENTATION-CHECKLIST.md
- [x] Define naming conventions (DAL, ATX-A, ATX-B, ATX-C)
- [x] Design Notion database schema
- [x] Compare tool options (NotebookLM vs Notion vs Sheets)
- [x] Document Ralph Wiggum philosophy
- [x] Create NotebookLM setup guide

**Asset Manager Skill**
- [x] Build asset_crud.py (CRUD operations)
- [x] Build qr_generator.py (QR code generation)
- [x] Build maintenance.py (maintenance logging/tracking)
- [x] Build depreciation.py (tax depreciation calculations)
- [x] Create naming-conventions.md
- [x] Create notebooklm-guide.md
- [x] Update ecosystem-config with new DB variables

**MCP Integration Planning**
- [x] Design 6 new MCP tools specification
- [x] Plan daily briefing integration
- [x] Plan Notion automation queue commands

---

*Last Updated: 2026-01-18*
*Next Focus: Create Notion databases, then Quick Wins*
