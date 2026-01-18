# Notifications

**Purpose:** Send unified notifications to your phone via Pushover.

## Quick Start

```bash
cd ~/claude-skills/productivity/notifications/scripts

# Send a notification
python3 notify.py --title "Test" --message "Hello from Treehouse"

# With priority
python3 notify.py --title "Alert" --message "Something happened" --priority high
```

## Configuration

Set environment variables:
```bash
export PUSHOVER_USER_KEY="your-user-key"
export PUSHOVER_APP_TOKEN="your-app-token"
```

Or save in `~/.config/treehouse/config.json`:
```json
{
  "pushover": {
    "user_key": "xxx",
    "app_token": "xxx"
  }
}
```

## Priority Levels

| Priority | Behavior |
|----------|----------|
| low | No sound |
| normal | Default sound |
| high | Bypasses quiet hours |
| emergency | Repeats until acknowledged |
