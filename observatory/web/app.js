'use strict';

const $ = selector => document.querySelector(selector);
const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;'
})[ch]);
const methodNames = {
  earlier: 'Earlier rule',
  four_weight: 'Four-weight rule',
  candidate: 'Residue certificate',
  grid: 'Denominator-32 grid'
};
const verdicts = {
  valid: 'Verified',
  abstain: 'Abstained',
  unsafe: 'Unsafe'
};
const highlights = [{
  id: 'historical-01',
  kind: 'direct',
  title: 'Direct witness',
  name: 'Why did this pass?',
  weights: [2, 3, 17, 42]
}, {
  id: 'historical-09',
  kind: 'shifted',
  title: 'Shifted witness',
  name: 'Why shift the time?',
  weights: [41, 80, 435, 564]
}, {
  id: 'historical-03',
  kind: 'unsafe',
  title: 'Unsafe return',
  name: 'Why did it fail?',
  weights: [3, 5, 28, 60]
}];
const marks = {
  direct: '<circle cx="12" cy="12" r="7"/><path d="m9 12 2 2 5-6"/>',
  shifted: '<path d="M3 18h18M5 14l5-5 3 2 6-7m-5 0h5v5"/>',
  unsafe: '<circle cx="12" cy="12" r="8"/><path d="m9 9 6 6m0-6-6 6"/>'
};
const icon = kind => `<svg aria-hidden="true" viewBox="0 0 24 24">${marks[kind] || '<path d="M2 14h5l3-8 4 13 3-8h5"/>'}</svg>`;
const state = {
  results: null,
  board: null,
  feed: 'connecting',
  method: 'earlier',
  representation: 'weights',
  controlTime: '1/15',
  panel: 'fresh',
  route: '',
  selectedCase: '',
  artifactError: false
};
const statuses = {
  connecting: 'Connecting',
  live: 'Connected',
  snapshot: 'Snapshot',
  disconnected: 'Feed lost',
  unavailable: 'No feed'
};
const esc = escapeHtml;
const cap = value => String(value || '').replace(/^./, c => c.toUpperCase());
const pretty = str => String(str ?? '').replaceAll('_', ' ');
const dash = '—';
const pct = (part, total) => total ? 100 * part / total : 0;
const formatTime = raw => {
  const date = new Date(raw);
  return raw && !isNaN(date) ? date.toISOString().replace('T', ' ').slice(0, 19) + ' UTC' : 'Time unavailable';
};
const timeTag = raw => `<time datetime="${esc(raw)}">${esc(formatTime(raw))}</time>`;

function duration(seconds) {
  if (seconds == null || !Number.isFinite(Number(seconds))) return 'Unrecorded';
  const s = Math.max(0, Math.floor(seconds));
  return s < 60 ? `${s}s` : s < 3600 ? `${Math.floor(s / 60)}m ${s % 60}s` : `${Math.floor(s / 3600)}h ${Math.floor(s % 3600 / 60)}m`;
}

function pill(state, label) {
  return `<span class="pill ${esc(state)}">${esc(label || verdicts[state] || cap(state))}</span>`;
}

function namedRow(entry) {
  return state.results?.rows.find(row => row.panel === 'historical' && String(row.weights) === String(entry.weights));
}

function hashFor(entry) {
  return '#case/' + encodeURIComponent(namedRow(entry)?.id || entry.id);
}

function caseCards() {
  return `<div class="cards">${highlights.map(item => `<a class="case-card" href="${hashFor(item)}"><span class="case-icon ${item.kind}">${icon(item.kind)}</span><h3>${item.title}</h3><small>${item.weights.join(', ')}</small><span class="case-action">${item.name}</span></a>`).join('')}</div>`;
}

function getRoute() {
  return location.hash.slice(1) || 'board';
}

function getRow() {
  return state.results?.rows.find(row => row.id === state.route.split('/')[1]);
}

function navTab() {
  return state.route === 'activity' ? 'activity' : state.route === 'board' ? 'board' : 'evidence';
}

function topNav() {
  document.querySelectorAll('[data-nav]').forEach(link => {
    if (link.dataset.nav === navTab()) link.setAttribute('aria-current', 'page');else link.removeAttribute('aria-current');
  });
  const badge = $('#feed-label');
  badge.textContent = statuses[state.feed];
  badge.className = 'feed-label ' + state.feed;
}

function evidenceNav(active) {
  return `<div class="tabs" aria-label="Evidence views">${[['evidence', 'Panel comparison'], ['controls', 'Input controls']].map(([path, name]) => `<a href="#${path}" ${path === active ? 'aria-current="page"' : ''}>${name}</a>`).join('')}</div>`;
}

function feedNotice() {
  if (state.feed === 'disconnected') return '<div class="notice" role="status">Connection lost. The board is showing the last state received from the executor.</div>';
  if (state.feed === 'unavailable') return '<div class="notice" role="status">The executor and its saved snapshot could not be reached. Worker activity is unknown.</div>';
  if (state.board?.mode === 'stale' || state.board?.stale_workers?.length) return '<div class="notice" role="status">Overdue heartbeat. The executor has lost contact with a worker.</div>';
  return '';
}

