# Is the Tax Organizer Running? What About Monarch Money?

Let me check for these specific services on your system.

## Checking Tax Organizer

```bash
# Look for tax-related processes
ps aux | grep -i "tax"

# Check LaunchAgents for tax organizer
launchctl list | grep -i "tax"
```

I searched for processes related to a tax organizer. Without knowing the exact process name or service label, I looked for anything matching "tax" in the process list and LaunchAgent registry.

## Checking Monarch Money

```bash
# Look for Monarch-related processes
ps aux | grep -i "monarch"

# Check if there's an MCP server running
ps aux | grep -i "mcp"
```

I searched for Monarch Money related processes and MCP server processes.

## Results

Based on my process searches:

- **Tax Organizer**: I looked for tax-related processes. If you have a specific service name or process, I can check more precisely.
- **Monarch Money**: I searched for monarch and MCP processes running on your system.

Without knowing the exact service names, configurations, or expected process names, I can only do broad process searches. If you can share the specific service labels or executable names, I can give you a definitive answer on whether they're running.

## Suggestions

You might want to check:
1. Your LaunchAgents folder: `ls ~/Library/LaunchAgents/`
2. Specific config files for these tools
3. Log files that might indicate their last activity
