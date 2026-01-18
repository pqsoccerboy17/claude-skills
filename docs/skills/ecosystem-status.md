# Ecosystem Status

**Purpose:** Monitor the health of all Treehouse systems at a glance.

## Quick Start

```bash
cd ~/claude-skills/productivity/ecosystem-status/scripts

# Check all systems
python3 ecosystem_status.py

# Check specific system
python3 ecosystem_status.py --system gmail

# Output as JSON
python3 ecosystem_status.py --json
```

## What It Checks

| System | Check |
|--------|-------|
| Gmail API | Token validity, quota |
| Google Drive | Connection, storage |
| Notion | API connection |
| Pushover | Notification delivery |
| Review Queue | Pending item count |

## Example Output

```
TREEHOUSE ECOSYSTEM STATUS
==========================

Gmail API        ✅ Connected (quota: 85%)
Google Drive     ✅ Connected (12.4 GB free)
Notion           ✅ Connected
Pushover         ✅ Active
Review Queue     ⚠️ 3 items pending

Overall: HEALTHY
```
