// Run `node --test observatory/web/check-board.cjs` from a checkout with Node 18+ and Python.
// The production app polls the actual read-only API. Here the same poll handler receives
// a captured executor projection, interrupted and restored without changing the queue.
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.resolve(__dirname, '../..');
const capture = `
import json, tempfile
from pathlib import Path
from observatory.runtime import Store
with tempfile.TemporaryDirectory() as directory:
    store = Store(Path(directory) / 'feed.sqlite')
    store.import_journal()
    print(json.dumps(store.board()))
`;
const board = JSON.parse(execFileSync('python', ['-c', capture], {cwd: root, encoding: 'utf8'}));
const results = JSON.parse(readFileSync(path.join(root, 'observatory/study/results.json')));
const app = readFileSync(path.join(__dirname, 'app.js'), 'utf8');

function mockView() {
  const elements = new Map();
  function querySelector(selector) {
    if (!elements.has(selector)) {
      elements.set(selector, {
        innerHTML: '', textContent: '', contains: () => false,
        querySelectorAll: () => [], setAttribute() {},
      });
    }
    return elements.get(selector);
  }
  return {querySelector, querySelectorAll: () => [], addEventListener() {}};
}

test('executor feed retains last known activity through disconnection and resumes', async () => {
  const document = mockView();
  let connection = 'unavailable';
  const snapshot = {...board, source:'snapshot'};
  const respond = data => ({ok:true, json:async () => data});
  const fetch = async url => {
    if (url === './results.json') return respond(results);
    if (url === '/api/board' && connection === 'online') return respond(board);
    if (url === '/api/board' && connection === 'overdue') return respond({...board, mode:'stale'});
    if (url === './snapshot.json' && connection === 'historical') return respond(snapshot);
    throw new Error('Connection unavailable');
  };
  // Keep polling under test control without replacing the application's own update logic.
  const context = vm.createContext({document, window:{addEventListener() {}},
    location:{hash:'#board'}, fetch, AbortController, setTimeout() {}, clearTimeout() {}});
  vm.runInContext(app, context);
  await new Promise(resolve => setImmediate(resolve));
  const poll = () => vm.runInContext('updateBoard()', context);
  const status = () => document.querySelector('#feed-label').textContent;
  const notice = () => document.querySelector('#operating-notice').innerHTML;
  const workers = () => document.querySelector('#worker-summary').innerHTML;

  assert.equal(status(), 'No feed');
  connection = 'historical';
  await poll();
  assert.equal(status(), 'Snapshot');
  assert.match(workers(), /Historical snapshot/);
  connection = 'online';
  await poll();
  assert.equal(status(), 'Connected');
  assert.ok(workers().includes(board.last_event_at));
  connection = 'unavailable';
  await poll();
  assert.equal(status(), 'Feed lost');
  assert.match(notice(), /Connection lost/);
  assert.match(workers(), /Last known state/);
  assert.ok(workers().includes(board.last_event_at));
  connection = 'online';
  await poll();
  assert.equal(status(), 'Connected');
  assert.equal(notice(), '');
  connection = 'overdue';
  await poll();
  assert.match(notice(), /Overdue heartbeat/);
});
