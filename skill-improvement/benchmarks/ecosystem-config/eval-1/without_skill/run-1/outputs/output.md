# Adding Notion API Token

You want to add your Notion API token to your ecosystem configuration. Here's how.

## Getting Your Notion API Token

1. Go to https://www.notion.so/my-integrations
2. Create a new integration (or select an existing one)
3. Copy the Internal Integration Token

## Adding It to Your Environment

The most common approach is to add it to your shell profile:

```bash
# Add to ~/.zshrc
echo 'export NOTION_API_TOKEN="your-token-here"' >> ~/.zshrc
source ~/.zshrc
```

Or if you prefer a `.env` file approach:

```bash
# Create a .env file in your project
echo 'NOTION_API_TOKEN=your-token-here' >> .env
```

Then load it with a tool like `dotenv` or source it manually.

## Verifying

```bash
echo $NOTION_API_TOKEN
```

## Security Tips

- Never commit API tokens to version control
- Consider using a keychain or secrets manager for production
- Add `.env` to your `.gitignore`
