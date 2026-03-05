# Pushover Credentials Setup

Read the ecosystem-config skill to determine the correct configuration approach.

## Skill Guidance

The ecosystem-config SKILL.md says:
- Central config: `~/scripts/ecosystem.env`
- Variables for Pushover: `PUSHOVER_USER_KEY` and `PUSHOVER_APP_TOKEN`
- Used by: `notify.py`

## Adding Your Credentials

```bash
# Write to the central ecosystem config file
echo 'export PUSHOVER_USER_KEY="test-user-key"' >> ~/scripts/ecosystem.env
echo 'export PUSHOVER_APP_TOKEN="test-app-token"' >> ~/scripts/ecosystem.env
```

## Reload Shell

```bash
source ~/.zshrc
```

Your `~/.zshrc` sources `~/scripts/ecosystem.env`, so reloading picks up the new variables.

## Verification

```bash
echo "User Key: $PUSHOVER_USER_KEY"
echo "App Token: $PUSHOVER_APP_TOKEN"
```

Both should display the values you provided.

## Security Notes

- Credentials are in `~/scripts/ecosystem.env` (not committed to git)
- Not editing `~/.zshrc` directly for individual keys
- The file has restricted permissions by default