function unsetEvidence() {
  return `<div class="notice" role="status">${state.artifactError ? 'The checked results file could not be loaded.' : 'Loading the checked results…'}</div>`;
}

function gcd(a, b) {
  while (b) {
    [a, b] = [b, a % b];
  }
  return a;
}

function fraction(n, d) {
  const g = gcd(n, d);
  return d / g === 1n ? String(n / g) : `${n / g}/${d / g}`;
}

function distances(speeds, time) {
  const [p, q = 1n] = time.split('/').map(BigInt);
  return speeds.map(speed => {
    const residue = BigInt(speed) * p % q;
    const nearest = residue < q - residue ? residue : q - residue;
    return {
      speed,
      residue,
      q,
      nearest,
      clearance: fraction(nearest, q)
    };
  });
}

function chart(speeds, result, large = false) {
  if (!result?.time || !speeds?.length) return '';
  const entries = distances(speeds, result.time);
  const groups = new Map();
  entries.forEach(entry => {
    const key = entry.residue.toString();
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(entry);
  });
  const cx = 192,
    cy = 126,
    r = 75;
  const pos = (turn, radius) => [cx + Math.sin(2 * Math.PI * turn) * radius, cy - Math.cos(2 * Math.PI * turn) * radius].map(n => n.toFixed(2));
  const radial = (turn, start, end, color, width) => {
    const [x1, y1] = pos(turn, start),
      [x2, y2] = pos(turn, end);
    return `<path d="M${x1} ${y1}L${x2} ${y2}" stroke="${color}" stroke-width="${width}"/>`;
  };
  const ticks = Array.from({
    length: 48
  }, (_, i) => radial(i / 48, 91, i % 4 === 0 ? 99 : 94, i % 4 === 0 ? '#8cac98' : '#638472', .8)).join('');
  const [x1, y1] = pos(-1 / 16, 85),
    [x2, y2] = pos(1 / 16, 85);
  let dots = '';
  groups.forEach(members => {
    const {
      residue,
      q
    } = members[0];
    const turn = Number(residue) / Number(q);
    const isLimit = members.some(m => result.limiting_speeds?.includes(m.speed));
    dots += radial(turn, 22, r - 4, '#466d58', .7);
    members.forEach((m, i) => {
      const [x, y] = pos(turn, r - i * 7);
      dots += `<circle cx="${x}" cy="${y}" r="3.5" stroke="#15352e" fill="${isLimit ? '#f4b786' : '#bfdfa9'}"/>`;
    });
  });
  const cleanTime = esc(result.time),
    cleanMin = esc(result.clearance);
  return `<svg role="img" aria-label="Runner positions at time ${cleanTime}. Minimum clearance ${cleanMin}. Limiting speeds ${esc(result.limiting_speeds?.join(', '))}." viewBox="0 0 385 257" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#66896f" stroke-width=".8"><circle cx="${cx}" cy="${cy}" r="90" stroke-dasharray="1 4"/><circle cx="${cx}" cy="${cy}" r="${r}"/><circle cx="${cx}" cy="${cy}" r="51" stroke-dasharray="2 5"/><path d="M78 ${cy}h228M${cx} 16v221" stroke="#5d7a635e"/></g>${ticks}<path d="M${x1} ${y1}A85 85 0 0 1 ${x2} ${y2}" stroke="#e8a878" stroke-width="3" fill="none"/>${dots}<path d="m${cx} 47 -3.5 5.5h7z" fill="#f1f4dc"/><circle cx="${cx}" cy="${cy}" r="17" fill="#173731" stroke="#5f8069"/><text x="${cx}" y="${cy + 4}" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#e1edcd">t</text><g fill="#b3cbb4" font-family="monospace" font-size="8"><text x="${cx}" y="17" text-anchor="middle">0</text><text x="304" y="129">¼</text><text x="${cx}" y="237" text-anchor="middle">½</text><text x="78" y="129" text-anchor="end">¾</text></g>${large ? '<g font-family="monospace" font-size="8.5" letter-spacing=".8" fill="#cce2c7"><text x="14" y="17">RUNNER PHASES</text><text x="371" y="246" text-anchor="end">t = ' + cleanTime + '</text></g>' : ''}</svg>`;
}

function sourceLine() {
  const board = state.board;
  if (!board) return state.feed === 'connecting' ? 'Connecting to the executor…' : 'Worker status unavailable.';
  const kind = state.feed === 'snapshot' ? 'Historical snapshot' : state.feed === 'disconnected' ? 'Last known state' : 'Executor feed';
  return `${kind} · ${esc(pretty(board.mode || 'unknown'))}`;
}

function jobStatus(job) {
  return job.stale ? 'stale' : job.state;
}

function lastStamp() {
  const board = state.board;
  return board ? `<div class="last-time">Last event ${timeTag(board.last_event_at)}${state.feed === 'snapshot' ? `<br>Snapshot ${timeTag(board.generated_at)}` : ''}</div>` : '';
}

