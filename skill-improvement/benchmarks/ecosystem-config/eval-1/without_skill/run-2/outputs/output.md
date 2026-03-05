# Setting Up Notion API Token

## Step 1: Get Your Token

Visit the Notion Developers page at https://www.notion.so/my-integrations and create an integration. Copy the token.

## Step 2: Configure the Environment Variable

Add it to your shell configuration:

```bash
# Open your shell profile
nano ~/.zshrc

# Add this line
export NOTION_API_TOKEN="secret_..."
```

Save and reload:
```bash
source ~/.zshrc
```

## Step 3: Connect to Your Workspace

In Notion, go to the page/database you want to access and share it with your integration.

## Alternative: Project-Level .env

If this is for a specific project:

```bash
# In your project root
echo "NOTION_API_TOKEN=secret_..." > .env
```

Use a library like `python-dotenv` to load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Verify

```bash
echo $NOTION_API_TOKEN
# Should print your token
```
