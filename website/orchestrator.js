// orchestrator.js
// Bridges: TTY (HTTP or WS) -> (svc0 -> svc1 via RunPod HTTP) -> Browser WS

require('dotenv').config();
const WebSocket = require('ws');
const express = require('express');          // ← NEW
const http = require('http');                // ← NEW
const axios = require('axios');
const crypto = require('crypto');

// ────────────── env ──────────────
const {
  ORCH_BROWSER_WS_PORT = '8090',            // used for BOTH HTTP + WS
  ORCH_USE_TTY_WS = 'false',                 // ← NEW: opt-in to TTY WS mode
  TTY_WS_URL = 'ws://localhost:8080',

  RUNPOD_API_KEY,
  RUNPOD_BASE_URL = 'https://api.runpod.ai/v2',
  ORCH_HTTP_TIMEOUT_MS = '60000',

  // Either give endpoint IDs...
  SERVICE0_ENDPOINT_ID,
  SERVICE1_ENDPOINT_ID,
  // ...or full URLs (if these are set, they take precedence)
  SERVICE0_HTTP_URL,
  SERVICE1_HTTP_URL,

  // Optional: skip HTTP, return mock outputs
  RUNPOD_USE_MOCK = 'false',

  // Debounce window (ms) before firing a run (only used in TTY WS mode)
  ORCH_DEBOUNCE_MS = '800'
} = process.env;

const USE_MOCK = RUNPOD_USE_MOCK === 'true';
const USE_TTY_WS = ORCH_USE_TTY_WS === 'true';

const svc0Url = SERVICE0_HTTP_URL ||
  (SERVICE0_ENDPOINT_ID
    ? `${RUNPOD_BASE_URL}/${SERVICE0_ENDPOINT_ID}/runsync`
    : null);

const svc1Url = SERVICE1_HTTP_URL ||
  (SERVICE1_ENDPOINT_ID
    ? `${RUNPOD_BASE_URL}/${SERVICE1_ENDPOINT_ID}/runsync`
    : null);

if (!USE_MOCK) {
  if (!RUNPOD_API_KEY) throw new Error('Missing RUNPOD_API_KEY in .env');
  if (!svc0Url) console.warn('⚠️  SERVICE0 URL/ID not set.');
  if (!svc1Url) console.warn('⚠️  SERVICE1 URL/ID not set.');
}

const runpodHttp = axios.create({
  timeout: Number(ORCH_HTTP_TIMEOUT_MS),
  headers: {
    'Content-Type': 'application/json',
    ...(RUNPOD_API_KEY ? { Authorization: `Bearer ${RUNPOD_API_KEY}` } : {})
  }
});

// ────────────── HTTP (ingest) + Browser WS on same port ──────────────
const app = express();
app.use(express.json({ limit: '2mb' }));
const server = http.createServer(app);

const browserWss = new WebSocket.Server({ server });
const browserClients = new Set();

browserWss.on('connection', ws => {
  browserClients.add(ws);
  ws.on('close', () => browserClients.delete(ws));
});

function broadcastToBrowser(obj) {
  const msg = JSON.stringify(obj);
  for (const ws of browserClients) {
    if (ws.readyState === WebSocket.OPEN) ws.send(msg);
  }
}

// ────────────── service calls ──────────────
async function callService0(castStr) {
  if (USE_MOCK || !svc0Url) {
    console.log('[orch] svc0(mock)');
    // pretend a parser output; pass something meaningful to svc1
    return `<mock-xml>\n<cast length="${castStr.length}"/>\n</mock-xml>`;
  }
  const payload = { input: { cast: castStr, mode: 'model0' } };
  const { data } = await runpodHttp.post(svc0Url, payload);
  if (data?.output == null) throw new Error('svc0: no output field');
  return data.output;
}

