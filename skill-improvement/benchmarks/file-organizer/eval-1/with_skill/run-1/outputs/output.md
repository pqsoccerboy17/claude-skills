# Downloads Folder Organization

Read the file-organizer SKILL.md first. Following the skill's `organize_downloads` pattern with `CATEGORY_RULES` and `KEYWORD_RULES`.

## Proposed Structure

```
Organized/
├── Financial/      (PDFs, CSVs, spreadsheets)
├── Images/         (JPGs, PNGs, HEICs)
├── Documents/      (DOC, DOCX, TXT)
├── Archives/       (ZIP, TAR, GZ)
├── Invoices/       (keyword match: invoice, inv-, bill)
├── Statements/     (keyword match: statement, stmt)
├── Receipts/       (keyword match: receipt, rcpt)
└── Other/          (anything uncategorized)
```

## Naming Convention

Following the skill's financial document pattern:
```
{YYYY-MM-DD}_{type}_{description}.{ext}
```

Examples:
- `2026-03-05_receipt_home-depot.pdf`
- `2026-03-05_invoice_client-project.pdf`
- `2026-03-05_document_meeting-notes.docx`

## Organization Script

```python
from pathlib import Path
import shutil
from datetime import datetime

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
    name_lower = filename.lower()
    ext = Path(filename).suffix.lower()
    for category, keywords in KEYWORD_RULES.items():
        if any(kw in name_lower for kw in keywords):
            return category
    for category, extensions in CATEGORY_RULES.items():
        if ext in extensions:
            return category
    return 'Other'

def handle_duplicate(dest_path):
    """Handle duplicate filenames by appending a counter"""
    if not dest_path.exists():
        return dest_path
    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    while dest_path.exists():
        dest_path = dest_path.parent / f"{stem}_{counter}{suffix}"
        counter += 1
    return dest_path

def organize_downloads(downloads_path, organized_path):
    downloads = Path(downloads_path)
    organized = Path(organized_path)

    for file in downloads.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            category = categorize_file(file.name)
            dest_dir = organized / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = handle_duplicate(dest_dir / file.name)
            shutil.copy2(str(file), dest)
            print(f"Moved {file.name} -> {category}/")

organize_downloads('evals/files/test-downloads/', 'Organized/')
```

## Edge Cases Handled
- Hidden files (starting with `.`) are skipped
- Duplicate filenames get a `_1`, `_2` suffix
- `shutil.copy2` preserves file metadata (timestamps)
- Keywords take priority over extension-based categorization
