# Setting Up Pushover for Notifications

Read ecosystem-config SKILL.md for the proper configuration pattern.

## Configuration

The skill specifies that all credentials go in `~/scripts/ecosystem.env`. Adding your Pushover keys:

```bash
# Add to ~/scripts/ecosystem.env
cat >> ~/scripts/ecosystem.env << 'EOF'
export PUSHOVER_USER_KEY="test-user-key"
export PUSHOVER_APP_TOKEN="test-app-token"
EOF
```

Variable names per the skill:
- `PUSHOVER_USER_KEY` = "test-user-key"
- `PUSHOVER_APP_TOKEN` = "test-app-token"

These are used by the `notify.py` script for sending push notifications through Pushover.

## Activate

Reload your shell:
```bash
source ~/.zshrc
```

The `~/.zshrc` already sources `~/scripts/ecosystem.env`, so this picks up the new variables immediately.

## Confirm

```bash
echo $PUSHOVER_USER_KEY   # should print: test-user-key
echo $PUSHOVER_APP_TOKEN  # should print: test-app-token
```

## Notes

- Written to `~/scripts/ecosystem.env` (central config), not `~/.zshrc` directly
- You can also set `NOTIFY_ENABLED="false"` in the same file to disable notifications
- The env file is git-ignored for security
