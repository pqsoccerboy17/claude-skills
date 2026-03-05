# Invoice MCP Server (Python)

```python
from fastmcp import FastMCP
import json

mcp = FastMCP("invoice-server")
invoices = []

@mcp.tool()
def list_invoices():
    """List all invoices"""
    return invoices

@mcp.tool()
def create_invoice(client_name: str, amount: float, description: str):
    """Create a new invoice"""
    invoice = {
        "id": len(invoices) + 1,
        "client_name": client_name,
        "amount": amount,
        "description": description
    }
    invoices.append(invoice)
    return f"Invoice created: {invoice}"

if __name__ == "__main__":
    mcp.run()
```

Install with `pip install fastmcp` and run `python server.py`.
