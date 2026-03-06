To add your Notion API token to the ecosystem, you'll edit the central config file.

**Tool call: Read**
```
~/scripts/ecosystem.env
```

I can see the file exists. I'll add the Notion token for you. The correct variable name is `NOTION_TOKEN`:

**Tool call: Edit** (adding to ~/scripts/ecosystem.env)
```
NOTION_TOKEN="paste-your-notion-integration-token-here"
```

There are also related Notion variables you might need depending on which tools you use:
- `NOTION_DOCUMENT_INDEX_DB_ID` - needed for drive-index-sync
- `NOTION_PROPERTIES_DB_ID` - needed for drive-index-sync

You can see all available variables in the template file: `~/scripts/ecosystem.env.example`

After editing, reload your shell so the changes take effect:
```bash
source ~/.zshrc
```

This works because `~/.zshrc` sources `~/scripts/ecosystem.env` on startup. If that source line is not in your `.zshrc` yet, add it:
```bash
echo 'source ~/scripts/ecosystem.env' >> ~/.zshrc
```

Keep all credentials in `ecosystem.env` - do not add them directly to `.zshrc`.
