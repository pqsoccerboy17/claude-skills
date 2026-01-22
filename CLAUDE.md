# Claude Skills Repository

Centralized repository of skills/prompts for Claude Code across multiple business contexts.

## Skill Categories

**Official Anthropic Skills:**
- `pdf` - PDF generation from markdown
- `xlsx` - Spreadsheet generation with LibreOffice recalc

**Custom Business Skills:**
- `notion-api` - Notion API operations (Code mode)
- `ecosystem-status` - Automation ecosystem health
- `gemini` - Gemini AI invocation wrapper

**Business Context Skills:**
- Treehouse LLC (company operations)
- YourCo Consulting (client engagement)
- Tap (product development)

## Authentication Patterns

**Notion API (Code mode only):**
- Uses API token: `NOTION_TOKEN` from `.env` or environment
- Works in Code mode (cloud sandbox with env vars)
- For Chat mode: Use `ecosystem-mcp-server` instead

**Ecosystem Status:**
- Requires: All automation repos in `~/dev/automation/`
- Checks: monarch-mcp, treehouse-sync, downloads-organizer, notion-rules
- Returns: Health status + attention items

## Deployment Differences

**Code Mode (Terminal CLI):**
- Has access to environment variables
- Can run subprocess commands
- notion-api skill works here

**Chat Mode (via MCP):**
- Sandboxed, no direct subprocess
- Use ecosystem-mcp-server for Notion operations
- Skills must be MCP-compatible

## Dependencies

**For xlsx skill:**
- LibreOffice installed (for `--recalc` flag)
- `soffice` binary must be in PATH

**For ecosystem-status:**
- All automation repos cloned in `~/dev/automation/`
- monarch-mcp-server installed and configured

See individual skill READMEs for business-specific setup and templates.
