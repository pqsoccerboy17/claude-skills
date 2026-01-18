# Getting Started

## Prerequisites

- Python 3.9+
- Git
- Google account (for Gmail/Drive features)

## Installation

```bash
# Clone the repository
git clone https://github.com/pqsoccerboy17/claude-skills.git
cd claude-skills

# Install Python dependencies
pip3 install -r requirements.txt

# View docs locally (optional)
pip3 install mkdocs-material
mkdocs serve
```

## First-Time Setup

### 1. Google OAuth (for Gmail/Drive)

Already done! Your tokens are at:
- `~/.config/treehouse/credentials.json`
- `~/.config/treehouse/token.json`

### 2. Pushover (for notifications)

1. Create account at [pushover.net](https://pushover.net)
2. Get your User Key and create an Application
3. Add to environment or config file

### 3. Notion (optional)

1. Create integration at [notion.so/my-integrations](https://notion.so/my-integrations)
2. Share databases with integration
3. Add token to config

## Verify Setup

```bash
cd ~/claude-skills/productivity/asset-manager/scripts

# Test Gmail connection
python3 gmail_scanner.py --days 1 --dry-run

# Test review queue
python3 review_queue.py --stats
```

## Next Steps

- Read [Daily Workflows](daily-workflows.md) for common tasks
- Explore [Skills](../skills/index.md) to see what's available
