// Load env (for optional interval override)
require('dotenv').config();

const WebSocket = require('ws');
const os = require('os');
const pty = require('node-pty');

const {
  createAsciinemaHeader,
  convertInputEvent,
  convertOutputEvent,
  toCastString,
} = require('./asciinemaUtils');

const PUBLISH_INTERVAL_MS = Number(process.env.PUBLISH_INTERVAL_MS || 1200);
const CONTEXT_LIMIT = 400; // rolling window size for context

// ───────── timekeeping ─────────
const startTime = Math.floor(Date.now() / 1000);
const monoStartNs = process.hrtime.bigint();
const relSeconds = () =>
  Number(process.hrtime.bigint() - monoStartNs) / 1e9;

// ───────── asciinema buffers ─────────
const fullSessionAsciinema = {
  header: createAsciinemaHeader(2, 80, 30, startTime, '/bin/bash', 'xterm'),
  events: []
};
const contextAsciinema = {
  header: fullSessionAsciinema.header,
  events: []
};

// ───────── ws server (browser + orchestrator both connect here) ─────────
const wss = new WebSocket.Server({ port: 8080 });
console.log('WebSocket server started on port 8080');

// ───────── SINGLE PTY shared by all clients ─────────
const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
const ptyprocess = pty.spawn(shell, [], {
  name: 'xterm-color',
  cols: 80,
  rows: 30,
  env: process.env,
});

// Broadcast convenience
function broadcastRaw(s) {
  for (const client of wss.clients) {
    if (client.readyState === WebSocket.OPEN) {
      // Browsers expect raw strings for terminal output
      client.send(s);
    }
  }
}
function broadcastJson(obj, predicate = () => true) {
  const s = JSON.stringify(obj);
  for (const client of wss.clients) {
    if (client.readyState === WebSocket.OPEN && predicate(client)) {
      client.send(s);
    }
  }
}

// PTY → broadcast to all browsers; also record output for context
ptyprocess.on('data', (data) => {
  const time = relSeconds();
  const event = convertOutputEvent(time, data);
  fullSessionAsciinema.events.push(event);
  contextAsciinema.events.push(event);
  if (contextAsciinema.events.length > CONTEXT_LIMIT) {
    contextAsciinema.events.shift();
  }

  broadcastRaw(data);
});

// Each connection can: send key inputs, or subscribe to context
wss.on('connection', (ws) => {
  console.log('New client connected');
  ws.wantContext = false; // opt-in

  ws.on('message', (raw) => {
    // Control messages are JSON; ignore non-JSON safely
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch { return; }

    // Orchestrator subscribes to context stream
    if (msg?.type === 'subscribe' && msg?.channel === 'context') {
      ws.wantContext = true;
      safeSend(ws, JSON.stringify({ type: 'subscribed', channel: 'context' }));
      return;
    }

    // Browser sends keypresses as {type:'i', data:'\r'|'a'|...}
    if (msg?.type !== 'i') return;

    const time = relSeconds();
    const inputData = msg.data;

    // Record input into buffers
    const event = convertInputEvent(time, inputData);
    fullSessionAsciinema.events.push(event);
    contextAsciinema.events.push(event);
    if (contextAsciinema.events.length > CONTEXT_LIMIT) {
      contextAsciinema.events.shift();
    }

    // Write to the single PTY
    ptyprocess.write(inputData);

    // On Enter, immediately publish current context + a flush signal
    if (inputData === '\r' || inputData === '\n') {
      publishContextToSubscribers();
      publishFlushToSubscribers();
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Periodic context publish (debounced-ish heartbeat for orchestrator)
setInterval(() => {
  publishContextToSubscribers();
}, PUBLISH_INTERVAL_MS);

// Helpers to publish context/flush only to subscribers
function publishContextToSubscribers() {
  const castStr = toCastString(
    contextAsciinema.header,
    contextAsciinema.events
  );
  broadcastJson(
    { type: 'context', cast: castStr },
    (client) => client.wantContext === true
  );
}

function publishFlushToSubscribers() {
  broadcastJson(
    { type: 'flush' },
    (client) => client.wantContext === true
  );
}

function safeSend(ws, s) {
  if (ws.readyState === WebSocket.OPEN) ws.send(s);
}