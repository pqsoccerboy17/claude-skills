I'll add your Pushover credentials to the ecosystem config file.

**Tool call: Read**
```
~/scripts/ecosystem.env
```

**Tool call: Edit** (adding Pushover credentials to ~/scripts/ecosystem.env)
```
PUSHOVER_USER_KEY="test-user-key"
PUSHOVER_APP_TOKEN="test-app-token"
NOTIFY_ENABLED="true"
```

Done. I've added your Pushover credentials to `~/scripts/ecosystem.env`:
- `PUSHOVER_USER_KEY` set to your user key
- `PUSHOVER_APP_TOKEN` set to your app token
- `NOTIFY_ENABLED` set to "true" so notifications are active

Now reload your shell to pick up the changes:

```bash
source ~/.zshrc
```

After reloading, you can verify the setup works by sending a test notification:

```bash
python3 ~/scripts/notify.py "Test" "Pushover setup complete"
```
