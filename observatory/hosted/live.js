'use strict';

let incomingReading = takeAllowance();
const byId = id => document.getElementById(id);
const text = (value, missing = '') => (typeof value === 'string' && value.trim()) || (typeof value === 'number' && Number.isFinite(value) ? String(value) : missing);
const esc = value => text(value).replace(/[&<>"']/g, char => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[char]));
const list = value => Array.isArray(value) ? value.filter(item => item && typeof item === 'object') : [];
const number = value => typeof value === 'number' && Number.isFinite(value) ? value.toLocaleString('en-US', {maximumFractionDigits:2}) : 'Unknown';
const pretty = value => text(value).replace(/[_-]/g, ' ').replace(/^\w/, first => first.toUpperCase());
const pacific = new Intl.DateTimeFormat('en-US', {timeZone:'America/Los_Angeles', month:'short', day:'numeric', year:'numeric', hour:'numeric', minute:'2-digit', timeZoneName:'short'});
const pacificDay = new Intl.DateTimeFormat('en-CA', {timeZone:'America/Los_Angeles', year:'numeric', month:'2-digit', day:'2-digit'});
const isoTime = value => typeof value === 'string' && value.length > 0 ? Date.parse(value) : NaN;
const timeLabel = value => Number.isFinite(isoTime(value)) ? pacific.format(new Date(value)) : 'Time unknown';
const timeTag = value => Number.isFinite(isoTime(value)) ? '<time datetime="' + esc(value) + '">' + esc(timeLabel(value)) + '</time>' : 'Time unknown';
const stamp = job => job.finished_at || job.updated_at || job.started_at || job.queued_at;
const recent = (items, getTime) => [...items].sort((a,b) => (isoTime(getTime(b)) || 0) - (isoTime(getTime(a)) || 0));
const empty = message => '<p class="muted">' + esc(message) + '</p>';
const metric = (label,value) => '<div><dt>' + esc(label) + '</dt><dd>' + esc(value) + '</dd></div>';
const details = (key,label,body) => '<details data-key="' + esc(key) + '"><summary>' + esc(label) + '</summary>' + body + '</details>';
const definition = (label,html) => '<div><dt>' + esc(label) + '</dt><dd>' + html + '</dd></div>';
const latestMarkup = new Map();
let record = null;
let connection = 'loading';
let busy = false;
let timer;
let retryWhenReady = false;
const pollInterval = 30000;

function setMarkup(id, markup) {
  if (latestMarkup.get(id) === markup) return;
  const target = byId(id);
  const expanded = new Set([...target.querySelectorAll('details[open]')].map(item => item.dataset.key));
  const focusKey = target.contains(document.activeElement) && document.activeElement.closest('details')?.dataset.key;
  target.innerHTML = markup;
  latestMarkup.set(id, markup);
  for (const item of target.querySelectorAll('details[data-key]')) {
    if (expanded.has(item.dataset.key)) item.open = true;
    if (focusKey && item.dataset.key === focusKey) item.querySelector('summary')?.focus({preventScroll:true});
  }
}

function artifact(path, revision) {
  const parts = text(path).split('/');
  const label = esc(path);
  if (!label || !/^[a-f\d]{40}$/i.test(text(revision)) || !parts.every(part => /^[\w.-]+$/.test(part) && part !== '..' && part !== '.')) return label;
  return '<a href="https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/' + esc(revision) + '/' + parts.map(encodeURIComponent).join('/') + '">' + label + '</a>';
}

function evidence(item, key) {
  const path = artifact(item.artifact, item.revision);
  const replay = text(item.replay);
  const revision = text(item.revision);
  if (!path && !replay && !revision) return '';
  return details(key, 'Evidence and replay', '<div class="evidence">' +
    (path ? '<p>Artifact</p>' + path : '') +
    (revision ? '<p>Revision</p><code>' + esc(revision) + '</code>' : '') +
    (replay ? '<p>Replay command</p><code>' + esc(replay) + '</code>' : '') + '</div>');
}

function working(job) {
  return job.state === 'running' && !(Number.isFinite(isoTime(job.lease_expires)) && isoTime(job.lease_expires) <= Date.now());
}

function jobStatus(job) {
  if (job.state === 'running' && !working(job)) return 'Lease expired';
  return pretty(job.state) || 'State unknown';
}

function roleCards(data) {
  const jobs = list(data.jobs);
  const events = list(data.events);
  const roles = [...new Set([...jobs,...events].map(item => item.role).filter(role => typeof role === 'string' && role))];
  const preferred = ['coordinator','researcher','challenger','verifier'];
  roles.sort((a,b) => (preferred.includes(a) ? preferred.indexOf(a) : 10) - (preferred.includes(b) ? preferred.indexOf(b) : 10) || a.localeCompare(b));
  byId('team-count').textContent = jobs.filter(working).length + ' running · ' + jobs.filter(job => job.state === 'queued').length + ' queued';
  return roles.map(role => {
    const own = recent(jobs.filter(job => job.role === role), stamp);
    const activity = recent(events.filter(event => event.role === role), item => item.time);
    const job = own.find(working) || own.find(item => item.state === 'running') || own.find(item => item.state === 'queued') || own[0];
    const last = activity[0];
    const updated = recent([...own.map(item => ({at:stamp(item)})),...activity.map(item => ({at:item.time}))],item => item.at)[0]?.at;
    const returned = own.find(item => text(item.summary));
    const historicalReturn = activity.find(event => event.source === 'historical-import' && ['completed','verified','returned'].includes(event.state));
    const state = job ? jobStatus(job) : (last?.source === 'historical-import' ? 'Historical · ' : '') + (pretty(last?.state) || 'No assignment');
    const history = own.map(item => '<div class="detail-record"><strong>' + esc(jobStatus(item)) + '</strong> · ' + esc(item.task) +
      '<p class="meta">' + timeTag(stamp(item)) + '</p>' + (item.controller_run_id ? '<p class="meta">Coordinator wake · <code>' + esc(item.controller_run_id) + '</code></p>' : '') + (item.summary ? '<p>' + esc(item.summary) + '</p>' : '') +
      evidence(item, 'role-evidence-' + item.id) + '</div>').join('');
    return '<article class="role-card"><div class="card-title"><h3>' + esc(pretty(role)) + '</h3><span class="state ' +
      (working(job || {}) ? 'good' : job?.state === 'failed' ? 'bad' : '') + '">' + esc(state) + '</span></div><dl>' +
      definition('Assignment',esc(job?.task || last?.task || 'No assignment recorded.')) +
      definition('Latest return',esc(returned?.summary || historicalReturn?.task || 'No finding returned yet.')) +
      definition('Last update',timeTag(updated)) + '</dl>' +
      (history ? details('role-' + role, 'Assignments (' + own.length + ')', history) : '') + '</article>';
  }).join('') || empty('No worker or coordinator activity has been recorded.');
}

function findTrace(finding, data) {
  const jobs = list(data.jobs), events = list(data.events);
  const origin = jobs.find(job => job.id === finding.job_id);
  const verifier = jobs.find(job => job.id === finding.verifier_job_id);
  const children = jobs.filter(job => job.source_finding_id === finding.id && !job.verification_of);
  return {finding, origin, verifier, children, events};
}

function traceMarkup(trace) {
  const {finding,origin,verifier,children,events} = trace;
  const source = [finding.source,origin?.source].find(value => text(value));
  const originEvent = events.find(event => finding.job_id && event.job_id === finding.job_id);
  const checkedBy = text(finding.verifier || verifier?.worker || verifier?.role || finding.verifier_job_id);
  const originLabel = [pretty(origin?.role || originEvent?.role), checkedBy ? 'Checked by ' + checkedBy : 'Verifier unrecorded'].filter(Boolean).join(' · ');
  const evidenceItem = {artifact:finding.artifact || verifier?.artifact, replay:finding.replay || verifier?.replay, revision:finding.revision || verifier?.revision};
  const first = '<li><h3>Verified finding</h3><p>' + esc(finding.summary || 'Summary unavailable.') +
    '</p><p class="meta">' + esc(originLabel) + ' · ' + timeTag(finding.time) +
    (source ? ' · ' + esc(pretty(source)) : '') + '</p>' + evidence(evidenceItem,'trace-evidence-' + finding.id) + '</li>';
  const changed = children.map(job => '<div class="detail-record">' + esc(job.task) + '<p class="meta">' + esc(pretty(job.role)) +
    ' · Queued ' + timeTag(job.queued_at) + '</p></div>').join('') || empty('No follow-up question linked to this finding yet.');
  const pickups = children.map(job => {
    const claimed = events.find(event => event.job_id === job.id && ['claim','claimed','worker_claimed','picked_up','job_claimed'].includes(event.kind));
    if (!job.started_at && !claimed) return '';
    const person = text(claimed?.worker || job.worker);
    return '<div class="detail-record"><strong>' + esc(pretty(job.role)) + '</strong>' + (person ? ' · ' + esc(person) : '') +
      '<p>' + esc(job.task) + '</p><p class="meta">Claimed ' + timeTag(claimed?.time || job.started_at) + ' · ' + esc(jobStatus(job)) + '</p>' +
      (job.summary ? '<p>' + esc(job.summary) + '</p>' : '') + evidence(job,'pickup-' + job.id) + '</div>';
  }).join('') || empty('Awaiting a recorded worker claim.');
  return '<div class="trace"><ol>' + first + '<li><h3>Changed question</h3>' + changed +
    '</li><li><h3>Worker pickup</h3>' + pickups + '</li></ol></div>';
}

function findings(data) {
  const traces = recent(list(data.findings),item => item.time).map(item => findTrace(item,data));
  if (!traces.length) return empty('A verified finding has yet to be recorded.');
  const featured = traces.find(trace => trace.children.some(job => job.started_at)) || traces.find(trace => trace.children.length) || traces[0];
  const others = traces.filter(trace => trace !== featured);
  return traceMarkup(featured) + (others.length ? details('other-traces', 'Other verified findings (' + others.length + ')', others.map(traceMarkup).join('')) : '');
}

function decisions(data) {
  const open = recent(list(data.decisions).filter(item => ['open','pending','awaiting','requested'].includes(item.state)),item => item.time);
  return open.map(item => '<p>' + esc(item.text) + '</p><p class="meta">' + timeTag(item.time) + '</p>').join('') || empty('No open decision is recorded.');
}

function measurement(data) {
  const p = data.pilot || {}, e = data.evaluation || {};
  const hours = typeof e.elapsed_hours === 'number' ? number(e.elapsed_hours) + ' h' : 'Unknown';
  const calls = typeof p.model_call_limit === 'number' ? number(e.model_calls_reserved) + ' / ' + number(p.model_call_limit) : number(e.model_calls_reserved);
  const dispatch = typeof p.model_dispatch_limit === 'number' ? number(e.model_dispatches) + ' / ' + number(p.model_dispatch_limit) : number(e.model_dispatches);
  return '<p class="meta">Start ' + timeTag(p.started_at) + ' · End ' + timeTag(p.ends_at) + '</p><dl class="metrics">' +
    metric('Elapsed',hours) + metric('Model call reservations',calls) + metric('Model calls remaining',number(e.model_calls_remaining)) +
    metric('Model job grants',dispatch) + metric('Coordinator runs',number(e.controller_runs)) +
    (e.over_budget_controller_runs ? metric('Over-cap wakes stopped',number(e.over_budget_controller_runs)) : '') +
    metric('Deterministic dispatches',number(e.deterministic_dispatches)) +
    metric('Completed jobs',number(e.completed_jobs)) + metric('Verified findings',number(e.verified_findings)) + metric('Hosted verified follow-ups claimed',number(e.followups_claimed)) +
    metric('Retries',number(e.retries)) + '</dl><p class="muted">Coverage · ' + esc(text(e.coverage,'Unknown')) +
    '</p>' + (e.decision ? '<p>Decision · ' + esc(e.decision) + '</p>' : '');
}

function planUsage(data) {
  const plan = data.plan || {};
  const windows = list(plan.windows).map(item => {
    const pct = typeof item.remaining_percent === 'number' ? number(item.remaining_percent) + '% remaining' : 'Remaining unknown';
    const passed = Number.isFinite(isoTime(item.resets_at)) && isoTime(item.resets_at) <= Date.now();
    return '<div class="usage-line"><strong>' + esc(item.label || 'Plan window') + '</strong><span>' + esc(pct) +
      '</span><small>Reset ' + timeTag(item.resets_at) + (passed ? ' · Reset passed since this reading' : '') + '</small></div>';
  }).join('');
  const attempt = plan.last_attempt;
  const lastAttempt = attempt?.error ? '<p class="muted">Latest attempt ' + timeTag(attempt.measured_at) + ' · ' + esc(attempt.error) + '</p>' : '';
  const captured = plan.captured_at ? 'Captured ' + timeTag(plan.captured_at) : 'Checked ' + timeTag(data.generated_at);
  return '<p class="meta">' + captured + '</p>' + (windows || empty('Plan remaining and reset times are unknown.')) + lastAttempt +
    (plan.source ? '<p class="meta">Source · ' + esc(plan.source) + '</p>' : '');
}

function activityUsage(data) {
  const u = data.usage || {};
  const today = pacificDay.format(new Date());
  const recordedDay = text(u.day);
  const current = recordedDay === today;
  const matchDay = key => current ? number(u[key]) : 'Unknown';
  const disclosed = current && text(u.coverage);
  const coverage = disclosed || (recordedDay && !current ? 'No reading for this Pacific day' : 'Unknown');
  const prior = recordedDay && !current ? '<p class="meta">Latest reported Pacific day · ' + esc(recordedDay) + '</p>' : '';
  return '<p class="meta">Pacific day · ' + esc(today) + '</p><dl class="metrics">' +
    metric('Model runs',matchDay('runs')) + metric('Exact computation runs',matchDay('deterministic_runs')) +
    metric('Measured model runs',matchDay('measured_runs')) + metric('Total measured tokens',matchDay('tokens_used')) + metric('Input tokens',matchDay('input_tokens')) +
    metric('Output tokens',matchDay('output_tokens')) + metric('Cached input tokens',matchDay('cached_input_tokens')) +
    '</dl><p class="muted">Coverage · ' + esc(coverage) + '</p><p class="meta">Measured ' + timeTag(u.measured_at) + '</p>' + prior +
    (u.source ? '<p class="meta">Source · ' + esc(u.source) + '</p>' : '');
}

function researchHistory(data) {
  const studies = list(data.studies);
  const restored = studies.map(item => '<div class="detail-record"><strong>' + esc(item.title || item.name) + '</strong>' +
    (item.summary ? '<p>' + esc(item.summary) + '</p>' : '') + evidence(item,'study-' + item.id) + '</div>').join('');
  const revision = '96dfed6b2ea74cec250c301e454b6b2c4cd13860';
  const published = 'https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/' + revision + '/observatory/escape_trial/';
  return restored + '<div class="detail-record"><a class="study-link" href="' + published + 'VERIFICATION.md">Fresh-06 · independent verification</a></div>' +
    '<div class="detail-record"><a class="study-link" href="' + published + 'CHALLENGE.md">Multi-collider anchor · challenger’s checks</a></div>' +
    '<div class="detail-record"><a class="study-link" href="/archive/#evidence">Reciprocal rule · two-panel comparison</a></div>' +
    '<div class="detail-record"><a class="study-link" href="/archive/#case/fresh-04/exploratory">Shifted anchor · independent endpoint check</a></div>';
}

function activityLog(data) {
  return recent(list(data.events),item => item.time).map(item => '<li><strong>' + esc(pretty(item.role) || 'System') + '</strong> · ' +
    esc(pretty(item.kind || item.state)) + '<p>' + esc(item.task) + '</p><p class="meta">' + timeTag(item.time) +
    (item.source ? ' · ' + esc(pretty(item.source)) : '') + '</p>' + evidence(item,'log-' + item.id) + '</li>').join('') ||
    '<li class="muted">No events recorded.</li>';
}

function staleFeed() {
  return !Number.isFinite(isoTime(record?.generated_at)) || Date.now() - isoTime(record.generated_at) > 120000;
}

function controlAction() {
  const p = record?.pilot;
  if (!p || connection !== 'online' || staleFeed() || !record.operator?.can_control) return '';
  if (['ended','expired','completed','stopped','not_started','inactive','closed'].includes(p.status)) return '';
  if (Number.isFinite(isoTime(p.ends_at)) && isoTime(p.ends_at) <= Date.now()) return '';
  if (p.paused === true) return 'resume';
  if (p.paused === false) return 'pause';
  return '';
}

function updateStatus() {
  const badge = byId('connection'), notice = byId('notice');
  const stale = record && staleFeed();
  let message = '';
  if (connection === 'offline') message = record ? 'Connection lost. Showing the last record received. Worker activity and pilot controls need a fresh connection.' : 'The pilot record is unavailable. Refresh to try again.';
  else if (stale) message = 'The pilot record is stale. The activity below reflects its timestamp. Refresh to check for a newer record.';
  badge.textContent = connection === 'offline' ? (record ? 'Feed lost' : 'Offline') : stale ? 'Stale record' : connection === 'online' ? 'Connected' : 'Connecting';
  badge.className = 'indicator ' + (connection === 'offline' ? 'bad' : stale ? 'warn' : connection === 'online' ? 'good' : '');
  byId('feed-time').textContent = record ? timeLabel(record.generated_at) : '';
  notice.textContent = message;
  notice.hidden = !message;
  const action = controlAction(), button = byId('control');
  button.hidden = !action;
  button.disabled = busy;
  button.textContent = action === 'pause' ? 'Pause pilot' : 'Resume pilot';
  byId('refresh').disabled = busy;
  byId('confirm-import').disabled = busy || !record?.operator?.can_control || connection !== 'online';
}

function draw(data) {
  record = data;
  const p = data.pilot;
  byId('question').textContent = text(data.current_question,'No current question recorded');
  const previous = recent(list(data.jobs).filter(job => job.role !== 'verifier' && job.task),stamp)[0];
  byId('question-meta').textContent = data.current_question ? text(data.project?.name) : previous ? 'Last assignment · ' + previous.task : '';
  byId('pilot-state').textContent = pretty(p.status) || (p.paused === true ? 'Paused' : 'Unknown');
  byId('pilot-detail').textContent = p.paused ? text(p.pause_reason,'Dispatch is paused.') : text(p.provider_hold) ||
    (p.ends_at ? (p.status === 'ended' ? 'Pilot ended ' : 'Pilot ends ') + timeLabel(p.ends_at) : '');
  setMarkup('roles',roleCards(data));
  setMarkup('findings',findings(data));
  setMarkup('decision',decisions(data));
  setMarkup('measurement',measurement(data));
  setMarkup('plan',planUsage(data));
  setMarkup('activity-usage',activityUsage(data));
  setMarkup('studies',researchHistory(data));
  setMarkup('events',activityLog(data));
  byId('desk').hidden = false;
}

async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(),10000);
  try {
    const result = await fetch(path,{mode:'same-origin',credentials:'same-origin',cache:'no-store',redirect:'error',...options,signal:controller.signal});
    if (!result.ok) throw new Error('Request unsuccessful');
    return await result.json();
  } finally { window.clearTimeout(timeout); }
}

