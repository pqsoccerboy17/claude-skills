# Agent Surveillance Dashboard

A real-time web UI for monitoring Claude Code Agent Teams. Watch agents collaborate, track inter-agent messages, and follow task progress on a live Kanban board -- all from your browser.

## Features

- **Real-time WebSocket streaming** -- instant updates as agents work
- **Agent Roster** -- see who's on the team with active/idle status indicators
- **Live Message Feed** -- inter-agent communication displayed as it happens
- **Kanban Task Board** -- tasks flow through Pending, In Progress, and Completed columns
- **Session History** -- archived sessions stored in SQLite, viewable in the History tab
- **Heritage green theme** -- clean, dark interface designed for extended monitoring
- **Zero-config file watching** -- automatically detects `~/.claude/teams/` and `~/.claude/tasks/` changes via chokidar

## Tech Stack

- **Server:** Express, ws (WebSocket), chokidar (file watching), better-sqlite3 (history)
- **Frontend:** React 18 (CDN), Babel standalone (JSX transform in browser)
- **No build step** -- runs directly with Node.js

## Quick Start

```bash
cd ~/Projects/claude-skills/dev-tools/agent-dashboard/app
npm install
node server.js
# Open http://localhost:3847
```

Or just say **"agent dashboard"** in Claude Code.

## Architecture

```
File System (~/.claude/)  -->  chokidar  -->  Express Server  -->  WebSocket  -->  React UI
                                                    |
                                              SQLite (history)
```

1. chokidar watches `~/.claude/teams/` and `~/.claude/tasks/` for file changes
2. On change, the server reads the current state and diffs against the last broadcast
3. If state changed, it pushes a `state_update` message over WebSocket to all connected clients
4. A 5-second polling fallback ensures nothing is missed
5. When a team session ends (config.json removed), the session is archived to SQLite

## Project Structure

```
agent-dashboard/
├── SKILL.md                  # Claude Code skill definition
├── README.md                 # This file
└── app/
    ├── package.json          # Node.js dependencies
    ├── server.js             # Express + WebSocket + chokidar + SQLite server
    ├── db/
    │   └── schema.sql        # SQLite schema (sessions, agents, tasks, messages)
    └── public/
        ├── index.html        # App shell (loads React + Babel from CDN)
        ├── style.css         # Heritage green theme styles
        └── app.js            # React components (JSX, transformed by Babel)
```

## How It Works

The dashboard reads the same files that Claude Code's Agent Teams system writes to:

- **`~/.claude/teams/{team-name}/config.json`** -- team membership and configuration
- **`~/.claude/tasks/{team-name}/*.json`** -- individual task files with status, owner, and dependencies

The server parses these JSON files on every detected change and pushes the full state to the browser. The React frontend renders three main views:

- **Agent Roster** (sidebar) -- avatar, name, role, and status for each team member
- **Messages Panel** -- synthesized activity events from team/task changes
- **Task Board** -- Kanban columns that update in real-time as tasks progress

The History tab fetches archived sessions from the SQLite database via REST API.

## Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Port | `3847` | Hardcoded in `server.js` |
| Teams directory | `~/.claude/teams/` | Created automatically if missing |
| Tasks directory | `~/.claude/tasks/` | Created automatically if missing |
| Database | `app/db/dashboard.db` | SQLite, created on first run |
| Poll interval | 5 seconds | Fallback in case chokidar misses a change |

## Troubleshooting

**Port 3847 already in use**
Kill the existing process: `lsof -ti:3847 | xargs kill` then restart.

**No teams showing up**
The dashboard watches `~/.claude/teams/`. Make sure you have an active Agent Teams session running. If no teams are active, the dashboard displays an empty state.

**SQLite errors on startup**
Delete the database file and restart -- it will be recreated from the schema:
```bash
rm app/db/dashboard.db
node server.js
```

**WebSocket disconnects**
The client auto-reconnects with exponential backoff (1s, 2s, 4s... up to 30s). The connection status indicator in the header shows the current state.

**Changes not appearing**
chokidar uses `awaitWriteFinish` with a 300ms stability threshold. Very rapid file changes may be batched. The 5-second polling fallback will catch anything missed.
