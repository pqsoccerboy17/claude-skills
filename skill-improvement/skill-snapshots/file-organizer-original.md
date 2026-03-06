---
name: file-organizer
description: "Intelligent file organization for business documents. Use when: (1) organizing financial documents (receipts, statements, invoices), (2) setting up photo capture pipelines for property documentation, (3) batch renaming files by date/type/category, (4) creating folder structures for real estate, consulting, or SaaS operations. Triggers: organize files, sort documents, rename files, photo pipeline, document management."
license: MIT
---

# File Organizer Skill

Automates file organization for business operations across Treehouse LLC (real estate), consulting, and Tap (SaaS).

## Quick Start

```python
from pathlib import Path
import shutil
from datetime import datetime

def organize_by_date(source_dir, dest_dir):
    """Organize files into YYYY/MM folders by modification date"""
    for file in Path(source_dir).rglob('*'):
        if file.is_file():
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            target = Path(dest_dir) / str(mtime.year) / f"{mtime.month:02d}"
            target.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), target / file.name)
```

## Business-Specific Organization Patterns

### Real Estate Documents (Treehouse LLC)

```
Treehouse-LLC/
├── Properties/
│   └── {address}/
│       ├── Acquisition/
│       │   ├── purchase-agreement.pdf
│       │   ├── title-report.pdf
│       │   └── inspection-report.pdf
│       ├── Financial/
│       │   ├── {year}/
│       │   │   ├── rent-rolls/
│       │   │   ├── expenses/
│       │   │   └── statements/
│       ├── Tenants/
│       │   └── {unit}/
│       │       ├── lease.pdf
│       │       └── application.pdf
│       └── Photos/
│           ├── exterior/
│           ├── interior/
│           └── maintenance/
├── Banking/
│   └── {year}/
│       └── {month}/
│           └── statement-{date}.pdf
└── Tax/
    └── {year}/
```

### Consulting Documents

```
Consulting/
├── Clients/
│   └── {client-name}/
│       ├── Contracts/
│       ├── Deliverables/
│       ├── Invoices/
│       └── Communications/
├── Templates/
└── Reference/
```

### SaaS Operations (Tap)

```
Tap/
├── Product/
│   ├── specs/
│   ├── roadmap/
│   └── releases/
├── Engineering/
│   ├── docs/
│   └── architecture/
├── Business/
│   ├── investors/
│   ├── metrics/
│   └── legal/
└── Marketing/
```

## File Naming Conventions

### Financial Documents
```
{YYYY-MM-DD}_{type}_{description}.{ext}
Examples:
- 2024-01-15_invoice_contractor-repairs.pdf
- 2024-01-31_statement_chase-checking.pdf
- 2024-02-01_receipt_home-depot.pdf
```

### Property Photos
```
{address}_{area}_{sequence}_{date}.{ext}
Examples:
- 123-main-st_kitchen_001_2024-01-15.jpg
- 123-main-st_exterior-front_001_2024-01-15.jpg
```

## Automation Scripts

### Organize Downloads Folder

```python
import os
from pathlib import Path
import shutil

CATEGORY_RULES = {
    'Financial': ['.pdf', '.csv', '.xlsx'],
    'Images': ['.jpg', '.jpeg', '.png', '.heic'],
    'Documents': ['.doc', '.docx', '.txt'],
    'Archives': ['.zip', '.tar', '.gz'],
}

KEYWORD_RULES = {
    'Invoices': ['invoice', 'inv-', 'bill'],
    'Statements': ['statement', 'stmt'],
    'Receipts': ['receipt', 'rcpt'],
    'Contracts': ['contract', 'agreement', 'lease'],
}

def categorize_file(filename):
    """Determine category based on extension and keywords"""
    name_lower = filename.lower()
    ext = Path(filename).suffix.lower()

    # Check keywords first
    for category, keywords in KEYWORD_RULES.items():
        if any(kw in name_lower for kw in keywords):
            return category

    # Fall back to extension
    for category, extensions in CATEGORY_RULES.items():
        if ext in extensions:
            return category

    return 'Other'

def organize_downloads(downloads_path, organized_path):
    """Move files from Downloads to organized structure"""
    downloads = Path(downloads_path)
    organized = Path(organized_path)

    for file in downloads.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            category = categorize_file(file.name)
            dest_dir = organized / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), dest_dir / file.name)
            print(f"Moved {file.name} -> {category}/")
```

