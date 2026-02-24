# Claude Skills Repository

A curated collection of Claude Code skills organized in 6 categories.

## Repo Structure

```
claude-skills/
├── document-processing/   # Anthropic official skills (pdf, xlsx)
├── data-analysis/         # csv-data-summarizer
├── productivity/          # file-organizer, internal-comms, notion-api,
│                          # ecosystem-status, notifications, ecosystem-config
├── ai-apis/               # gemini
├── dev-tools/             # mcp-builder, factory-pm
├── research/              # cowork-ecosystem-playbook, intelligence reports
├── tests/                 # Smoke tests (pytest)
└── setup.sh               # Installation and symlink setup
```

## Skill Conventions

- Every skill lives in its own folder with a `SKILL.md` file
- `SKILL.md` uses YAML frontmatter: `name` (required), `description` (required), `license` (optional)
- Optional subdirectories: `scripts/`, `references/`, `commands/`
- Scripting is Python-first; no shell scripts beyond `setup.sh`

## Path Convention

- Repo clone target: `~/claude-skills`
- Scripts that also need to exist in `~/scripts/` are symlinked by `setup.sh` (not copied)
- Do not hardcode `~/Documents/claude-skills` — that path is deprecated

## Licensing

- Anthropic skills (`pdf`, `xlsx`): Proprietary — see individual `LICENSE.txt` files
- All custom skills: MIT License

## Working in This Repo

- Run `pytest tests/` to verify nothing is broken
- After adding a new skill, update `setup.sh` skills list and `README.md` directory tree
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
