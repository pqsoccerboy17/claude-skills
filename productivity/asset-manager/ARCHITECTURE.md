# Asset Manager Architecture

> **Design Principle:** AI-agnostic, modular, portable. Every component works standalone with clear interfaces. No AI lock-in.

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ASSET MANAGER SYSTEM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │    Gmail     │    │   Manual     │    │    Drive     │          │
│  │   Scanner    │───▶│   Finder     │───▶│   Uploader   │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                   │                   │                    │
│         ▼                   ▼                   ▼                    │
│  ┌─────────────────────────────────────────────────────┐           │
│  │                  Review Queue                        │           │
│  │        (JSON file - human review interface)          │           │
│  └─────────────────────────────────────────────────────┘           │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │    Notion    │    │  NotebookLM  │    │     QR       │          │
│  │    Sync      │    │  (via Drive) │    │  Generator   │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. AI-Agnostic
- Core logic is pure Python with no AI dependencies
- AI (Claude, GPT, etc.) can orchestrate but isn't required
- All components have CLI interfaces for manual operation
- Configuration via environment variables and JSON files

### 2. Modular Architecture
- Each component is a standalone Python module
- Components communicate via well-defined data structures
- No tight coupling between components
- Can run any component independently

### 3. Data Portability
- All data stored in standard formats (JSON, CSV)
- Notion is optional - system works with local JSON
- Easy export/import between systems
- Version controlled configurations

### 4. Fail-Safe Design
- Uncertain items go to review queue (never auto-commit)
- All operations are idempotent
- Comprehensive logging
- Dry-run mode for all operations

## Component Specifications

### 1. Gmail Scanner (`gmail_scanner.py`)

**Purpose:** Extract purchase information from Gmail emails

**Input:**
- Gmail API credentials (token.json)
- Configuration: vendors, date range, keywords

**Output:**
```python
PurchaseRecord = {
    "id": str,              # Unique ID (hash of email)
    "vendor": str,          # Amazon, Home Depot, etc.
    "product_name": str,    # Extracted product name
    "model_number": str,    # If available
    "purchase_date": str,   # ISO format
    "price": float,         # If available
    "email_id": str,        # Gmail message ID
    "email_subject": str,   # For reference
    "confidence": float,    # 0.0-1.0 extraction confidence
    "raw_snippet": str,     # Original text for review
    "suggested_property": str,  # DAL, ATX-A, etc. (if detected)
    "suggested_category": str,  # HVAC, APPL, etc. (if detected)
    "status": str           # "pending_review", "approved", "rejected"
}
```

**CLI Interface:**
```bash
python gmail_scanner.py --days 365 --vendors amazon,homedepot --output purchases.json
python gmail_scanner.py --dry-run --days 30  # Preview only
python gmail_scanner.py --email-id <id>      # Process single email
```

**Supported Vendors:**
- Amazon (order confirmations, shipping)
- Home Depot (receipts, order confirmations)
- Lowe's (receipts, order confirmations)
- Best Buy (receipts, order confirmations)
- Costco (receipts)
- Walmart (receipts)
- Target (receipts)
- Wayfair (order confirmations)
- IKEA (order confirmations)
- Menards (receipts)
- Ace Hardware (receipts)

### 2. Manual Finder (`manual_finder.py`)

**Purpose:** Find and download product manuals from the web

**Input:**
```python
ProductQuery = {
    "product_name": str,
    "model_number": str,    # Optional but preferred
    "brand": str,           # Optional
    "purchase_id": str      # Reference to PurchaseRecord
}
```

**Output:**
```python
ManualResult = {
    "purchase_id": str,
    "manual_url": str,
    "manual_path": str,     # Local path if downloaded
    "source": str,          # "manufacturer", "manualslib", "search"
    "confidence": float,
    "file_size": int,
    "status": str           # "found", "not_found", "review_needed"
}
```

**CLI Interface:**
```bash
python manual_finder.py --product "LG Refrigerator" --model "LRMVS3006S"
python manual_finder.py --input purchases.json --output manuals.json
python manual_finder.py --download --output-dir ./manuals/
```

**Search Strategy:**
1. Manufacturer website (highest confidence)
2. ManualsLib.com
3. ManualsOnline.com
4. Google search: "{product} {model} user manual PDF"

### 3. Drive Uploader (`drive_uploader.py`)

**Purpose:** Upload files to Google Drive with proper organization

**Input:**
```python
UploadRequest = {
    "local_path": str,
    "drive_folder": str,    # "Dallas/Manuals", "Austin-A/Warranties"
    "filename": str,        # Optional rename
    "asset_id": str,        # For naming convention
    "doc_type": str         # "manual", "warranty", "receipt"
}
```

**Output:**
```python
UploadResult = {
    "local_path": str,
    "drive_id": str,
    "drive_url": str,
    "folder_path": str,
    "status": str           # "uploaded", "exists", "failed"
}
```

**CLI Interface:**
```bash
python drive_uploader.py --file manual.pdf --folder "Dallas/Manuals" --asset-id "DAL-HVAC-01"
python drive_uploader.py --batch manuals.json --create-folders
python drive_uploader.py --list-folders  # Show Drive structure
```

