# Skills Overview

Skills are automation capabilities that Claude can execute on your behalf. Each skill is a self-contained Python module with a CLI interface.

## Available Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| Asset Manager | `productivity/asset-manager/` | Track purchases, manuals, warranties |
| Notifications | `productivity/notifications/` | Send alerts via Pushover |
| Ecosystem Status | `productivity/ecosystem-status/` | Monitor system health |
| PDF Tools | `document-processing/pdf/` | Fill forms, extract data |
| CSV Summarizer | `data-analysis/csv-data-summarizer/` | Analyze spreadsheet data |

## How Skills Work

1. **AI-Agnostic**: Every skill works via CLI without requiring AI
2. **Modular**: Skills can be composed into pipelines
3. **Documented**: Each has `--help` and README
4. **Tested**: Integration tests verify functionality

## Running a Skill

```bash
# Direct CLI usage
python3 skill_name.py --help

# Or ask Claude
"Scan my Gmail for purchases from the last 30 days"
```