async function callService1(model0Output) {
  if (USE_MOCK || !svc1Url) {
    console.log('[orch] svc1(mock)');
    // Return a tiny Model-1 style TXT so your tree can render:
    return [
      '1',
      '[GOAL] Demo goal from mock',
      '0',
      'User runs `echo hello`',
      '-1',
      '[GOAL_END] Done'
    ].join('\n');
  }
  const payload = { input: { xml: model0Output, mode: 'model1' } };
  const { data } = await runpodHttp.post(svc1Url, payload);
  if (data?.output == null) throw new Error('svc1: no output field');
  return data.output;
}

// ────────────── HTTP ingest: TTY posts rolling .cast here ──────────────
app.post('/ingest', async (req, res) => {
  const cast = req.body?.cast;
  if (!cast) return res.status(400).json({ error: 'missing cast' });
  try {
    const m0 = await callService0(cast);
    const m1 = await callService1(m0);
    // Standardize broadcast payload for frontend.js
    broadcastToBrowser({ type: 'tree_update', txt: m1 });
    res.json({ ok: true });
  } catch (e) {
    console.error('[orch] /ingest pipeline error:', e.message);
    res.status(500).json({ error: 'pipeline failed' });
  }
});

// ────────────── OPTIONAL: TTY WS client (only if your TTY sends JSON) ─────────
let ttyWs = null;
let reconnectTimer = null;
let pendingCast = '';
let debounceTimer = null;
let lastHash = '';

function hashOf(s) { return crypto.createHash('sha1').update(s).digest('hex'); }
function onContextFrame(castStr) { pendingCast = castStr || ''; scheduleProcess(); }
function scheduleProcess() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(processPending, Number(ORCH_DEBOUNCE_MS));
}
function flushNow() { clearTimeout(debounceTimer); processPending(); }

async function processPending() {
  const castStr = pendingCast;
  if (!castStr) return;
  const h = hashOf(castStr);
  if (h === lastHash) return; // no change
  lastHash = h;
  try {
    const m0 = await callService0(castStr);
    const m1 = await callService1(m0);
    broadcastToBrowser({ type: 'tree_update', txt: m1 });
  } catch (err) {
    console.error('[orch] pipeline failed:', err.message);
    broadcastToBrowser({ type: 'error', data: 'orchestrator pipeline failed' });
  }
}

function connectToTty() {
  console.log(`[orch] connecting to TTY at ${TTY_WS_URL}…`);
  ttyWs = new WebSocket(TTY_WS_URL);
  ttyWs.on('open', () => {
      console.log('[orch] TTY connected');
      ttyWs.send(JSON.stringify({ type: 'subscribe', channel: 'context' }));
  });
  ttyWs.on('message', (data) => {
    let msg;
    try { msg = JSON.parse(data.toString()); } catch { return; }
    if (msg?.type === 'context' && typeof msg.cast === 'string') onContextFrame(msg.cast);
    else if (msg?.type === 'flush') flushNow();
  });
  ttyWs.on('close', () => { console.warn('[orch] TTY disconnected'); scheduleReconnect(); });
  ttyWs.on('error', (err) => { console.error('[orch] TTY error:', err.message); try { ttyWs.close(); } catch {} });
}
function scheduleReconnect() {
  if (reconnectTimer) return;
  reconnectTimer = setTimeout(() => { reconnectTimer = null; connectToTty(); }, 1000);
}

// ────────────── boot ──────────────
server.listen(Number(ORCH_BROWSER_WS_PORT), () =>
  console.log(`[orch] HTTP+WS listening on :${ORCH_BROWSER_WS_PORT} (mock=${USE_MOCK})`)
);
console.log('[orch] TTY WS mode    :', USE_TTY_WS);
console.log('[orch] TTY WS url     :', TTY_WS_URL);
console.log('[orch] svc0 url       :', svc0Url || '(mock)');
console.log('[orch] svc1 url       :', svc1Url || '(mock)');

if (USE_TTY_WS) connectToTty();