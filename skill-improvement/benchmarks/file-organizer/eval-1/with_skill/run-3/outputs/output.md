# File Organization Plan

Read the file-organizer SKILL.md. Using the organize_downloads function pattern with pathlib and shutil.

## Target Structure

```
Organized/
├── Financial/      (.pdf, .csv, .xlsx)
├── Images/         (.jpg, .jpeg, .png, .heic)
├── Documents/      (.doc, .docx, .txt)
├── Archives/       (.zip, .tar, .gz)
├── Invoices/       (keyword: invoice, bill)
├── Statements/     (keyword: statement)
├── Receipts/       (keyword: receipt)
└── Other/
```

## Naming Convention

```
{YYYY-MM-DD}_{type}_{description}.{ext}
```

Date-prefixed for chronological sorting. Type tag for quick identification.

## Script

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
    for cat, kws in KEYWORD_RULES.items():
        if any(kw in name_lower for kw in kws):
            return cat
    for cat, exts in CATEGORY_RULES.items():
        if ext in exts:
            return cat
    return 'Other'

def organize_downloads(source, dest):
    src = Path(source)
    dst = Path(dest)

    for f in src.iterdir():
        if f.is_file() and not f.name.startswith('.'):
            cat = categorize_file(f.name)
            target_dir = dst / cat
            target_dir.mkdir(parents=True, exist_ok=True)

            # Handle duplicates
            target = target_dir / f.name
            if target.exists():
                stem = f.stem
                i = 1
                while target.exists():
                    target = target_dir / f"{stem}_{i}{f.suffix}"
                    i += 1

            shutil.copy2(str(f), target)
            print(f"  {f.name} -> {cat}/")

organize_downloads('evals/files/test-downloads/', 'Organized/')
```

## Edge Cases
- Hidden files skipped
- Duplicates get numbered suffix
- copy2 preserves timestamps
- Keywords checked before extensions
