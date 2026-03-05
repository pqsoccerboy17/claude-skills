# Show Me What My Agents Are Doing

Read the agent-dashboard skill. This is a request for the Agent Surveillance Dashboard.

## Launching the Dashboard

Per the skill, the existing dashboard is at ~/Projects/claude-skills/dev-tools/agent-dashboard/app:

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

```bash
open http://localhost:3847
```

## What You'll See

The dashboard at localhost:3847 shows:

- **Agent Roster** -- all team members, their roles, and whether they're active or idle
- **Live Messages** -- real-time inter-agent communication stream
- **Task Board** -- Kanban-style board showing tasks as Pending, In Progress, or Completed
- **History** -- past agent team sessions saved in SQLite

The dashboard watches ~/.claude/teams/ and ~/.claude/tasks/ directories and streams updates automatically. If agent teams are currently running, you'll see their activity immediately.
