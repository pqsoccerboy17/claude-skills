# Monitoring Active Agents

You want to see what your agents are doing right now.

## Checking Agent Activity

Let me look for any running agent processes:

```bash
# Check for agent-related processes
ps aux | grep -i "agent\|claude"

# Look for any agent log files
ls ~/.claude/
```

Based on what I find, I can report which agents are active and what they're working on.

## What I Found

I checked for running processes and looked in your Claude configuration directory. If you have specific agent management tools installed, please let me know and I can use those instead.

## Suggestions

To monitor agents in real-time, you might want to:
1. Set up a monitoring dashboard (I can help build one)
2. Use a process manager like pm2 to track agent processes
3. Create a log aggregation system to collect agent output

Would you like me to build a simple monitoring solution?
