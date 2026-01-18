# Asset Manager

**Purpose:** Automatically track home/property assets by scanning Gmail for purchases, finding product manuals, and organizing everything in Google Drive.

## The Pipeline

```
Gmail Purchases → Review Queue → Find Manuals → Upload to Drive
```

## Quick Reference

### Daily Workflow

```bash
cd ~/claude-skills/productivity/asset-manager/scripts

# 1. SCAN - Pull new purchases from Gmail
python3 gmail_scanner.py --days 30 --output purchases.json

# 2. REVIEW - Check what was found
python3 review_queue.py --list

# 3. APPROVE - Confirm good items
python3 review_queue.py --approve abc123

# 4. EXPORT - Get approved items
python3 review_queue.py --export approved.json
```

### Command Reference

| Situation | Command |
|-----------|---------|
| What did I buy recently? | `python3 gmail_scanner.py --days 30 --dry-run` |
| Save purchases to file | `python3 gmail_scanner.py --days 30 --output purchases.json` |
| What needs my review? | `python3 review_queue.py --list` |
| Show item details | `python3 review_queue.py --show <id>` |
| This looks right | `python3 review_queue.py --approve <id>` |
| This is wrong | `python3 review_queue.py --reject <id>` |
| Queue stats | `python3 review_queue.py --stats` |

## Modules

### gmail_scanner.py
Scans Gmail for purchase emails from 11 vendors:
- Amazon, Home Depot, Lowe's, Best Buy, Costco
- Walmart, Target, Wayfair, IKEA, Menards, Ace Hardware

**Features:**
- Extracts product names, prices, dates
- Detects property (DAL, ATX-A, ATX-B, ATX-C)
- Confidence scoring (items < 80% go to review queue)

### review_queue.py
Human review interface for uncertain items.

**Features:**
- List pending items
- Approve/reject with reasons
- Modify item data before approval
- Export approved items

### manual_finder.py
Finds product manuals online.

**Features:**
- Searches manufacturer sites
- Searches ManualsLib
- Downloads PDFs
- Rate limiting to avoid blocks

### drive_uploader.py
Uploads files to Google Drive with organization.

**Folder Structure:**
```
Treehouse-Assets/
├── Dallas/
│   ├── Manuals/
│   ├── Warranties/
│   └── Receipts/
├── Austin-A/
├── Austin-B/
└── Austin-C/
```

## Configuration

### Key Files

| Location | Purpose |
|----------|---------|
| `~/.config/treehouse/token.json` | Gmail auth (auto-refreshes) |
| `~/.config/treehouse/credentials.json` | OAuth credentials |
| `~/.config/treehouse/review_queue.json` | Pending review items |

### Troubleshooting

```bash
# Token expired? Re-auth:
rm ~/.config/treehouse/token.json
python3 gmail_scanner.py --days 1 --dry-run

# Need help?
python3 gmail_scanner.py --help
python3 review_queue.py --help
```

## Architecture

See [ARCHITECTURE.md](https://github.com/pqsoccerboy17/claude-skills/blob/main/productivity/asset-manager/ARCHITECTURE.md) for full technical details.
