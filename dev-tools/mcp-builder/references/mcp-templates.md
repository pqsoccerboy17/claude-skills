# MCP Server Templates

Complete templates for building MCP servers.

## TypeScript Server Template (Full)

### package.json

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "watch": "tsc --watch",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### src/index.ts (Complete)

```typescript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
  ErrorCode,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";

// Configuration
const SERVER_NAME = "my-mcp-server";
const SERVER_VERSION = "1.0.0";

// Initialize server
const server = new Server(
  { name: SERVER_NAME, version: SERVER_VERSION },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// ============================================
// TOOLS - Functions Claude can call
// ============================================

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "hello_world",
      description: "Returns a greeting message",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "The name to greet",
          },
        },
        required: ["name"],
      },
    },
    {
      name: "fetch_url",
      description: "Fetches content from a URL",
      inputSchema: {
        type: "object",
        properties: {
          url: {
            type: "string",
            description: "The URL to fetch",
          },
        },
        required: ["url"],
      },
    },
    {
      name: "calculate",
      description: "Performs a mathematical calculation",
      inputSchema: {
        type: "object",
        properties: {
          expression: {
            type: "string",
            description: "Mathematical expression to evaluate",
          },
        },
        required: ["expression"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "hello_world": {
        const greeting = `Hello, ${args?.name}! How can I help you today?`;
        return {
          content: [{ type: "text", text: greeting }],
        };
      }

      case "fetch_url": {
        const response = await fetch(args?.url as string);
        const text = await response.text();
        return {
          content: [{ type: "text", text: text.slice(0, 5000) }], // Limit response
        };
      }

      case "calculate": {
        // Simple math eval (use a proper library in production)
        const result = eval(args?.expression as string);
        return {
          content: [{ type: "text", text: `Result: ${result}` }],
        };
      }

      default:
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: "text", text: `Error: ${message}` }],
      isError: true,
    };
  }
});

// ============================================
// RESOURCES - Data Claude can access
// ============================================

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "config://settings",
      name: "Server Settings",
      description: "Current server configuration",
      mimeType: "application/json",
    },
    {
      uri: "file://readme",
      name: "README",
      description: "Server documentation",
      mimeType: "text/markdown",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  switch (uri) {
    case "config://settings":
      return {
        contents: [
          {
            uri,
            mimeType: "application/json",
            text: JSON.stringify(
              {
                serverName: SERVER_NAME,
                version: SERVER_VERSION,
                environment: process.env.NODE_ENV || "development",
              },
              null,
              2
            ),
          },
        ],
      };

    case "file://readme":
      return {
        contents: [
          {
            uri,
            mimeType: "text/markdown",
            text: `# ${SERVER_NAME}\n\nThis is a custom MCP server.\n\n## Available Tools\n- hello_world\n- fetch_url\n- calculate`,
          },
        ],
      };

    default:
      throw new McpError(ErrorCode.InvalidRequest, `Unknown resource: ${uri}`);
  }
});

// ============================================
// PROMPTS - Pre-defined templates
// ============================================

