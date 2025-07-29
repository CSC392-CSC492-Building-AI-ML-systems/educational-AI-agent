document.getElementById('uploadBtn').onclick = () =>
  document.getElementById('txtFile').click();

document.getElementById('txtFile').onchange = e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => loadTxtAndBuildTree(reader.result);
  reader.readAsText(file);
};

// create a WebSocket connection to the server
const socket = new WebSocket("ws://localhost:8080");
socket.onopen = () => {
  console.log("WebSocket connection established");
}

// handle new messages from the server (real shell output)
socket.onmessage = (event) => {
  term.write(event.data);
}

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
}

socket.onclose = () => {
  console.log("WebSocket connection closed");
}


// create terminal instance
const term = new Terminal({
  cursorBlink: true,
  rows: 30,
  cols: 80,
});

// element that shows the latest annotation under the tree
const currentNoteEl = document.getElementById('currentNote');
const updateAnnotation = txt => (currentNoteEl.textContent = txt);

// open xterm terminal and display intro message
term.open(document.getElementById('terminal'));
term.focus();
term.write(
  '\x1B[1;34mWelcome to AutoDocs AI Terminal!\x1B[0m\r\n' +  // blue bold
  'You are now connected to a live shell environment.\r\n' +
  'All your actions will be automatically tracked and summarized.\r\n' +
  '────────────────────────────────────────────────────────────────────────────────\r\n'
);

let command = '';

term.onKey(e => {
  const char = e.key;               // what the user just typed
  const now  = performance.now();   // ms since page-load, high-resolution

  /* tell the back-end exactly what happened */
  socket.send(
    JSON.stringify({                // keep it tiny but explicit
      type : 'i',                   // “input” event
      data : char,                  // the raw character (↵, ⌫ etc. stay intact)
      t    : now / 1000             // seconds with micro-second-ish precision
    })
  );

  // Below is just to test whether the annotation box updates correctly
  // Build up command as user types
  if (e.domEvent.key === 'Enter') {
    updateAnnotation(`the last event was: ${command}`);
    command = ''; // Reset for next input
  } else if (e.domEvent.key === 'Backspace') {
    // Remove last character (basic handling, won't match terminal exactly)
    command = command.slice(0, -1);
  } else if (e.domEvent.key.length === 1) {
    // Add normal printable characters only
    command += char;
  }
});



