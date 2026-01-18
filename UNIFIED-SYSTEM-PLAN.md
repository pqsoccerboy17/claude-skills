# Unified System Plan: NotebookLM + Asset Management Integration

> **Philosophy:** "Ralph Wiggum Plugin Ethos" - Incremental development for non-developers. Small focused changes, clear success criteria, test before commit, chip away progressively.
>
> *Reference: [github.com/pqsoccerboy17/Ralph-Wiggum](https://github.com/pqsoccerboy17/Ralph-Wiggum)*

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Philosophy](#system-philosophy)
3. [Tool Comparison: Static Library vs Dynamic Tracker](#tool-comparison)
4. [Architecture Design](#architecture-design)
5. [Asset Management System](#asset-management-system)
6. [NotebookLM Integration](#notebooklm-integration)
7. [Naming Conventions](#naming-conventions)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Skill Specifications](#skill-specifications)

---

## Executive Summary

This plan unifies two parallel initiatives into a cohesive "Retire Now" efficiency system:

| Initiative | Purpose | Primary Tool |
|------------|---------|--------------|
| **Static Library** | Manuals, leases, warranties, mentor wisdom | NotebookLM |
| **Dynamic Tracker** | Assets, maintenance, depreciation, daily ops | Notion |

**Key Insight:** NotebookLM excels at *comprehension* (query documents), Notion excels at *operations* (track state changes). Using both in their strengths creates a system greater than either alone.

---

## System Philosophy

### The Ralph Wiggum Plugin Ethos

> *Source: [Ralph-Wiggum Repository](https://github.com/pqsoccerboy17/Ralph-Wiggum)*

The Ralph Wiggum approach is designed for **non-developer users** who leverage AI (Claude Code) for technical implementation. The core principles:

#### Development Principles

1. **Small & Focused** - Each function, script, or skill does exactly one thing well
2. **Incremental Changes** - Build piece by piece, not all at once
3. **Clear Success Criteria** - Define what "done" looks like before starting
4. **Test Before Commit** - Always validate changes work before saving
5. **Plain Communication** - Explain errors and decisions in simple terms

#### Task Classification

| Safe for Autonomous Work | Requires Human Review |
|-------------------------|----------------------|
| Testing & validation | Security implementations |
| Documentation updates | Payment/financial logic |
| Code formatting/linting | Architectural decisions |
| Simple bug fixes | Database migrations |
| Adding comments | Credential handling |

#### Workflow Cycle

```
1. UNDERSTAND → What needs to be done?
2. PLAN       → How will we approach it?
3. IMPLEMENT  → Make small, focused changes
4. TEST       → Validate it works
5. COMMIT     → Save with clear message
6. REPEAT     → Next small piece
```

### Applied to This System

```
DON'T: Build a monolithic "asset management platform"
DO:    Build small pieces that connect

Phase 1: QR label generator script (one thing)
Phase 2: Notion asset database (one thing)
Phase 3: Maintenance reminder automation (one thing)
Phase 4: Depreciation tracker (one thing)
Phase 5: NotebookLM notebooks (one thing)
Phase 6: Material processor skill (one thing)

Each piece works alone. Together they're powerful.
Each piece has clear success criteria.
Each piece is tested before moving on.
```

---

## Tool Comparison

### Static Library vs Dynamic Tracker Decision Matrix

| Requirement | NotebookLM | Excel/Sheets | Notion | MaintainX |
|-------------|------------|--------------|--------|-----------|
| **Query unstructured docs** | ✅ Excellent | ❌ Poor | ⚠️ Limited | ❌ Poor |
| **Track asset state changes** | ❌ Not designed for this | ⚠️ Manual | ✅ Excellent | ✅ Excellent |
| **Automated reminders** | ❌ No | ⚠️ Manual | ✅ Native | ✅ Native |
| **QR code integration** | ❌ No | ⚠️ Manual | ✅ Via links | ✅ Native |
| **Financial tracking** | ❌ No | ✅ Good | ✅ Good | ⚠️ Limited |
| **API access** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Existing in your ecosystem** | 🆕 New | ⚠️ Separate | ✅ Central hub | 🆕 New |
| **Cost** | Free | Free | Free/Paid | $16+/mo |
| **Learning curve** | Low | Low | Medium | Medium |

### Recommendation

```
┌─────────────────────────────────────────────────────────────────┐
│                     RECOMMENDED ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   STATIC LIBRARY (NotebookLM)     DYNAMIC TRACKER (Notion)      │
│   ─────────────────────────────   ────────────────────────      │
│                                                                  │
│   • Equipment manuals             • Asset inventory              │
│   • Lease agreements              • Maintenance log              │
│   • Warranties & receipts         • Service schedules            │
│   • Mentor teachings              • Depreciation tracking        │
│   • Career archives               • Vendor contacts              │
│   • Industry research             • Cost history                 │
│   • Client discovery docs         • QR code links                │
│                                                                  │
│   "What does the manual say?"     "When was this last serviced?" │
│   "What's the warranty period?"   "What's the depreciation YTD?" │
│   "What did my mentor advise?"    "Schedule next maintenance"    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why NOT MaintainX:**
- You already have Notion as your central hub
- Adding another tool fragments your ecosystem
- MaintainX is overkill for 1 rental property
- Monthly cost adds up for features you won't use

**Why NOT just Notion for everything:**
- Notion's search can't intelligently query PDFs
- You'd need to manually extract and paste content
- NotebookLM's AI comprehension is genuinely better for "what does this document say?"

**The Hybrid Approach:**
- NotebookLM: Upload PDFs, query with natural language
- Notion: Track operational state, trigger automations
- Link them via Asset IDs (QR codes point to Notion, Notion links to NotebookLM notebooks)

---

## Architecture Design

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        UNIFIED KNOWLEDGE SYSTEM                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   CAPTURE    │    │   PROCESS    │    │    ACTION    │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                   │                        │
│         ▼                   ▼                   ▼                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │  Raw Inputs  │───▶│  NotebookLM  │───▶│    Claude    │               │
│  │              │    │  (Comprehend) │    │  (Execute)   │               │
│  │ • PDFs       │    │              │    │              │               │
│  │ • Manuals    │    │ "What does   │    │ • Draft comms│               │
│  │ • Receipts   │    │  this say?"  │    │ • Update DB  │               │
│  │ • Research   │    │              │    │ • Generate   │               │
│  └──────────────┘    └──────────────┘    │   reports    │               │
│                             │            └──────────────┘               │
│                             │                   │                        │
│                             ▼                   ▼                        │
│                      ┌──────────────┐    ┌──────────────┐               │
│                      │   Extracted  │    │    Notion    │               │
│                      │   Insights   │───▶│  (Operate)   │               │
│                      │              │    │              │               │
│                      │ Atomic notes │    │ • Assets     │               │
│                      │ Key facts    │    │ • Maintenance│               │
│                      │ Decisions    │    │ • Schedules  │               │
│                      └──────────────┘    │ • Tracking   │               │
│                                          └──────────────┘               │
│                                                 │                        │
│                                                 ▼                        │
│                                          ┌──────────────┐               │
│                                          │   QR Codes   │               │
│                                          │  Link to DB  │               │
│                                          └──────────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Examples

**Example 1: New HVAC Unit Installed**

```
1. CAPTURE
   └── Receive: Invoice, manual, warranty card

2. PROCESS (NotebookLM)
   └── Upload to "Treehouse Equipment" notebook
   └── Query: "What's the warranty period and what does it cover?"

3. ACTION (Claude + Notion)
   └── Claude: Extract key specs, warranty dates
   └── Notion: Create asset record with:
       • Asset ID: TH-HVAC-01
       • Install date, cost, warranty expiry
       • Maintenance schedule (filter: 90 days, service: annual)
   └── Generate: QR code label → affix to unit

4. ONGOING
   └── Notion: Auto-reminder at 90 days for filter
   └── NotebookLM: "What does the manual say about the E4 error code?"
   └── Claude: Draft maintenance request to vendor
```

**Example 2: Tax Time Depreciation**

```
1. Query Notion: "Show all assets with depreciation schedules"
   └── Returns: List with purchase dates, costs, categories

2. Export to CSV → Process with csv-data-summarizer skill
   └── Calculate: YTD depreciation per asset
   └── Generate: Tax-ready depreciation schedule

3. Cross-reference NotebookLM: "What receipts support these purchases?"
   └── Verify: Documentation exists for each depreciable asset
```

---

## Asset Management System

### Database Schema (Notion)

**Database: `Asset Inventory`**

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `Asset ID` | Title | Unique identifier | `TH-HVAC-01` |
| `Name` | Text | Human-readable name | "Primary AC Unit" |
| `Category` | Select | Asset type | HVAC, Appliance, Tool, Tech |
| `Location` | Select | Physical location | Property address, Room |
| `Status` | Select | Current state | Active, Needs Service, Retired |
| `Purchase Date` | Date | Acquisition date | 2024-01-15 |
| `Purchase Cost` | Number | Original cost | $3,500 |
| `Vendor` | Text | Where purchased | "Home Depot" |
| `Warranty Expiry` | Date | When warranty ends | 2029-01-15 |
| `Depreciation Category` | Select | IRS category | 5-year, 7-year, 27.5-year |
| `Depreciation Method` | Select | Calculation method | Straight-line, MACRS |
| `Service Interval` | Number | Days between service | 90 (for filters) |
| `Last Service` | Date | Most recent maintenance | 2024-10-01 |
| `Next Service Due` | Formula | Auto-calculated | `Last Service + Service Interval` |
| `Service History` | Relation | Link to maintenance log | → Maintenance Log |
| `Documentation` | URL | Link to NotebookLM | notebook URL |
| `QR Code` | Files | Generated QR image | QR PNG |
| `Photo` | Files | Current photo | Asset photo |
| `Notes` | Text | Additional info | "Filter size: 20x25x1" |

**Database: `Maintenance Log`**

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `Log ID` | Title | Unique identifier | `ML-2024-001` |
| `Asset` | Relation | Which asset | → Asset Inventory |
| `Date` | Date | Service date | 2024-10-01 |
| `Type` | Select | Service type | Preventive, Repair, Inspection |
| `Description` | Text | What was done | "Replaced air filter" |
| `Cost` | Number | Service cost | $25 |
| `Vendor/Tech` | Text | Who performed | "Self" or vendor name |
| `Receipt` | Files | Documentation | Receipt image |
| `Notes` | Text | Additional info | "Used MERV 11 filter" |

**Database: `Depreciation Schedule`**

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `Asset` | Relation | Which asset | → Asset Inventory |
| `Tax Year` | Select | Applicable year | 2024 |
| `Beginning Value` | Number | Start of year value | $3,500 |
| `Depreciation Amount` | Number | This year's depreciation | $700 |
| `Ending Value` | Formula | End of year value | $2,800 |
| `Cumulative Depreciation` | Rollup | Total depreciated | $700 |
| `Method` | Text | Calculation used | "5-year straight-line" |

### QR Code Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      QR CODE WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CREATE ASSET                                                 │
│     └── Add to Notion database                                   │
│     └── Assign Asset ID (TH-HVAC-01)                            │
│     └── Get Notion page URL                                      │
│                                                                  │
│  2. GENERATE QR CODE                                             │
│     └── Run: qr-generator skill                                  │
│     └── Input: Asset ID + Notion URL                            │
│     └── Output: QR code PNG with ID label                       │
│                                                                  │
│  3. PRINT & AFFIX                                                │
│     └── Print on weatherproof label (Brother P-Touch or similar)│
│     └── Affix to asset in visible location                      │
│                                                                  │
│  4. SCAN TO ACCESS                                               │
│     └── Phone camera → Notion page                              │
│     └── See: All asset details, service history, docs           │
│     └── Action: Log maintenance, update status                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Preventive Maintenance Automation

**Notion Automation (Native):**

```
TRIGGER: When "Next Service Due" is today
ACTION:
  1. Send notification (via Notion → Zapier → Pushover)
  2. Create task in Tasks database
  3. Update Status to "Needs Service"
```

**Alternative: Claude Skill Check (ecosystem-status integration):**

```python
# Add to ecosystem_status.py

def check_maintenance_due():
    """Check Notion for assets with maintenance due."""
    # Query Notion API for assets where Next Service Due <= today
    # Return list of assets needing attention
    # Integrate with notify.py for alerts
```

### Depreciation Tracking

**Supported Methods:**

| Method | Use Case | Calculation |
|--------|----------|-------------|
| **Straight-Line** | Most equipment | (Cost - Salvage) / Useful Life |
| **MACRS 5-Year** | Computers, vehicles | IRS percentage tables |
| **MACRS 7-Year** | Furniture, fixtures | IRS percentage tables |
| **27.5-Year** | Residential rental property | Straight-line |

**Annual Workflow:**

```
1. January: Run depreciation skill
   └── Query all assets with depreciation schedules
   └── Calculate current year depreciation
   └── Update Depreciation Schedule database

2. Tax Time: Export report
   └── Generate IRS-ready depreciation schedule
   └── Cross-reference with receipts in NotebookLM
   └── Output: CSV or Excel for accountant
```

---

## NotebookLM Integration

### Notebook Structure

```
NotebookLM/
├── Treehouse LLC/
│   ├── [Property: 123 Main St]
│   │   ├── Lease agreement
│   │   ├── Inspection reports
│   │   └── Property disclosures
│   │
│   ├── [Equipment Manuals]
│   │   ├── HVAC manual
│   │   ├── Appliance manuals
│   │   └── System documentation
│   │
│   └── [Financial Records]
│       ├── Purchase documents
│       ├── Insurance policies
│       └── Warranty cards
│
├── Consulting/
│   ├── [Client: Company A]
│   │   ├── Discovery notes
│   │   ├── Signed proposals
│   │   └── Meeting transcripts
│   │
│   ├── [Methodologies]
│   │   ├── Frameworks I use
│   │   ├── Case studies
│   │   └── Templates
│   │
│   └── [Industry Research]
│       ├── Market reports
│       └── Trend analysis
│
├── Personal Knowledge Base/
│   ├── [Mentor: Name]
│   │   ├── Meeting notes
│   │   └── Advice received
│   │
│   ├── [Career Archives]
│   │   ├── Major projects
│   │   └── Lessons learned
│   │
│   └── [Philosophy]
│       ├── Decision frameworks
│       └── Principles
│
└── Tap (Startup)/
    ├── [Product Research]
    ├── [Competitive Analysis]
    └── [User Research]
```

### Query Patterns

| Domain | Sample Queries |
|--------|---------------|
| **Equipment** | "What does the HVAC manual say about the E4 error code?" |
| **Leases** | "What's the security deposit amount and return conditions?" |
| **Warranties** | "Is the refrigerator still under warranty? What does it cover?" |
| **Consulting** | "What were Client A's main concerns from discovery?" |
| **Mentorship** | "What has [Mentor] said about negotiating compensation?" |

### Material Processor Skill

**Purpose:** Bridge between NotebookLM insights and your structured systems.

**Workflow:**

```
1. Query NotebookLM for insights
2. Copy synthesized response
3. Run material-processor skill
4. Skill formats for:
   └── Notion database entry
   └── Markdown knowledge file
   └── Asset record update
   └── Communication draft
```

---

## Naming Conventions

### Asset ID Format

```
{ENTITY}-{CATEGORY}-{SEQUENCE}

ENTITY (2 chars):
  TH = Treehouse LLC (rental property)
  CO = Consulting
  TP = Tap (startup)
  PR = Personal

CATEGORY (variable):
  HVAC   = Heating/cooling
  APPL   = Appliances
  PLMB   = Plumbing
  ELEC   = Electrical
  TOOL   = Tools
  TECH   = Technology/computers
  FURN   = Furniture
  LAND   = Landscaping equipment
  SAFE   = Safety equipment
  MISC   = Miscellaneous

SEQUENCE (2 digits):
  01, 02, 03...
```

**Examples:**

| Asset ID | Meaning |
|----------|---------|
| `TH-HVAC-01` | Treehouse, HVAC unit #1 |
| `TH-APPL-01` | Treehouse, Appliance #1 (refrigerator) |
| `TH-APPL-02` | Treehouse, Appliance #2 (dishwasher) |
| `CO-TECH-01` | Consulting, Tech #1 (work laptop) |
| `PR-TOOL-01` | Personal, Tool #1 (drill) |

### File Naming (Documents)

```
{ASSET-ID}_{DOCTYPE}_{DATE}.{ext}

DOCTYPE:
  manual    = User manual/documentation
  warranty  = Warranty card/certificate
  receipt   = Purchase receipt
  invoice   = Service invoice
  photo     = Asset photograph

Examples:
  TH-HVAC-01_manual_2024-01-15.pdf
  TH-HVAC-01_warranty_2024-01-15.pdf
  TH-HVAC-01_receipt_2024-01-15.pdf
  TH-HVAC-01_photo_2024-01-15.jpg
```

### Maintenance Log ID

```
ML-{YEAR}-{SEQUENCE}

Examples:
  ML-2024-001  (first maintenance log of 2024)
  ML-2024-002  (second maintenance log of 2024)
```

### NotebookLM Notebook Naming

```
{Domain}: {Specific Context}

Examples:
  Treehouse: 123 Main St Equipment
  Treehouse: Lease & Legal
  Consulting: Client ABC Corp
  Consulting: Methodologies
  PKB: Mentor John Smith
  PKB: Career Archives
```

---

## Implementation Roadmap

### Phase 0: Foundation (Prerequisites)

| Task | Description | Effort |
|------|-------------|--------|
| Document Ralph Wiggum philosophy | Add to repo README | Small |
| Verify Notion API access | Ensure ecosystem.env has valid token | Small |
| Verify Pushover setup | Test notifications working | Small |

### Phase 1: Asset Database (Week 1-2)

| Task | Description | Skill/Tool |
|------|-------------|------------|
| Create Notion databases | Asset Inventory, Maintenance Log, Depreciation | Manual in Notion |
| Build `asset-manager` skill | CRUD operations for assets via API | New skill |
| Create QR generator script | Generate QR codes with Asset IDs | Python script |
| Document naming conventions | Add to skill documentation | Documentation |

**Deliverables:**
- [ ] Notion databases live and configured
- [ ] `asset-manager` skill functional
- [ ] QR codes can be generated for any asset
- [ ] First 5 assets entered as proof of concept

### Phase 2: Maintenance Automation (Week 3-4)

| Task | Description | Skill/Tool |
|------|-------------|------------|
| Add maintenance tracking to asset-manager | Log service, update dates | Extend skill |
| Create reminder automation | Check for due maintenance | ecosystem-status integration |
| Connect to notifications | Alert when maintenance due | notify.py |
| Build depreciation calculator | Calculate annual depreciation | Python script |

**Deliverables:**
- [ ] Maintenance can be logged via Claude
- [ ] Daily check for due maintenance
- [ ] Notifications sent for upcoming service
- [ ] Depreciation calculations working

### Phase 3: NotebookLM Setup (Week 5-6)

| Task | Description | Skill/Tool |
|------|-------------|------------|
| Create notebook structure | Set up all notebooks per architecture | Manual in NotebookLM |
| Upload existing documents | Manuals, leases, warranties | Manual upload |
| Document query patterns | Common queries per domain | Documentation |
| Build `material-processor` skill | Format NotebookLM output for systems | New skill |

**Deliverables:**
- [ ] All notebooks created and organized
- [ ] Key documents uploaded (leases, manuals)
- [ ] Query patterns documented
- [ ] Material processor skill functional

### Phase 4: Integration (Week 7-8)

| Task | Description | Skill/Tool |
|------|-------------|------------|
| Link assets to NotebookLM | Add documentation URLs to Notion | Data entry |
| Update ecosystem-status | Add asset/maintenance monitoring | Extend script |
| Create unified dashboard view | Notion dashboard for all systems | Notion |
| End-to-end testing | Full workflow validation | Manual testing |

**Deliverables:**
- [ ] Assets linked to their documentation
- [ ] Ecosystem status includes asset health
- [ ] Dashboard shows unified view
- [ ] Complete workflow documented

### Phase 5: Refinement (Ongoing)

| Task | Description | Frequency |
|------|-------------|-----------|
| Backfill historical assets | Add older equipment | As time permits |
| Upload mentor materials | Personal knowledge base | As time permits |
| Refine automations | Optimize based on usage | Monthly review |
| Update depreciation | Annual tax prep | Annually |

---

## Skill Specifications

### New Skill: `asset-manager`

**Location:** `productivity/asset-manager/`

**Capabilities:**
- Create new asset records in Notion
- Generate QR codes for assets
- Log maintenance entries
- Query asset status and history
- Calculate depreciation
- Export reports (CSV, Excel)

**File Structure:**
```
asset-manager/
├── SKILL.md
├── scripts/
│   ├── asset_crud.py      # Create, read, update, delete
│   ├── qr_generator.py    # QR code generation
│   ├── maintenance.py     # Log and query maintenance
│   └── depreciation.py    # Calculate depreciation
└── references/
    └── naming-conventions.md
```

### New Skill: `material-processor`

**Location:** `productivity/material-processor/`

**Capabilities:**
- Accept NotebookLM synthesized output
- Extract structured data (dates, amounts, key facts)
- Format for Notion database entry
- Format for markdown knowledge files
- Generate atomic notes

**File Structure:**
```
material-processor/
├── SKILL.md
├── scripts/
│   └── processor.py       # Main processing logic
└── references/
    ├── atomic-note-format.md
    └── extraction-patterns.md
```

### Updates to Existing Skills

**ecosystem-status:**
- Add: Asset maintenance due checks
- Add: Depreciation schedule status

**ecosystem-config:**
- Add: `NOTION_ASSETS_DB_ID`
- Add: `NOTION_MAINTENANCE_DB_ID`
- Add: `NOTION_DEPRECIATION_DB_ID`

**notifications:**
- Add: `notify_maintenance_due()` function
- Add: `notify_depreciation_reminder()` function

---

## Success Metrics

### Quantitative

| Metric | Before | Target | How to Measure |
|--------|--------|--------|----------------|
| Time to find manual/warranty | 5-15 min | <1 min | NotebookLM query |
| Missed maintenance reminders | Unknown | 0 | Notification logs |
| Tax prep time (depreciation) | 2-4 hours | 30 min | Export + verify |
| Asset information retrieval | Manual lookup | QR scan | Workflow timing |

### Qualitative

- [ ] Can answer "what does the manual say about X?" in under 60 seconds
- [ ] Never miss a filter change or scheduled maintenance
- [ ] Tax prep is export + verify, not research + calculate
- [ ] New asset onboarding is a 5-minute process
- [ ] Mentor wisdom is queryable, not buried in files

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| NotebookLM changes/discontinues | Core operations in Notion (owned data) |
| Notion API rate limits | Batch operations, caching |
| QR code labels wear off | Use weatherproof labels, store backup in Notion |
| Overcomplicated system | Ralph Wiggum ethos: keep it simple, chip away |
| Not using it | Start with 5 assets, prove value, then expand |

---

## Quick Reference: Where Does What Live?

| Data Type | Location | Why |
|-----------|----------|-----|
| Asset records | Notion | Structured, queryable, automatable |
| Maintenance history | Notion | Relational to assets, trackable |
| Depreciation schedules | Notion | Calculable, exportable |
| QR codes | Notion (attached to asset) | Single source of truth |
| Equipment manuals | NotebookLM | Natural language queryable |
| Lease agreements | NotebookLM | Complex document comprehension |
| Warranties | NotebookLM | Query coverage and terms |
| Purchase receipts | NotebookLM + Notion link | Query + tax reference |
| Vendor contacts | Notion | Operational data |
| Mentor notes | NotebookLM | Wisdom retrieval |

---

## Appendix: Sample Queries

### Asset Management

```
"Create a new asset: HVAC unit, purchased today for $3500 from
Home Depot, 5-year warranty, install at 123 Main St"

"What maintenance is due this week?"

"Show me the service history for TH-HVAC-01"

"Generate depreciation report for 2024 tax year"

"What's the total value of assets at the rental property?"
```

### NotebookLM Queries

```
"What does the HVAC manual say about the E4 error code?"

"What's the procedure for winterizing the sprinkler system?"

"What are the lease terms for early termination?"

"What has [Mentor] advised about work-life balance?"

"What were the key concerns from Client A's discovery call?"
```

### Integrated Workflows

```
"The AC is showing an E4 error. What does that mean and when
was it last serviced?"

→ Claude queries NotebookLM for error code meaning
→ Claude queries Notion for service history
→ Claude synthesizes: "E4 means low refrigerant. Last serviced
   6 months ago. Recommend scheduling service. Draft email to
   HVAC vendor?"
```

---

*Document Version: 1.0*
*Created: 2024*
*Philosophy: Ralph Wiggum Plugin Ethos - Chip away, small wins, progress over perfection*
