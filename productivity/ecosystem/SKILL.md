---
name: ecosystem
description: >
  Use this skill to manage your automation ecosystem - check system health,
  configure credentials, or send notifications. Activate when the user asks
  "are my automations running?", "system health check", "status of my tools",
  "add my API key to ecosystem config", "set up Pushover credentials",
  "edit ecosystem.env", "send a test notification", "add push notifications
  to a script", or "configure notification priority". Covers three domains:
  (1) Status monitoring of Tax PDF Organizer, Media Organizer, Monarch Money,
  Context Sync, and Notion Rules via ~/scripts/ecosystem_status.py.
  (2) Credential management via the central ~/scripts/ecosystem.env file.
  (3) Push notifications via ~/scripts/notify.py supporting Pushover and
  macOS fallback. Do NOT use for email notifications, Slack messages, or
  non-ecosystem environment variables.
---

# Ecosystem Management Skill

Unified skill for managing all automation infrastructure - status monitoring, credential configuration, and push notifications.

---

## Status Monitoring

Shows health of all automation systems in your ecosystem:
- Tax PDF Organizer (LaunchAgent + watcher)
- Media Organizer
- Monarch Money MCP Server
- Treehouse Context Sync
- Notion Rules (Tax OCR)

### Usage

```bash
~/scripts/status
# or directly:
python3 ~/scripts/ecosystem_status.py
```

### Status Indicators

| Icon | Meaning |
|------|---------|
| Running/Connected/Synced | Active and healthy |
| Idle/Loaded/Installed | Present but not active |
| Stale | Needs attention (last activity too old) |
| Down/Not configured | Not running or missing config |

### Troubleshooting

**System shows as down or not configured:**
1. Check if LaunchAgent is loaded: `launchctl list | grep <service>`
2. Verify environment variables: `echo $VARIABLE_NAME`
3. Check logs in `~/Library/Logs/` or `~/scripts/logs/`

**Stale status (last activity too old):**
1. Check if watcher is running: `ps aux | grep <process>`
2. Restart LaunchAgent: `launchctl kickstart -k gui/$(id -u)/<label>`
3. Check disk space and permissions

---

## Configuration

Central configuration file for all automation tools: `~/scripts/ecosystem.env`

### Setup

1. Copy the example: `cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env`
2. Fill in your credentials
3. Add to `~/.zshrc`: `source ~/scripts/ecosystem.env`
4. Reload: `source ~/.zshrc`

### Environment Variables

#### Notion API
| Variable | Required For | Description |
|----------|-------------|-------------|
| `NOTION_TOKEN` | treehouse-context-sync, drive-index-sync | Notion integration token |
| `NOTION_DOCUMENT_INDEX_DB_ID` | drive-index-sync | Document Index database ID |
| `NOTION_PROPERTIES_DB_ID` | drive-index-sync | Properties database ID |

#### Google Drive API
| Variable | Required For | Description |
|----------|-------------|-------------|
| `GDRIVE_SERVICE_ACCOUNT_JSON` | drive-index-sync | Service account JSON |
| `DRIVE_ROOT_FOLDER` | drive-index-sync | Root folder ID to scan |

#### Notifications
| Variable | Required For | Description |
|----------|-------------|-------------|
| `PUSHOVER_USER_KEY` | notify.py | Pushover user key |
| `PUSHOVER_APP_TOKEN` | notify.py | Pushover app token |
| `NOTIFY_ENABLED` | notify.py | Set to "false" to disable |

#### Monarch Money
Authentication uses session files, not environment variables. Run `login_setup.py` to authenticate.

### Files

- `~/scripts/ecosystem.env.example` - Template with all variables
- `~/scripts/ecosystem.env` - Your actual configuration (not committed to git)

### Security

- Never commit `ecosystem.env` to git
- Use keychain/keyring for highly sensitive credentials where possible

---

## Notifications

Unified notification module for all ecosystem automation tools.

### Supported Backends

1. **Pushover** (primary) - Mobile/desktop push notifications
2. **macOS Notifications** (fallback) - System notification center

### Pushover Setup

1. Create a Pushover account at https://pushover.net
2. Create an application to get an API token
3. Set environment variables in `~/scripts/ecosystem.env`:
   ```
   PUSHOVER_USER_KEY="your-user-key"
   PUSHOVER_APP_TOKEN="your-app-token"
   ```

### Usage

#### From Python
```python
from notify import send_notification, notify_organization_complete

# Simple notification
send_notification("Title", "Message body", priority=0)

# Organization complete notification
notify_organization_complete(
    organizer_name="Tax Organizer",
    files_organized=5,
    categories={"Bank Statements": 3, "Tax Forms": 2},
    pending_review=1
)
```

#### From Command Line
```bash
python3 ~/scripts/notify.py "Title" "Message"
python3 ~/scripts/notify.py "Title" "Message" 1  # priority 1 (high)
```

### Priority Levels

| Priority | Meaning |
|----------|---------|
| -2 | Silent (no sound/vibration) |
| -1 | Low (no sound) |
| 0 | Normal (default) |
| 1 | High (bypasses quiet hours) |
| 2 | Emergency (requires acknowledgment) |

### Integration

Currently integrated with tax-pdf-organizer (watch_downloads.py).

To add to other tools:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "scripts"))

try:
    from notify import notify_organization_complete
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
```

## Installation

Scripts are installed at:
- `~/scripts/ecosystem_status.py` - Status monitoring
- `~/scripts/ecosystem.env` - Configuration
- `~/scripts/notify.py` - Notifications

Verification: `python3 ~/scripts/ecosystem_status.py`
