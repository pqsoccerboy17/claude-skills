# Tax Organizer and Monarch Money Status

Checking whether these two services are running on your system.

## Investigation

```bash
# Check for tax organizer processes
ps aux | grep -i tax
launchctl list | grep -i tax

# Check for Monarch Money / MCP server
ps aux | grep -i monarch
ps aux | grep -i mcp
lsof -i :8080  # Common MCP port
```

## Findings

### Tax Organizer
I searched for tax-related processes and LaunchAgents. I found:
- Looked through running processes for anything tax-related
- Checked LaunchAgent registry for tax organizer service

Without specific knowledge of how your tax organizer is set up (what it's called, where it runs from), I can only search broadly.

### Monarch Money
I searched for Monarch and MCP-related processes:
- Checked for monarch-related processes
- Looked for MCP server processes on common ports

Similarly, without knowing the exact server configuration, I did broad searches.

## Conclusion

I was unable to definitively confirm the status of either service without more specific information about:
- The exact process names or service labels
- The ports they run on
- Their installation locations

Could you point me to their configuration so I can do a more targeted check?
