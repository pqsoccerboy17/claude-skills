I'll check your Pushover config and send a test notification.

**Tool call: Bash**
```
env | grep -E "PUSHOVER_(USER_KEY|APP_TOKEN)" | sed 's/=.*/=***/'
```

Both Pushover environment variables are present. Sending a test notification at priority 0:

**Tool call: Bash**
```
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'scripts'))
from notify import send_notification
result = send_notification('Ecosystem Test', 'Verifying Pushover notification delivery. Priority: normal (0).', priority=0)
print('Notification sent successfully' if result else 'Notification failed')
"
```

Notification sent successfully. The test was delivered via Pushover at normal priority (0).

Summary:
- Used `send_notification()` from `~/scripts/notify.py`
- Title: "Ecosystem Test"
- Message: "Verifying Pushover notification delivery. Priority: normal (0)."
- Priority: 0 (normal)
- Result: Delivered

Your Pushover setup is working. All ecosystem scripts that use `notify.py` will be able to send push notifications.
