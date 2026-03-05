# Organizing Your Downloads

## Folder Structure

```
organized/
├── documents/    (.pdf, .doc, .docx, .txt)
├── images/       (.jpg, .png, .gif)
├── spreadsheets/ (.csv, .xlsx)
├── archives/     (.zip, .tar)
└── other/
```

## Script

```python
import os
import shutil

file_types = {
    'documents': ['.pdf', '.doc', '.docx', '.txt'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.heic'],
    'spreadsheets': ['.csv', '.xlsx', '.xls'],
    'archives': ['.zip', '.tar', '.gz'],
}

src = 'evals/files/test-downloads/'
dst = 'organized/'

for f in os.listdir(src):
    full = os.path.join(src, f)
    if not os.path.isfile(full):
        continue
    ext = os.path.splitext(f)[1].lower()
    category = 'other'
    for cat, exts in file_types.items():
        if ext in exts:
            category = cat
            break
    os.makedirs(os.path.join(dst, category), exist_ok=True)
    shutil.move(full, os.path.join(dst, category, f))
```

## Naming

Use descriptive names like `report-q1-2026.pdf` instead of `download(3).pdf`.
