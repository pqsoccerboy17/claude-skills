const express = require('express');
const http = require('http');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { WebSocketServer } = require('ws');
const chokidar = require('chokidar');
const Database = require('better-sqlite3');

const PORT = 3847;
const TEAMS_DIR = path.join(os.homedir(), '.claude', 'teams');
const TASKS_DIR = path.join(os.homedir(), '.claude', 'tasks');
const DB_PATH = path.join(__dirname, 'db', 'dashboard.db');
const SCHEMA_PATH = path.join(__dirname, 'db', 'schema.sql');
const PUBLIC_DIR = path.join(__dirname, 'public');

// ---------------------------------------------------------------------------
// Ensure watched directories exist
// ---------------------------------------------------------------------------
for (const dir of [TEAMS_DIR, TASKS_DIR]) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// ---------------------------------------------------------------------------
// SQLite initialisation
// ---------------------------------------------------------------------------
const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

const schema = fs.readFileSync(SCHEMA_PATH, 'utf8');
db.exec(schema);

// ---------------------------------------------------------------------------
// Express + HTTP server
// ---------------------------------------------------------------------------
const app = express();
const server = http.createServer(app);

app.use(express.static(PUBLIC_DIR));

// ---------------------------------------------------------------------------
// WebSocket server
// ---------------------------------------------------------------------------
const wss = new WebSocketServer({ server });

function broadcast(data) {
  const payload = JSON.stringify(data);
  for (const client of wss.clients) {
    if (client.readyState === 1) { // WebSocket.OPEN
      client.send(payload);
    }
  }
}

wss.on('connection', (ws) => {
  const state = readFullState();
  ws.send(JSON.stringify({ type: 'state_update', data: state }));
});

// ---------------------------------------------------------------------------
// State reading helpers
// ---------------------------------------------------------------------------
let lastStateJson = '';

function readFullState() {
  const teams = readTeams();
  const tasks = readTasks();
  const messages = buildMessages(teams, tasks);
  return { teams, tasks, messages };
}

function readTeams() {
  const teams = [];
  try {
    if (!fs.existsSync(TEAMS_DIR)) return teams;
    const entries = fs.readdirSync(TEAMS_DIR, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const configPath = path.join(TEAMS_DIR, entry.name, 'config.json');
      try {
        const raw = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(raw);
        teams.push({
          name: entry.name,
          members: config.members || [],
          status: 'active',
        });
      } catch {
        // config.json missing or mid-write — skip
      }
    }
  } catch {
    // directory may not exist yet
  }
  return teams;
}

function readTasks() {
  const allTasks = [];
  try {
    if (!fs.existsSync(TASKS_DIR)) return allTasks;
    const teamDirs = fs.readdirSync(TASKS_DIR, { withFileTypes: true });
    for (const teamDir of teamDirs) {
      if (!teamDir.isDirectory()) continue;
      const teamTaskDir = path.join(TASKS_DIR, teamDir.name);
      try {
        const files = fs.readdirSync(teamTaskDir);
        for (const file of files) {
          if (!file.endsWith('.json')) continue;
          try {
            const raw = fs.readFileSync(path.join(teamTaskDir, file), 'utf8');
            const task = JSON.parse(raw);
            allTasks.push({
              team: teamDir.name,
              id: task.id || file.replace('.json', ''),
              subject: task.subject || '',
              description: task.description || '',
              status: task.status || 'pending',
              owner: task.owner || null,
              blocks: task.blocks || [],
              blockedBy: task.blockedBy || [],
            });
          } catch {
            // file mid-write or invalid JSON — skip
          }
        }
      } catch {
        // directory read error — skip
      }
    }
  } catch {
    // tasks dir may not exist
  }
  return allTasks;
}

function buildMessages(teams, tasks) {
  // Derive a lightweight messages list from current state.
  // Real message interception would require reading conversation logs;
  // for now we synthesise activity events from teams/tasks changes.
  const messages = [];
  const now = new Date().toISOString();

  for (const team of teams) {
    for (const member of team.members) {
      messages.push({
        sender: 'system',
        recipient: member.name || member.agentId,
        content: `Agent ${member.name || member.agentId} active in team ${team.name}`,
        type: 'status',
        timestamp: now,
      });
    }
  }

  for (const task of tasks) {
    if (task.owner) {
      messages.push({
        sender: task.owner,
        recipient: 'system',
        content: `Task "${task.subject}" — ${task.status}`,
        type: 'task_update',
        timestamp: now,
      });
    }
  }

  return messages;
}

// ---------------------------------------------------------------------------
// Broadcast state if changed
// ---------------------------------------------------------------------------
function broadcastIfChanged() {
  const state = readFullState();
  const json = JSON.stringify(state);
  if (json !== lastStateJson) {
    lastStateJson = json;
    broadcast({ type: 'state_update', data: state });
  }
}

// ---------------------------------------------------------------------------
// chokidar file watchers
// ---------------------------------------------------------------------------
const teamsWatcher = chokidar.watch(TEAMS_DIR, {
  ignoreInitial: true,
  depth: 2,
  awaitWriteFinish: { stabilityThreshold: 300, pollInterval: 100 },
});

