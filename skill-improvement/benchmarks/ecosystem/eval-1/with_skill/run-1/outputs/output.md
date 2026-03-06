I'll check the health of all your automation systems by running the ecosystem status script.

**Tool call: Bash**
```
python3 ~/scripts/ecosystem_status.py
```

Here's the status of your automation ecosystem:

**Ecosystem Status Dashboard**

| System | Status | Details |
|--------|--------|---------|
| Tax PDF Organizer | Running | LaunchAgent active, watcher monitoring ~/Downloads |
| Media Organizer | Idle | LaunchAgent loaded but no recent activity |
| Monarch Money MCP Server | Connected | MCP server responding normally |
| Treehouse Context Sync | Synced | Last sync 12 minutes ago |
| Notion Rules (Tax OCR) | Running | Processing queue empty, ready |

**Summary:** 4 of 5 systems are actively running. The Media Organizer is loaded but idle - this is normal if no new media files have been added recently. No systems are down or stale.

If you want to investigate the idle Media Organizer or need to restart any service, let me know.
