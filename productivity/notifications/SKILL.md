---
name: notifications
description: Unified notification system for ecosystem tools
---

# Notifications Skill

Unified notification module for all ecosystem automation tools.

## Supported Backends

1. **Pushover** (primary) - Mobile/desktop push notifications
2. **macOS Notifications** (fallback) - System notification center

## Setup

### Pushover (Recommended)

1. Create a Pushover account at https://pushover.net
2. Create an application to get an API token
3. Set environment variables:

```bash
export PUSHOVER_USER_KEY="your-user-key"
export PUSHOVER_APP_TOKEN="your-app-token"
```

Add to `~/.zshrc` or `~/.bashrc` for persistence.

### macOS Fallback

No setup required - uses built-in notification center.

## Usage

### From Python

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

### From Command Line

```bash
python3 ~/scripts/notify.py "Title" "Message"
python3 ~/scripts/notify.py "Title" "Message" 1  # priority 1 (high)
```

## Priority Levels

| Priority | Meaning |
|----------|---------|
| -2 | Silent (no sound/vibration) |
| -1 | Low (no sound) |
| 0 | Normal (default) |
| 1 | High (bypasses quiet hours) |
| 2 | Emergency (requires acknowledgment) |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PUSHOVER_USER_KEY` | For Pushover | Your Pushover user key |
| `PUSHOVER_APP_TOKEN` | For Pushover | Your Pushover app token |
| `NOTIFY_ENABLED` | No | Set to "false" to disable all notifications |

## Integration

Currently integrated with:
- **tax-pdf-organizer** (watch_downloads.py) - Notifies after files are organized

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

# Then call notify_organization_complete() after processing
```

## Installation

The module is installed at `~/scripts/notify.py`. A copy is maintained here for version control.

To update:
```bash
cp ~/Documents/claude-skills/productivity/notifications/scripts/notify.py ~/scripts/
```
