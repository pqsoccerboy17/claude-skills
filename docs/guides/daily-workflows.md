# Daily Workflows

Common tasks and how to accomplish them.

## Asset Tracking

### "What did I buy this month?"

```bash
cd ~/claude-skills/productivity/asset-manager/scripts
python3 gmail_scanner.py --days 30 --dry-run
```

### "Save my purchases and review them"

```bash
# 1. Scan and save
python3 gmail_scanner.py --days 30 --output purchases.json

# 2. See what needs review
python3 review_queue.py --list

# 3. Approve good items
python3 review_queue.py --approve <id>
```

### "Clear my review queue"

```bash
# See pending items
python3 review_queue.py --list

# Approve each one
python3 review_queue.py --approve abc123
python3 review_queue.py --approve def456

# Or reject with reason
python3 review_queue.py --reject xyz789 --reason "not a real purchase"

# Archive completed items
python3 review_queue.py --clear-approved
```

## System Maintenance

### "Is everything working?"

```bash
cd ~/claude-skills/productivity/ecosystem-status/scripts
python3 ecosystem_status.py
```

### "My Gmail auth expired"

```bash
rm ~/.config/treehouse/token.json
cd ~/claude-skills/productivity/asset-manager/scripts
python3 gmail_scanner.py --days 1 --dry-run
# Browser opens, re-authorize
```

### "Update to latest code"

```bash
cd ~/claude-skills
git pull origin main
```

## Asking Claude

Instead of running commands, you can ask:

- "Scan my Gmail for purchases from the last 30 days"
- "Show me what's in my review queue"
- "Approve all high-confidence items"
- "What's the status of my systems?"
