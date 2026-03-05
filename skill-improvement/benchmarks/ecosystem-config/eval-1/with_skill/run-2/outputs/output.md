# Setting Up Notion API Token

Read the ecosystem-config skill first.

## How the Ecosystem Config Works

The skill at ~/Projects/claude-skills/productivity/ecosystem-config/SKILL.md explains that all automation credentials are centralized in `~/scripts/ecosystem.env`. This file is sourced from `~/.zshrc` so variables are available in every shell session.

## Add Your Notion Token

1. Open `~/scripts/ecosystem.env`:

```bash
nano ~/scripts/ecosystem.env
```

2. Add the Notion token variable:

```
export NOTION_TOKEN="your-token-here"
```

According to the skill, the variable name is `NOTION_TOKEN` and it's used by treehouse-context-sync and drive-index-sync.

If you also need database-specific IDs, the config supports:
- `NOTION_DOCUMENT_INDEX_DB_ID` - Document Index database ID
- `NOTION_PROPERTIES_DB_ID` - Properties database ID

3. If you haven't set up ecosystem.env yet, start with the example:

```bash
cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env
```

4. Make sure `~/.zshrc` sources it:

```bash
# Should already contain:
source ~/scripts/ecosystem.env
```

5. Reload:

```bash
source ~/.zshrc
```

## Key Points

- All keys go in `~/scripts/ecosystem.env`, not directly in `~/.zshrc`
- The `ecosystem.env.example` file shows all available variables
- Never commit the actual `.env` file to git
