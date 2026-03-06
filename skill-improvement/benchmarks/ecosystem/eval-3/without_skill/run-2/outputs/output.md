To add your Notion API token to your environment, the simplest approach is to add it to your shell configuration.

Add this line to your `~/.zshrc`:

```bash
export NOTION_TOKEN="ntn_your_token_here"
```

Then reload:
```bash
source ~/.zshrc
```

You can verify it's set:
```bash
echo $NOTION_TOKEN
```

**Where to get the token:**
- Visit https://www.notion.so/my-integrations
- Create an integration or select an existing one
- Copy the Internal Integration Secret
- Don't forget to connect the integration to the pages you want to access

**Security note:** If you're committing dotfiles to git, make sure your `.zshrc` with the token is in `.gitignore`, or use a separate file that's not tracked.

Would you like me to add this to your `~/.zshrc` now?