async function readRecord() {
  const next = await request('/api/pilot');
  if (!next?.pilot || !Array.isArray(next.jobs) || !Array.isArray(next.events)) throw new Error('Invalid pilot record');
  connection = 'online';
  draw(next);
}

function finishRequest() {
  busy = false;
  updateStatus();
  window.clearTimeout(timer);
  timer = window.setTimeout(refresh,retryWhenReady ? 0 : pollInterval);
  retryWhenReady = false;
}

async function refresh() {
  if (busy) { retryWhenReady = true; return; }
  busy = true;
  updateStatus();
  try {
    await readRecord();
  } catch {
    connection = 'offline';
    if (!record) byId('question').textContent = 'Research desk unavailable';
  } finally { finishRequest(); }
}

function sendOperator(payload) {
  return request('/api/operator',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
}

async function control() {
  const action = controlAction();
  if (!action || busy) return;
  busy = true;
  updateStatus();
  const message = byId('control-feedback');
  message.textContent = action === 'pause' ? 'Requesting pause…' : 'Requesting resume…';
  let accepted = false;
  try {
    await sendOperator({action});
    accepted = true;
    await readRecord();
    message.textContent = action === 'pause' && record.pilot.paused || action === 'resume' && record.pilot.paused === false ?
      (action === 'pause' ? 'Pause confirmed.' : 'Resume confirmed.') : 'Request received. Check the operating state.';
  } catch {
    connection = 'offline';
    message.textContent = accepted ? 'Request received. Refresh to confirm the operating state.' : 'Request unconfirmed. Refresh to check the operating state.';
  } finally { finishRequest(); }
}

function allowedKeys(obj, keys) {
  return obj && !Array.isArray(obj) && typeof obj === 'object' &&
    Object.keys(obj).length === keys.length && keys.every(key => Object.hasOwn(obj,key));
}

function validUTC(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(value)) return false;
  const stamp = Date.parse(value);
  return Number.isFinite(stamp) && new Date(stamp).toISOString().slice(0,19) === value.slice(0,19);
}

