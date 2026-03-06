I'll check on both of those for you.

```bash
ps aux | grep -i "tax\|organizer"
ps aux | grep -i "monarch"
```

**Tax Organizer:**
I searched for processes matching "tax" or "organizer" but didn't find a clear match. Is this a Python script that runs as a background process, or a LaunchAgent? If you can share the script name or plist file, I can check more precisely.

**Monarch Money Server:**
I didn't find a process specifically named "monarch" running. I know there's a Monarch Money MCP server - is it configured in your Claude Code MCP settings? If it's an MCP server, it would start on demand when Claude Code connects to it, rather than running as a persistent process.

Would you like me to check your MCP configuration to see if the Monarch Money server is configured there?
