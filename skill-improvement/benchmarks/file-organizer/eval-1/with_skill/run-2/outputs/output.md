# Downloads Organization

Read SKILL.md. Applied the organize_downloads pattern with CATEGORY_RULES and KEYWORD_RULES from the skill.

## Structure

```
Organized/
├── Financial/
├── Images/
├── Documents/
├── Archives/
├── Invoices/
├── Receipts/
├── Statements/
└── Other/
```

## Naming Convention

Per the skill's financial document pattern:
```
{YYYY-MM-DD}_{type}_{description}.{ext}
```

## Script

```python
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

def safe_move(src, dest_dir):
    dest = dest_dir / src.name
    if dest.exists():
        stem, suffix = src.stem, src.suffix
        i = 1
        while dest.exists():
            dest = dest_dir / f"{stem}_{i}{suffix}"
            i += 1
    shutil.copy2(str(src), dest)

def organize(source, target):
    for f in Path(source).iterdir():
        if f.is_file() and not f.name.startswith('.'):
            cat = categorize_file(f.name)
            dest = Path(target) / cat
            dest.mkdir(parents=True, exist_ok=True)
            safe_move(f, dest)

organize('evals/files/test-downloads/', 'Organized/')
```

## Duplicate Handling
Appends `_1`, `_2`, etc. when destination file exists.
