# Implementation Checklist: Unified System Build

> **Ethos:** Chip away. Each checkbox is progress. Don't try to do it all at once.

---

## Phase 0: Foundation (Do First)

### Prerequisites
- [ ] Verify Notion API token is valid in `ecosystem.env`
- [ ] Test Pushover notifications are working
- [ ] Verify Python environment has required packages

### Documentation
- [ ] Review UNIFIED-SYSTEM-PLAN.md
- [ ] Locate Ralph Wiggum plugin original reference (check other repos)
- [ ] Update README.md with new system overview

---

## Phase 1: Asset Database

### Notion Setup
- [ ] Create `Asset Inventory` database with all properties:
  - [ ] Asset ID (Title)
  - [ ] Name (Text)
  - [ ] Category (Select: HVAC, Appliance, Tool, Tech, Plumbing, Electrical, Furniture, Landscaping, Safety, Misc)
  - [ ] Location (Select: property addresses, rooms)
  - [ ] Status (Select: Active, Needs Service, Retired)
  - [ ] Purchase Date (Date)
  - [ ] Purchase Cost (Number, currency)
  - [ ] Vendor (Text)
  - [ ] Warranty Expiry (Date)
  - [ ] Depreciation Category (Select: 5-year, 7-year, 27.5-year)
  - [ ] Depreciation Method (Select: Straight-line, MACRS)
  - [ ] Service Interval (Number, days)
  - [ ] Last Service (Date)
  - [ ] Next Service Due (Formula: Last Service + Service Interval)
  - [ ] Documentation (URL)
  - [ ] QR Code (Files)
  - [ ] Photo (Files)
  - [ ] Notes (Text)

- [ ] Create `Maintenance Log` database:
  - [ ] Log ID (Title)
  - [ ] Asset (Relation → Asset Inventory)
  - [ ] Date (Date)
  - [ ] Type (Select: Preventive, Repair, Inspection)
  - [ ] Description (Text)
  - [ ] Cost (Number, currency)
  - [ ] Vendor/Tech (Text)
  - [ ] Receipt (Files)
  - [ ] Notes (Text)

- [ ] Create `Depreciation Schedule` database:
  - [ ] Asset (Relation → Asset Inventory)
  - [ ] Tax Year (Select)
  - [ ] Beginning Value (Number)
  - [ ] Depreciation Amount (Number)
  - [ ] Ending Value (Formula)
  - [ ] Cumulative Depreciation (Rollup)
  - [ ] Method (Text)

- [ ] Get database IDs and add to ecosystem.env:
  - [ ] `NOTION_ASSETS_DB_ID`
  - [ ] `NOTION_MAINTENANCE_DB_ID`
  - [ ] `NOTION_DEPRECIATION_DB_ID`

### Skill: asset-manager
- [ ] Create directory: `productivity/asset-manager/`
- [ ] Create SKILL.md with frontmatter
- [ ] Create `scripts/` directory
- [ ] Build `asset_crud.py`:
  - [ ] `create_asset()` function
  - [ ] `get_asset()` function
  - [ ] `update_asset()` function
  - [ ] `list_assets()` function
  - [ ] `search_assets()` function
- [ ] Build `qr_generator.py`:
  - [ ] Generate QR code from Notion URL
  - [ ] Add Asset ID label below QR
  - [ ] Save as PNG
  - [ ] Support batch generation
- [ ] Create `references/naming-conventions.md`
- [ ] Test: Create first asset via skill

### Initial Data Entry
- [ ] Identify top 5 assets to enter first (high-value or maintenance-critical)
- [ ] Enter Asset 1: ____________________
- [ ] Enter Asset 2: ____________________
- [ ] Enter Asset 3: ____________________
- [ ] Enter Asset 4: ____________________
- [ ] Enter Asset 5: ____________________
- [ ] Generate QR codes for all 5
- [ ] Print and affix labels

---

## Phase 2: Maintenance Automation

### Extend asset-manager
- [ ] Build `maintenance.py`:
  - [ ] `log_maintenance()` function
  - [ ] `get_maintenance_history()` function
  - [ ] `get_due_maintenance()` function
  - [ ] `update_last_service()` function (auto-updates Next Service Due)

### Ecosystem Integration
- [ ] Update `ecosystem-status/scripts/ecosystem_status.py`:
  - [ ] Add `check_maintenance_due()` function
  - [ ] Query Notion for assets where Next Service Due <= today + 7 days
  - [ ] Display in status output

- [ ] Update `notifications/scripts/notify.py`:
  - [ ] Add `notify_maintenance_due(asset_id, asset_name, service_type)` function

### Automation Setup
- [ ] Create maintenance check script that runs daily
- [ ] Option A: Add to existing LaunchAgent
- [ ] Option B: Create new LaunchAgent for asset checks
- [ ] Test: Manually trigger maintenance reminder

### Depreciation
- [ ] Build `depreciation.py`:
  - [ ] `calculate_straight_line()` function
  - [ ] `calculate_macrs()` function (with IRS tables)
  - [ ] `generate_annual_schedule()` function
  - [ ] `export_tax_report()` function (CSV output)
