# Python MCP Server: Invoice Management

Read the mcp-builder SKILL.md. Following the Python MCP server pattern from the skill.

## Server Implementation

```python
import json
from pathlib import Path
from datetime import datetime
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

INVOICES_FILE = Path("invoices.json")
server = Server("invoice-manager")

def load_invoices():
    if INVOICES_FILE.exists():
        return json.loads(INVOICES_FILE.read_text())
    return []

def save_invoices(invoices):
    INVOICES_FILE.write_text(json.dumps(invoices, indent=2))

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_invoices",
            description="List recent invoices",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        types.Tool(
            name="create_invoice",
            description="Create a new invoice",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_name": {"type": "string", "description": "Client name"},
                    "amount": {"type": "number", "description": "Invoice amount"},
                    "description": {"type": "string", "description": "Invoice description"}
                },
                "required": ["client_name", "amount", "description"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "list_invoices":
        invoices = load_invoices()
        return [types.TextContent(type="text", text=json.dumps(invoices, indent=2))]
    
    elif name == "create_invoice":
        invoices = load_invoices()
        new_invoice = {
            "id": len(invoices) + 1,
            "client_name": arguments["client_name"],
            "amount": arguments["amount"],
            "description": arguments["description"],
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        invoices.append(new_invoice)
        save_invoices(invoices)
        return [types.TextContent(type="text", text=f"Invoice #{new_invoice['id']} created for {arguments['client_name']}")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            InitializationOptions(
                server_name="invoice-manager",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Setup

```bash
pip install mcp
python server.py
```

## Configuration

Add to Claude Code settings:
```json
{
  "mcpServers": {
    "invoice-manager": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```
