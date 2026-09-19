/* Optional DOM interaction checks: node scripts/check_demo_dom.cjs
 * Requires jsdom. This executes the UI but does NOT render or verify layout.
 */
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const errors = [];
const consoleCapture = new VirtualConsole();
consoleCapture.on('jsdomError', error => errors.push(error.message));
const dom = new JSDOM(fs.readFileSync(path.resolve(__dirname, '../demo/index.html'), 'utf8'), {
  runScripts: 'dangerously',
  virtualConsole: consoleCapture,
  beforeParse(window) {
    window.ResizeObserver = class { observe() {} };
    // A manual frame clock avoids flaky wall-time tests. There is no layout engine.
    let nextId = 1;
    window.__frames = new Map();
    window.requestAnimationFrame = callback => { const id = nextId++; window.__frames.set(id, callback); return id; };
    window.cancelAnimationFrame = id => window.__frames.delete(id);
  },
});
const window = dom.window;
const root = window.document.getElementById('lonely-runner-demo');
const control = name => root.querySelector(`[data-control="${name}"]`);
const state = () => root.querySelector('[data-state]').textContent;
const time = () => root.querySelector('[data-time-label]').textContent;
function select(name, value) {
  control(name).value = String(value);
  control(name).dispatchEvent(new window.Event('change'));
}
function scrub(value) {
  control('time').value = String(value);
  control('time').dispatchEvent(new window.Event('input'));
}
function tick(now) {
  const frames = [...window.__frames.values()]; window.__frames.clear();
  frames.forEach(callback => callback(now));
}
const expected = {2: ['1/3', '1/2', '1/3'], 3: ['1/2', '1/3', '2/5'], 4: ['2/5', '1/2', '3/7']};
for (const third of [2, 3, 4]) {
  select('speed', third);
  for (let ref = 0; ref < 3; ref++) {
    select('reference', ref);
    assert(state().includes(`nearest gap ${expected[third][ref]} lap`), JSON.stringify({third, ref, state: state(), errors}));
    assert(time().includes('(exact)'));
    assert.equal(root.querySelectorAll('svg circle[fill="none"]').length, 2);
    assert(!root.querySelector('svg').innerHTML.includes('NaN'));
  }
}
select('speed', 2); select('reference', 0);
assert(time().includes('20 seconds'));
control('peak').click(); assert(time().includes('40 seconds'));
control('peak').click(); assert(time().includes('20 seconds'));
scrub(0); assert(state().includes('Motion preview')); assert(time().includes('0.00'));
control('play').click(); tick(0); tick(100);
assert.equal(control('play').textContent, 'Pause'); assert(!time().includes('0.00'));
control('play').click(); assert.equal(control('play').textContent, 'Play');
scrub(999); control('play').click(); tick(0); tick(100);
assert.equal(control('play').textContent, 'Play'); assert(time().includes('60.00'));
assert.equal(window.__frames.size, 0);
control('peak').click(); assert(time().includes('20 seconds'));
assert.deepEqual(errors, []);
window.close();
console.log('DOM checks passed: all 9 references, exact peaks, scrub preview, play/pause, and period-end stop. Rendering/layout not tested.');
