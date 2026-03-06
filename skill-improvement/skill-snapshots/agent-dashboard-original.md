---
name: agent-dashboard
description: Launch the Agent Surveillance Dashboard — a real-time web UI that monitors Agent Teams activity, showing agent status, inter-agent messages, and task progress on a live Kanban board. Say "surveil agents", "agent dashboard", "monitor agents", or "watch agents" to launch.
---

# Agent Surveillance Dashboard

You are launching the Agent Surveillance Dashboard, a local web UI for monitoring Claude Code Agent Teams in real-time.

## What This Does

The dashboard watches the native `~/.claude/teams/` and `~/.claude/tasks/` directories that Agent Teams create automatically. It streams all activity to a browser UI on `localhost:3847`, showing:

- **Agent Roster** — who's on the team, their roles, active/idle status
- **Live Messages** — inter-agent communication in real-time
- **Task Board** — Kanban view of all tasks (Pending → In Progress → Completed)
- **History** — archived sessions you can review after a team finishes

## Launch Steps

1. Start the dashboard server:

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

2. Open the dashboard in the browser:

```bash
open http://localhost:3847
```

3. Tell the user: "The Agent Dashboard is now running at http://localhost:3847. It will automatically detect any Agent Teams that start or are already running. You can watch agents work in real-time — their messages, task progress, and status updates will all appear on the dashboard."

## Important Notes

- The server runs in the background — leave it running while agent teams work
- If no teams are active, the dashboard shows an empty state with instructions
- Historical sessions are saved to SQLite and viewable in the History tab
- The dashboard auto-reconnects if the connection drops
- To stop: Ctrl+C in the terminal running the server, or kill the process on port 3847
