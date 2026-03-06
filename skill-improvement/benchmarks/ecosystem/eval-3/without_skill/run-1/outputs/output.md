To set up your Notion API token, you'll want to add it as an environment variable. Here's how:

**Option 1: Add to your shell profile**

Open your `~/.zshrc` and add:

```bash
export NOTION_API_TOKEN="your-notion-token-here"
```

Then reload your shell:
```bash
source ~/.zshrc
```

**Option 2: Create a .env file for your project**

If this is for a specific project, create a `.env` file in the project root:

```
NOTION_API_TOKEN=your-notion-token-here
```

Then load it in your scripts using `python-dotenv` or `source .env` in shell scripts.

**Getting the token:**
1. Go to https://www.notion.so/my-integrations
2. Create a new integration (or use an existing one)
3. Copy the "Internal Integration Token"
4. Make sure to share the relevant Notion pages/databases with your integration

Which approach would you prefer? The shell profile method makes the token available globally, while the .env approach is more project-specific.