**Folder Structure:**
```
Treehouse-Assets/
├── Dallas/
│   ├── Manuals/
│   ├── Warranties/
│   ├── Receipts/
│   └── Service-Records/
├── Austin-A/
│   └── (same structure)
├── Austin-B/
│   └── (same structure)
├── Austin-C/
│   └── (same structure)
└── Treehouse-General/
    ├── Insurance/
    ├── LLC-Documents/
    └── Multi-Property/
```

### 4. Review Queue (`review_queue.py`)

**Purpose:** Manage items needing human review

**Storage:** `~/.config/treehouse/review_queue.json`

**Data Structure:**
```python
ReviewItem = {
    "id": str,
    "type": str,            # "purchase", "manual", "property_match"
    "created_at": str,
    "data": dict,           # Original record
    "suggested_action": str,
    "notes": str,
    "status": str           # "pending", "approved", "rejected", "modified"
}
```

**CLI Interface:**
```bash
python review_queue.py --list                    # Show pending items
python review_queue.py --show <id>               # Show item details
python review_queue.py --approve <id>            # Approve item
python review_queue.py --reject <id>             # Reject item
python review_queue.py --modify <id> --json '{}' # Modify and approve
python review_queue.py --export approved.json    # Export approved items
```

### 5. Notion Sync (`notion_sync.py`)

**Purpose:** Sync approved items to Notion databases

**Input:** Approved items from review queue

**CLI Interface:**
```bash
python notion_sync.py --create-asset purchases.json
python notion_sync.py --log-maintenance maintenance.json
python notion_sync.py --dry-run  # Preview changes
python notion_sync.py --export assets.json  # Backup from Notion
```

## Data Flow

### Full Pipeline (Automated)
```
1. Gmail Scanner
   └── Extracts purchases → purchases.json

2. Manual Finder
   └── Finds manuals → manuals.json
   └── Downloads PDFs → ./manuals/

3. Drive Uploader
   └── Uploads to Drive → upload_results.json

4. Review Queue
   └── Items with confidence < 0.8 → review_queue.json
   └── Human reviews and approves

5. Notion Sync
   └── Creates/updates Notion records
```

### Manual Operation (Any Component)
```bash
# Run just the Gmail scanner
python gmail_scanner.py --days 30 --output purchases.json

# Manually add an item
echo '{"product": "AC Unit", "vendor": "Home Depot"}' | python review_queue.py --add

# Upload a single file
python drive_uploader.py --file manual.pdf --folder "Dallas/Manuals"
```

## Configuration

### Environment Variables
```bash
# Google APIs
TREEHOUSE_CREDENTIALS_PATH=~/.config/treehouse/credentials.json
TREEHOUSE_TOKEN_PATH=~/.config/treehouse/token.json

# Notion (optional)
NOTION_TOKEN=secret_xxx
NOTION_ASSETS_DB_ID=xxx
NOTION_MAINTENANCE_DB_ID=xxx

# Notifications (optional)
PUSHOVER_USER_KEY=xxx
PUSHOVER_APP_TOKEN=xxx
```

### Config File (`~/.config/treehouse/config.json`)
```json
{
  "properties": {
    "DAL": {"name": "Dallas", "keywords": ["dallas", "dal"]},
    "ATX-A": {"name": "Austin Main", "keywords": ["austin", "main"]},
    "ATX-B": {"name": "Austin ADU B", "keywords": ["adu", "unit b"]},
    "ATX-C": {"name": "Austin ADU C", "keywords": ["adu c"]}
  },
  "vendors": {
    "amazon": {"domains": ["amazon.com"], "patterns": ["order confirmation"]},
    "homedepot": {"domains": ["homedepot.com"], "patterns": ["receipt", "order"]}
  },
  "categories": {
    "HVAC": ["ac", "air conditioner", "furnace", "hvac", "thermostat"],
    "APPL": ["refrigerator", "washer", "dryer", "dishwasher", "microwave"]
  },
  "review_threshold": 0.8,
  "dry_run": false
}
```

## Testing Strategy

### Unit Tests
- Each module has `test_<module>.py`
- Mock external APIs (Gmail, Drive, Notion)
- Test data extraction patterns

### Integration Tests
- End-to-end pipeline with test data
- Dry-run mode verification
- Review queue workflow

### Test Data
- Sample emails in `tests/fixtures/emails/`
- Sample manuals in `tests/fixtures/manuals/`
- Expected outputs in `tests/fixtures/expected/`

## Error Handling

### Graceful Degradation
- If Notion unavailable → save to local JSON
- If Drive unavailable → save locally, queue for upload
- If vendor pattern fails → add to review queue

### Logging
- All operations logged to `~/.config/treehouse/logs/`
- Structured JSON logs for parsing
- Debug mode for troubleshooting

## Security

### Credentials
- OAuth tokens in `~/.config/treehouse/` (mode 600)
- Never committed to git
- Refresh tokens auto-rotate

### Data
- No PII in logs
- Email content not stored (only extracted fields)
- Review queue excludes sensitive data

## Migration Path

### From Manual Tracking
1. Export existing data to CSV
2. Run `import_legacy.py --csv legacy.csv`
3. Review and approve imported items

### To Different System
1. Export all data: `export_all.py --format csv`
2. All data in standard formats
3. No proprietary dependencies

---

*Last Updated: January 2026*
*Version: 1.0*
