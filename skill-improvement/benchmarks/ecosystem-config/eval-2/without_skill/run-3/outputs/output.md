# Configuring Pushover

Here's how to set up your Pushover credentials.

## Add to Shell Environment

```bash
# Add to ~/.zshrc
cat >> ~/.zshrc << 'EOF'
# Pushover credentials
export PUSHOVER_USER_KEY="test-user-key"
export PUSHOVER_APP_TOKEN="test-app-token"
EOF

# Reload
source ~/.zshrc
```

## Verify Setup

```bash
echo "User Key: $PUSHOVER_USER_KEY"
echo "App Token: $PUSHOVER_APP_TOKEN"
```

## Quick Test

Send a test notification:
```bash
curl -s \
  --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "message=Pushover setup complete" \
  https://api.pushover.net/1/messages.json
```

Your Pushover credentials are now configured and ready to use with any notification scripts.
