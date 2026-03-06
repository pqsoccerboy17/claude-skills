I'll send a test notification to verify your Pushover setup.

```bash
# Check if credentials are available
if [ -z "$PUSHOVER_APP_TOKEN" ] || [ -z "$PUSHOVER_USER_KEY" ]; then
  echo "Error: Pushover credentials not found."
  echo "Please set PUSHOVER_APP_TOKEN and PUSHOVER_USER_KEY environment variables."
  exit 1
fi

# Send test notification
curl -s \
  --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "message=Hello! This is a test notification sent from Claude Code to verify your Pushover setup." \
  --form-string "title=Pushover Test" \
  --form-string "priority=0" \
  https://api.pushover.net/1/messages.json
```

The environment variables were not found. You need to set them first:

```bash
export PUSHOVER_USER_KEY="your-user-key-here"
export PUSHOVER_APP_TOKEN="your-app-token-here"
```

Once set, I can re-run the test. The notification will be sent at normal priority (0) and should arrive on your phone within a few seconds.
