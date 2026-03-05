# Adding Notion API Token to Ecosystem Config

After reading the ecosystem-config skill, here's how to set up your Notion API token.

## Steps

1. Read SKILL.md at ~/Projects/claude-skills/productivity/ecosystem-config/SKILL.md

The skill explains that all ecosystem environment variables are managed in a central file: `~/scripts/ecosystem.env`

## Instructions

### 1. Edit the ecosystem.env file

```bash
# Open the central config file
nano ~/scripts/ecosystem.env
```

Add this line:
```
export NOTION_TOKEN="your-notion-integration-token-here"
```

The variable name is `NOTION_TOKEN` (used by treehouse-context-sync and drive-index-sync).

### 2. If starting fresh, copy from the example

```bash
cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env
```

The example file (`ecosystem.env.example`) has all variable names as a template with placeholder values.

### 3. Source it from your shell

Your `~/.zshrc` should contain:
```bash
source ~/scripts/ecosystem.env
```

If it's not there yet, add that line.

### 4. Reload your shell

```bash
source ~/.zshrc
```

## Important Notes

- Do NOT edit `~/.zshrc` directly to add individual API keys -- all ecosystem credentials go in `~/scripts/ecosystem.env`
- The `.env` file is not committed to git (it contains secrets)
- The `.env.example` file is safe to commit as a template
- You can verify your config by running: `python3 ~/scripts/ecosystem_status.py`