function jobsShort() {
  const jobs = state.board?.jobs || [];
  const grouped = new Map();
  jobs.forEach(job => {
    const key = job.role || 'Worker';
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key).push(job);
  });
  const summary = [...grouped].map(([role, items]) => {
    const latest = items.slice().sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
    const job = ['stale', 'failed', 'running', 'queued', 'completed'].map(s => latest.find(j => jobStatus(j) === s)).find(Boolean) || latest[0];
    return `<div class="mini-job"><strong>${esc(cap(role))}</strong>${pill(jobStatus(job))}<small title="${esc(job.task)}">${esc(job.task)}</small></div>`;
  }).join('');
  return `<div class="line-head"><h2>Worker status</h2><a href="#activity">Assignments</a></div><p class="team-summary">${sourceLine()}</p><div class="mini-jobs">${summary}</div>${lastStamp()}`;
}

function latestFinding() {
  const failure = state.results?.rows.find(row => row.id === 'fresh-04');
  const probe = failure?.exploratory_witness;
  if (probe?.status === 'valid') return {
    text: `Five runners collide at ${probe.anchor}, yet a shift clears all fifteen. The earlier rule’s one-collision start failed.`,
    href: '#case/fresh-04/exploratory',
    label: 'Latest finding · after scoring'
  };
  return {
    text: 'Nine of ten earlier-only successes share a clear denominator. The tenth needs a shift.',
    href: hashFor(highlights[1])
  };
}

function home() {
  const direct = namedRow(highlights[0]);
  const result = direct?.methods.earlier;
  const finding = latestFinding();
  return `<div id="operating-notice">${feedNotice()}</div>
      <section class="hero">
      <div class="hero-copy"><span class="eyebrow">Current investigation</span>
      <h1>Can four weights predict a lonely time?</h1>
      <p>The earlier rule found a time in ten middle-gap lineups where the four-weight rule abstained. Which calculation made the difference?</p>
      <div class="scope"><span><b>16</b> total runners</span><span><b>1/16</b> threshold</span><span>Reference <b>0</b></span>
      </div>
      </div>
      <figure class="hero-figure">${result ? `<a href="${hashFor(highlights[0])}" aria-label="Inspect the runner positions in the direct witness">${chart(direct.speeds, result, true)}</a>` : '<span class="eyebrow">Awaiting exact evidence</span>'}</figure></section>
  <section class="finding"><div class="signal">${icon('signal')}</div><div><span class="kicker">${esc(finding.label || 'Opened-panel finding')}</span><h2>${esc(finding.text)}</h2></div><a href="${finding.href}"><span class="read-label">See </span>evidence</a>
      </section>
  <div class="home-grid">
      <div>
      <section class="section">
      <div class="section-head">
      <h2>Featured cases</h2><a href="#evidence">All evidence</a></div>${caseCards()}</section>
      <aside class="decision"><span class="sigil" aria-hidden="true">◇</span>
      <div><span class="kicker">Decision for Vance</span>
      <p>Should the next rule choose a starting time by how far it can safely shift, or try more denominators?</p>
      </div>
      </aside>
      </div>
      <section class="panel team-card" id="worker-summary">${jobsShort()}</section></div>`;
}

function chartPanel(panel) {
  const summary = state.results.summaries[panel],
    total = summary.cases;
  const counts = Object.entries(methodNames).map(([key, name]) => {
    const m = summary.methods[key];
    const label = `${name}: ${m.valid} verified, ${m.unsafe} unsafe, ${m.abstain} abstained.`;
    return `<div class="measure" aria-label="${esc(label)}"><span>${name}</span><div class="bar" aria-hidden="true">${['valid', 'unsafe', 'abstain'].filter(s => m[s]).map(s => `<i class="${s}" style="width:${pct(m[s], total)}%"></i>`).join('')}</div><strong>${m.valid}/${total}</strong></div>`;
  }).join('');
  const ranks = summary.overlaps.earlier_vs_candidate;
  return `<section class="panel"><span class="kicker">${panel === 'fresh' ? 'Tested after freeze' : 'Previously opened'}</span><h2>${panel === 'fresh' ? 'Fresh panel' : 'Historical panel'}</h2><div class="legend">${['valid', 'unsafe', 'abstain'].map(s => `<span class="key ${s}"><i></i>${verdicts[s]}</span>`).join('')}</div>${counts}<p class="small">Earlier and residue rules both passed ${ranks.both}. Earlier alone passed ${ranks.left_only}, residue alone ${ranks.right_only}, and neither passed ${ranks.neither}.</p>
      <details class="detail-block">
      <summary>Outcome counts and work measured</summary>
      <table class="basic-table">
      <thead>
      <tr><th>Method</th><th>Verified</th><th>Unsafe</th><th>Abstained</th>
      </tr>
      </thead>
      <tbody>${Object.entries(methodNames).map(([k, n]) => {
    const m = summary.methods[k];
    return `<tr><td>${n}</td><td>${m.valid}</td><td>${m.unsafe}</td><td>${m.abstain}</td></tr>`;
  }).join('')}</tbody></table>${summary.work ? `<p class="small">The residue rule read ${summary.work.candidate.weights_read} weights and made ${summary.work.candidate.mask_updates} residue-set updates. The earlier rule read ${summary.work.earlier.physical_speeds_read} speeds and made ${summary.work.earlier.speed_divisibility_tests_for_ranking} divisibility tests to rank denominators. These are operation counts.</p>` : ''}</details></section>`;
}

