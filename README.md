# Claude Skills Repository

A curated collection of Claude Code skills for business operations across **Treehouse LLC** (real estate), **[YourCo] Consulting**, and **Tap** (AI SaaS startup).

## Quick Setup

```bash
# Clone the repository
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/claude-skills

# Run the setup script
cd ~/claude-skills
./setup.sh
```

## Skills Overview

| Category | Skill | Purpose |
|----------|-------|---------|
| Document Processing | [pdf](document-processing/pdf/) | Statement processing, form filling, PDF manipulation |
| Document Processing | [xlsx](document-processing/xlsx/) | Financial spreadsheet creation and analysis |
| Data Analysis | [csv-data-summarizer](data-analysis/csv-data-summarizer/) | Quick analysis of exported financial data |
| Productivity | [file-organizer](productivity/file-organizer/) | Financial document organization, photo pipelines |
| Productivity | [internal-comms](productivity/internal-comms/) | Client/tenant/investor communication templates |
| Productivity | [ecosystem](productivity/ecosystem/) | Automation status, config, and notifications |
| Dev Tools | [mcp-builder](dev-tools/mcp-builder/) | Build custom MCP servers for Claude integrations |
| Dev Tools | [factory-pm](dev-tools/factory-pm/) | Spec-before-code PM agent with approval gate |
| Dev Tools | [agent-dashboard](dev-tools/agent-dashboard/) | Monitor and manage Claude agent sessions |
| Research | [last30days](research/last30days/) | Real-time social listening across Reddit and X/Twitter |

## Directory Structure

```
claude-skills/
├── document-processing/
│   ├── pdf/                    # Anthropic official PDF skill
│   │   ├── SKILL.md
│   │   ├── FORMS.md
│   │   ├── REFERENCE.md
│   │   └── scripts/
│   └── xlsx/                   # Anthropic official Excel skill
│       ├── SKILL.md
│       └── recalc.py
├── data-analysis/
│   └── csv-data-summarizer/    # Financial data analysis
│       ├── SKILL.md
│       └── scripts/
├── productivity/
│   ├── file-organizer/         # Document organization
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── internal-comms/         # Communication templates
│   │   ├── SKILL.md
│   │   └── references/
│   └── ecosystem/              # Status, config, and notifications
│       └── SKILL.md
├── dev-tools/
│   ├── mcp-builder/            # MCP server development
│   │   ├── SKILL.md
│   │   └── references/
│   └── factory-pm/             # Spec-before-code PM agent
│       ├── SKILL.md
│       └── commands/
│           └── spec.md
├── research/
│   └── last30days/             # Social listening (Reddit & X/Twitter)
│       └── SKILL.md
├── tests/                      # Smoke tests
├── CLAUDE.md                   # Project instructions for Claude
├── GITHUB_SETUP.md             # GitHub repository setup guide
├── setup.sh                    # Installation script
└── README.md
```

## Skill Details

### Document Processing

#### PDF (`document-processing/pdf/`)
**Source:** Anthropic official skill

Comprehensive PDF manipulation for:
- Extracting text and tables from bank statements
- Filling PDF forms (tax forms, lease agreements)
- Merging/splitting documents
- Processing scanned documents with OCR

**Key files:**
- `SKILL.md` - Main instructions
- `FORMS.md` - PDF form filling guide
- `REFERENCE.md` - Advanced features
- `scripts/` - Python utilities for form processing

#### XLSX (`document-processing/xlsx/`)
**Source:** Anthropic official skill

Excel spreadsheet operations for:
- Creating financial models with proper formatting
- Analyzing property revenue data
- Generating reports with formulas
- Treehouse LLC rent rolls and expense tracking

**Key files:**
- `SKILL.md` - Instructions with financial modeling standards
- `recalc.py` - Formula recalculation via LibreOffice

### Data Analysis

#### CSV Data Summarizer (`data-analysis/csv-data-summarizer/`)
**Source:** Custom skill based on coffeefuelbump/csv-data-summarizer-claude-skill

Quick analysis of exported data:
- Transaction summaries
- Property revenue analysis
- Consulting time tracking
- SaaS metrics (Tap)

**Usage:**
```bash
python scripts/summarize.py transactions.csv --type financial
```

### Productivity

#### File Organizer (`productivity/file-organizer/`)
**Source:** Custom skill based on ComposioHQ/awesome-claude-skills

