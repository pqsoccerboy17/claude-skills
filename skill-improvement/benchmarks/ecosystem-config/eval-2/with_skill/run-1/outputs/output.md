# Setting Up Pushover Credentials

Read the ecosystem-config skill first for the correct approach.

## Process

Per the skill at ~/Projects/claude-skills/productivity/ecosystem-config/SKILL.md, all credentials go in `~/scripts/ecosystem.env`.

## Adding Pushover Credentials

I'll add your Pushover credentials to the central config file:

```bash
# Append to ~/scripts/ecosystem.env
cat >> ~/scripts/ecosystem.env << 'EOF'

# Pushover Notifications
export PUSHOVER_USER_KEY="test-user-key"
export PUSHOVER_APP_TOKEN="test-app-token"
EOF
```

The skill specifies these exact variable names:
- `PUSHOVER_USER_KEY` - your Pushover user key
- `PUSHOVER_APP_TOKEN` - your Pushover app token

These are used by `notify.py` for sending push notifications.

## Activate the Changes

Reload your shell so the new variables take effect:

```bash
source ~/.zshrc
```

This works because `~/.zshrc` sources `~/scripts/ecosystem.env`.

## Verify

```bash
echo $PUSHOVER_USER_KEY
echo $PUSHOVER_APP_TOKEN
```

## Notes

- Credentials are stored in `~/scripts/ecosystem.env`, not directly in `~/.zshrc`
- You can disable notifications by setting `NOTIFY_ENABLED="false"` in the same file
- The ecosystem.env file is not committed to git
