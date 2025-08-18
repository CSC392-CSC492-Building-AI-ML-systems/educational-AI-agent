const WebSocket = require('ws');
const readline = require('readline');

// Connect to the WebSocket server on port 8090
const ws = new WebSocket('ws://localhost:8090');

// Setup stdin reader
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: true
});

ws.on('open', () => {
    console.log('Connected to WebSocket server');
    console.log('Type input lines to send to server. Type "/end" to finish the session.');

    rl.on('line', (line) => {
        if (!line.trim()) return;

        if (line.trim() === '/end') {
            console.log('Ending session...');
            ws.close();  // triggers stdin.end() in service0.js
            return;
        }

        console.log(`Sending: ${line}`);
        ws.send(line);
    });
});

ws.on('message', message => {
    console.log(`\nReceived from server:\n${message}\n`);
    process.stdout.write("> ");
});

ws.on('error', error => {
    console.error(`WebSocket error: ${error}`);
});

ws.on('close', () => {
    console.log('Disconnected from WebSocket server');
    rl.close();
});
