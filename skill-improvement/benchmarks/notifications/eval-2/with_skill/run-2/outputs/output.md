# Pushover Test Notification

Read the notifications SKILL.md. Using send_notification() from ~/scripts/notify.py to send a test.

```python
import sys
import os
from pathlib import Path

# Import per skill pattern
sys.path.insert(0, str(Path.home() / "scripts"))

# Check required env vars first
pushover_user = os.environ.get("PUSHOVER_USER_KEY")
pushover_token = os.environ.get("PUSHOVER_APP_TOKEN")

if not pushover_user:
    print("ERROR: PUSHOVER_USER_KEY not set in environment")
    print("Set it with: export PUSHOVER_USER_KEY='your-key'")
    sys.exit(1)

if not pushover_token:
    print("ERROR: PUSHOVER_APP_TOKEN not set in environment")
    print("Set it with: export PUSHOVER_APP_TOKEN='your-token'")
    sys.exit(1)

from notify import send_notification

# Send test notification
try:
    result = send_notification(
        title="Pushover Test",
        message="This is a test notification to verify your Pushover setup is working correctly. If you see this, everything is configured properly!",
        priority=0  # Normal priority
    )
    print("Test notification sent successfully!")
    print(f"Result: {result}")
except Exception as e:
    print(f"Failed to send notification: {e}")
    print("Check your PUSHOVER_USER_KEY and PUSHOVER_APP_TOKEN values.")
```
