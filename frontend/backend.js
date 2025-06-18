const WebSocket = require('ws');
const os = require('os');
const pty = require('node-pty');

// create backend websocket server
const wss = new WebSocket.Server({ port: 8080 });

console.log('WebSocket server started on port 8080');

// since we will be running a shell, check the OS platform and determine the shell to use
var shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';

// handle pty process creation
var ptyprocess = pty.spawn(shell, [], {
	name: 'xterm-color',
	cols: 80,
	rows: 30,
	// cwd: process.env.HOME,
	env: process.env,
});

wss.on('connection', ws => {
	console.log('New client connected');

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
		console.log('Client disconnected');
	});
});