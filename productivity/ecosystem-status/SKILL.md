---
name: ecosystem-status
description: >
  Use this skill to check the health and running status of all ecosystem
  automation systems. Activate when the user asks "are my automations
  running?", "is the tax organizer working?", "system health check",
  "status of my tools", or wants a dashboard view of background services.
  Monitors: Tax PDF Organizer, Media Organizer, Monarch Money MCP Server,
  Treehouse Context Sync, and Notion Rules (Tax OCR). Shows running, idle,
  stale, or down status for each system and flags items needing attention.
  Runs ~/scripts/ecosystem_status.py. Do NOT use this skill for configuring
  systems (use ecosystem-config) or setting up notifications (use
  notifications skill).
---

# Ecosystem Status Skill

Shows status of all automation systems in your ecosystem:
- Tax PDF Organizer (LaunchAgent + watcher)
- Media Organizer
- Monarch Money MCP Server
- Treehouse Context Sync
- Notion Rules (Tax OCR)

## Usage

Run from anywhere:
```bash
~/scripts/status
```

Or directly:
```bash
python3 ~/scripts/ecosystem_status.py
```

## Output Example

```
📊 ECOSYSTEM STATUS - 2026-01-17 13:19:11
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Tax PDF Organizer
   Status: ✅ Watching
   Watcher running (PID 1572)
   Last activity: 22 hours ago

📷 Media Organizer
   Status: ⏸️ Installed
   Pending: 10 files

💰 Monarch Money
   Status: ✅ Connected
   Session: 4 minutes ago

🔄 Context Sync
   Status: ✅ Synced
   Last sync: 1 hour ago

📄 Notion Rules (Tax OCR)
   Status: ⏸️ Idle
   Last run: 51 minutes ago

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ATTENTION NEEDED:
   • 📁 1 PDF files in Downloads
   • 📷 10 media files in Downloads
```

## Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Running/Connected/Synced |
| ⏸️ | Idle/Loaded/Installed |
| ⚠️ | Stale (needs attention) |
| ❌ | Not running/Not configured |

## Troubleshooting

### System shows as down or not configured
1. Check if the LaunchAgent plist is loaded: `launchctl list | grep <service>`
2. Verify environment variables are set: `echo $VARIABLE_NAME`
3. Check logs for the specific service in `~/Library/Logs/` or `~/scripts/logs/`
4. Re-run the service setup script if available

### Stale status (last activity too old)
1. Check if the watcher process is still running: `ps aux | grep <process>`
2. Restart the LaunchAgent: `launchctl kickstart -k gui/$(id -u)/<label>`
3. Check disk space and permissions on watched directories

## Installation

The script is installed at `~/scripts/ecosystem_status.py`. A copy is also maintained in this skill for version control.

To update the installed version:
```bash
cp ~/Projects/claude-skills/productivity/ecosystem-status/scripts/ecosystem_status.py ~/scripts/
```
