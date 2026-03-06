Let me set up your Pushover credentials. I'll add them as environment variables.

First, let me check your current setup:
```bash
grep -i pushover ~/.zshrc 2>/dev/null
```

No existing Pushover config found. I'll add the credentials to your `~/.zshrc`:

```bash
echo '' >> ~/.zshrc
echo '# Pushover credentials' >> ~/.zshrc
echo 'export PUSHOVER_USER_KEY="test-user-key"' >> ~/.zshrc
echo 'export PUSHOVER_APP_TOKEN="test-app-token"' >> ~/.zshrc
```

Reload to apply:
```bash
source ~/.zshrc
```

Your Pushover credentials are now set. You can use them in scripts via:
- `$PUSHOVER_USER_KEY` - your user key
- `$PUSHOVER_APP_TOKEN` - your app token

Want me to send a test notification to verify they work?
