const WebSocket = require('ws');
const os = require('os');
const pty = require('node-pty');
const { createAsciinemaHeader, createInputEvent, createOutputEvent } = require('./asciinemaUtils');

// Variable to hold the entire session's asciinema data
const startTime = Math.floor(Date.now() / 1000); // UNIX timestamp in seconds (float)
const fullSessionAsciinema = {
  header: createAsciinemaHeader(2, Terminal.cols, Terminal.rows, startTime, '/bin/bash', 'xterm'),
  events: []
};

// Variable to hold the latest context asciinema data
// Older events will automatically be removed to keep the context relevant
// and newer events will be added as the user interacts with the terminal
const contextAsciinema = {
  header: fullSessionAsciinema.header,
  events: []
};

// create backend websocket server
const wss = new WebSocket.Server({ port: 8080 });

// since local shell is run, check the OS platform and determine which shell to use
var shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';

console.log('WebSocket server started on port 8080');

wss.on('connection', ws => {
	console.log('New client connected');

	// handle pty process creation
	var ptyprocess = pty.spawn(shell, [], {
		name: 'xterm-color',
		cols: 80,
		rows: 30,
		// cwd: process.env.HOME,
		env: process.env,
	});

	// handle incoming messages from the client
	ws.on('message', message => {
		// write the message to the pty process
		if (ptyprocess) {
			ptyprocess.write(message);
		}
	});

	ptyprocess.on('data', output => {
		// send the output back to the client
		if (ws.readyState === WebSocket.OPEN) {
			ws.send(output);
		}
	});

	ws.on('close', () => {
		ptyprocess.kill();
		console.log('Client disconnected');
	});
});