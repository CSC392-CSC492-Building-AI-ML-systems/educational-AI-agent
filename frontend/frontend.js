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

term.open(document.getElementById('terminal'));
term.focus();
term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m\r\n$ ');

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


        // if (e.domEvent.key === 'Backspace') {
      //   if (command.length > 0) {
      //     command = command.slice(0, -1);
      //     term.write('\b \b');
      //   }
      // } else if (e.domEvent.key === 'Enter') {
      //   term.write('\r\nYou typed: ' + command + '\r\n$ ');
      //   command = '';
      // } else if (e.domEvent.key.length === 1) {
      //   command += char;
      //   term.write(char);
      // }
});



