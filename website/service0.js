
// To start, assume orchastrator is going to pass in the first input (over websocket)



const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const YOUR_API_KEY = process.env.YOUR_API_KEY;
const ENDPOINT_ID = process.env.ENDPOINT_ID;
const runpodSdk = require("runpod-sdk");

// create service 0 websocket server to recieve input from orchastrator
const wss = new WebSocket.Server({ port: 8090 });

console.log('Service 0 WebSocket server started on port 8090');

wss.on('connection', ws => {
	console.log('New client connected');

	// path to parser0_live.py
	const scriptPath = path.join(__dirname, 'model-0','parser0_live.py');

	// spawn a python process to run parser0_live.py
	const pythonProcess = spawn('python', [scriptPath]);


	// handle incoming messages from the client
	ws.on('message', message => {
		// write the message to the parser0
		if (pythonProcess.stdin.writable) {
			pythonProcess.stdin.write(message + '\n');
		}
	});


	pythonProcess.stdout.on('data', async output => {

		// send parsed output to Runpod over HTTP

		const runpod = runpodSdk(YOUR_API_KEY);
		const endpoint = runpod.endpoint(ENDPOINT_ID);
		const result = await endpoint.runSync({
			"input": {
				"prompt": output.toString().trim(),
			},
		});

		// need to send the result back to the client
		if (ws.readyState === WebSocket.OPEN) {
			ws.send(JSON.stringify(result));
		}	
		// Log the result
		console.log(result);
	});


	// Handle the Python process exiting
    pythonProcess.on('close', code => {
        console.log(`Python process exited with code ${code}`);
    });

	ws.on('close', () => {
		pythonProcess.kill();
		console.log('Client disconnected');
	});
});