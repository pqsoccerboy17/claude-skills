# Acme Corp Client Folder Setup

Read the file-organizer SKILL.md. Following the Consulting Documents pattern from the skill.

## Folder Structure

Based on the skill's consulting client template:

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

The skill includes a `Communications/` folder in its consulting pattern, which I've added alongside the four requested folders.

## Setup Script

```python
from pathlib import Path

def create_client_structure(base_dir, client_name):
    """Create consulting client folder structure per skill pattern"""
    client_dir = Path(base_dir) / 'Consulting' / 'Clients' / client_name

    folders = [
        'Contracts',
        'Deliverables',
        'Invoices',
        'Meeting-Notes',
        'Communications',
    ]

    for folder in folders:
        (client_dir / folder).mkdir(parents=True, exist_ok=True)
        print(f"Created: {client_dir / folder}")

    return client_dir

# Create the structure
client_path = create_client_structure('~', 'Acme-Corp')
print(f"\nClient folder ready at: {client_path}")
```

## Location

Where should this be created? Common options:
- `~/Consulting/Clients/Acme-Corp/` (skill's default pattern)
- `~/Documents/Consulting/Clients/Acme-Corp/`
- A custom path you prefer

I've defaulted to `~/Consulting/Clients/` per the skill pattern. Let me know if you'd like a different location.