function rowList() {
  const rows = state.results.rows.filter(row => row.panel === state.panel);
  return `<div class="segmented" aria-label="Panel for case list">${['fresh', 'historical'].map(panel => `<button type="button" data-panel="${panel}" aria-pressed="${state.panel === panel}">${cap(panel)}</button>`).join('')}</div><div class="row-links" style="margin-top:12px">${rows.map(row => `<a href="#case/${encodeURIComponent(row.id)}"><span>${esc(row.weights.join(', '))}</span></a>`).join('')}</div>`;
}

function evidence() {
  const head = `<div class="page-head"><span class="kicker">Exact evidence</span>
      <h1>Prediction ledger</h1>
      <p>One returned time per predictor, checked against all 15 moving speeds. The grid can inspect multiple times.</p>
      </div>${evidenceNav('evidence')}`;
  const r = state.results;
  if (!r) return head + unsetEvidence();
  const baseline = r.historical_baseline;
  return head + `<div class="comparison">${chartPanel('fresh')}${chartPanel('historical')}</div>
      <section class="section">
      <div class="section-head">
      <h2>Inspect a lineup</h2>
      </div>
      <p class="small" style="margin-bottom:10px">Twelve stretched middle-gap cases per panel, three from each scale band.</p>
      <div id="row-list">${rowList()}</div>
      </section>
      <section class="panel section"><span class="kicker">Historical replay · all gap patterns</span>
      <h2>Earlier 60-case baseline</h2>
      <p class="subline">The earlier rule passed ${baseline.earlier_valid} of ${baseline.cases}, the four-weight rule passed ${baseline.four_weight_valid} and abstained on ${baseline.four_weight_abstain}. The grid found a witness in ${baseline.grid_valid}.</p><details class="detail-block"><summary>Revision and replay</summary>${provenance()}</details></section>`;
}

function provenance(row) {
  const data = state.results;
  return `<dl class="info-list"><dt>Scope</dt><dd>${esc(data.scope)}</dd><dt>Claim</dt><dd>${esc(row?.claim_status || 'OBSERVED / REPRODUCED')}</dd><dt>Source revision</dt><dd><code>${esc(data.source_revision)}</code></dd><dt>Seal revision</dt><dd><code>${esc(data.seal_revision)}</code></dd><dt>Frozen rule</dt><dd><code>${esc(data.rule_revision)}</code></dd></dl><pre>${esc(data.replay_command)}${row ? ` --case ${esc(row.id)}` : ''}</pre><a class="text-link" href="./results.json">Complete machine-readable result</a>`;
}

function selectCase(row) {
  return `<div class="case-nav">
      <label for="case-select">Switch lineup</label>
      <select id="case-select">${['historical', 'fresh'].map(panel => `<optgroup label="${cap(panel)}">${state.results.rows.filter(r => r.panel === panel).map(r => `<option value="${esc(r.id)}" ${r.id === row.id ? 'selected' : ''}>${esc(r.weights.join(', '))}</option>`).join('')}</optgroup>`).join('')}</select></div>`;
}

function fullMethods(row) {
  return row.exploratory_witness ? {
    ...row.methods,
    exploratory: row.exploratory_witness
  } : row.methods;
}

function describeRow(row) {
  if (row.id === 'historical-01') return 'Why did this pass? No moving speed is divisible by 12. At time 1/12, the nearest any runner can come to zero is 1/12 of a lap.';
  if (row.id === 'historical-09') return 'Each denominator from 2 to 16 divides at least one speed. The earlier rule starts at 1/9 and shifts to a time where clearance meets the threshold exactly.';
  if (row.id === 'historical-03') return 'The earlier rule returned an unsafe time. The four-weight rule abstained. The grid found a witness, and a later check tested a different starting time.';
  if (row.id === 'fresh-04') return 'The earlier rule picked a starting time with one collision and returned an unsafe shift. Five runners collide at the later starting time tested after scoring.';
  return 'All four predictors were compared on this lineup. Select a method to inspect its proposed time and the independent clearance check.';
}

