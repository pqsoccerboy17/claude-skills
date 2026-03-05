# Acme Corp Folders

```
acme-corp/
├── contracts/
├── deliverables/
├── invoices/
└── meeting-notes/
```

```python
import os

base = 'acme-corp'
for d in ['contracts', 'deliverables', 'invoices', 'meeting-notes']:
    os.makedirs(os.path.join(base, d), exist_ok=True)
```

Created the four requested subdirectories under acme-corp.
