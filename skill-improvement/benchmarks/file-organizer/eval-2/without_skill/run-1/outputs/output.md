# Acme Corp Folder Structure

Here's a folder structure for the new client:

```
Acme-Corp/
├── contracts/
├── deliverables/
├── invoices/
└── meeting-notes/
```

## Script

```python
import os

folders = [
    'Acme-Corp/contracts',
    'Acme-Corp/deliverables',
    'Acme-Corp/invoices',
    'Acme-Corp/meeting-notes',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")
```

This creates the four folders you requested. You can run this from wherever you want the client folder to live.
