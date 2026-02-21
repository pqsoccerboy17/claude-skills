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
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="40" stroke="#5cb88a" strokeWidth="6"/>
          <circle cx="50" cy="50" r="8" fill="#5cb88a"/>
          <line x1="50" y1="50" x2="80" y2="30" stroke="#5cb88a" strokeWidth="4"/>
        </svg>
        <span className="header-title">Agent Dashboard</span>
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
            <span className="empty-state-text">No active agents</span>
          </div>
        )}
        {teamEntries.map(([teamId, team]) => (
          <div className="team-group" key={teamId}>
            {teamEntries.length > 1 && (
              <div className="team-group-header">{team.name || teamId}</div>
            )}
            {(team.members || []).map((agent, i) => (
              <AgentCard key={agent.name || i} agent={agent} />
            ))}
          </div>
        ))}
      </div>
    </aside>
  );
}

function AgentCard({ agent }) {
  const color = getAgentColor(agent.name);
  const isActive = agent.status === 'active' || agent.status === 'in_progress';

  return (
    <div className="agent-card">
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
          <div className="empty-state">
            <span className="empty-state-text">None</span>
          </div>
        )}
        {tasks.map(task => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
}

function TaskCard({ task }) {
  return (
    <div className="task-card">
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
          <div className="empty-state">
            <span className="empty-state-text">No active teams — start an agent team to see live activity</span>
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
        <div className="empty-state">
          <span className="empty-state-text">No session history yet</span>
        </div>
      )}
      {!loading && history.length > 0 && (
        <div className="history-grid">
          {history.map(session => (
            <div
              className="session-card"
              key={session.id}
              onClick={() => openSession(session.id)}
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
            <div className="empty-state"><span className="empty-state-text">No agent data</span></div>
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
              <div className="empty-state"><span className="empty-state-text">No messages</span></div>
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
            <div className="empty-state"><span className="empty-state-text">No tasks</span></div>
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
          if (data.teams) setTeams(data.teams);
          if (data.tasks) setTasks(data.tasks);
          if (data.messages) setMessages(data.messages);
          break;

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
    // Hydrate initial state
    fetch('/api/state')
      .then(r => r.json())
      .then(data => {
        if (data.teams) setTeams(data.teams);
        if (data.tasks) setTasks(data.tasks);
        if (data.messages) setMessages(data.messages);
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
