/**
 * @file __tests__/service0.test.js
 * Tests for service0.js
 */

const WebSocket = require('ws');
const { spawn } = require('child_process');
const runpodSdk = require('runpod-sdk');

jest.mock('child_process');
jest.mock('runpod-sdk');

let server;

beforeAll(() => {
  // Import your server (starts automatically on port 8090)
  server = require('../service0');
});

afterAll(() => {
  if (server && server.close) {
    server.close();
  }
});

//
// --- TEST 1: Server connectivity ---
//
test("WebSocket server accepts connections", done => {
  const client = new WebSocket('ws://localhost:8090');

  client.on('open', () => {
    console.log("[TEST] Client connected to ws://localhost:8090");
    expect(client.readyState).toBe(WebSocket.OPEN);
    client.close();
    done();
  });
});

//
// --- TEST 2: Python process spawned on new connection ---
//
test("Python process is spawned on new connection", done => {
  spawn.mockReturnValue({
    stdin: { writable: true, write: jest.fn() },
    stdout: { on: jest.fn() },
    on: jest.fn()
  });

  const client = new WebSocket('ws://localhost:8090');
  client.on('open', () => {
    console.log("[TEST] Client connected, checking spawn...");
    expect(spawn).toHaveBeenCalledWith(
      'python',
      expect.arrayContaining([expect.stringContaining('parser0_live.py')])
    );
    client.close();
    done();
  });
});

//
// --- TEST 3: Client messages forwarded to Python stdin ---
//
test("Messages from client are written to Python stdin", done => {
  const mockWrite = jest.fn((msg) => console.log("[MOCK PYTHON WRITE]", msg));

  spawn.mockReturnValue({
    stdin: { writable: true, write: mockWrite },
    stdout: { on: jest.fn() },
    on: jest.fn()
  });

  const client = new WebSocket('ws://localhost:8090');
  client.on('open', () => {
    console.log("[CLIENT] Connected, sending 'hello'");
    client.send("hello");

    setTimeout(() => {
      expect(mockWrite).toHaveBeenCalledWith("hello\n");
      console.log("[ASSERTION] Python stdin received message correctly");
      client.close();
      done();
    }, 100);
  });
});

//
// --- TEST 4: Python stdout triggers RunPod call + response to client ---
//
test("Python output triggers RunPod call and response back to client", done => {
  const mockRunSync = jest.fn().mockResolvedValue({ result: "fake-response" });

  runpodSdk.mockReturnValue({
    endpoint: () => ({ runSync: mockRunSync })
  });

  let stdoutHandlers = {};
  spawn.mockReturnValue({
    stdin: { writable: true, write: jest.fn() },
    stdout: {
      on: (event, cb) => {
        stdoutHandlers[event] = cb;
      }
    },
    on: jest.fn()
  });

  const client = new WebSocket('ws://localhost:8090');
  client.on('open', () => {
    console.log("[CLIENT] Connected, simulating Python output");

    // Simulate Python sending output
    stdoutHandlers['data'](Buffer.from("hello from python"));

    client.on('message', msg => {
      console.log("[CLIENT] Received from server:", msg);
      const parsed = JSON.parse(msg);

      expect(parsed).toEqual({ result: "fake-response" });
      expect(mockRunSync).toHaveBeenCalledWith({
        input: { prompt: "hello from python" }
      });

      console.log("[ASSERTION] RunPod call + client response verified");
      client.close();
      done();
    });
  });
});
