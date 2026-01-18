# System Overview

## Design Principles

### 1. AI-Agnostic
- All tools work via CLI without AI
- Claude orchestrates but isn't required
- No vendor lock-in

### 2. Modular
- Each skill is standalone
- Skills can be composed into pipelines
- Clear interfaces between components

### 3. Fail-Safe
- Uncertain items go to review queue
- Never auto-commits questionable data
- Comprehensive logging

### 4. Portable
- JSON for data interchange
- Standard file formats
- Easy export/import

## Repository Structure

```
claude-skills/
├── docs/                    # This documentation
├── productivity/
│   ├── asset-manager/       # Gmail → Manuals → Drive
│   ├── notifications/       # Pushover alerts
│   ├── ecosystem-status/    # Health monitoring
│   └── file-organizer/      # File management
├── document-processing/
│   ├── pdf/                 # PDF manipulation
│   └── xlsx/                # Excel tools
├── data-analysis/
│   └── csv-data-summarizer/ # Data analysis
└── dev-tools/
    └── mcp-builder/         # MCP scaffolding
```

## Key Technologies

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| APIs | Google (Gmail, Drive), Notion |
| Notifications | Pushover |
| Docs | MkDocs Material |
| Version Control | Git/GitHub |

## Configuration

All configuration stored in `~/.config/treehouse/`:

```
~/.config/treehouse/
├── credentials.json      # Google OAuth credentials
├── token.json           # Google OAuth token
├── config.json          # App settings
├── review_queue.json    # Pending reviews
└── logs/                # Operation logs
```
