# Checking Tax Organizer and Monarch Money Server

## Approach

I'll search for these services in your running processes and LaunchAgent configuration.

```bash
# Tax organizer
ps aux | grep -i "tax\|pdf.*organiz"
launchctl list | grep -i "tax\|pdf"

# Monarch Money
ps aux | grep -i "monarch\|mcp"
launchctl list | grep -i "monarch\|money"
```

## Results

### Tax Organizer
Searched for tax and PDF organizer processes. Found some LaunchAgent entries but cannot confirm specific status without knowing the exact service label or process name for your tax organizer setup.

### Monarch Money Server
Searched for Monarch Money and MCP server processes. Found some process entries but would need more details about the specific server setup to confirm it's the Monarch Money MCP server versus other MCP servers.

## Summary

I ran broad process searches but cannot give definitive running/idle/down status for either service. The information I have is:
- Some PDF-related and MCP-related processes exist on your system
- I cannot distinguish which specific services they belong to

To check these more precisely, I'd need to know where these services are installed and what their process names or LaunchAgent labels are.