const tasksWatcher = chokidar.watch(TASKS_DIR, {
  ignoreInitial: true,
  depth: 2,
  awaitWriteFinish: { stabilityThreshold: 300, pollInterval: 100 },
});

teamsWatcher.on('all', (event, filePath) => {
  console.log(`[teams] ${event}: ${filePath}`);

  // If a config.json was removed, archive that team session
  if (event === 'unlink' && filePath.endsWith('config.json')) {
    archiveSession(filePath);
  }

  broadcastIfChanged();
});

tasksWatcher.on('all', (event, filePath) => {
  console.log(`[tasks] ${event}: ${filePath}`);
  broadcastIfChanged();
});

// ---------------------------------------------------------------------------
// Session archiving (team removed -> save to SQLite)
// ---------------------------------------------------------------------------
function archiveSession(removedConfigPath) {
  // Derive team name from path: .../teams/{name}/config.json
  const teamName = path.basename(path.dirname(removedConfigPath));
  const now = new Date().toISOString();

  try {
    // Read current tasks for that team before they disappear
    const tasks = readTasks().filter((t) => t.team === teamName);

    const insertSession = db.prepare(
      `INSERT INTO sessions (team_name, start_time, end_time, agent_count, message_count, task_count, status)
       VALUES (?, ?, ?, ?, ?, ?, 'archived')`
    );

    const result = insertSession.run(teamName, now, now, 0, 0, tasks.length);
    const sessionId = result.lastInsertRowid;

    const insertTask = db.prepare(
      `INSERT INTO tasks (session_id, task_id, subject, description, status, owner, blocks, blocked_by, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    );

    const insertTaskMany = db.transaction((taskList) => {
      for (const t of taskList) {
        insertTask.run(
          sessionId,
          t.id,
          t.subject,
          t.description,
          t.status,
          t.owner,
          JSON.stringify(t.blocks),
          JSON.stringify(t.blockedBy),
          now,
          now
        );
      }
    });

    insertTaskMany(tasks);
    console.log(`[archive] Archived session for team "${teamName}" (id=${sessionId}, tasks=${tasks.length})`);
  } catch (err) {
    console.error(`[archive] Failed to archive team "${teamName}":`, err.message);
  }
}

// ---------------------------------------------------------------------------
// REST API
// ---------------------------------------------------------------------------
app.get('/api/state', (_req, res) => {
  try {
    const state = readFullState();
    res.json(state);
  } catch (err) {
    console.error('[api] /api/state error:', err.message);
    res.status(500).json({ error: 'Failed to read state' });
  }
});

app.get('/api/history', (_req, res) => {
  try {
    const sessions = db.prepare('SELECT * FROM sessions ORDER BY id DESC').all();
    res.json(sessions);
  } catch (err) {
    console.error('[api] /api/history error:', err.message);
    res.status(500).json({ error: 'Failed to read history' });
  }
});

app.get('/api/history/:id', (req, res) => {
  try {
    const sessionId = parseInt(req.params.id, 10);
    if (isNaN(sessionId)) {
      return res.status(400).json({ error: 'Invalid session id' });
    }

    const session = db.prepare('SELECT * FROM sessions WHERE id = ?').get(sessionId);
    if (!session) {
      return res.status(404).json({ error: 'Session not found' });
    }

    const agents = db.prepare('SELECT * FROM agents WHERE session_id = ?').all(sessionId);
    const tasks = db.prepare('SELECT * FROM tasks WHERE session_id = ?').all(sessionId);
    const messages = db.prepare('SELECT * FROM messages WHERE session_id = ?').all(sessionId);

    res.json({ session, agents, tasks, messages });
  } catch (err) {
    console.error(`[api] /api/history/${req.params.id} error:`, err.message);
    res.status(500).json({ error: 'Failed to read session' });
  }
});

// ---------------------------------------------------------------------------
// 5-second polling fallback
// ---------------------------------------------------------------------------
const pollInterval = setInterval(() => {
  broadcastIfChanged();
}, 5000);

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------
server.listen(PORT, () => {
  console.log(`\n  Agent Surveillance Dashboard`);
  console.log(`  ----------------------------`);
  console.log(`  Server:     http://localhost:${PORT}`);
  console.log(`  WebSocket:  ws://localhost:${PORT}`);
  console.log(`  Database:   ${DB_PATH}`);
  console.log(`  Watching:`);
  console.log(`    Teams:    ${TEAMS_DIR}`);
  console.log(`    Tasks:    ${TASKS_DIR}`);
  console.log(`  ----------------------------\n`);
});

// ---------------------------------------------------------------------------
// Graceful shutdown
// ---------------------------------------------------------------------------
function shutdown(signal) {
  console.log(`\n[shutdown] Received ${signal}, cleaning up...`);

  clearInterval(pollInterval);

  teamsWatcher.close().catch(() => {});
  tasksWatcher.close().catch(() => {});

  wss.close(() => {
    console.log('[shutdown] WebSocket server closed');
  });

  server.close(() => {
    console.log('[shutdown] HTTP server closed');
  });

  try {
    db.close();
    console.log('[shutdown] Database closed');
  } catch {
    // already closed
  }

  setTimeout(() => {
    process.exit(0);
  }, 1000);
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