function takeAllowance() {
  const prefix = '#sync-allowance=';
  if (!location.hash.startsWith(prefix)) return null;
  const encoded = location.hash.slice(prefix.length);
  window.history.replaceState(window.history.state,'',location.pathname + location.search);
  try {
    if (encoded.length > 5462 || !/^[A-Za-z0-9_-]+$/.test(encoded)) throw new Error();
    const raw = atob(encoded.replaceAll('-','+').replaceAll('_','/'));
    if (raw.length > 4096) throw new Error();
    const bytes = Uint8Array.from(raw,char => char.charCodeAt(0));
    const parsed = JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
    if (!allowedKeys(parsed,['measured_at','windows']) || !validUTC(parsed.measured_at) ||
        Date.parse(parsed.measured_at) > Date.now() + 300000 ||
        !Array.isArray(parsed.windows) || !parsed.windows.length || parsed.windows.length > 2) throw new Error();
    const labels = new Set(['5-hour','Weekly','Primary','Secondary']);
    for (const row of parsed.windows) {
      if (!allowedKeys(row,['label','remaining_percent','resets_at']) || !labels.delete(row.label) ||
          !Number.isFinite(row.remaining_percent) || row.remaining_percent < 0 || row.remaining_percent > 100 ||
          row.resets_at !== null && !validUTC(row.resets_at)) throw new Error();
    }
    return {reading:parsed};
  } catch { return {invalid:true}; }
}