function caseDetails(row) {
  const method = fullMethods(row)[state.method] || row.methods.earlier,
    limit = method.limiting_speeds || [];
  const names = {
    ...methodNames,
    exploratory: 'Post-score shift'
  };
  const methods = Object.keys(fullMethods(row));
  const action = method.status === 'abstain' ? 'This rule returned no time. There is no proposed time to check.' : `${limit.length === 1 ? 'Speed' : 'Speeds'} <strong>${esc(limit.join(', '))}</strong> ${limit.length === 1 ? 'sets' : 'set'} the minimum distance to the stationary runner. ${method.status === 'unsafe' ? 'The returned time is below the threshold.' : method.clearance === state.results.threshold ? 'Equality meets the inclusive threshold.' : 'The distance exceeds the threshold.'}`;
  const numbers = state.representation === 'weights' ? row.weights : row.speeds;
  return `<div class="case-layout">
      <section class="panel"><span class="kicker">Exact check</span>
      <div class="line-head">
      <h2>Returned time</h2>${pill(method.status)}</div><div class="segmented" aria-label="Prediction method">${methods.map(k => `<button type="button" data-method="${k}" aria-pressed="${k === state.method}">${names[k]}</button>`).join('')}</div><div class="metrics">${[['Proposed time', method.time || dash], ['Actual clearance', method.clearance ?? dash], ['Threshold', '≥ ' + state.results.threshold]].map(([k, v]) => `<dl class="metric"><dt>${k}</dt><dd>${esc(v)}</dd></dl>`).join('')}</div><p class="exact-line">${action}</p>${method.time ? `<div class="axis-plot">${chart(row.speeds, method)}</div>
      <div class="legend"><span class="key" style="--dot:#bd8a5b"><i></i>Limiting speed</span><span class="key" style="--dot:#71946b"><i></i>Other runner</span>
      </div>` : ''}${state.method === 'exploratory' ? '<p class="method-note">This time was tested after scoring. The frozen prediction and panel totals retain their original outcomes.</p>' : ''}</section>
  <section class="panel"><span class="kicker">Same lineup</span>
      <h2>What the rule sees</h2>
      <p class="subline small">Every nonempty subset of the four weights gives one moving speed. All runners start together.</p>
      <div class="segmented" style="margin-top:14px" aria-label="Lineup representation">${[['weights', 'Four weights'], ['speeds', '15 speeds']].map(([k, v]) => `<button type="button" data-representation="${k}" aria-pressed="${k === state.representation}">${v}</button>`).join('')}</div><div class="numbers">${numbers.map(v => `<span class="number ${state.representation === 'speeds' && limit.includes(v) ? 'limit' : ''}">${esc(v)}</span>`).join('')}</div><p class="small">Clear denominators from 2 through 16: <strong>${row.clear_denominators.length ? esc(row.clear_denominators.join(', ')) : 'none'}</strong>.</p>
      <div class="detail-block"><span class="kicker">Selection</span>
      <p class="small">${esc(selectionText(row, method))}</p></div>${method.work ? `<details class="detail-block"><summary>Inputs and work</summary><dl class="info-list">${Object.entries(method.work).map(([k, v]) => `<dt>${esc(cap(pretty(k)))}</dt><dd>${esc(v)}</dd>`).join('')}</dl></details>` : ''}${method.time ? `<details class="detail-block">
      <summary>All exact runner distances</summary>
      <table class="basic-table">
      <thead>
      <tr><th>Moving speed</th><th>Distance in laps</th>
      </tr>
      </thead>
      <tbody>${distances(row.speeds, method.time).map(m => `<tr><td>${m.speed}${limit.includes(m.speed) ? ' · limiting' : ''}</td><td>${m.clearance}</td></tr>`).join('')}</tbody></table></details>` : ''}</section></div>`;
}

function selectionText(row, method) {
  if (state.method === 'candidate') return `From the four weights, update reachable subset-sum residues modulo each denominator. Return the first reciprocal with no zero residue. ${method.status === 'abstain' ? 'All tested denominators were blocked.' : 'The checker then inspects the 15 physical speeds.'}`;
  if (state.method === 'earlier') {
    const c = method.choices;
    return c ? `Rank denominators using the 15 speeds. At ${c.anchor}, ${c.colliding_speeds.length} moving ${c.colliding_speeds.length === 1 ? 'speed collides' : 'speeds collide'} with zero. The selected shift is ${c.shift} of a time unit.` : 'Rank candidate denominators using speed divisibility, then test a shift when the anchor has a collision.';
  }
  if (state.method === 'exploratory') return `At ${method.anchor}, speeds ${method.colliding_speeds.join(', ')} collide with zero. A shift of ${method.shift} reaches ${method.time}.`;
  if (state.method === 'grid') return `Examine reduced times up to denominator 32 against all 15 speeds. Return the first verified time in denominator order.`;
  return `Read the four weights and test seven certificate branches in order. ${method.status === 'abstain' ? 'None supplied a time.' : `The ${pretty(method.branch)} branch supplied this time.`}`;
}

function auditedWindow(row) {
  if (row.id !== 'fresh-04' || row.exploratory_witness?.time !== '625/1872') return '';
  return `<section class="panel section">
    <span class="kicker">Independent post-score audit · OBSERVED</span>
    <h2>The first safe window after 1/3</h2>
    <p class="subline">Every moving runner clears the threshold throughout the closed interval
      <strong>[625/1872, 1375/4112]</strong>. Speed 117 sets the minimum at the left endpoint,
      and speed 257 sets it at the right. Both endpoints count.</p>
    <details class="detail-block"><summary>Check the endpoints</summary>
      <p class="small">The verifier ordered every threshold crossing and checked the endpoints and
        interior cells separately. Speed 117 blocks immediately before entry and speed 257 blocks immediately after exit.</p>
      <pre>python observatory/study/verify_shift.py</pre>
      <a href="https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/implement/lonely-runner-observatory/observatory/study/shift-verification.md">Independent window audit</a>
    </details></section>`;
}

