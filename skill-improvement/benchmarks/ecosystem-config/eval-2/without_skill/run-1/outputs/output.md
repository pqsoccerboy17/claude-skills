# Setting Up Pushover Credentials

I'll help you configure Pushover for notifications.

## Adding Environment Variables

Add your Pushover credentials to your shell profile:

```bash
# Add to ~/.zshrc
echo 'export PUSHOVER_USER_KEY="test-user-key"' >> ~/.zshrc
echo 'export PUSHOVER_APP_TOKEN="test-app-token"' >> ~/.zshrc
source ~/.zshrc
```

## Verify

```bash
echo $PUSHOVER_USER_KEY   # test-user-key
echo $PUSHOVER_APP_TOKEN  # test-app-token
```

## Testing the Setup

You can test Pushover with a simple curl command:

```bash
curl -s \
  --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "message=Test notification from setup" \
  https://api.pushover.net/1/messages.json
```

## Security

- Don't commit your `.zshrc` with credentials visible
- Consider using a separate `.env` file if you prefer
