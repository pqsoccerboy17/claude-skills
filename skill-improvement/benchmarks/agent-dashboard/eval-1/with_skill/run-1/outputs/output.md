# Launching Agent Dashboard

Read the agent-dashboard SKILL.md first.

## Steps

Per the skill instructions:

1. Start the dashboard server:

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

2. Open in browser:

```bash
open http://localhost:3847
```

3. The Agent Dashboard is now running at http://localhost:3847. It will automatically detect any Agent Teams that start or are already running. You can watch agents work in real-time -- their messages, task progress, and status updates will all appear on the dashboard.

## What the Dashboard Shows

- **Agent Roster** -- who's on the team, their roles, active/idle status
- **Live Messages** -- inter-agent communication in real-time
- **Task Board** -- Kanban view of all tasks (Pending -> In Progress -> Completed)
- **History** -- archived sessions you can review after a team finishes

## Notes

- The server watches ~/.claude/teams/ and ~/.claude/tasks/ directories
- Leave the server running while agent teams work
- Historical sessions saved to SQLite in the History tab
- Auto-reconnects if connection drops
- To stop: Ctrl+C or kill the process on port 3847
