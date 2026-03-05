# Adding Notion API Token to Your Config

## Get the Token

1. Go to https://www.notion.so/my-integrations
2. Click "New Integration"
3. Name it and select your workspace
4. Copy the "Internal Integration Secret"

## Set the Environment Variable

Add it to your shell profile (`~/.zshrc`):

```bash
echo 'export NOTION_API_KEY="secret_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

Or create a dedicated environment file:

```bash
echo 'NOTION_API_KEY=secret_your_token_here' > ~/.notion.env
```

Then source it from `~/.zshrc`:
```bash
echo 'source ~/.notion.env' >> ~/.zshrc
```

## Using It

The token is now available as `$NOTION_API_KEY` in your terminal and any scripts you run.

## Security

- Don't commit tokens to git
- Use file permissions: `chmod 600 ~/.notion.env`
- Consider using macOS Keychain for sensitive tokens
