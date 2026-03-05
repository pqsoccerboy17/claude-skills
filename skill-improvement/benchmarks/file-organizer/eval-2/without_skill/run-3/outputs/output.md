# Client Folder Structure

```
Acme-Corp/
├── contracts/
├── deliverables/
├── invoices/
└── meeting-notes/
```

```python
import os

dirs = ['contracts', 'deliverables', 'invoices', 'meeting-notes']
for d in dirs:
    os.makedirs(f'Acme-Corp/{d}', exist_ok=True)
    print(f'Created Acme-Corp/{d}')
```

Where would you like me to create this? I can put it in your Documents folder or wherever your client files live.
