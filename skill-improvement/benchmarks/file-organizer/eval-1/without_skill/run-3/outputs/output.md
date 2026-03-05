# Downloads Cleanup

## Structure

```
sorted/
├── docs/
├── images/
├── spreadsheets/
├── archives/
└── other/
```

## Code

```python
import os
import shutil

type_map = {
    '.pdf': 'docs', '.doc': 'docs', '.docx': 'docs', '.txt': 'docs',
    '.jpg': 'images', '.jpeg': 'images', '.png': 'images',
    '.csv': 'spreadsheets', '.xlsx': 'spreadsheets',
    '.zip': 'archives', '.tar': 'archives',
}

for f in os.listdir('evals/files/test-downloads/'):
    src = os.path.join('evals/files/test-downloads/', f)
    if os.path.isfile(src):
        ext = os.path.splitext(f)[1].lower()
        folder = type_map.get(ext, 'other')
        dest = os.path.join('sorted', folder)
        os.makedirs(dest, exist_ok=True)
        shutil.copy(src, os.path.join(dest, f))

print("Done organizing.")
```

## Naming Suggestion

Rename files to include a date prefix: `2026-03-05-filename.ext`