- [ ] Test: Calculate depreciation for entered assets

---

## Phase 3: NotebookLM Setup

### Create Notebooks
- [ ] **Treehouse LLC**
  - [ ] Create notebook: "Treehouse: [Property Address] Equipment"
  - [ ] Create notebook: "Treehouse: Lease & Legal"
  - [ ] Create notebook: "Treehouse: Financial Records"

- [ ] **Consulting**
  - [ ] Create notebook: "Consulting: Methodologies"
  - [ ] Create notebook: "Consulting: Industry Research"
  - [ ] (Create per-client notebooks as needed)

- [ ] **Personal Knowledge Base**
  - [ ] Create notebook: "PKB: Career Archives"
  - [ ] Create notebook: "PKB: Philosophy & Principles"
  - [ ] (Create per-mentor notebooks as needed)

- [ ] **Tap (Startup)**
  - [ ] Create notebook: "Tap: Product Research"
  - [ ] Create notebook: "Tap: Competitive Analysis"

### Upload Priority Documents
- [ ] Current lease agreement
- [ ] Property inspection reports
- [ ] HVAC manual
- [ ] Major appliance manuals (refrigerator, dishwasher, etc.)
- [ ] Warranty cards/certificates
- [ ] Insurance policy

### Document Query Patterns
- [ ] Create `notebooklm-queries.md` reference file
- [ ] Document 10 most useful queries per domain

### Skill: material-processor
- [ ] Create directory: `productivity/material-processor/`
- [ ] Create SKILL.md with frontmatter
- [ ] Create `scripts/processor.py`:
  - [ ] Accept pasted NotebookLM output
  - [ ] Extract key facts (dates, amounts, names)
  - [ ] Format for Notion entry
  - [ ] Format for markdown notes
  - [ ] Generate atomic note format
- [ ] Create `references/atomic-note-format.md`
- [ ] Create `references/extraction-patterns.md`
- [ ] Test: Process a manual query into structured data

---

## Phase 4: Integration

### Link Systems
- [ ] For each asset in Notion:
  - [ ] Upload relevant docs to NotebookLM
  - [ ] Add NotebookLM notebook URL to Documentation field
- [ ] Update QR codes if needed (should link to Notion which links to NotebookLM)

### Unified Dashboard
- [ ] Create Notion dashboard page:
  - [ ] Asset overview (count by category, total value)
  - [ ] Maintenance due this week
  - [ ] Recent maintenance log
  - [ ] Depreciation summary

### Update ecosystem-config
- [ ] Add new environment variables to `ecosystem.env.example`:
  ```
  # Asset Management
  NOTION_ASSETS_DB_ID=
  NOTION_MAINTENANCE_DB_ID=
  NOTION_DEPRECIATION_DB_ID=
  ```
- [ ] Document in ecosystem-config SKILL.md

### End-to-End Testing
- [ ] Test workflow: New asset creation → QR generation → Label printing
- [ ] Test workflow: Log maintenance → Update dates → Verify next service due
- [ ] Test workflow: Query NotebookLM → Process with skill → Update Notion
- [ ] Test workflow: Generate depreciation report → Export CSV
- [ ] Test workflow: Maintenance due → Notification sent

---

## Phase 5: Refinement (Ongoing)

### Backfill
- [ ] List all remaining assets to enter: ____________________
- [ ] Enter remaining assets (chunk: 5 at a time)
- [ ] Upload remaining manuals/documentation
- [ ] Generate and affix remaining QR labels

### Personal Knowledge Base
- [ ] Gather mentor notes and materials
- [ ] Upload to respective NotebookLM notebooks
- [ ] Gather career archives
- [ ] Upload project retrospectives, lessons learned

### Monthly Review
- [ ] Check: Are notifications working?
- [ ] Check: Is maintenance being logged?
- [ ] Check: Any assets missing from system?
- [ ] Refine: Query patterns based on actual usage

### Annual Tasks
- [ ] January: Run depreciation calculations for previous year
- [ ] January: Export tax reports
- [ ] Review: Asset inventory accuracy
- [ ] Review: Update asset values if needed

---

## Quick Wins (Do Anytime)

These are small tasks that provide immediate value:

- [ ] Create 1 NotebookLM notebook and upload 1 manual
- [ ] Query it: "What's the warranty period?" - feel the magic
- [ ] Enter your most expensive asset into Notion
- [ ] Generate 1 QR code and stick it on something
- [ ] Set up 1 maintenance reminder

---

## Blocked / Waiting

| Item | Waiting On | Date Added |
|------|------------|------------|
| | | |
| | | |

---

## Completed Archive

Move completed phases here for reference:

### ✅ Completed
- [x] Create UNIFIED-SYSTEM-PLAN.md
- [x] Create IMPLEMENTATION-CHECKLIST.md
- [x] Define naming conventions
- [x] Design database schema
- [x] Compare tool options

---

*Last Updated: [DATE]*
*Next Focus: Phase 0 Prerequisites*
