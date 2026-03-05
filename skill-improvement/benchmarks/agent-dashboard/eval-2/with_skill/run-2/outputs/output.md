# Monitoring Active Agents

Read the agent-dashboard skill. Recognizing this as a request for the surveillance dashboard.

## Launch

The existing dashboard at ~/Projects/claude-skills/dev-tools/agent-dashboard/app:

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app && node server.js
```

```bash
open http://localhost:3847
```

## Dashboard Shows

The Agent Surveillance Dashboard at localhost:3847 provides:

- **Agent Roster**: Who's on each team, their roles, active/idle status
- **Live Messages**: Real-time inter-agent communication
- **Task Board**: Kanban view of all tasks across states
- **History**: Archived sessions for review

It watches ~/.claude/teams/ and ~/.claude/tasks/ for live updates. Any active Agent Teams will appear automatically.
