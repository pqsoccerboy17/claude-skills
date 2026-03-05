# What Are My Agents Doing?

Read the agent-dashboard skill. Launching the surveillance dashboard.

## Steps

Using the existing dashboard at ~/Projects/claude-skills/dev-tools/agent-dashboard/app:

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

```bash
open http://localhost:3847
```

## What the Dashboard Shows

At localhost:3847 you'll see:

- **Agent Roster**: Team members, roles, active/idle status
- **Live Messages**: Inter-agent communication in real-time
- **Task Board**: Kanban board (Pending -> In Progress -> Completed)
- **History**: Past sessions stored in SQLite

The server watches ~/.claude/teams/ and ~/.claude/tasks/ directories for changes. Any currently running Agent Teams will appear live on the dashboard.
