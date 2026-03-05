# MCP Server: Property Lookup

Read the mcp-builder SKILL.md first. Following the TypeScript MCP server pattern from the skill.

## Project Setup

package.json:
```json
{{
  "name": "property-lookup-mcp",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {{
    "@modelcontextprotocol/sdk": "^1.0.0",
    "typescript": "^5.0.0",
    "axios": "^1.6.0"
  }},
  "scripts": {{
    "build": "tsc",
    "start": "node dist/index.js"
  }}
}}
```

## Server Implementation

```typescript
import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
import {{ ListToolsRequestSchema, CallToolRequestSchema }} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

const server = new Server(
  {{ name: "property-lookup", version: "1.0.0" }},
  {{ capabilities: {{ tools: {{}} }} }}
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({{
  tools: [
    {{
      name: "lookup_property",
      description: "Look up property details by address",
      inputSchema: {{
        type: "object",
        properties: {{
          address: {{ type: "string", description: "Property address to look up" }}
        }},
        required: ["address"]
      }}
    }}
  ]
}}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {{
  if (request.params.name === "lookup_property") {{
    const address = request.params.arguments?.address as string;
    try {{
      const response = await axios.get(
        `https://api.properties.example/v1/lookup`,
        {{ params: {{ address }} }}
      );
      return {{
        content: [{{ type: "text", text: JSON.stringify(response.data, null, 2) }}]
      }};
    }} catch (error) {{
      return {{
        content: [{{ type: "text", text: `Error looking up property: ${{error}}` }}],
        isError: true
      }};
    }}
  }}
  throw new Error("Unknown tool");
}});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Configuration

Add to Claude Code settings (.mcp.json or settings.json):

```json
{{
  "mcpServers": {{
    "property-lookup": {{
      "command": "node",
      "args": ["/path/to/property-lookup-mcp/dist/index.js"]
    }}
  }}
}}
```