server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "greeting_template",
      description: "A friendly greeting prompt",
      arguments: [
        {
          name: "user_name",
          description: "The user's name",
          required: true,
        },
      ],
    },
  ],
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "greeting_template") {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please greet ${args?.user_name} warmly and ask how you can help them today.`,
          },
        },
      ],
    };
  }

  throw new McpError(ErrorCode.InvalidRequest, `Unknown prompt: ${name}`);
});

// ============================================
// ERROR HANDLING
// ============================================

server.onerror = (error) => {
  console.error("[MCP Error]", error);
};

process.on("SIGINT", async () => {
  await server.close();
  process.exit(0);
});

// ============================================
// START SERVER
// ============================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`${SERVER_NAME} v${SERVER_VERSION} running on stdio`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

## Python Server Template (Full)

### requirements.txt

```
mcp>=1.0.0
httpx>=0.25.0
```

### server.py

```python
#!/usr/bin/env python3
"""
MCP Server Template - Python
"""

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configuration
SERVER_NAME = "my-mcp-server"
SERVER_VERSION = "1.0.0"

# Initialize server
server = Server(SERVER_NAME)


# ============================================
# TOOLS - Functions Claude can call
# ============================================

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Return list of available tools."""
    return [
        types.Tool(
            name="hello_world",
            description="Returns a greeting message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="fetch_url",
            description="Fetches content from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="query_api",
            description="Query an API endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST"],
                        "description": "HTTP method"
                    },
                    "body": {
                        "type": "object",
                        "description": "Request body for POST"
                    }
                },
                "required": ["endpoint"]
            }
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution."""

    if arguments is None:
        arguments = {}

    try:
        if name == "hello_world":
            greeting = f"Hello, {arguments.get('name', 'friend')}! How can I help you today?"
            return [types.TextContent(type="text", text=greeting)]

        elif name == "fetch_url":
            async with httpx.AsyncClient() as client:
                response = await client.get(arguments["url"], timeout=30.0)
                content = response.text[:5000]  # Limit response size
                return [types.TextContent(type="text", text=content)]

        elif name == "query_api":
            base_url = os.environ.get("API_BASE_URL", "https://api.example.com")
            endpoint = arguments["endpoint"]
            method = arguments.get("method", "GET")

            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(f"{base_url}{endpoint}")
                else:
                    response = await client.post(
                        f"{base_url}{endpoint}",
                        json=arguments.get("body", {})
                    )

                return [types.TextContent(
                    type="text",
                    text=json.dumps(response.json(), indent=2)
                )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


# ============================================
# RESOURCES - Data Claude can access
# ============================================

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """Return list of available resources."""
    return [
        types.Resource(
            uri="config://settings",
            name="Server Settings",
            description="Current server configuration",
            mimeType="application/json"
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if uri == "config://settings":
        return json.dumps({
            "server_name": SERVER_NAME,
            "version": SERVER_VERSION,
            "environment": os.environ.get("ENV", "development")
        }, indent=2)

    raise ValueError(f"Unknown resource: {uri}")


# ============================================
# PROMPTS - Pre-defined templates
# ============================================

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """Return list of available prompts."""
    return [
        types.Prompt(
            name="greeting_template",
            description="A friendly greeting prompt",
            arguments=[
                types.PromptArgument(
                    name="user_name",
                    description="The user's name",
                    required=True
                )
            ]
        ),
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Get a prompt by name."""
    if name == "greeting_template":
        user_name = arguments.get("user_name", "friend") if arguments else "friend"
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Please greet {user_name} warmly and ask how you can help."
                    )
                )
            ]
        )

    raise ValueError(f"Unknown prompt: {name}")


# ============================================
# MAIN
# ============================================

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication Patterns

### API Key Authentication

```typescript
// TypeScript
const API_KEY = process.env.API_KEY;

async function authenticatedFetch(url: string) {
  const response = await fetch(url, {
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    }
  });
  return response.json();
}
```

```python
# Python
import os
import httpx

API_KEY = os.environ.get("API_KEY")

async def authenticated_fetch(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
        )
        return response.json()
```

### OAuth2 Token Management

```typescript
// TypeScript - OAuth2 token refresh
let accessToken: string | null = null;
let tokenExpiry: number = 0;

async function getAccessToken(): Promise<string> {
  if (accessToken && Date.now() < tokenExpiry) {
    return accessToken;
  }

  const response = await fetch(process.env.TOKEN_URL!, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: process.env.CLIENT_ID!,
      client_secret: process.env.CLIENT_SECRET!,
    }),
  });

  const data = await response.json();
  accessToken = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in - 60) * 1000;
  return accessToken!;
}
```

## Error Handling Patterns

```typescript
// TypeScript - Comprehensive error handling
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // Validate required arguments
  if (!args?.requiredField) {
    throw new McpError(
      ErrorCode.InvalidParams,
      "Missing required field: requiredField"
    );
  }

  try {
    // Tool implementation
    const result = await performOperation(args);
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (error) {
    // Handle specific error types
    if (error instanceof NetworkError) {
      return {
        content: [{ type: "text", text: "Network error. Please try again." }],
        isError: true,
      };
    }

    if (error instanceof AuthenticationError) {
      throw new McpError(ErrorCode.InvalidRequest, "Authentication failed");
    }

    // Generic error
    console.error("Tool error:", error);
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});
```

## Testing MCP Servers

### Manual Testing with Inspector

```bash
# Install and run inspector
npx @modelcontextprotocol/inspector node dist/index.js

# Or for Python
npx @modelcontextprotocol/inspector python server.py
```

### Unit Testing (TypeScript)

```typescript
// tests/tools.test.ts
import { describe, it, expect } from "vitest";
import { handleToolCall } from "../src/tools";

describe("Tools", () => {
  it("hello_world returns greeting", async () => {
    const result = await handleToolCall("hello_world", { name: "Test" });
    expect(result.content[0].text).toContain("Hello, Test");
  });
});
```
