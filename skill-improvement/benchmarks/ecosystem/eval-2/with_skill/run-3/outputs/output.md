Checking those two systems for you now.

**Tool call: Bash**
```
python3 ~/scripts/ecosystem_status.py
```

From the ecosystem status output, here are the two you asked about:

**Tax PDF Organizer**
- Status: Running
- The LaunchAgent (`com.user.tax-pdf-organizer`) is loaded and the `watch_downloads.py` watcher is active
- No issues detected

**Monarch Money MCP Server**
- Status: Connected
- MCP server is responding normally
- Note: Monarch uses session-based authentication (not env vars), and the session is currently valid

Both systems are running without problems. The other three systems (Media Organizer, Treehouse Context Sync, Notion Rules) were not requested but are also available if you want a full status check.