function setupImport() {
  if (!incomingReading) return;
  byId('allowance-import').hidden = false;
  const reading = incomingReading.reading;
  byId('import-description').textContent = reading ? 'Review the plan reading captured ' + timeLabel(reading.measured_at) + '.' :
    'This link contains an invalid plan reading. Run the WSL meter again.';
  byId('import-windows').textContent = reading ? reading.windows.map(row => row.label + ' · ' + number(row.remaining_percent) + '% remaining · Reset ' + timeLabel(row.resets_at)).join(' | ') : '';
  byId('confirm-import').hidden = !reading;
  byId('cancel-import').hidden = !reading;
  byId('import-message').textContent = '';
  updateStatus();
}

async function importAllowance() {
  const reading = incomingReading?.reading;
  if (!reading || busy || !record?.operator?.can_control || connection !== 'online') return;
  busy = true;
  updateStatus();
  byId('cancel-import').disabled = true;
  byId('import-message').textContent = 'Saving reading…';
  try {
    await sendOperator({action:'usage',request_id:crypto.randomUUID(),source:'Owner WSL · Codex app-server',...reading});
    incomingReading = null;
    byId('confirm-import').hidden = true;
    byId('cancel-import').hidden = true;
    byId('import-description').textContent = 'WSL plan reading received.';
    byId('import-windows').textContent = '';
    byId('import-message').textContent = 'The newest accepted reading appears under Codex plan.';
    await readRecord();
  } catch {
    connection = 'offline';
    byId('import-message').textContent = 'Refresh to check the latest saved reading.';
  } finally {
    byId('cancel-import').disabled = false;
    finishRequest();
  }
}

function initialize() {
  byId('refresh').addEventListener('click',refresh);
  byId('control').addEventListener('click',control);
  byId('confirm-import').addEventListener('click',importAllowance);
  byId('cancel-import').addEventListener('click',() => { incomingReading = null; byId('allowance-import').hidden = true; });
  document.addEventListener('visibilitychange',() => { if (!document.hidden) refresh(); });
  window.addEventListener('online',refresh);
  window.addEventListener('offline',() => { connection = 'offline'; updateStatus(); });
  const route = () => {
    if (location.hash.startsWith('#sync-allowance=')) { incomingReading = takeAllowance(); setupImport(); }
    if (location.hash === '#connect-meter') byId('connect-meter').open = true;
  };
  window.addEventListener('hashchange',route);
  route();
  setupImport();
  refresh();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',initialize,{once:true});
else initialize();
