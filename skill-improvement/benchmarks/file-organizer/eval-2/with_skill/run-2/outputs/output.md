# Client Folder: Acme Corp

Read SKILL.md. Using the Consulting Documents pattern.

## Structure

```
Consulting/
└── Clients/
    └── Acme-Corp/
        ├── Contracts/
        ├── Deliverables/
        ├── Invoices/
        ├── Meeting-Notes/
        └── Communications/
```

## Script

```python
from pathlib import Path

client = Path.home() / 'Consulting' / 'Clients' / 'Acme-Corp'
for folder in ['Contracts', 'Deliverables', 'Invoices', 'Meeting-Notes', 'Communications']:
    (client / folder).mkdir(parents=True, exist_ok=True)

print(f"Acme Corp client structure created at {client}")
```

Following the skill's consulting template. The structure nests under `Consulting/Clients/` for consistency with other clients.

Where would you like this created? Default is `~/Consulting/Clients/Acme-Corp/`.
