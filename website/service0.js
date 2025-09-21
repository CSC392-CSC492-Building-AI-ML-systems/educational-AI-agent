// To start, assume orchastrator is going to pass in the first input (over websocket)

require('dotenv').config();
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');

// Access the default export from runpod-sdk
const { default: runpodSdk } = require("runpod-sdk");

// Use process.env to access environment variables
const runpod = runpodSdk(process.env.YOUR_API_KEY);
const endpoint = runpod.endpoint(process.env.ENDPOINT_ID);

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
		console.log(`Received message from client: ${message}`);
		// write the message to the parser0
		if (pythonProcess.stdin.writable) {
			pythonProcess.stdin.write(message + '\n');
		}
	});

	pythonProcess.stdout.on('data', async output => {
    	console.log("Python stdout:", output.toString());

		// send parsed output to Runpod over HTTP 
		// replace "prompt": with output.toString().trim()
		try {
			const result = await endpoint.runSync({
				"input": {
					"prompt": "<system_output timestamp=\"0.096022\">[?2004h]0;demo@boxtop: ~demo@boxtop:~$ </system_output>\n <user_input timestamp=\"9.163614\">s</user_input>\n <system_output timestamp=\"9.164051\">s</system_output>\n <user_input timestamp=\"9.365744\">s</user_input>\n <system_output timestamp=\"9.366263\">s</system_output>\n <user_input timestamp=\"9.589844\">h</user_input>\n <system_output timestamp=\"9.59026\">h</system_output>\n <user_input timestamp=\"9.708352\"> </user_input>\n <system_output timestamp=\"9.708844\"> </system_output>\n <user_input timestamp=\"10.1118\">1</user_input>\n <system_output timestamp=\"10.112236\">1</system_output>\n <user_input timestamp=\"10.270878\">0</user_input>\n <system_output timestamp=\"10.271223\">0</system_output>\n <user_input timestamp=\"10.471565\">.</user_input>\n <system_output timestamp=\"10.471898\">.</system_output>\n <user_input timestamp=\"10.594981\">0</user_input>\n <system_output timestamp=\"10.595383\">0</system_output>\n <user_input timestamp=\"10.757499\">.</user_input>\n <system_output timestamp=\"10.757882\">.</system_output>\n <user_input timestamp=\"11.140897\">7</user_input>\n <system_output timestamp=\"11.14119\">7</system_output>\n <user_input timestamp=\"11.603706\">.</user_input>\n <system_output timestamp=\"11.604019\">.</system_output>\n <user_input timestamp=\"12.330584\">1</user_input>\n <system_output timestamp=\"12.331455\">1</system_output>\n <user_input timestamp=\"12.632256\">3</user_input>\n <system_output timestamp=\"12.633323\">3</system_output>\n <user_input timestamp=\"13.446626\">8</user_input>\n <system_output timestamp=\"13.447562\">8</system_output>\n <user_input timestamp=\"14.510021\"> (End of input marker or newline)</user_input>`",
				},
			});

			// Parse and extract only the value after "Answer:"
			console.log("RunPod result:", result);
			if (result?.output?.output) {
				const match = result.output.output.match(/Answer:\s*(\d+)/);
				const answer = match ? match[1] : null;

				if (answer) {
					if (ws.readyState === WebSocket.OPEN) {
						ws.send(answer); // Send only the number as a string
					}
					console.log(`Extracted Answer: ${answer}`);
				} else {
					console.log('No "Answer:" found in result output.');
					if (ws.readyState === WebSocket.OPEN) {
						ws.send('No answer found');
					}
				}
			} else {
				console.error('Unexpected result format from RunPod:', result);
				if (ws.readyState === WebSocket.OPEN) {
					ws.send('Error: Invalid response format');
				}
			}


		} catch (error) {
			console.error('Error calling RunPod endpoint:', error);
			if (ws.readyState === WebSocket.OPEN) {
				ws.send(JSON.stringify({ error: 'Failed to process request' }));
			}
		}
	});

	// Handle the Python process exiting
    pythonProcess.on('close', code => {
        console.log(`Python process exited with code ${code}`);
    });

	ws.on('close', () => {
		// signal EOF to Python instead of killing immediately
		if (pythonProcess.stdin.writable) {
			pythonProcess.stdin.end();  // lets Python finish and print </recording>
		}
		console.log('Client disconnected');
	});
});