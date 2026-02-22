const { useState, useEffect, useRef, useCallback } = React;

// ── Helpers ────────────────────────────────────────

function formatTime(iso) {
  if (!iso) return '';
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 5) return 'just now';
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function getInitials(name) {
  if (!name) return '?';
  return name.split(/[-_ ]+/).map(w => w[0]).filter(Boolean).slice(0, 2).join('').toUpperCase();
}

const AGENT_COLORS = [
  '#5cb88a', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16'
];

function getAgentColor(name) {
  if (!name) return AGENT_COLORS[0];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = ((hash << 5) - hash) + name.charCodeAt(i);
    hash |= 0;
  }
  return AGENT_COLORS[Math.abs(hash) % AGENT_COLORS.length];
}

/**
 * Normalize raw state from either REST or WebSocket into the shape
 * the UI expects: teams and tasks as keyed objects, messages as array.
 *
 * Fixes three bugs:
 *  A) Server sends type:'state_update', client only handled 'state'
 *  B) Server wraps in { type, data: { teams, tasks, messages } }
 *  C) Server returns teams/tasks as arrays, UI expects keyed objects
 */
function normalizeState(raw) {
  // Unwrap server envelope { type, data: { ... } } if present
  const payload = (raw.type && raw.data !== undefined) ? raw.data : raw;

  // Normalize teams: array -> keyed object by name
  let teams = payload.teams || {};
  if (Array.isArray(teams)) {
    const obj = {};
    teams.forEach(t => { obj[t.name || t.id] = t; });
    teams = obj;
  }

  // Normalize tasks: array -> keyed object by id
  let tasks = payload.tasks || {};
  if (Array.isArray(tasks)) {
    const obj = {};
    tasks.forEach(t => { obj[t.id] = t; });
    tasks = obj;
  }

  const messages = Array.isArray(payload.messages) ? payload.messages : [];

  return { teams, tasks, messages };
}

// ── Mycelium SVG Components ───────────────────────

function MyceliumLogo({ size = 24 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="mycel-logo">
      <path d="M50 50C42 35 30 25 22 18" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
      <path d="M50 50C62 38 72 28 80 22" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
      <path d="M50 50C38 62 28 72 20 80" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
      <path d="M50 50C62 62 72 72 80 82" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      <path d="M22 18C40 15 60 12 80 22" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5"/>
      <path d="M20 80C35 78 55 88 80 82" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5"/>
      <circle cx="50" cy="50" r="7" fill="currentColor"/>
      <circle cx="22" cy="18" r="4.5" fill="currentColor"/>
      <circle cx="80" cy="22" r="4" fill="currentColor"/>
      <circle cx="20" cy="80" r="4" fill="currentColor"/>
      <circle cx="80" cy="82" r="4.5" fill="currentColor"/>
    </svg>
  );
}

function MyceliumIllustration({ size = 140 }) {
  return (
    <svg width={size} height={size * 0.75} viewBox="0 0 200 150" fill="none" xmlns="http://www.w3.org/2000/svg" className="empty-illustration">
      <circle cx="100" cy="75" r="8" fill="currentColor" opacity="0.12"/>
      <circle cx="100" cy="75" r="4" fill="currentColor" opacity="0.25"/>
      <path d="M100 75C85 58 65 48 40 38" stroke="currentColor" strokeWidth="1.5" opacity="0.12" strokeLinecap="round"/>
      <path d="M100 75C115 58 135 48 160 38" stroke="currentColor" strokeWidth="1.5" opacity="0.12" strokeLinecap="round"/>
      <path d="M100 75C80 88 60 102 35 118" stroke="currentColor" strokeWidth="1.5" opacity="0.12" strokeLinecap="round"/>
      <path d="M100 75C120 88 140 102 165 118" stroke="currentColor" strokeWidth="1.5" opacity="0.12" strokeLinecap="round"/>
      <path d="M100 75C100 55 100 38 100 18" stroke="currentColor" strokeWidth="1" opacity="0.08" strokeLinecap="round"/>
      <path d="M100 75C100 95 100 115 100 140" stroke="currentColor" strokeWidth="1" opacity="0.08" strokeLinecap="round"/>
      <circle cx="40" cy="38" r="3" fill="currentColor" opacity="0.15"/>
      <circle cx="160" cy="38" r="3" fill="currentColor" opacity="0.15"/>
      <circle cx="35" cy="118" r="3" fill="currentColor" opacity="0.15"/>
      <circle cx="165" cy="118" r="3" fill="currentColor" opacity="0.15"/>
      <circle cx="100" cy="18" r="2.5" fill="currentColor" opacity="0.1"/>
      <circle cx="100" cy="140" r="2.5" fill="currentColor" opacity="0.1"/>
      <path d="M40 38C70 28 130 28 160 38" stroke="currentColor" strokeWidth="1" opacity="0.06" strokeLinecap="round"/>
      <path d="M35 118C70 128 130 128 165 118" stroke="currentColor" strokeWidth="1" opacity="0.06" strokeLinecap="round"/>
    </svg>
  );
}

