# Agent Dashboard

Read the agent-dashboard skill. Following its launch steps exactly.

## Launch

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

```bash
open http://localhost:3847
```

The Agent Dashboard is now running at http://localhost:3847. It automatically detects any Agent Teams that start or are already running. Watch agents work in real-time -- messages, task progress, and status updates appear on the dashboard.

## Dashboard Features

The dashboard watches `~/.claude/teams/` and `~/.claude/tasks/` directories and streams updates:

- Agent Roster: team members, roles, status
- Live Messages: inter-agent communication
- Task Board: Kanban view (Pending/In Progress/Completed)
- History: archived sessions in SQLite

## Important

- Leave server running during agent team work
- Empty state shown when no teams active
- Auto-reconnects on connection drop
- Stop with Ctrl+C
