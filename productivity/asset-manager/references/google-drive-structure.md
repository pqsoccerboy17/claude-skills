# Google Drive Folder Structure for NotebookLM Sync

> **Purpose:** Define the Google Drive folder organization that syncs with NotebookLM notebooks for document comprehension and querying.

---

## Table of Contents

1. [Folder Structure](#folder-structure)
2. [File Naming Conventions](#file-naming-conventions)
3. [NotebookLM Linking Strategy](#notebooklm-linking-strategy)
4. [Automation Script Design](#automation-script-design)
5. [One-Time Setup Instructions](#one-time-setup-instructions)
6. [Sync Behavior Reference](#sync-behavior-reference)

---

## Folder Structure

### Complete Hierarchy

```
Google Drive/
└── Treehouse-LLC/
    │
    ├── Properties/
    │   │
    │   ├── Dallas/
    │   │   ├── Manuals/           → Links to "Treehouse: Dallas" notebook
    │   │   ├── Leases/
    │   │   ├── Warranties/
    │   │   └── Inspections/
    │   │
    │   ├── Austin-Main-A/
    │   │   ├── Manuals/           → Links to "Treehouse: Austin Main A" notebook
    │   │   ├── Leases/
    │   │   ├── Warranties/
    │   │   └── Inspections/
    │   │
    │   ├── Austin-ADU-B/
    │   │   ├── Manuals/           → Links to "Treehouse: Austin ADU B" notebook
    │   │   ├── Leases/
    │   │   ├── Warranties/
    │   │   └── Inspections/
    │   │
    │   └── Austin-ADU-C/
    │       ├── Manuals/           → Links to "Treehouse: Austin ADU C" notebook
    │       ├── Leases/
    │       ├── Warranties/
    │       └── Inspections/
    │
    ├── Treehouse-General/
    │   ├── Insurance/             → Links to "Treehouse General" notebook
    │   ├── LLC-Docs/
    │   └── Tax-Records/
    │
    └── Consulting/
        ├── Methodologies/         → Links to "Consulting: Methodologies" notebook
        └── Clients/
            ├── ClientA/           → Links to "Consulting: ClientA" notebook
            ├── ClientB/           → Links to "Consulting: ClientB" notebook
            └── ...

```

### Folder Purposes

#### Property Folders

| Folder | Contents | Example Files |
|--------|----------|---------------|
| `Manuals/` | Equipment user manuals, operating instructions | `DAL-HVAC-01_manual_2024-01-15.pdf` |
| `Leases/` | Signed lease agreements, addendums | `lease_DAL_Smith_2024-06-01.pdf` |
| `Warranties/` | Warranty certificates, coverage documents | `DAL-HVAC-01_warranty_2024-01-15.pdf` |
| `Inspections/` | Property inspections, move-in/out reports | `inspection_DAL_2024-01-15.pdf` |

#### Treehouse-General Folders

| Folder | Contents | Example Files |
|--------|----------|---------------|
| `Insurance/` | Umbrella policies, liability coverage | `TH_insurance_umbrella_2024.pdf` |
| `LLC-Docs/` | Articles of organization, operating agreement | `TH_llc_articles_2022-01.pdf` |
| `Tax-Records/` | EIN letters, tax filings, depreciation schedules | `TH_tax_ein-letter.pdf` |

#### Consulting Folders

| Folder | Contents | Example Files |
|--------|----------|---------------|
| `Methodologies/` | Frameworks, templates, case studies | `discovery-framework.pdf` |
| `Clients/[Name]/` | Client-specific discovery docs, SOWs, deliverables | `sow_ClientA_2024-03.pdf` |

---

## File Naming Conventions

### Asset-Related Documents

Follow the asset naming convention from `naming-conventions.md`:

```
{ASSET-ID}_{DOCTYPE}_{DATE}.pdf
```

| Component | Format | Examples |
|-----------|--------|----------|
| `ASSET-ID` | `{PROPERTY}-{CATEGORY}-{SEQ}` | `DAL-HVAC-01`, `ATX-A-APPL-02` |
| `DOCTYPE` | Lowercase descriptor | `manual`, `warranty`, `receipt`, `invoice` |
| `DATE` | `YYYY-MM-DD` | `2024-01-15` |

**Examples:**
```
DAL-HVAC-01_manual_2024-01-15.pdf
DAL-HVAC-01_warranty_2024-01-15.pdf
ATX-A-APPL-01_manual_2023-08-20.pdf
ATX-B-HVAC-01_warranty_2024-03-10.pdf
```

### Lease Documents

```
lease_{PROPERTY}_{TENANT-LASTNAME}_{START-DATE}.pdf
```

**Examples:**
```
lease_DAL_Smith_2024-06-01.pdf
lease_ATX-A_Johnson_2024-01-15.pdf
lease_ATX-B_Williams_2024-09-01.pdf
```

### Inspection Reports

```
inspection_{PROPERTY}_{DATE}.pdf
inspection_{PROPERTY}_{TYPE}_{DATE}.pdf
```

| Type | Use Case |
|------|----------|
| `movein` | Move-in condition report |
| `moveout` | Move-out condition report |
| `annual` | Annual property inspection |
| `purchase` | Pre-purchase inspection |

**Examples:**
```
inspection_DAL_2024-01-15.pdf
inspection_DAL_movein_2024-06-01.pdf
inspection_ATX-A_annual_2024-07-15.pdf
inspection_ATX-B_moveout_2024-08-31.pdf
```

### LLC and General Documents

```
TH_{DOCTYPE}_{DESCRIPTION}_{DATE}.pdf
```

**Examples:**
```
TH_llc_articles-of-organization_2022-01.pdf
TH_llc_operating-agreement_2022-01.pdf
TH_insurance_umbrella-policy_2024.pdf
TH_insurance_liability_2024.pdf
TH_tax_ein-letter.pdf
```

### Consulting Documents

```
{DOCTYPE}_{CLIENT}_{DATE}.pdf
{DOCTYPE}_{DESCRIPTION}.pdf
```

**Examples:**
```
sow_ClientA_2024-03-15.pdf
proposal_ClientB_2024-06-01.pdf
discovery-notes_ClientA_2024-02-28.pdf
pricing-models-reference.pdf
strategy-engagement-template.pdf
```

---

## NotebookLM Linking Strategy

### Mapping Table

| NotebookLM Notebook | Google Drive Folder(s) | Notes |
|---------------------|------------------------|-------|
| `Treehouse: Dallas` | `Properties/Dallas/Manuals/` | Link all 4 subfolders |
| | `Properties/Dallas/Leases/` | |
| | `Properties/Dallas/Warranties/` | |
| | `Properties/Dallas/Inspections/` | |
| `Treehouse: Austin Main A` | `Properties/Austin-Main-A/Manuals/` | Link all 4 subfolders |
| | `Properties/Austin-Main-A/Leases/` | |
| | `Properties/Austin-Main-A/Warranties/` | |
| | `Properties/Austin-Main-A/Inspections/` | |
| `Treehouse: Austin ADU B` | `Properties/Austin-ADU-B/Manuals/` | Link all 4 subfolders |
| | `Properties/Austin-ADU-B/Leases/` | |
| | `Properties/Austin-ADU-B/Warranties/` | |
| | `Properties/Austin-ADU-B/Inspections/` | |
| `Treehouse: Austin ADU C` | `Properties/Austin-ADU-C/Manuals/` | Create when unit ready |
| | `Properties/Austin-ADU-C/Leases/` | |
| | `Properties/Austin-ADU-C/Warranties/` | |
| | `Properties/Austin-ADU-C/Inspections/` | |
| `Treehouse General` | `Treehouse-General/Insurance/` | Link all 3 subfolders |
| | `Treehouse-General/LLC-Docs/` | |
| | `Treehouse-General/Tax-Records/` | |
| `Consulting: Methodologies` | `Consulting/Methodologies/` | Single folder |
| `Consulting: ClientA` | `Consulting/Clients/ClientA/` | One notebook per client |
| `Consulting: ClientB` | `Consulting/Clients/ClientB/` | |

### Why Multiple Folders Per Notebook?

NotebookLM allows linking multiple Google Drive folders to a single notebook. This approach:

1. **Keeps Drive organized** - Separate folders for different document types
2. **Unified querying** - All property documents queryable in one notebook
3. **Easier maintenance** - Add/remove folders as needs change
4. **Parallel uploads** - Different people can upload to different folders

### Alternative: Single Folder Per Notebook

If managing multiple folder links is cumbersome, use a flatter structure:

```
Properties/
├── Dallas-NotebookLM/           → Single folder linked to notebook
│   ├── [all Dallas documents]
├── Austin-Main-A-NotebookLM/
│   ├── [all Austin A documents]
...
```

**Trade-off:** Simpler linking, but less organized file browsing.

---

## Automation Script Design

### Script: `gdrive_organizer.py`

**Purpose:** Automate file organization, naming, and placement in the correct Google Drive folders.

**Location:** `productivity/asset-manager/scripts/gdrive_organizer.py`

### Core Functions

```python
"""
Google Drive Folder Organizer for NotebookLM Sync

Functions:
1. create_folder_structure() - Create all folders if not exists
2. categorize_file() - Determine correct folder for a file
3. rename_file() - Rename file to convention
4. move_file() - Move file to correct location
5. log_action() - Record what was placed where
"""

# Folder structure definition
FOLDER_STRUCTURE = {
    "Treehouse-LLC": {
        "Properties": {
            "Dallas": ["Manuals", "Leases", "Warranties", "Inspections"],
            "Austin-Main-A": ["Manuals", "Leases", "Warranties", "Inspections"],
            "Austin-ADU-B": ["Manuals", "Leases", "Warranties", "Inspections"],
            "Austin-ADU-C": ["Manuals", "Leases", "Warranties", "Inspections"],
        },
        "Treehouse-General": ["Insurance", "LLC-Docs", "Tax-Records"],
        "Consulting": {
            "Methodologies": [],
            "Clients": []  # Dynamic: ClientA, ClientB, etc.
        }
    }
}

# Property code mapping
PROPERTY_CODES = {
    "DAL": "Dallas",
    "ATX-A": "Austin-Main-A",
    "ATX-B": "Austin-ADU-B",
    "ATX-C": "Austin-ADU-C"
}

# Document type to folder mapping
DOCTYPE_FOLDERS = {
    "manual": "Manuals",
    "warranty": "Warranties",
    "lease": "Leases",
    "inspection": "Inspections",
    "inspect": "Inspections",
    "receipt": "Warranties",  # Group with warranties
    "invoice": "Warranties"   # Group with warranties
}
```

### Function: Create Folder Structure

```python
def create_folder_structure(gdrive_path: str) -> dict:
    """
    Create the complete folder structure if it doesn't exist.

    Args:
        gdrive_path: Path to Google Drive root

    Returns:
        dict: Report of created folders
    """
    created = []
    existed = []

    def create_recursive(base_path, structure):
        for name, children in structure.items():
            folder_path = os.path.join(base_path, name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                created.append(folder_path)
            else:
                existed.append(folder_path)

            if isinstance(children, dict):
                create_recursive(folder_path, children)
            elif isinstance(children, list):
                for subfolder in children:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                        created.append(subfolder_path)
                    else:
                        existed.append(subfolder_path)

    create_recursive(gdrive_path, FOLDER_STRUCTURE)

    return {
        "created": created,
        "existed": existed,
        "total_created": len(created)
    }
```

### Function: Categorize File

```python
def categorize_file(filename: str) -> dict:
    """
    Determine the correct folder for a file based on its name.

    Args:
        filename: The file name (e.g., "DAL-HVAC-01_manual_2024-01-15.pdf")

    Returns:
        dict: {property, doctype, folder, asset_id}
    """
    # Parse asset-based naming: {ASSET-ID}_{DOCTYPE}_{DATE}.pdf
    asset_pattern = r'^([A-Z]{3}(?:-[A-Z])?-[A-Z]{4}-\d{2})_(\w+)_(\d{4}-\d{2}-\d{2})\.'

    # Parse lease naming: lease_{PROPERTY}_{TENANT}_{DATE}.pdf
    lease_pattern = r'^lease_([A-Z]{3}(?:-[A-Z])?)_(\w+)_(\d{4}-\d{2}-\d{2})\.'

    # Parse inspection naming: inspection_{PROPERTY}_{DATE}.pdf
    inspection_pattern = r'^inspection_([A-Z]{3}(?:-[A-Z])?)_(?:(\w+)_)?(\d{4}-\d{2}-\d{2})\.'

    # Try asset pattern
    match = re.match(asset_pattern, filename)
    if match:
        asset_id, doctype, date = match.groups()
        property_code = asset_id.split('-')[0]
        if asset_id.startswith('ATX'):
            property_code = '-'.join(asset_id.split('-')[:2])

        return {
            "property": PROPERTY_CODES.get(property_code),
            "doctype": doctype,
            "folder": DOCTYPE_FOLDERS.get(doctype, "Manuals"),
            "asset_id": asset_id,
            "date": date
        }

    # Try lease pattern
    match = re.match(lease_pattern, filename)
    if match:
        property_code, tenant, date = match.groups()
        return {
            "property": PROPERTY_CODES.get(property_code),
            "doctype": "lease",
            "folder": "Leases",
            "tenant": tenant,
            "date": date
        }

    # Try inspection pattern
    match = re.match(inspection_pattern, filename)
    if match:
        property_code, inspection_type, date = match.groups()
        return {
            "property": PROPERTY_CODES.get(property_code),
            "doctype": "inspection",
            "folder": "Inspections",
            "inspection_type": inspection_type,
            "date": date
        }

    return {"error": "Could not categorize file", "filename": filename}
```

### Function: Rename File

```python
def rename_file_to_convention(
    original_name: str,
    asset_id: str = None,
    doctype: str = None,
    property_code: str = None,
    date: str = None
) -> str:
    """
    Rename a file to match the naming convention.

    Args:
        original_name: Original filename
        asset_id: Asset ID (e.g., "DAL-HVAC-01")
        doctype: Document type (manual, warranty, etc.)
        property_code: Property code (DAL, ATX-A, etc.)
        date: Date in YYYY-MM-DD format

    Returns:
        str: New filename following convention
    """
    ext = os.path.splitext(original_name)[1].lower()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    if asset_id and doctype:
        return f"{asset_id}_{doctype}_{date}{ext}"
    elif doctype == "lease" and property_code:
        # Need tenant name - return partial
        return f"lease_{property_code}_TENANT_{date}{ext}"
    elif doctype == "inspection" and property_code:
        return f"inspection_{property_code}_{date}{ext}"

    return original_name  # Return original if can't determine format
```

### Function: Process and Move File

```python
def process_file(
    file_path: str,
    gdrive_root: str,
    dry_run: bool = True
) -> dict:
    """
    Process a single file: categorize, rename, and move to correct location.

    Args:
        file_path: Path to the file to process
        gdrive_root: Root path to Google Drive Treehouse-LLC folder
        dry_run: If True, only report what would happen

    Returns:
        dict: Action report
    """
    filename = os.path.basename(file_path)
    category = categorize_file(filename)

    if "error" in category:
        return {
            "status": "error",
            "message": category["error"],
            "file": filename
        }

    # Build destination path
    dest_folder = os.path.join(
        gdrive_root,
        "Properties",
        category["property"],
        category["folder"]
    )

    dest_path = os.path.join(dest_folder, filename)

    action = {
        "status": "success",
        "source": file_path,
        "destination": dest_path,
        "category": category,
        "dry_run": dry_run
    }

    if not dry_run:
        # Ensure destination folder exists
        os.makedirs(dest_folder, exist_ok=True)

        # Move or copy file
        shutil.copy2(file_path, dest_path)
        action["moved"] = True

    return action
```

### Function: Log Actions

```python
def log_actions(actions: list, log_file: str = None) -> str:
    """
    Log all file organization actions.

    Args:
        actions: List of action dicts from process_file()
        log_file: Path to log file (optional)

    Returns:
        str: Formatted log output
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_lines = [
        f"=== Google Drive Organization Log ===",
        f"Timestamp: {timestamp}",
        f"Total files processed: {len(actions)}",
        "",
        "--- Actions ---"
    ]

    for action in actions:
        if action["status"] == "success":
            log_lines.append(
                f"[OK] {os.path.basename(action['source'])} "
                f"-> {action['destination']}"
            )
        else:
            log_lines.append(
                f"[ERROR] {action.get('file', 'unknown')}: "
                f"{action.get('message', 'Unknown error')}"
            )

    log_output = "\n".join(log_lines)

    if log_file:
        with open(log_file, "a") as f:
            f.write(log_output + "\n\n")

    return log_output
```

### CLI Usage

```bash
# Create folder structure
python gdrive_organizer.py create-structure --path "/path/to/Google Drive"

# Categorize a single file (dry run)
python gdrive_organizer.py categorize --file "DAL-HVAC-01_manual_2024-01-15.pdf"

# Process files from inbox folder (dry run)
python gdrive_organizer.py process --inbox "/path/to/inbox" --gdrive "/path/to/Google Drive" --dry-run

# Process files for real
python gdrive_organizer.py process --inbox "/path/to/inbox" --gdrive "/path/to/Google Drive"

# Rename a file to convention
python gdrive_organizer.py rename --file "hvac manual.pdf" --asset-id "DAL-HVAC-01" --doctype "manual"
```

---

## One-Time Setup Instructions

### Step 1: Create Google Drive Folder Structure

1. Open Google Drive in browser
2. Navigate to your root folder (or create `Treehouse-LLC`)
3. Create the folder hierarchy manually, OR
4. Run: `python gdrive_organizer.py create-structure --path "/path/to/Google Drive/Treehouse-LLC"`

### Step 2: Create NotebookLM Notebooks

For each property and category, create a notebook:

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Click "New Notebook"
3. Name it following convention (e.g., "Treehouse: Dallas")
4. Repeat for all notebooks in the mapping table

**Notebooks to create:**
- [ ] `Treehouse: Dallas`
- [ ] `Treehouse: Austin Main A`
- [ ] `Treehouse: Austin ADU B`
- [ ] `Treehouse: Austin ADU C` (when ready)
- [ ] `Treehouse General`
- [ ] `Consulting: Methodologies`
- [ ] `Consulting: [ClientName]` (per client)

### Step 3: Link Google Drive Folders to NotebookLM

For each notebook:

1. Open the notebook in NotebookLM
2. Click **"Add source"** (or **"+"** button in sources panel)
3. Select **"Google Drive"**
4. Navigate to the appropriate folder(s)
5. Select the folder and click **"Add"**
6. Repeat for all folders that should link to this notebook

**Example for "Treehouse: Dallas":**
- Add source: `Properties/Dallas/Manuals/`
- Add source: `Properties/Dallas/Leases/`
- Add source: `Properties/Dallas/Warranties/`
- Add source: `Properties/Dallas/Inspections/`

### Step 4: Verify Sync

1. Add a test file to a linked Drive folder
2. Wait 1-2 minutes for sync
3. In NotebookLM, check if the file appears in sources
4. Try a query about the test file content

### Step 5: Document the Links

Create a tracking record (in Notion or a spreadsheet):

| Notebook | Drive Folder | Link Date | Verified |
|----------|--------------|-----------|----------|
| Treehouse: Dallas | Properties/Dallas/Manuals/ | 2024-01-15 | Yes |
| Treehouse: Dallas | Properties/Dallas/Leases/ | 2024-01-15 | Yes |
| ... | ... | ... | ... |

---

## Sync Behavior Reference

### How NotebookLM Sync Works

| Behavior | Details |
|----------|---------|
| **Initial sync** | Files are indexed when folder is first linked |
| **New file detection** | New files in linked folders appear within minutes |
| **Update detection** | Modified files are re-indexed automatically |
| **Deletion handling** | Deleted files are removed from sources |
| **Sync frequency** | Near real-time (typically 1-5 minutes) |

### File Size Limits

| Limit | Value | Notes |
|-------|-------|-------|
| **Max file size** | 500,000 words | Per document |
| **Max sources per notebook** | 50 sources | Includes all linked files/folders |
| **Recommended file size** | < 100 pages | For best query performance |

### Supported File Formats

| Format | Support | Notes |
|--------|---------|-------|
| **PDF** | Excellent | Primary format for manuals, leases |
| **Google Docs** | Excellent | Native integration |
| **TXT** | Good | Plain text files |
| **Markdown** | Good | `.md` files |
| **Word (.docx)** | Limited | Convert to PDF or Google Docs preferred |
| **Excel (.xlsx)** | Limited | Convert to Google Sheets or PDF |
| **Images** | No | Text extraction not supported |
| **Scanned PDFs** | Partial | OCR quality varies |

### Best Practices for Sync

1. **Use PDF format** for manuals, leases, warranties
2. **Ensure PDFs are text-based** (not scanned images)
3. **Keep file sizes reasonable** (< 100 pages per document)
4. **Use consistent naming** so documents are identifiable in sources
5. **Don't exceed 50 sources** per notebook
6. **Test queries** after adding new documents

### Troubleshooting

| Issue | Solution |
|-------|----------|
| File not appearing | Wait 5 minutes, then refresh notebook |
| "Source failed to load" | Check file format and size |
| Queries not finding content | Verify PDF is text-based, not scanned |
| Too many sources warning | Split into multiple notebooks |
| Sync stopped working | Re-link the Drive folder |

---

## Quick Reference Card

### Property Codes

| Code | Property |
|------|----------|
| `DAL` | Dallas |
| `ATX-A` | Austin Main Unit A |
| `ATX-B` | Austin ADU Unit B |
| `ATX-C` | Austin ADU Unit C |

### Document Types

| Type | Folder | Example |
|------|--------|---------|
| `manual` | Manuals/ | `DAL-HVAC-01_manual_2024-01-15.pdf` |
| `warranty` | Warranties/ | `DAL-HVAC-01_warranty_2024-01-15.pdf` |
| `receipt` | Warranties/ | `DAL-HVAC-01_receipt_2024-01-15.pdf` |
| `lease` | Leases/ | `lease_DAL_Smith_2024-06-01.pdf` |
| `inspection` | Inspections/ | `inspection_DAL_2024-01-15.pdf` |

### Notebook Names

| Notebook | Purpose |
|----------|---------|
| `Treehouse: Dallas` | Dallas property documents |
| `Treehouse: Austin Main A` | Austin main house documents |
| `Treehouse: Austin ADU B` | Austin ADU B documents |
| `Treehouse: Austin ADU C` | Austin ADU C documents |
| `Treehouse General` | LLC-wide documents |
| `Consulting: Methodologies` | Consulting frameworks |
| `Consulting: [Client]` | Per-client documents |

---

*Last Updated: 2024*
*Related: notebooklm-guide.md, naming-conventions.md, UNIFIED-SYSTEM-PLAN.md*
