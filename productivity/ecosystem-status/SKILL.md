---
name: ecosystem-status
description: Check status of all automation systems at a glance
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

## Installation

The script is installed at `~/scripts/ecosystem_status.py`. A copy is also maintained in this skill for version control.

To update the installed version:
```bash
cp ~/claude-skills/productivity/ecosystem-status/scripts/ecosystem_status.py ~/scripts/
```
