---
name: notion-api
description: Direct Notion API access for Code mode sessions
---

# Notion API Skill

Direct Notion API access for Claude Code mode sessions, providing the same capabilities as the ecosystem-mcp-server but without requiring MCP.

## Why This Exists

MCP servers run locally on your Mac and connect to Claude Desktop's Chat mode. However, Code mode sessions run in isolated cloud containers that can't access local MCP servers. This skill provides direct API access that works in Code mode.

## Capabilities

### Database Operations
- **Query databases** - Filter, sort, and paginate database entries
- **Create pages** - Add new entries to databases
- **Update pages** - Modify existing page properties

### Page Operations
- **Get page** - Retrieve page content and properties
- **Search** - Find pages and databases by title

### Automation Requests (mirrors ecosystem-mcp-server)
- **Get pending requests** - List queued automation requests
- **Process request** - Execute and update request status
- **Create requests database** - Set up automation control plane

## Setup

### Option 1: Environment Variable (Recommended)

Set `NOTION_TOKEN` in your environment:

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
```

For Code mode, you can set this in the session or include it in a `.env` file.

### Option 2: Config File

Create `~/.config/notion/config.json`:

```json
{
  "token": "secret_xxxxxxxxxxxxx",
  "automation_db_id": "your-database-id"
}
```

### Getting Your Token

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Share your databases/pages with the integration

## Usage

### From Python

```python
from notion_api import NotionClient

# Initialize client
notion = NotionClient()

# Query a database
results = notion.query_database(
    database_id="your-db-id",
    filter={"property": "Status", "select": {"equals": "Active"}}
)

# Search for pages
pages = notion.search("Meeting Notes")

# Get a specific page
page = notion.get_page("page-id")

# Create a new page
new_page = notion.create_page(
    database_id="your-db-id",
    properties={
        "Name": {"title": [{"text": {"content": "New Entry"}}]},
        "Status": {"select": {"name": "Draft"}}
    }
)

# Update a page
notion.update_page(
    page_id="page-id",
    properties={"Status": {"select": {"name": "Complete"}}}
)
```

### Automation Requests

```python
from notion_api import NotionClient

notion = NotionClient()

# Get pending requests
pending = notion.get_pending_requests()

# Process a request
result = notion.process_request(request_id="page-id")
```

### From Command Line

```bash
# Query a database
python3 notion_api.py query <database-id>

# Search for pages
python3 notion_api.py search "query text"

# Get pending automation requests
python3 notion_api.py pending

# Check connection status
python3 notion_api.py status
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_TOKEN` | Yes | Notion integration token |
| `NOTION_AUTOMATION_DB_ID` | No | Default automation requests database |

## Database Schema for Automation Requests

If using the automation control plane feature, your database should have:

| Property | Type | Values |
|----------|------|--------|
| Name | Title | Request name |
| Command | Select | organize, extract, sync, reconcile, custom |
| Arguments | Rich Text | Command arguments (JSON) |
| Status | Select | queued, running, done, failed |
| Created | Created Time | Auto-populated |
| Processed | Date | When completed |
| Result | Rich Text | Execution result |

## Integration with Ecosystem

This skill is designed to work alongside:
- **ecosystem-mcp-server** (for Chat mode)
- **treehouse-context-sync** (for context management)
- **notion-rules** (for tax document OCR)

## Troubleshooting

### "Unauthorized" errors
- Verify your token is correct
- Ensure the integration has been shared with the target database/page

### "Object not found" errors
- The page/database ID might be incorrect
- The integration might not have access to that resource

### Rate limiting
- Notion API has rate limits (3 requests/second)
- The client includes automatic retry with backoff
