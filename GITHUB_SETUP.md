# GitHub Setup Instructions

Since the sandbox environment can't directly push to GitHub, follow these steps on your Mac:

## Step 1: Create the GitHub Repository

```bash
# Option A: Using GitHub CLI (recommended)
gh repo create claude-skills --public --description "Claude Code skills for business operations"

# Option B: Create manually at https://github.com/new
#   - Repository name: claude-skills
#   - Description: Claude Code skills for business operations
#   - Public repository
#   - Don't initialize with README (we have one)
```

## Step 2: Initialize and Push

```bash
# Navigate to the skills directory
cd ~/claude-skills

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Claude skills for Treehouse LLC, Consulting, and Tap

Skills included:
- pdf: Anthropic official PDF processing
- xlsx: Anthropic official Excel manipulation
- file-organizer: Document organization
- csv-data-summarizer: Financial data analysis
- internal-comms: Communication templates
- mcp-builder: MCP server development"

# Add remote
git remote add origin https://github.com/pqsoccerboy17/claude-skills.git

# Push to GitHub
git push -u origin main
```

## Step 3: Run Setup

```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

## Step 4: Verify in Claude Code

1. Restart Claude Code
2. Try: "Help me organize my Downloads folder using the file-organizer skill"
3. Or: "Draft a tenant lease renewal notice using internal-comms"

## Syncing to Other Machines

On your Mac Mini or any other machine:

```bash
# Clone the repository
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/claude-skills

# Run setup
cd ~/claude-skills
./setup.sh
```

## Updating Skills

```bash
# Pull latest changes
cd ~/claude-skills
git pull

# Or after making local changes
git add .
git commit -m "Description of changes"
git push
```
