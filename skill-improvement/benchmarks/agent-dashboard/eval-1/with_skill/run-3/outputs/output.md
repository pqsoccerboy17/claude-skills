# Launch Agent Dashboard

Read SKILL.md for the agent-dashboard skill.

## Starting the Server

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

## Open Dashboard

```bash
open http://localhost:3847
```

The Agent Dashboard is running at localhost:3847. It will automatically detect Agent Teams and show their activity in real-time.

## What It Shows

Per the skill, the dashboard monitors ~/.claude/teams/ and ~/.claude/tasks/ directories:

- **Agent Roster** -- team members and their status (active/idle)
- **Live Messages** -- real-time inter-agent communication
- **Task Board** -- Kanban board of tasks across states
- **History** -- past sessions stored in SQLite

The server runs in the background. Leave it running while agents work. Stop with Ctrl+C.