function casePage() {
  const row = getRow();
  if (!row) return `<a class="back" href="#evidence">← Evidence</a>${state.results ? '<p class="notice">That lineup is absent from the published ledger.</p>' : unsetEvidence()}`;
  const named = highlights.find(h => String(row.weights) === String(h.weights));
  const key = row.id === 'fresh-04' ? 'Five collisions, one safe shift' : named?.title || 'Lineup evidence';
  const all = fullMethods(row);
  return `<a class="back" href="#evidence">← Prediction ledger</a>
      <div class="case-intro"><span class="kicker">${esc(cap(row.panel))} panel · ${esc(row.id)} · ${esc(row.claim_status)}</span><h1>${key}</h1><h2 style="font:normal 20px var(--mono);margin-top:8px">(${esc(row.weights.join(', '))})</h2><p>${describeRow(row)}</p></div><div class="section" id="case-inspect">${caseDetails(row)}</div>
      <section class="panel section">
      <h2>Method comparison</h2>
      <table class="basic-table">
      <thead>
      <tr><th>Method</th><th>Outcome</th><th>Time</th><th>Clearance</th>
      </tr>
      </thead>
      <tbody>${Object.entries(all).map(([k, m]) => `<tr><td>${methodNames[k] || 'Post-score shift'}</td><td>${verdicts[m.status]}</td><td>${esc(m.time || dash)}</td><td>${esc(m.clearance ?? dash)}</td></tr>`).join('')}</tbody></table>${row.exploratory_witness ? '<p class="small" style="margin-top:10px">The post-score shift is an exploratory observation outside the scored comparison.</p>' : ''}<details class="detail-block"><summary>Source, scope and replay command</summary>${provenance(row)}</details>${selectCase(row)}</section>${auditedWindow(row)}`;
}

function controlOutput() {
  const data = state.results.reduced_record,
    key = state.controlTime === '1/15' ? 'at_1_15' : 'at_1_16',
    under = data[key] === 'underdetermined';
  return `<div class="segmented" aria-label="Proposed time">${['1/15', '1/16'].map(t => `<button type="button" data-control="${t}" aria-pressed="${state.controlTime === t}">t = ${t}</button>`).join('')}</div><div class="control-output"><h3>${under ? 'Underdetermined by this record' : 'Supported answer: no'}</h3><p>${under ? 'Two lineups fit exactly the same record and give opposite answers. The extrema and family leave the interior speeds unresolved.' : 'The known maximum speed 112 completes seven laps at 1/16 and meets the stationary runner. Every lineup matching the record therefore has zero clearance at this time.'}</p>
      <table class="basic-table">
      <thead>
      <tr><th>Full weights</th><th>Answer</th><th>Clearance</th><th>Limiting speeds</th>
      </tr>
      </thead>
      <tbody>${data.cases.map(c => `<tr><td>${esc(c.weights.join(', '))}</td><td>${c[key].status === 'valid' ? 'Yes' : 'No'}</td><td>${esc(c[key].clearance)}</td><td>${esc(c[key].limiting_speeds.join(', '))}</td></tr>`).join('')}</tbody></table><p class="small" style="margin-top:12px">${under ? 'In the first completion, speed 15 returns to zero. In the second, all 15 moving speeds stay at least 1/15 of a lap away.' : 'The interior speeds determine which other runners join the collision. Speed 112 alone settles the yes-or-no question.'}</p></div>`;
}

function controls() {
  const head = `<div class="page-head"><span class="kicker">Representation controls</span>
      <h1>What can the input settle?</h1>
      <p>At a proposed time, does every moving runner clear the stationary reference by at least 1/16 of a lap?</p>
      </div>${evidenceNav('controls')}`;
  const r = state.results;
  if (!r?.reduced_record) return head + unsetEvidence();
  const e = r.equality_control;
  return head + `<section class="panel"><span class="kicker">Reduced input</span>
      <h2>Same extrema, same family</h2>
      <p class="subline">The shared record gives the smallest speed as 1 and the largest as 112. There are 16 common-start runners, including the stationary reference. The 15 moving speeds are all nonempty subset sums of four positive superincreasing weights, with gcd one and total divisible by 16.</p>
      <p class="small" style="margin:12px 0">Choose the proposed time to see whether those facts determine the answer. The full weights below reveal what each completion actually does.</p>
      <div id="control-inspect">${controlOutput()}</div></section><section class="panel section"><span class="kicker">${esc(e.claim_status)} · inclusive threshold</span>
      <h2>Equality counts</h2>
      <p class="subline">For speeds 0 through 15 at time ${esc(e.time)}, the nearest runners have speeds ${esc(e.limiting_speeds.join(' and '))}. Both are exactly ${esc(e.clearance)} of a lap from zero. The result passes.</p>
      <details class="detail-block">
      <summary>Reproduce these controls</summary>${provenance()}</details></section>`;
}

