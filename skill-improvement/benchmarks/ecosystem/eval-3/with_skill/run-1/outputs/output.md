Your ecosystem uses a central config file for all API credentials. Here's how to add your Notion token:

1. **Open the config file:**
   ```bash
   nano ~/scripts/ecosystem.env
   ```

2. **Add the Notion token variable:**
   ```
   NOTION_TOKEN="your-notion-integration-token-here"
   ```

   If you also need Drive Index Sync, you may want to add these at the same time:
   ```
   NOTION_DOCUMENT_INDEX_DB_ID="your-database-id"
   NOTION_PROPERTIES_DB_ID="your-properties-db-id"
   ```

3. **Make sure your shell sources it.** Check that `~/.zshrc` includes:
   ```bash
   source ~/scripts/ecosystem.env
   ```
   If that line isn't there, add it. Then reload:
   ```bash
   source ~/.zshrc
   ```

You can reference `~/scripts/ecosystem.env.example` for a template showing all available variables with descriptions.

The variable name to use is `NOTION_TOKEN` - this is used by treehouse-context-sync and drive-index-sync. Do not add the token directly to `~/.zshrc` - keep all ecosystem credentials in the central `ecosystem.env` file.