### Photo Pipeline for Property Documentation

```python
from pathlib import Path
from datetime import datetime
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

def get_photo_date(image_path):
    """Extract date from EXIF data or file modification time"""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                if TAGS.get(tag_id) == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except:
        pass
    return datetime.fromtimestamp(Path(image_path).stat().st_mtime)

def organize_property_photos(source_dir, dest_dir, property_address):
    """Organize property photos by area and date"""
    source = Path(source_dir)
    dest = Path(dest_dir) / property_address.replace(' ', '-').lower()

    # Area detection keywords
    areas = {
        'exterior': ['exterior', 'outside', 'front', 'back', 'yard'],
        'kitchen': ['kitchen', 'cook'],
        'bathroom': ['bath', 'toilet', 'shower'],
        'bedroom': ['bedroom', 'bed', 'master'],
        'living': ['living', 'lounge', 'family'],
        'maintenance': ['repair', 'damage', 'issue', 'fix'],
    }

    for photo in source.glob('*.{jpg,jpeg,png,heic}'):
        # Detect area from filename
        name_lower = photo.stem.lower()
        detected_area = 'uncategorized'
        for area, keywords in areas.items():
            if any(kw in name_lower for kw in keywords):
                detected_area = area
                break

        # Get date and create destination
        photo_date = get_photo_date(photo)
        target_dir = dest / detected_area
        target_dir.mkdir(parents=True, exist_ok=True)

        # Rename with date prefix
        new_name = f"{photo_date.strftime('%Y%m%d')}_{photo.name}"
        shutil.copy2(photo, target_dir / new_name)
```

### Bank Statement Organizer

```python
import re
from pathlib import Path
import shutil

def organize_bank_statements(source_dir, dest_dir):
    """Organize bank statements by year/month"""
    # Common bank statement filename patterns
    patterns = [
        r'(\d{4})-(\d{2})',  # 2024-01
        r'(\d{2})(\d{2})(\d{4})',  # 01152024
        r'statement.*?(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
    ]

    source = Path(source_dir)
    dest = Path(dest_dir)

    for file in source.glob('*.pdf'):
        filename = file.name.lower()
        year, month = None, None

        # Try to extract date from filename
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    year, month = groups
                elif len(groups) == 3:
                    month, _, year = groups
                break

        if year and month:
            year = year if len(year) == 4 else f"20{year}"
            target = dest / year / f"{int(month):02d}"
            target.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), target / file.name)
```

## Command Line Usage

```bash
# Quick organize by file type
python scripts/organize.py ~/Downloads ~/Organized --by-type

# Organize with date-based folders
python scripts/organize.py ~/Downloads ~/Organized --by-date

# Property photo pipeline
python scripts/photo_pipeline.py ~/Photos/property --address "123 Main St"

# Bank statement organization
python scripts/bank_statements.py ~/Downloads/statements ~/Finance/Banking
```

## Integration with macOS

### Folder Actions (Automator)
Create a Folder Action that runs the organize script when files are added:

```bash
#!/bin/bash
# Save as ~/Library/Scripts/Folder Action Scripts/organize.sh
python3 ~/claude-skills/productivity/file-organizer/scripts/organize.py "$1" ~/Organized
```

### Hazel Rules (if using Hazel)
- Match: Kind is PDF AND Name contains "statement"
- Action: Move to ~/Finance/Banking/{year}/{month}

## Best Practices

1. **Don't delete originals** - Copy first, verify, then delete
2. **Preserve metadata** - Use `shutil.copy2()` to maintain timestamps
3. **Log everything** - Keep a log of file moves for auditing
4. **Test with samples** - Run on test folder before production
5. **Regular backups** - Before major reorganization, backup first