function workerCard(job) {
  const source = {
    'recorded-research': 'Recorded research assignment',
    'deterministic-replay': 'Local replay assignment',
    'operator-assignment': 'Operator assignment'
  }[job.source] || pretty(job.source);
  const artifact = artifactRef(job.artifact);
  return `<article class="panel job"><span class="kicker">${esc(source)}</span><div class="line-head"><h2>${esc(cap(job.role))}</h2>${pill(jobStatus(job), job.stale ? 'Heartbeat overdue' : null)}</div><p>${esc(job.task)}</p><dl class="info-list"><dt>Last update</dt><dd>${timeTag(job.updated_at)}</dd><dt>Elapsed</dt><dd>${esc(duration(job.elapsed_seconds))}</dd><dt>Attempt</dt><dd>${esc(job.attempt ?? dash)}</dd><dt>Depends on</dt><dd>${esc((job.dependencies || []).join(', ') || 'None')}</dd>${job.claim_status ? `<dt>Research claim</dt><dd>${esc(job.claim_status)}</dd>` : ''}${job.lease_expires ? `<dt>Lease expiry</dt><dd>${timeTag(job.lease_expires)}</dd>` : ''}${artifact ? `<dt>Artifact</dt><dd>${artifact}</dd>` : ''}</dl></article>`;
}

function artifactRef(path) {
  if (!path) return '';
  if (path === 'observatory/study/results.json') return '<a href="./results.json">Published results</a>';
  const safePath = String(path).split('/');
  if (!safePath.every(p => /^[\w.-]+$/.test(p) && p !== '.' && p !== '..')) return `<code>${esc(path)}</code>`;
  const branch = 'https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/implement/lonely-runner-observatory/';
  return `<a href="${branch}${safePath.map(encodeURIComponent).join('/')}"><code>${esc(path)}</code></a>`;
}

function eventRows(board) {
  return [...(board.events || [])].reverse().map(e => `<article class="event">${timeTag(e.time)}${pill(e.state)}<div><strong>${esc(cap(e.role))}</strong> · ${esc(e.task)}${e.artifact ? `<div>${artifactRef(e.artifact)}</div>` : ''}</div></article>`).join('');
}

function activityDetails() {
  const b = state.board;
  if (!b) return feedNotice() || '<p>Waiting for the executor…</p>';
  const p = b.pilot || {},
    unfinished = b.unfinished || [];
  const historical = state.feed === 'snapshot',
    lost = state.feed === 'disconnected';
  return `${feedNotice()}<div class="two-col">
      <section class="panel"><span class="kicker">Operating state</span>
      <div class="line-head">
      <h2>${esc(historical ? 'Historical snapshot' : lost ? 'Last known state' : 'Worker host')}</h2>${pill(b.mode)}</div><p>${historical ? 'Read-only copy of the worker host at the capture time.' : lost ? 'The connection failed after the last successful response.' : 'Read-only connection to the executor on this host.'}</p><dl class="info-list"><dt>${historical ? 'Captured' : 'State received'}</dt><dd>${timeTag(b.generated_at)}</dd><dt>Last action</dt><dd>${timeTag(b.last_event_at)}</dd><dt>Study claim</dt><dd>${esc(b.claim_status)}</dd><dt>Unfinished</dt><dd>${esc(unfinished.join(', ') || 'None')}</dd></dl></section><section class="panel"><span class="kicker">Pilot budget</span><h2>${p.enabled ? p.stop_reason ? 'Pilot stopped' : 'Pilot enabled' : 'Pilot inactive'}</h2><dl class="info-list"><dt>Dispatches</dt><dd>${p.dispatches_used ?? dash} used · ${p.dispatches_remaining ?? dash} remaining of ${p.max_dispatches ?? dash}</dd><dt>Model calls</dt><dd>${p.model_calls_used ?? dash} used · ${p.model_calls_remaining ?? dash} remaining of ${p.max_model_calls ?? dash}</dd><dt>Concurrency</dt><dd>${p.concurrency ?? dash} workers</dd>${p.ends_at ? `<dt>Ends</dt><dd>${timeTag(p.ends_at)}</dd>` : ''}${p.next_dispatch_at ? `<dt>Next dispatch</dt><dd>${timeTag(p.next_dispatch_at)}</dd>` : ''}${p.stop_reason ? `<dt>Stop reason</dt><dd>${esc(p.stop_reason)}</dd>` : ''}</dl>
      <details id="operator-detail" class="detail-block">
      <summary>Operator pause and resume</summary>
      <p class="small">On the worker host, run the command against the same database. Pause stops new claims and allows current assignments to finish.</p>
      <pre>python -m observatory pause\npython -m observatory resume</pre>
      </details>
      </section>
      </div>
      <div class="section">
      <div class="section-head">
      <h2>Assignments</h2><span class="small">${b.jobs.length} recorded</span></div><div class="work-grid">${b.jobs.map(workerCard).join('') || '<p>No assignments recorded.</p>'}</div>
      </div>
      <section class="panel section">
      <details id="event-detail">
      <summary>Action history · ${b.events.length} events</summary>${eventRows(b) || '<p>No executor events recorded.</p>'}</details></section>`;
}

function activity() {
  return `<div class="page-head"><span class="kicker">Executor and research history</span>
      <h1>Activity log</h1>
      <p>Follow real assignments, check their dependencies and inspect the event that produced each return.</p>
      </div>
      <div id="activity-data">${activityDetails()}</div>
      <section class="panel section"><span class="kicker">Direction and revisions</span>
      <h2>Why the next assignment changed</h2>
      <p class="subline">On the opened panel, a small shift at a different denominator repaired an unsafe return. The fresh failure then showed that a starting time with more collisions could be easier to repair.</p>
      <p class="subline"><a href="#case/historical-03">Opened-panel correction</a> · <a href="#case/fresh-04">Fresh post-score check</a>
      </p>
      <p class="subline small">Proposed next assignment: freeze a rule that compares the time colliding runners need to move away with the time other runners can safely move. A new sealed panel would test the choice.</p>${state.results ? `<details class="detail-block"><summary>Input, seal and frozen rule revisions</summary>${provenance()}</details>` : ''}</section>`;
}

