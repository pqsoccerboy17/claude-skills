Running the ecosystem status script to check all your automations.

**Tool call: Bash**
```
python3 ~/scripts/ecosystem_status.py
```

**Ecosystem Status**

| System | Health | Notes |
|--------|--------|-------|
| Tax PDF Organizer | Running | Watcher active, LaunchAgent loaded |
| Media Organizer | Stale | Last activity was 3 days ago |
| Monarch Money MCP Server | Connected | Healthy |
| Treehouse Context Sync | Synced | Last sync 5 minutes ago |
| Notion Rules (Tax OCR) | Running | Queue clear |

**Attention needed:** The Media Organizer is showing as stale - its last activity was over 3 days ago. You may want to check if the watcher process is still running:

```bash
ps aux | grep media
launchctl list | grep media
```

If it needs a restart:
```bash
launchctl kickstart -k gui/$(id -u)/com.user.media-organizer
```

The other 4 systems are all healthy and running normally.