// ── Theme Toggle ──────────────────────────────────

function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('mycel-theme') || 'dark';
  });

  const applyTheme = (t) => {
    setTheme(t);
    localStorage.setItem('mycel-theme', t);
    document.documentElement.setAttribute('data-theme', t);
  };

  return (
    <div className="theme-toggle">
      <button
        className={`theme-btn ${theme === 'light' ? 'active' : ''}`}
        onClick={() => applyTheme('light')}
        title="Light"
        aria-label="Light theme"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/>
          <line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/>
          <line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
      </button>
      <button
        className={`theme-btn ${theme === 'system' ? 'active' : ''}`}
        onClick={() => applyTheme('system')}
        title="System"
        aria-label="System theme"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="2" y="3" width="20" height="14" rx="2"/>
          <line x1="8" y1="21" x2="16" y2="21"/>
          <line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
      </button>
      <button
        className={`theme-btn ${theme === 'dark' ? 'active' : ''}`}
        onClick={() => applyTheme('dark')}
        title="Dark"
        aria-label="Dark theme"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>
    </div>
  );
}

// ── Header ─────────────────────────────────────────

function Header({ connected, lastUpdate, view, setView }) {
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="header">
      <div className="header-left">
        <MyceliumLogo size={24} />
        <span className="header-title">Mycel</span>
      </div>
      <div className="header-center">
        <button
          className={`tab-btn ${view === 'live' ? 'active' : ''}`}
          onClick={() => setView('live')}
        >
          Live
        </button>
        <button
          className={`tab-btn ${view === 'history' ? 'active' : ''}`}
          onClick={() => setView('history')}
        >
          History
        </button>
      </div>
      <div className="header-right">
        <ThemeToggle />
        <div className="connection-status">
          <span className={`connection-dot ${connected ? 'connected' : 'disconnected'}`} />
          <span className={`connection-text ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        {lastUpdate && (
          <span className="last-update">Updated {formatTime(lastUpdate)}</span>
        )}
      </div>
    </header>
  );
}

// ── Agent Roster (Sidebar) ─────────────────────────

function AgentRoster({ teams }) {
  const teamEntries = Object.entries(teams);
  const totalAgents = teamEntries.reduce(
    (sum, [, t]) => sum + (t.members ? t.members.length : 0), 0
  );

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-title">Agent Roster</span>
        <span className="count-badge">{totalAgents}</span>
      </div>
      <div className="agent-list">
        {teamEntries.length === 0 && (
          <div className="empty-state">
            <span className="empty-state-text">No active networks</span>
          </div>
        )}
        {teamEntries.map(([teamId, team]) => (
          <div className="team-group" key={teamId}>
            {teamEntries.length > 1 && (
              <div className="team-group-header">{team.name || teamId}</div>
            )}
            {(team.members || []).map((agent, i) => (
              <AgentCard key={agent.name || i} agent={agent} index={i} />
            ))}
          </div>
        ))}
      </div>
    </aside>
  );
}

function AgentCard({ agent, index = 0 }) {
  const color = getAgentColor(agent.name);
  const isActive = agent.status === 'active' || agent.status === 'in_progress';

  return (
    <div className="agent-card" style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="agent-avatar" style={{ background: color }}>
        {getInitials(agent.name)}
      </div>
      <div className="agent-info">
        <div className="agent-name">{agent.name}</div>
        {agent.type && <span className="role-badge">{agent.type}</span>}
      </div>
      <span className={`status-dot ${isActive ? 'active' : 'idle'}`} />
    </div>
  );
}

// ── Messages Panel ─────────────────────────────────

function MessagesPanel({ messages }) {
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages.length]);

  return (
    <div className="messages-panel">
      <div className="panel-header">
        <span className="panel-title">Messages</span>
        <span className="count-badge">{messages.length}</span>
      </div>
      <div className="message-list" ref={listRef}>
        {messages.length === 0 && (
          <div className="empty-state">
            <span className="empty-state-text">No messages yet</span>
          </div>
        )}
        {messages.map((msg, i) => (
          <MessageItem key={msg.id || i} msg={msg} />
        ))}
      </div>
    </div>
  );
}

function MessageItem({ msg }) {
  const [expanded, setExpanded] = useState(false);
  const senderColor = getAgentColor(msg.sender);
  const recipientColor = getAgentColor(msg.recipient);

  return (
    <div className="message-item">
      <div className="message-route">
        <span className="sender-badge" style={{ background: senderColor + '22', color: senderColor }}>
          {msg.sender || 'unknown'}
        </span>
        <span className="message-arrow">&rarr;</span>
        <span className="recipient-badge" style={{ background: recipientColor + '22', color: recipientColor }}>
          {msg.recipient || 'all'}
        </span>
      </div>
      <div className="message-body">
        <div
          className={`message-content ${expanded ? 'expanded' : ''}`}
          onClick={() => setExpanded(!expanded)}
        >
          {msg.summary || msg.content || ''}
        </div>
        {(msg.summary || msg.content || '').length > 120 && (
          <button className="show-more-btn" onClick={() => setExpanded(!expanded)}>
            {expanded ? 'Show less' : 'Show more'}
          </button>
        )}
      </div>
      <span className="message-time">{formatTime(msg.timestamp)}</span>
    </div>
  );
}

// ── Task Board ─────────────────────────────────────

function TaskBoard({ tasks }) {
  const allTasks = Object.values(tasks);

  const pending = allTasks.filter(t => t.status === 'pending');
  const inProgress = allTasks.filter(t => t.status === 'in_progress');
  const completed = allTasks.filter(t => t.status === 'completed');

  const sortNewest = (a, b) => {
    const ta = a.updatedAt || a.createdAt || '';
    const tb = b.updatedAt || b.createdAt || '';
    return tb.localeCompare(ta);
  };

  pending.sort(sortNewest);
  inProgress.sort(sortNewest);
  completed.sort(sortNewest);

  return (
    <div className="task-board">
      <div className="panel-header">
        <span className="panel-title">Tasks</span>
        <span className="count-badge">{allTasks.length}</span>
      </div>
      <div className="task-columns">
        <TaskColumn name="Pending" status="pending" tasks={pending} />
        <TaskColumn name="In Progress" status="in-progress" tasks={inProgress} />
        <TaskColumn name="Completed" status="completed" tasks={completed} />
      </div>
    </div>
  );
}

function TaskColumn({ name, status, tasks }) {
  return (
    <div className="task-column">
      <div className="column-header">
        <span className={`column-name ${status}`}>{name}</span>
        <span className={`column-count ${status}`}>{tasks.length}</span>
      </div>
      <div className="column-cards">
        {tasks.length === 0 && (
          <div className="empty-state empty-state-sm">
            <span className="empty-state-text">None</span>
          </div>
        )}
        {tasks.map((task, index) => (
          <TaskCard key={task.id} task={task} index={index} />
        ))}
      </div>
    </div>
  );
}

function TaskCard({ task, index = 0 }) {
  return (
    <div className="task-card" style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="task-subject">{task.subject}</div>
      <div className="task-meta">
        {task.owner && <span className="owner-badge">{task.owner}</span>}
        {task.blockedBy && task.blockedBy.length > 0 && (
          <span className="blocked-indicator">blocked by: {task.blockedBy.join(', ')}</span>
        )}
      </div>
      {task.description && (
        <div className="task-description">{task.description}</div>
      )}
    </div>
  );
}

// ── Live View ──────────────────────────────────────

function LiveView({ teams, messages, tasks }) {
  const hasTeams = Object.keys(teams).length > 0;

  if (!hasTeams) {
    return (
      <>
        <aside className="sidebar">
          <div className="sidebar-header">
            <span className="sidebar-title">Agent Roster</span>
            <span className="count-badge">0</span>
          </div>
          <div className="empty-state empty-state-large">
            <MyceliumIllustration size={120} />
            <span className="empty-state-text">No active networks</span>
            <span className="empty-state-hint">Start an agent team to see live activity</span>
          </div>
        </aside>
        <div className="main">
          <MessagesPanel messages={messages} />
          <TaskBoard tasks={tasks} />
        </div>
      </>
    );
  }

  return (
    <>
      <AgentRoster teams={teams} />
      <div className="main">
        <MessagesPanel messages={messages} />
        <TaskBoard tasks={tasks} />
      </div>
    </>
  );
}

// ── History View ───────────────────────────────────

function HistoryView({ history, setHistory, selectedSession, setSelectedSession }) {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch('/api/history')
      .then(r => r.json())
      .then(data => {
        setHistory(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const openSession = useCallback((id) => {
    fetch(`/api/history/${id}`)
      .then(r => r.json())
      .then(data => setSelectedSession(data))
      .catch(() => {});
  }, [setSelectedSession]);

  return (
    <div className="history-view">
      {selectedSession && (
        <SessionDetail session={selectedSession} onClose={() => setSelectedSession(null)} />
      )}
      {loading && (
        <div className="empty-state">
          <span className="empty-state-text">Loading history...</span>
        </div>
      )}
      {!loading && history.length === 0 && (
        <div className="empty-state empty-state-large">
          <MyceliumIllustration size={160} />
          <span className="empty-state-text">No session history</span>
          <span className="empty-state-hint">Completed agent sessions will appear here</span>
        </div>
      )}
      {!loading && history.length > 0 && (
        <div className="history-grid">
          {history.map((session, index) => (
            <div
              className="session-card"
              key={session.id}
              onClick={() => openSession(session.id)}
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div className="session-team-name">{session.teamName || session.team_name || 'Unnamed Team'}</div>
              <div className="session-stats">
                <span className="stat-badge">
                  <span className="stat-value">{session.agentCount ?? session.agent_count ?? 0}</span> agents
                </span>
                <span className="stat-badge">
                  <span className="stat-value">{session.messageCount ?? session.message_count ?? 0}</span> msgs
                </span>
                <span className="stat-badge">
                  <span className="stat-value">{session.taskCount ?? session.task_count ?? 0}</span> tasks
                </span>
              </div>
              <div className="session-dates">
                {session.startedAt || session.started_at
                  ? new Date(session.startedAt || session.started_at).toLocaleString()
                  : ''}
                {(session.endedAt || session.ended_at) &&
                  ` — ${new Date(session.endedAt || session.ended_at).toLocaleString()}`
                }
              </div>
              <span className={`session-status-badge ${session.status === 'completed' ? 'completed' : 'in-progress'}`}>
                {session.status || 'completed'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Session Detail Modal ───────────────────────────

function SessionDetail({ session, onClose }) {
  if (!session) return null;

  const agents = session.agents || [];
  const messages = session.messages || [];
  const tasks = session.tasks || [];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-panel" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        <div className="modal-title">{session.teamName || session.team_name || 'Session Detail'}</div>

        <div className="modal-section">
          <div className="modal-section-title">Agents</div>
          {agents.length === 0 ? (
            <div className="empty-state empty-state-sm"><span className="empty-state-text">No agent data</span></div>
          ) : (
            <table className="detail-table">
              <thead>
                <tr><th>Name</th><th>Type</th><th>Status</th></tr>
              </thead>
              <tbody>
                {agents.map((a, i) => (
                  <tr key={i}>
                    <td>{a.name}</td>
                    <td><span className="role-badge">{a.type || 'agent'}</span></td>
                    <td>
                      <span className={`status-dot ${a.status === 'active' ? 'active' : 'idle'}`}
                            style={{ display: 'inline-block', verticalAlign: 'middle', marginRight: 6 }} />
                      {a.status || 'unknown'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="modal-section">
          <div className="modal-section-title">Messages ({messages.length})</div>
          <div className="message-list" style={{ maxHeight: 240, overflowY: 'auto' }}>
            {messages.length === 0 ? (
              <div className="empty-state empty-state-sm"><span className="empty-state-text">No messages</span></div>
            ) : (
              messages.map((msg, i) => (
                <MessageItem key={msg.id || i} msg={msg} />
              ))
            )}
          </div>
        </div>

        <div className="modal-section">
          <div className="modal-section-title">Tasks ({tasks.length})</div>
          {tasks.length === 0 ? (
            <div className="empty-state empty-state-sm"><span className="empty-state-text">No tasks</span></div>
          ) : (
            <table className="detail-table">
              <thead>
                <tr><th>Subject</th><th>Owner</th><th>Status</th><th>Dependencies</th></tr>
              </thead>
              <tbody>
                {tasks.map((t, i) => (
                  <tr key={i}>
                    <td>{t.subject}</td>
                    <td>{t.owner || '—'}</td>
                    <td>
                      <span className={`session-status-badge ${t.status === 'completed' ? 'completed' : 'in-progress'}`}>
                        {t.status}
                      </span>
                    </td>
                    <td style={{ color: 'var(--text-dim)', fontSize: 11 }}>
                      {t.blockedBy && t.blockedBy.length > 0 ? t.blockedBy.join(', ') : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

// ── App (Root) ─────────────────────────────────────

function App() {
  const [teams, setTeams] = useState({});
  const [tasks, setTasks] = useState({});
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [view, setView] = useState('live');
  const [history, setHistory] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);

  const wsRef = useRef(null);
  const reconnectDelay = useRef(1000);

  const handleWsMessage = useCallback((event) => {
    try {
      const data = JSON.parse(event.data);
      setLastUpdate(new Date().toISOString());

      switch (data.type) {
        case 'state':
        case 'state_update': {
          const normalized = normalizeState(data);
          setTeams(normalized.teams);
          setTasks(normalized.tasks);
          setMessages(normalized.messages);
          break;
        }

        case 'team_update':
          setTeams(prev => ({
            ...prev,
            [data.teamId]: { ...prev[data.teamId], ...data.team }
          }));
          break;

        case 'team_remove':
          setTeams(prev => {
            const next = { ...prev };
            delete next[data.teamId];
            return next;
          });
          break;

        case 'task_update':
          setTasks(prev => ({
            ...prev,
            [data.task.id]: data.task
          }));
          break;

        case 'task_remove':
          setTasks(prev => {
            const next = { ...prev };
            delete next[data.taskId];
            return next;
          });
          break;

        case 'message':
          setMessages(prev => [...prev, data.message]);
          break;

        case 'messages':
          setMessages(prev => [...prev, ...(data.messages || [])]);
          break;

        default:
          break;
      }
    } catch (e) {
      console.error('WebSocket message parse error:', e);
    }
  }, []);

  const connectWs = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState <= 1) return;

    const ws = new WebSocket(`ws://${window.location.hostname}:3847`);

    ws.onopen = () => {
      setConnected(true);
      reconnectDelay.current = 1000;
    };

    ws.onmessage = handleWsMessage;

    ws.onclose = () => {
      setConnected(false);
      const delay = reconnectDelay.current;
      reconnectDelay.current = Math.min(delay * 2, 30000);
      setTimeout(connectWs, delay);
    };

    ws.onerror = () => {
      ws.close();
    };

    wsRef.current = ws;
  }, [handleWsMessage]);

  useEffect(() => {
    // Hydrate initial state via REST (uses same normalizeState)
    fetch('/api/state')
      .then(r => r.json())
      .then(data => {
        const normalized = normalizeState(data);
        setTeams(normalized.teams);
        setTasks(normalized.tasks);
        setMessages(normalized.messages);
        setLastUpdate(new Date().toISOString());
      })
      .catch(() => {});

    // Connect WebSocket
    connectWs();

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [connectWs]);

  return (
    <div className="app" style={view === 'history' ? { gridTemplateColumns: '1fr' } : undefined}>
      <Header
        connected={connected}
        lastUpdate={lastUpdate}
        view={view}
        setView={setView}
      />
      {view === 'live' ? (
        <LiveView teams={teams} messages={messages} tasks={tasks} />
      ) : (
        <HistoryView
          history={history}
          setHistory={setHistory}
          selectedSession={selectedSession}
          setSelectedSession={setSelectedSession}
        />
      )}
    </div>
  );
}

// ── Mount ──────────────────────────────────────────

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
