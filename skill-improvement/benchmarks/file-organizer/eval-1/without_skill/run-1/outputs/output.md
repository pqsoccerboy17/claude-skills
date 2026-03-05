# Organizing Downloads Folder

## Proposed Folder Structure

I'd organize the files by type:

```
Organized/
├── documents/
├── images/
├── spreadsheets/
├── pdfs/
├── archives/
└── misc/
```

## Script

```python
import os
import shutil

extensions = {
    'documents': ['.doc', '.docx', '.txt', '.rtf'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.heic'],
    'spreadsheets': ['.xlsx', '.xls', '.csv'],
    'pdfs': ['.pdf'],
    'archives': ['.zip', '.tar', '.gz', '.rar'],
}

source = 'evals/files/test-downloads/'
dest = 'Organized/'

for filename in os.listdir(source):
    filepath = os.path.join(source, filename)
    if os.path.isfile(filepath):
        ext = os.path.splitext(filename)[1].lower()
        folder = 'misc'
        for cat, exts in extensions.items():
            if ext in exts:
                folder = cat
                break
        target = os.path.join(dest, folder)
        os.makedirs(target, exist_ok=True)
        shutil.copy2(filepath, os.path.join(target, filename))
```

## Naming Convention

I'd suggest renaming files to be more descriptive:
- `document_2026-03-05_original-name.pdf`
- `image_2026-03-05_photo.jpg`
