---
name: docs-to-notion
description: Sync MkDocs documentation to Notion for mobile access
---

# Docs to Notion Sync

Mirrors the MkDocs documentation site to Notion pages, enabling mobile access through the Notion app.

## Purpose

The MkDocs site provides rich documentation but isn't easily accessible on mobile. This tool creates a Notion mirror that:

- Syncs automatically from the docs/ directory
- Preserves document hierarchy and structure
- Converts markdown formatting to Notion blocks
- Provides mobile-friendly access via Notion app

## Prerequisites

1. **Notion Integration**
   - Create an integration at https://www.notion.so/my-integrations
   - Get your integration token
   - Share a parent page with the integration

2. **Python Dependencies**
   ```bash
   pip install notion-client
   ```

3. **Environment Variables**
   Add to your `~/scripts/ecosystem.env`:
   ```bash
   NOTION_DOCS_PARENT_PAGE_ID=<your-parent-page-id>
   ```
   (NOTION_TOKEN should already be set from ecosystem config)

## Setup

1. Find the parent page ID in Notion:
   - Open the page where docs should be created
   - Copy the ID from the URL: `notion.so/Page-Name-<PAGE_ID>`

2. Set the environment variable:
   ```bash
   export NOTION_DOCS_PARENT_PAGE_ID="your-page-id-here"
   ```

3. Run a dry-run first:
   ```bash
   cd ~/claude-skills
   python productivity/docs-to-notion/scripts/sync_docs.py --dry-run
   ```

4. Run the actual sync:
   ```bash
   python productivity/docs-to-notion/scripts/sync_docs.py
   ```

## Usage

### First-time Sync

```bash
# From claude-skills directory
python productivity/docs-to-notion/scripts/sync_docs.py
```

### Preview Changes (Dry Run)

```bash
python productivity/docs-to-notion/scripts/sync_docs.py --dry-run
```

### Custom Docs Path

```bash
python productivity/docs-to-notion/scripts/sync_docs.py --docs-path /path/to/docs
```

## What Gets Synced

The script creates this structure in Notion:

```
📚 Documentation
├── 🏠 Home (from index.md)
├── ⚡ Skills
│   ├── Skills Overview
│   ├── Asset Manager
│   ├── Notifications
│   └── Ecosystem Status
├── 📖 Guides
│   ├── Getting Started
│   └── Daily Workflows
└── 🏗️ Architecture
    ├── System Overview
    └── Data Flow
```

## Markdown Conversion

The script converts:

| Markdown | Notion Block |
|----------|--------------|
| `# Header` | Heading 1/2/3 |
| `- item` | Bulleted list |
| `1. item` | Numbered list |
| ` ```code``` ` | Code block |
| `> quote` | Callout |
| `**bold**` | Bold text |
| `` `code` `` | Inline code |

## Limitations

- Notion API limits: 100 blocks per request
- Code blocks: 2000 character limit
- Tables: Not yet supported (appear as text)
- Images: Not synced (use external URLs)

## Re-syncing

Currently, the script creates new pages each time. To update:

1. Delete the old "📚 Documentation" page in Notion
2. Run the sync again

Future versions may support incremental updates.

## Troubleshooting

### "NOTION_TOKEN not set"

Make sure you've sourced the ecosystem config:
```bash
source ~/scripts/ecosystem.env
```

### "NOTION_DOCS_PARENT_PAGE_ID not set"

Set the parent page where docs should be created:
```bash
export NOTION_DOCS_PARENT_PAGE_ID="your-page-id"
```

### "Could not find page"

Make sure:
1. The integration has access to the parent page
2. In Notion, click "Share" on the parent page
3. Add your integration to the page

## Files

- `scripts/sync_docs.py` - Main sync script
- `SKILL.md` - This documentation
