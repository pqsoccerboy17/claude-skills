---
name: mcp-builder
description: "Build custom MCP (Model Context Protocol) servers for Claude integrations. Use when: (1) creating new MCP servers, (2) extending Claude's capabilities with external APIs, (3) building tool integrations, (4) debugging MCP server issues, (5) connecting Claude to business systems. Triggers: build MCP, create MCP server, MCP integration, Claude tools, API integration."
license: MIT
---

# MCP Builder Skill

Create custom Model Context Protocol (MCP) servers to extend Claude's capabilities with external APIs and tools.

## What is MCP?

MCP (Model Context Protocol) is Anthropic's open standard for connecting AI assistants to external data sources and tools. MCP servers expose:
- **Tools** - Functions Claude can call
- **Resources** - Data Claude can access
- **Prompts** - Pre-defined prompt templates

## Quick Start

### TypeScript MCP Server (Recommended)

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "hello_world",
      description: "Returns a greeting",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Name to greet" }
        },
        required: ["name"]
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "hello_world") {
    const name = request.params.arguments?.name;
    return { content: [{ type: "text", text: `Hello, ${name}!` }] };
  }
  throw new Error("Unknown tool");
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python MCP Server

```python
# server.py
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("my-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="hello_world",
            description="Returns a greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "hello_world":
        return [types.TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="my-mcp-server",
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

## Project Structure

```
my-mcp-server/
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── src/
│   ├── index.ts         # Entry point
│   ├── tools/           # Tool implementations
│   │   ├── api.ts
│   │   └── database.ts
│   └── utils/           # Helpers
│       └── auth.ts
└── README.md
```

## Configuration

### Claude Desktop Configuration

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/my-mcp-server/dist/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Code Configuration

```json
// ~/.claude/settings.json or project .claude/settings.json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/dist/index.js"]
    }
  }
}
```

## Common MCP Patterns

### API Integration

```typescript
// tools/api.ts
import axios from "axios";

export async function fetchData(endpoint: string, apiKey: string) {
  const response = await axios.get(endpoint, {
    headers: { "Authorization": `Bearer ${apiKey}` }
  });
  return response.data;
}

// In server
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "fetch_data") {
    const { endpoint } = request.params.arguments;
    const data = await fetchData(endpoint, process.env.API_KEY!);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
});
```

### Database Integration

```typescript
// tools/database.ts
import sqlite3 from "sqlite3";
import { promisify } from "util";

export async function queryDatabase(db: sqlite3.Database, sql: string) {
  const all = promisify(db.all.bind(db));
  return await all(sql);
}
```

### File Operations

```typescript
// tools/files.ts
import fs from "fs/promises";
import path from "path";

export async function listFiles(directory: string) {
  const files = await fs.readdir(directory);
  return files.map(f => path.join(directory, f));
}

export async function readFile(filePath: string) {
  return await fs.readFile(filePath, "utf-8");
}
```

## Business-Specific MCP Ideas

### Treehouse LLC

**Property Management MCP:**
- Tool: `get_property_info(address)` - Fetch property details
- Tool: `list_tenants(property_id)` - List current tenants
- Tool: `get_rent_roll(property_id)` - Generate rent roll
- Tool: `log_maintenance(property_id, issue)` - Log maintenance request
- Resource: Property documents, lease templates

### Consulting

**Client Management MCP:**
- Tool: `get_client_info(client_id)` - Fetch client details
- Tool: `log_time(client_id, hours, description)` - Time tracking
- Tool: `get_project_status(project_id)` - Project overview
- Tool: `generate_invoice(client_id, period)` - Create invoice draft

### Tap (SaaS)

**Product Metrics MCP:**
- Tool: `get_metrics(metric_name, date_range)` - Fetch business metrics
- Tool: `query_analytics(query)` - Query analytics database
- Tool: `get_user_info(user_id)` - Customer lookup
- Resource: Dashboards, reports

## Development Workflow

### 1. Initialize Project

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk typescript
npx tsc --init
```

### 2. Build

```bash
npx tsc
```

### 3. Test Locally

```bash
# Run server directly (for debugging)
node dist/index.js

# Or use the MCP inspector
npx @modelcontextprotocol/inspector node dist/index.js
```

### 4. Install in Claude

1. Add to configuration (see above)
2. Restart Claude Desktop / Claude Code
3. Test tools in conversation

## Debugging

### Enable Debug Logging

```typescript
// Add at start of server
console.error("Server starting...");

server.onerror = (error) => {
  console.error("MCP Error:", error);
};
```

### Test with Inspector

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Server not found | Check path in config |
| Tool not appearing | Verify ListTools handler |
| Tool errors | Check CallTool handler, add logging |
| Environment vars | Ensure env block in config |

## Resources

- **MCP Spec:** https://spec.modelcontextprotocol.io/
- **SDK Docs:** https://modelcontextprotocol.io/docs
- **Example Servers:** https://github.com/modelcontextprotocol/servers
- **Community:** https://github.com/punkpeye/awesome-mcp-servers

## Reference Files

See [references/mcp-templates.md](references/mcp-templates.md) for:
- Complete TypeScript server template
- Python server template
- Common tool patterns
- Authentication patterns
