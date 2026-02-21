CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT,
  agent_count INTEGER DEFAULT 0,
  message_count INTEGER DEFAULT 0,
  task_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS agents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES sessions(id),
  name TEXT NOT NULL,
  type TEXT,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES sessions(id),
  task_id TEXT,
  subject TEXT,
  description TEXT,
  status TEXT DEFAULT 'pending',
  owner TEXT,
  blocks TEXT,
  blocked_by TEXT,
  created_at TEXT,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES sessions(id),
  sender TEXT,
  recipient TEXT,
  content TEXT,
  type TEXT,
  timestamp TEXT NOT NULL
);
