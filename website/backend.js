const WebSocket = require('ws');
const os = require('os');
const pty = require('node-pty');
const { createAsciinemaHeader, convertInputEvent, convertOutputEvent } = require('./asciinemaUtils');

// Timekeeping variables
const startTime = Math.floor(Date.now() / 1000); // UNIX timestamp in seconds used for header
const monoStartNs = process.hrtime.bigint(); // High-resolution time in nanoseconds

// Helper function to calculate relative seconds since the start of the session
const relSeconds = () =>
  Number(process.hrtime.bigint() - monoStartNs) / 1e9;

// Variable to hold the entire session's asciinema data
const fullSessionAsciinema = {
  header: createAsciinemaHeader(2, 80, 30, startTime, '/bin/bash', 'xterm'),
  events: []
};

// Variable to hold the latest context asciinema data
// Older events will automatically be removed to keep the context relevant
// and newer events will be added as the user interacts with the terminal
const contextAsciinema = {
  header: fullSessionAsciinema.header,
  events: []
};

// Limit for the number of events in contextAsciinema
const CONTEXT_LIMIT = 400;

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

	/* --------  Logic relating to INPUT from browser (each key-press) -------- */
	// Frontend ensures only one character is sent at a time.
	ws.on('message', raw => {
		// Incoming messages are expected to be JSON strings
		// Messages are parsed if possible, otherwise ignored
		let msg;
		try   { msg = JSON.parse(raw); }
		catch { return; }

		// Input messages are expected to have a type of 'i'
		if (msg?.type !== 'i') return;

		// Calculate the relative time since the start of the session
		// for this specific key press
		const time = relSeconds();
		const inputData = msg.data;

		// Record the input event in both full session and context asciinema
		const event = convertInputEvent(time, inputData);
		fullSessionAsciinema.events.push(event);
		// console.log('Input event:', event); // For testing valid input events
		contextAsciinema.events.push(event);

		// If context exceeds the limit, remove the oldest event(s)
		if (contextAsciinema.events.length > CONTEXT_LIMIT)
		  	contextAsciinema.events.shift();

		// Forward the input to the pty process
		ptyprocess.write(inputData);
	});

  	/* ----------  Logic relating to OUTPUT from the shell -------------------- */
	ptyprocess.on('data', data => {
		// Calculate the relative time since the start of the session
		// for this specific piece of output data
		const time = relSeconds();

		// Record the output event in both full session and context asciinema
		const event = convertOutputEvent(time, data);
		fullSessionAsciinema.events.push(event);
		// console.log('Output event:', event); // For testing valid output events
		contextAsciinema.events.push(event);

		// If context exceeds the limit, remove the oldest event(s)
		if (contextAsciinema.events.length > CONTEXT_LIMIT)
			contextAsciinema.events.shift();

		// Send back to the browser so the user sees it
			ws.readyState === WebSocket.OPEN && ws.send(data);
	});

	ws.on('close', () => {
		ptyprocess.kill();
		console.log('Client disconnected');
	});
});