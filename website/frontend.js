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

// create annotation box for displaying event annotations
const annotationBox = document.getElementById('annotationBox');

// helper function to update the annotation box after each event
function updateAnnotation(text) {
  annotationBox.value = text;
}

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
  const char = e.key;
  
  // if the WebSocket is not open, do not send data
  if (socket.readyState !== WebSocket.OPEN) {
    console.error("WebSocket is not open. Cannot send data.");
    return;
  }
  
  // send the character to the server via WebSocket
  socket.send(char);

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



