// Registers this bot with the arena controller as a fighter.
// Called from start.sh before npm start.
// Uses only Node built-ins — no external deps required.
const http = require('http');
const https = require('https');

const arenaUrl = process.env.ARENA_CONTROLLER_URL || 'http://host.docker.internal:30300';
const botName = process.env.BOT_NAME || 'arena_bot';

const url = new URL('/arena/register', arenaUrl);
const body = JSON.stringify({ name: botName });
const client = url.protocol === 'https:' ? https : http;

const req = client.request({
  hostname: url.hostname,
  port: url.port || (url.protocol === 'https:' ? 443 : 80),
  path: url.pathname,
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
  timeout: 5000,
}, (res) => {
  res.resume(); // drain response body so the socket closes cleanly
  console.log(`[arena] registered "${botName}" at ${arenaUrl} (HTTP ${res.statusCode})`);
});

req.on('timeout', () => {
  console.log(`[arena] registration timed out — continuing anyway`);
  req.destroy();
});

req.on('error', (e) => {
  console.log(`[arena] registration failed: ${e.message} — continuing anyway`);
});

req.write(body);
req.end();
