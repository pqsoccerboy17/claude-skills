# Monitoring Agent Teams

I'll help you set up a dashboard to monitor your agent teams.

## Approach

Let me create a monitoring dashboard from scratch:

```bash
mkdir -p agent-monitor
cd agent-monitor
npm init -y
npm install express ws
```

```javascript
// server.js
const express = require('express');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const app = express();
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static('public'));

// Watch for agent activity
const watchDir = process.env.HOME + '/.claude/';

server.listen(8080, () => {
    console.log('Agent monitor running on http://localhost:8080');
});
```

## Features to Add

- Real-time agent status updates via WebSocket
- Task tracking board
- Message log viewer

What data format do your agents use? I'll need to know the structure to build the right parsers.
