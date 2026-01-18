# Treehouse Systems

Welcome to the central documentation for all Treehouse automation systems.

## What Is This?

This is your **intranet** - a single place to understand what your Claude assistant can do, how your automation pipelines work, and how to use them.

## Quick Links

| System | Purpose | Status |
|--------|---------|--------|
| [Asset Manager](skills/asset-manager.md) | Track home purchases, manuals, warranties | ✅ Active |
| [Notifications](skills/notifications.md) | Unified alerts via Pushover | ✅ Active |
| [Ecosystem Status](skills/ecosystem-status.md) | Monitor all system health | ✅ Active |

## Your Claude Assistant Can...

### Automation
- Scan Gmail for purchase receipts
- Find product manuals online
- Organize files in Google Drive
- Send notifications to your phone

### Development
- Build MCP servers
- Create Python automation scripts
- Manage Git repositories
- Run tests and deployments

### Data
- Process PDFs and documents
- Analyze CSV data
- Generate QR codes
- Sync with Notion

## Getting Started

```bash
# Clone the repo
git clone https://github.com/pqsoccerboy17/claude-skills.git
cd claude-skills

# View these docs locally
pip3 install mkdocs-material
mkdocs serve
# Open http://localhost:8000
```

## Repository Structure

```
claude-skills/
├── docs/                    # This documentation
├── productivity/
│   ├── asset-manager/       # Gmail scanning, manual finding
│   ├── notifications/       # Pushover alerts
│   └── ecosystem-status/    # System health checks
├── document-processing/
│   ├── pdf/                 # PDF tools
│   └── xlsx/                # Excel tools
├── data-analysis/
│   └── csv-data-summarizer/ # CSV analysis
└── dev-tools/
    └── mcp-builder/         # MCP server scaffolding
```
