# Acme Corp - Consulting Client Setup

Read the file-organizer SKILL.md. Applied the consulting client folder pattern.

## Structure (per skill template)

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

def setup_client(base, name):
    root = Path(base) / 'Consulting' / 'Clients' / name
    for d in ['Contracts', 'Deliverables', 'Invoices', 'Meeting-Notes', 'Communications']:
        (root / d).mkdir(parents=True, exist_ok=True)
    return root

path = setup_client(Path.home(), 'Acme-Corp')
print(f"Created at: {path}")
```

## Location Note

Default location: `~/Consulting/Clients/Acme-Corp/` per the skill's consulting pattern. Happy to adjust if you prefer a different path.