function replaceContent(selector, html) {
  const element = $(selector);
  if (!element || element._previousHTML === html) return;
  const keepOpen = new Set([...element.querySelectorAll('details[open][id]')].map(el => el.id));
  const focus = document.activeElement;
  const focusId = element.contains(focus) ? focus.closest('details[id]')?.id : null;
  element.innerHTML = html;
  element._previousHTML = html;
  keepOpen.forEach(id => {
    const d = document.getElementById(id);
    if (d) d.open = true;
  });
  if (focusId) document.getElementById(focusId)?.querySelector('summary')?.focus({
    preventScroll: true
  });
}

function render() {
  topNav();
  const route = state.route;
  const html = route === 'board' ? home() : route === 'activity' ? activity() : route === 'evidence' ? evidence() : route === 'controls' ? controls() : route.startsWith('case/') ? casePage() : '<h1>View unavailable</h1><p><a href="#board">Return to the research board</a></p>';
  replaceContent('#page', html);
  $('#page').setAttribute('aria-busy', 'false');
  const title = $('main h1')?.textContent;
  document.title = title ? `${title} · Lonely Runner Observatory` : 'Lonely Runner Observatory';
}

function renderOperatingState() {
  topNav();
  if (state.route === 'board') {
    replaceContent('#worker-summary', jobsShort());
    replaceContent('#operating-notice', feedNotice());
  }
  if (state.route === 'activity') replaceContent('#activity-data', activityDetails());
}

function navigate(initial = false) {
  state.route = getRoute();
  if (state.route.startsWith('case/') && state.selectedCase !== state.route) {
    state.selectedCase = state.route;
    state.method = state.route.split('/')[2] === 'exploratory' ? 'exploratory' : 'earlier';
    state.representation = 'weights';
  }
  render();
  if (!initial) {
    window.scrollTo(0, 0);
    $('#main-content').focus({
      preventScroll: true
    });
  }
}

function pressUpdate(target, selector, markup) {
  const dataName = Object.keys(target.dataset)[0],
    value = target.dataset[dataName];
  replaceContent(selector, markup);
  const buttons = $(selector)?.querySelectorAll('button');
  [...(buttons || [])].find(b => b.dataset[dataName] === value)?.focus({
    preventScroll: true
  });
}
document.addEventListener('click', event => {
  const b = event.target.closest('button');
  if (!b) return;
  if (b.dataset.method) {
    state.method = b.dataset.method;
    pressUpdate(b, '#case-inspect', caseDetails(getRow()));
  }
  if (b.dataset.representation) {
    state.representation = b.dataset.representation;
    pressUpdate(b, '#case-inspect', caseDetails(getRow()));
  }
  if (b.dataset.control) {
    state.controlTime = b.dataset.control;
    pressUpdate(b, '#control-inspect', controlOutput());
  }
  if (b.dataset.panel) {
    state.panel = b.dataset.panel;
    pressUpdate(b, '#row-list', rowList());
  }
});
document.addEventListener('change', event => {
  if (event.target.id === 'case-select') location.hash = 'case/' + encodeURIComponent(event.target.value);
});
window.addEventListener('hashchange', () => navigate());

async function loadJSON(path) {
  const controller = new AbortController(),
    timeout = setTimeout(() => controller.abort(), 4000);
  try {
    const response = await fetch(path, {
      cache: 'no-store',
      signal: controller.signal
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

function validateBoard(b) {
  if (!b || !Array.isArray(b.jobs) || !Array.isArray(b.events) || !b.generated_at) throw new Error('Invalid executor record');
  return b;
}

async function updateBoard() {
  try {
    const data = validateBoard(await loadJSON('/api/board'));
    if (data.source !== 'local-executor') throw new Error('Not a worker feed');
    state.board = data;
    state.feed = 'live';
  } catch {
    if (state.board && state.board.source !== 'snapshot') {
      state.feed = 'disconnected';
    } else if (!state.board) {
      try {
        const snapshot = validateBoard(await loadJSON('./snapshot.json'));
        state.board = {
          ...snapshot,
          source: 'snapshot'
        };
        state.feed = 'snapshot';
      } catch {
        state.feed = 'unavailable';
      }
    }
  }
  renderOperatingState();
}

async function loadResults() {
  try {
    const data = await loadJSON('./results.json');
    if (data.schema_version !== 1 || !Array.isArray(data.rows) || !data.summaries) throw new Error('Invalid evidence record');
    state.results = data;
    state.artifactError = false;
  } catch {
    state.artifactError = true;
  }
  render();
}

async function refreshLoop() {
  await updateBoard();
  if (state.artifactError) await loadResults();
  setTimeout(refreshLoop, state.feed === 'snapshot' ? 30000 : 5000);
}
navigate(true);
loadResults();
refreshLoop();
