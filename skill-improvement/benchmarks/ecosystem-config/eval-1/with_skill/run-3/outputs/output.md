# Adding Notion API Token to Ecosystem Config

Read the ecosystem-config SKILL.md first.

## The Central Config File

Per the skill, all ecosystem automation credentials live in `~/scripts/ecosystem.env`. This file is sourced from your `~/.zshrc`.

## Steps to Add Notion Token

1. If you haven't created the config file yet:
```bash
cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env
```

2. Edit `~/scripts/ecosystem.env` and add:
```
export NOTION_TOKEN="your-notion-integration-token"
```

The ecosystem-config skill lists `NOTION_TOKEN` as the variable name, used by treehouse-context-sync and drive-index-sync.

3. Ensure `~/.zshrc` sources the file:
```bash
# This line should be in ~/.zshrc:
source ~/scripts/ecosystem.env
```

4. Reload your shell:
```bash
source ~/.zshrc
```

5. Verify it's set:
```bash
echo $NOTION_TOKEN
```

## Notes

- Do not add individual API keys directly to `~/.zshrc` -- use the centralized `ecosystem.env` file
- The `ecosystem.env.example` template shows all supported variables
- The actual `ecosystem.env` is gitignored for security
