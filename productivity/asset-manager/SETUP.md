# Asset Manager Setup Guide

## Quick Start (No Installation Required)

The **review_queue.py** module works immediately with zero dependencies:

```bash
cd productivity/asset-manager/scripts

# Add items manually
python review_queue.py --add --type purchase --json '{"vendor": "Amazon", "product_name": "Refrigerator"}'

# List pending items
python review_queue.py --list

# Approve items
python review_queue.py --approve <item_id>

# Export approved items
python review_queue.py --export approved.json
```

## Module Dependencies

| Module | Dependencies | When Needed |
|--------|--------------|-------------|
| `review_queue.py` | None | Ready now |
| `gmail_scanner.py` | Google API + OAuth | To scan Gmail |
| `manual_finder.py` | beautifulsoup4 | To find manuals |
| `drive_uploader.py` | Google API + OAuth | To upload to Drive |

## Installation Steps

### Step 1: Python Dependencies

```bash
# From the asset-manager directory
pip install -r requirements.txt

# Or install individually:
pip install beautifulsoup4                    # For manual_finder.py
pip install google-api-python-client \
            google-auth-httplib2 \
            google-auth-oauthlib              # For Gmail/Drive
```

### Step 2: Google OAuth Setup (One-Time)

Required for `gmail_scanner.py` and `drive_uploader.py`:

1. **Go to Google Cloud Console:** https://console.cloud.google.com/
2. **Create a new project** (or use existing)
3. **Enable APIs:**
   - Gmail API (for gmail_scanner.py)
   - Google Drive API (for drive_uploader.py)
4. **Create OAuth credentials:**
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: Desktop app
   - Download the JSON file
5. **Save credentials:**
   ```bash
   mkdir -p ~/.config/treehouse
   mv ~/Downloads/client_secret_*.json ~/.config/treehouse/credentials.json
   chmod 600 ~/.config/treehouse/credentials.json
   ```

### Step 3: First Run (Authorize)

```bash
# This will open a browser for OAuth consent
python gmail_scanner.py --days 1 --dry-run

# Token saved to ~/.config/treehouse/token.json
```

## Verify Installation

```bash
# Should show help (no errors)
python gmail_scanner.py --help
python manual_finder.py --help
python drive_uploader.py --help
python review_queue.py --help
```

## Usage Order (Recommended)

```bash
# 1. Scan Gmail for purchases (creates purchases.json)
python gmail_scanner.py --days 365 --output purchases.json

# 2. Review low-confidence items
python review_queue.py --list
python review_queue.py --approve <id>

# 3. Find manuals for approved items
python manual_finder.py --input purchases.json --download --output-dir ./manuals/

# 4. Upload to Drive
python drive_uploader.py --setup  # Create folder structure (first time)
python drive_uploader.py --batch manuals.json
```

## Troubleshooting

### "Error: beautifulsoup4 library required"
```bash
pip install beautifulsoup4
```

### "Error: Google API libraries required"
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### "credentials.json not found"
Follow Step 2 above to create OAuth credentials.

### "Token expired"
Delete token and re-authorize:
```bash
rm ~/.config/treehouse/token.json
python gmail_scanner.py --days 1 --dry-run  # Re-authorizes
```

## Data Storage

All data stored in `~/.config/treehouse/`:
- `credentials.json` - OAuth credentials (you create)
- `token.json` - OAuth token (auto-generated)
- `review_queue.json` - Pending review items
- `review_queue_archive.json` - Approved/rejected history
- `logs/` - Operation logs
