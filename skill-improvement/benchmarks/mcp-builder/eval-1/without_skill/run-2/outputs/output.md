# Property Lookup MCP Server

Here's a TypeScript MCP server with a lookup_property tool.

```typescript
import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  {{ name: "property-lookup", version: "1.0.0" }},
  {{ capabilities: {{ tools: {{}} }} }}
);

// Define tools
server.setRequestHandler("tools/list", async () => ({{
  tools: [{{
    name: "lookup_property",
    description: "Look up property details by address",
    inputSchema: {{
      type: "object",
      properties: {{
        address: {{ type: "string" }}
      }},
      required: ["address"]
    }}
  }}]
}}));

// Handle calls
server.setRequestHandler("tools/call", async (request) => {{
  if (request.params.name === "lookup_property") {{
    const address = request.params.arguments?.address;
    const response = await fetch(`https://api.properties.example/v1/lookup?address=${{encodeURIComponent(address)}}`);
    const data = await response.json();
    return {{ content: [{{ type: "text", text: JSON.stringify(data) }}] }};
  }}
}});

const transport = new StdioServerTransport();
await server.connect(transport);
```

You'll need to install the MCP SDK: `npm install @modelcontextprotocol/sdk`
