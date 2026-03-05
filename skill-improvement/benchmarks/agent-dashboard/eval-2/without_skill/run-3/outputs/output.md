# Show Agent Activity

## Investigation

```bash
ps aux | grep -i "agent\|claude\|node"
ls ~/.claude/ 2>/dev/null
```

I'll check what's running on your system related to agents.

## Findings

I searched for agent and Claude-related processes. Without a specific monitoring tool, I can only check:
- Process list for running agents
- File system for status/log files
- Network ports for running services

## Recommendation

For real-time agent monitoring, I'd suggest building a dashboard. Want me to create one? I'd need to know:
- What agent framework you're using
- Where agent state/status is stored
- Whether you want a web UI or terminal interface
