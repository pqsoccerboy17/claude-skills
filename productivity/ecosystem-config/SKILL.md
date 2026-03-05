---
name: ecosystem-config
description: >
  Use this skill to configure, set up, or troubleshoot environment variables
  and credentials for ecosystem automation tools. Activate when the user
  wants to add API keys for automations, configure Notion tokens, set up
  Google Drive credentials, configure Pushover notification keys, edit
  ecosystem.env, or troubleshoot missing environment variables. Manages the
  central ~/scripts/ecosystem.env file that all automation tools source.
  Covers Notion API tokens, Google Drive service accounts, Pushover keys,
  and Monarch Money auth. Do NOT use for checking system status (use
  ecosystem-status) or for non-ecosystem environment variables.
---

# Ecosystem Configuration

Central configuration file for all automation tools in the ecosystem.

## Purpose

Consolidates all environment variable configuration into a single file that can be sourced from your shell profile.

## Setup

1. Copy the example file:
   ```bash
   cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env
   ```

2. Fill in your credentials (edit the file)

3. Add to your `~/.zshrc`:
   ```bash
   source ~/scripts/ecosystem.env
   ```

4. Reload your shell:
   ```bash
   source ~/.zshrc
   ```

## Environment Variables

### Notion API
| Variable | Required For | Description |
|----------|-------------|-------------|
| `NOTION_TOKEN` | treehouse-context-sync, drive-index-sync | Notion integration token |
| `NOTION_DOCUMENT_INDEX_DB_ID` | drive-index-sync | Document Index database ID |
| `NOTION_PROPERTIES_DB_ID` | drive-index-sync | Properties database ID |

### Google Drive API
| Variable | Required For | Description |
|----------|-------------|-------------|
| `GDRIVE_SERVICE_ACCOUNT_JSON` | drive-index-sync | Service account JSON |
| `DRIVE_ROOT_FOLDER` | drive-index-sync | Root folder ID to scan |

### Notifications
| Variable | Required For | Description |
|----------|-------------|-------------|
| `PUSHOVER_USER_KEY` | notify.py | Pushover user key |
| `PUSHOVER_APP_TOKEN` | notify.py | Pushover app token |
| `NOTIFY_ENABLED` | notify.py | Set to "false" to disable |

### Monarch Money
Authentication uses session files, not environment variables. Run `login_setup.py` to authenticate.

## Files

- `~/scripts/ecosystem.env.example` - Template with all variables
- `~/scripts/ecosystem.env` - Your actual configuration (not committed to git)

## Verification

Check your configuration status:
```bash
python3 ~/scripts/ecosystem_status.py
```

## Security

- Never commit `ecosystem.env` to git
- The example file contains no sensitive data
- Use keychain/keyring for highly sensitive credentials where possible