Intelligent file organization:
- Bank statement organization by year/month
- Property photo pipelines
- Document categorization by type
- Consulting project file structures

**Business-specific patterns included for:**
- Treehouse LLC property management
- Consulting client organization
- Tap product documentation

**Usage:**
```bash
python scripts/organize.py ~/Downloads ~/Organized --by-type
```

#### Internal Comms (`productivity/internal-comms/`)
**Source:** Custom skill inspired by Anthropic patterns

Professional communication templates:
- Tenant communications (lease renewals, maintenance notices)
- Consulting client updates (status reports, invoices)
- Investor updates (monthly/quarterly reports for Tap)
- Meeting summaries

**Reference files:**
- `references/real-estate-templates.md` - Treehouse LLC
- `references/consulting-templates.md` - [YourCo] Consulting
- `references/startup-templates.md` - Tap investor relations

#### Ecosystem (`productivity/ecosystem/`)
**Source:** Custom skill (merged from ecosystem-status, ecosystem-config, notifications)

Unified automation infrastructure management:
- Status monitoring of all automation systems
- Central credential configuration via ~/scripts/ecosystem.env
- Push notifications via Pushover and macOS fallback

### Dev Tools

#### MCP Builder (`dev-tools/mcp-builder/`)
**Source:** Custom skill for MCP development

Build custom MCP servers for:
- Property management integrations
- Client management tools
- SaaS metrics dashboards
- API integrations (Zillow, Readwise, etc.)

**Includes:**
- TypeScript and Python templates
- Authentication patterns
- Testing guidance

#### Factory PM (`dev-tools/factory-pm/`)
**Source:** Custom skill for spec-before-code discipline

Product manager agent that plans before coding:
- Reads project context (CLAUDE.md, deps, structure)
- Asks 3-5 clarifying questions before planning
- Writes spec to `specs/<feature>.md` in the project directory
- Hard gate: waits for explicit "Approved" before any implementation
- Pairs with `/spec` slash command for quick invocation

**Usage:**
```
/spec add user authentication
/spec build payment integration
```

### Research

#### Last 30 Days (`research/last30days/`)
**Source:** Custom social listening skill

Real-time social listening across Reddit, X/Twitter, and the web:
- Search any topic from the last 30 days
- Structured output with sentiment, key voices, and trending themes
- Confidence ratings on all findings
- Conflicting viewpoint detection

**Usage:**
```
/last30days "AI consulting trends"
```

**Requires:** brave-search MCP server (configured globally)

## Configuration

### Claude Code

Skills are configured via `~/.claude/settings.json`:

```json
{
  "skills": {
    "paths": ["~/claude-skills"]
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "skills": {
    "paths": ["/Users/YOUR_USERNAME/claude-skills"]
  }
}
```

## Dependencies

Some skills require Python packages:

```bash
# PDF processing
pip install pypdf pdfplumber reportlab Pillow

# Excel processing
pip install openpyxl pandas

# CSV analysis
pip install pandas
```

LibreOffice is required for Excel formula recalculation:
```bash
brew install --cask libreoffice
```

## Syncing Across Machines

This repository is designed to be pulled on any machine:

```bash
# On Mac Mini
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/claude-skills

# On MacBook (same command)
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/claude-skills

# Pull updates
cd ~/claude-skills && git pull
```

## Customization

### Adding Business-Specific Data

1. **Treehouse LLC properties:** Add property addresses to file-organizer templates
2. **Client list:** Add client names to internal-comms templates
3. **API keys:** Add to environment variables for MCP servers

### Creating New Skills

Use the skill-creator pattern:
1. Create folder with `SKILL.md`
2. Add frontmatter with `name` and `description`
3. Add scripts/references as needed
4. Test with Claude Code

## Next Steps

### Planned MCP Integrations

| Integration | Purpose | Setup |
|-------------|---------|-------|
| Zillow | Real estate market data | Free RapidAPI key |
| Readwise | Knowledge management | Existing account |

> **Note:** Notion integration is available via the Notion MCP server (`mcp__claude_ai_Notion__*`).

## Contributing

To add or modify skills:
1. Create a branch
2. Add/modify skill files
3. Test with Claude Code
4. Push and create PR

## License

- Anthropic skills (pdf, xlsx): Proprietary - see individual LICENSE.txt files
- Custom skills: MIT License
