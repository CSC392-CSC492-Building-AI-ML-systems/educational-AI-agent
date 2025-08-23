// Orchestrator -> browser (tree updates)
const orch = new WebSocket('ws://localhost:8090');
orch.onopen = () => console.log('Orchestrator WS connected');

orch.onmessage = (e) => {
  try {
    const msg = JSON.parse(e.data);
    if (msg.type === 'model1.txt' || msg.type === 'tree_update') {
      const txt = msg.data || msg.txt || '';
      if (txt) loadTxtAndBuildTree(txt);
    }
  } catch (_) {}
};
orch.onerror = (err) => console.error('Orchestrator WS error:', err);
orch.onclose = () => console.log('Orchestrator WS closed');

// ───────── File upload / tree wiring ───────────────────────────────────────
document.getElementById('uploadBtn').onclick = () =>
  document.getElementById('txtFile').click();

document.getElementById('txtFile').onchange = e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => loadTxtAndBuildTree(reader.result);
  reader.readAsText(file);
};

// ───────── WebSocket / terminal wiring ────────────────────────────────────
const socket = new WebSocket("ws://localhost:8080");
socket.onopen    = () => console.log("WebSocket connection established");
socket.onmessage = evt => term.write(evt.data);
socket.onerror   = err => console.error("WebSocket error:", err);
socket.onclose   = ()  => console.log("WebSocket connection closed");

const term = new Terminal({ cursorBlink: true, rows: 30, cols: 80 });

const currentNoteEl    = document.getElementById('currentNote');
const updateAnnotation = txt => (currentNoteEl.textContent = txt);

term.open(document.getElementById('terminal'));
term.focus();
term.write(
  '\x1B[1;34mWelcome to AutoDocs AI Terminal!\x1B[0m\r\n' +
  'You are now connected to a live shell environment.\r\n' +
  'All your actions will be automatically tracked and summarized.\r\n' +
  '────────────────────────────────────────────────────────────────────────────────\r\n'
);

term.onKey(e => {
  const char = e.key;
  const now  = performance.now();
  socket.send(JSON.stringify({
    type: 'i',
    data: char,
    t: now / 1000
  }));
});

// ───────── Feedback UI wiring ─────────────────────────────────────────────
// 1) store per-event feedback
const feedbackMap        = new Map();
let   currentSelectedNode = null;

// 2) wrap the original selectNode to capture the selection
if (window.selectNode) {
  const _origSelect = window.selectNode;
  window.selectNode = node => {
    currentSelectedNode = node;
    _origSelect(node);
  };
}

// 3) grab all modal/buttons
const feedbackBtn       = document.getElementById('feedbackBtn');
const showFeedbackBtn   = document.getElementById('showFeedbackBtn');
const feedbackModal     = document.getElementById('feedbackModal');
const feedbackInput     = document.getElementById('feedbackInput');
const submitFeedback    = document.getElementById('submitFeedback');
const cancelFeedback    = document.getElementById('cancelFeedback');
const feedbackListModal = document.getElementById('feedbackListModal');
const feedbackList      = document.getElementById('feedbackList');
const closeFeedbackList = document.getElementById('closeFeedbackList');

// 4) open the “Enter Feedback” modal
feedbackBtn.addEventListener('click', () => {
  if (!currentSelectedNode) {
    return alert('Please select an event first.');
  }
  // preload any existing feedback or the original summary
  feedbackInput.value = feedbackMap.get(currentSelectedNode.id)
                      || currentSelectedNode.summary;
  feedbackModal.style.display = 'flex';
  feedbackInput.focus();
});

// 5) cancel without saving
cancelFeedback.addEventListener('click', () => {
  feedbackModal.style.display = 'none';
});

// 6) **submit** — save into feedbackMap and close
submitFeedback.addEventListener('click', () => {
  const txt = feedbackInput.value.trim();
  if (!txt) {
    return alert('Feedback cannot be empty.');
  }
  feedbackMap.set(currentSelectedNode.id, txt);
  feedbackModal.style.display = 'none';
});

// 7) show all feedbacks in a list
showFeedbackBtn.addEventListener('click', () => {
  feedbackList.innerHTML = '';
  if (feedbackMap.size === 0) {
    feedbackList.innerHTML = '<li><em>No feedback entered yet.</em></li>';
  } else {
    for (const [id, fb] of feedbackMap.entries()) {
      const li = document.createElement('li');
      li.textContent = `Event ${id}: ${fb}`;
      feedbackList.appendChild(li);
    }
  }
  feedbackListModal.style.display = 'flex';
});

// 8) close the “Show Feedback” modal
closeFeedbackList.addEventListener('click', () => {
  feedbackListModal.style.display = 'none';
});