I'll set up your Pushover credentials. The standard way to store these is as environment variables in your shell profile.

Let me add them to your `~/.zshrc`:

```bash
# Pushover notifications
export PUSHOVER_USER_KEY="test-user-key"
export PUSHOVER_APP_TOKEN="test-app-token"
```

```bash
echo '' >> ~/.zshrc
echo '# Pushover notifications' >> ~/.zshrc
echo 'export PUSHOVER_USER_KEY="test-user-key"' >> ~/.zshrc
echo 'export PUSHOVER_APP_TOKEN="test-app-token"' >> ~/.zshrc
```

Now reload your shell to pick up the changes:

```bash
source ~/.zshrc
```

You can verify they're set:
```bash
echo "User Key: $PUSHOVER_USER_KEY"
echo "App Token: $PUSHOVER_APP_TOKEN"
```

Your Pushover credentials are now configured. You can use them in any script by referencing `$PUSHOVER_USER_KEY` and `$PUSHOVER_APP_TOKEN`.

To test them, you can send a quick notification:
```bash
curl -s --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "message=Test notification from shell" \
  https://api.pushover.net/1/messages.json
```
