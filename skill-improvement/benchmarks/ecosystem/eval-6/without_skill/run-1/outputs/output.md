I'll send a test Pushover notification for you. Let me use curl to hit the Pushover API directly:

```bash
curl -s \
  --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "message=Test notification from Claude Code - verifying Pushover setup is working correctly" \
  --form-string "title=Pushover Test" \
  --form-string "priority=0" \
  https://api.pushover.net/1/messages.json
```

Let me check if the environment variables are set first:

```bash
echo "PUSHOVER_APP_TOKEN is: $([ -n "$PUSHOVER_APP_TOKEN" ] && echo 'set' || echo 'NOT SET')"
echo "PUSHOVER_USER_KEY is: $([ -n "$PUSHOVER_USER_KEY" ] && echo 'set' || echo 'NOT SET')"
```

If the variables are not set, you'll need to configure them first:

```bash
export PUSHOVER_USER_KEY="your-user-key"
export PUSHOVER_APP_TOKEN="your-app-token"
```

Then run the curl command above again. You should receive a push notification on your phone if everything is configured correctly. The API will return a JSON response with `{"status":1}` on success.
