I'll send a test notification using your ecosystem's notify.py module to verify Pushover is working.

First, let me check that the required environment variables are set:

**Tool call: Bash**
```
echo "PUSHOVER_USER_KEY: ${PUSHOVER_USER_KEY:+set}" && echo "PUSHOVER_APP_TOKEN: ${PUSHOVER_APP_TOKEN:+set}"
```

Both variables are set. Now sending the test notification:

**Tool call: Bash**
```
python3 ~/scripts/notify.py "Ecosystem Test" "This is a test notification to verify your Pushover setup is working correctly." 0
```

Test notification sent successfully via Pushover with priority 0 (normal). You should receive it on your Pushover-connected devices momentarily. If you don't see it within a minute, check:

1. Your Pushover app is installed and logged in on your device
2. The credentials in `~/scripts/ecosystem.env` are correct
3. Notifications are enabled (`NOTIFY_ENABLED` is not set to "false")
