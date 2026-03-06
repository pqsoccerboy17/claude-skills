The Notion API token goes in your central ecosystem configuration file at `~/scripts/ecosystem.env`. Here's what to do:

**Step 1:** Open the config file and add your token:

**Tool call: Read**
```
~/scripts/ecosystem.env
```

**Tool call: Edit** (adding the Notion token)
```
NOTION_TOKEN="your-notion-integration-token"
```

The variable you need is `NOTION_TOKEN`. This is used by treehouse-context-sync and drive-index-sync. If you don't have the file yet, copy the template first:

```bash
cp ~/scripts/ecosystem.env.example ~/scripts/ecosystem.env
```

**Step 2:** Verify your `~/.zshrc` sources the ecosystem config. It should contain this line:

```bash
source ~/scripts/ecosystem.env
```

**Step 3:** Reload your shell to pick up the changes:

```bash
source ~/.zshrc
```

All ecosystem credentials are managed through this single `ecosystem.env` file rather than adding individual exports to your shell profile. This keeps things organized and makes sure nothing gets committed to git accidentally.
