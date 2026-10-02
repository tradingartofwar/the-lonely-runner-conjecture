#!/usr/bin/env python3
"""Build the self-contained, read-only evidence viewer. Run from any directory.

The page displays saved exact outputs. Its JavaScript converts fractions to
floating-point positions only for drawing; it performs no feasibility checks.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = ("fixtures.json", "results.json", "sympy_periodic/report.json")


def main() -> None:
    inputs = {}
    hashes = {}
    for name in FILES:
        raw = (HERE / name).read_bytes()
        inputs[name] = json.loads(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    if inputs["results.json"]["fixture_sha256"] != hashes["fixtures.json"]:
        raise ValueError("Saved results do not match the current fixtures.json")
    hashes["build_demo.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    bundle = {"inputs": inputs, "sha256": hashes}
    encoded = json.dumps(bundle, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    output = HTML.replace("__EVIDENCE_JSON__", encoded)
    (HERE / "index.html").write_text(output, encoding="utf-8")
    print(f"Built {HERE / 'index.html'} ({len(output.encode('utf-8')):,} bytes)")


HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; font-src 'none'; base-uri 'none'">
<title>Compatibility • Exact evidence, kept in view</title>
<style>
:root{--paper:#f4f1e9;--surface:#fffdf8;--navy:#152c3c;--ink:#243d4b;--muted:#5b6c73;--line:#dcded6;--teal:#14766c;--teal-soft:#e3f0e9;--coral:#ae4b35;--coral-soft:#faeae2;--focus:#225aa0;--mono:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;--sans:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55}button,select{font:inherit}button{cursor:pointer}button:focus-visible,select:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--focus);outline-offset:4px}button{touch-action:manipulation}a{color:var(--teal)}.shell{max-width:1320px;padding:0 42px;margin:auto}.masthead{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:25px 0;border-bottom:1px solid var(--line)}.brand{font-size:13px;letter-spacing:.16em;font-weight:750;color:var(--navy)}.brand span{color:var(--teal)}.quiet-label{font-size:12px;color:var(--muted);letter-spacing:.035em}.hero{display:grid;grid-template-columns:1.5fr 1fr;gap:50px;align-items:end;padding:42px 0 35px}.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:750;color:var(--teal);margin:0 0 11px}h1{font-size:clamp(30px,3.8vw,47px);line-height:1.13;letter-spacing:-.043em;color:var(--navy);font-weight:650;margin:0;max-width:650px}h2{font-size:clamp(23px,2.1vw,30px);line-height:1.2;letter-spacing:-.025em;color:var(--navy);margin:7px 0 12px;font-weight:650}h3{font-size:15px;color:var(--navy);margin:0;font-weight:650}p{margin:0 0 12px}.hero p{color:var(--muted);font-size:15px;max-width:430px;margin:0}.collections{display:flex;gap:5px;padding:5px;background:#e7e8df;border-radius:10px;margin:0 0 28px;width:fit-content}.collection{border:0;border-radius:6px;background:transparent;color:var(--ink);padding:12px 17px;text-align:left;font-size:13px;font-weight:650}.collection[aria-pressed=true]{background:var(--navy);color:var(--surface)}.collection .count{display:inline-block;margin-left:9px;font-family:var(--mono);font-size:11px;opacity:.75}.workspace{display:grid;grid-template-columns:252px minmax(0,1fr);gap:28px;align-items:start}.sidebar-title{display:flex;justify-content:space-between;align-items:baseline;margin:0 8px 10px;font-size:11px;font-weight:750;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}.case-list{display:grid;gap:5px}.case-button{display:grid;grid-template-columns:24px 1fr;gap:9px;align-items:start;text-align:left;border:1px solid transparent;border-radius:8px;background:transparent;padding:14px 12px;color:var(--muted);width:100%;font-size:13px;line-height:1.45}.case-button .case-num{font-family:var(--mono);font-size:11px;padding-top:2px;color:var(--muted)}.case-button[aria-current=true]{background:var(--surface);border-color:var(--line);color:var(--navy);font-weight:650;box-shadow:0 3px 7px #152c3c04}.case-button[aria-current=true] .case-num{color:var(--teal)}.case-button:hover{background:#fffdf880}.sidebar-note{border-top:1px solid var(--line);margin:22px 10px 0;padding-top:15px;color:var(--muted);font-size:12px}.mobile-picker{display:none}.detail{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 8px 30px #152c3c04}.detail-head{padding:28px 30px 24px}.case-meta{display:flex;gap:12px;flex-wrap:wrap;align-items:center;color:var(--muted);font-size:11px;letter-spacing:.08em;text-transform:uppercase}.status-dot{width:6px;height:6px;border-radius:50%;background:var(--teal);display:inline-block;margin-right:5px}.question{max-width:750px;font-size:16px;line-height:1.5;color:var(--ink);margin:0}.facts{display:flex;flex-wrap:wrap;gap:7px 20px;margin-top:17px;font-size:12px;color:var(--muted)}.facts code{font-family:var(--mono);font-size:12px;color:var(--ink);overflow-wrap:anywhere}.outcomes{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 30px 25px}.outcome{padding:18px 19px;border-radius:8px;background:var(--coral-soft)}.outcome.complete{background:var(--teal-soft)}.outcome-label{font-size:11px;font-weight:750;letter-spacing:.07em;text-transform:uppercase;color:var(--coral);margin:0 0 8px}.complete .outcome-label{color:var(--teal)}.outcome-value{font-size:22px;font-weight:650;color:var(--navy);letter-spacing:-.025em;margin:0 0 6px;line-height:1.2}.outcome-note{font-size:12px;color:var(--ink);margin:0;line-height:1.5}.section{padding:24px 30px;border-top:1px solid var(--line)}.section-heading{display:flex;gap:12px;justify-content:space-between;align-items:baseline;margin-bottom:15px}.small{font-size:12px;color:var(--muted)}.axis-title{font-size:12px;color:var(--muted);margin-top:8px}.plot-lane{margin-bottom:14px}.lane-label{font-size:12px;font-weight:650;color:var(--muted);margin-bottom:1px}.lane-label.complete{color:var(--teal)}.plot{height:85px;width:100%;display:block;overflow:visible}.plot text{font-family:var(--mono);font-size:11px;fill:var(--ink)}.plot .tick{fill:var(--muted);font-size:10px}.plot .empty{fill:var(--muted);font-family:var(--sans);font-size:12px}.legend{display:flex;flex-wrap:wrap;gap:10px 21px;align-items:center;font-size:11px;color:var(--muted);padding-top:6px}.legend-item{display:flex;gap:6px;align-items:center}.dot{display:inline-block;width:8px;height:8px;border:2px solid var(--teal);border-radius:50%}.dot.filled{background:var(--teal)}.singleton-symbol{font-size:14px;color:var(--teal);line-height:1}.plot-note{font-size:12px;color:var(--muted);margin-top:12px;margin-bottom:0}.sets{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:18px}.set-label{font-size:11px;font-weight:750;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:8px}.exact-list{margin:0;padding:0;list-style:none;font-family:var(--mono);font-size:12px;line-height:1.8;display:grid;grid-template-columns:repeat(auto-fit,minmax(166px,1fr));gap:3px 8px;color:var(--ink)}.exact-list .number{font-family:var(--sans);color:var(--muted);font-size:10px;display:inline-block;min-width:21px}.empty-set{font-family:var(--mono);font-size:14px;color:var(--muted)}.lesson{padding:18px 21px;background:#f1f2ea;border-left:3px solid var(--teal);font-size:14px;line-height:1.6;border-radius:0 5px 5px 0}.lesson strong{display:block;color:var(--navy);font-size:11px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}th{color:var(--muted);font-size:11px;font-weight:650;padding:9px 11px 9px 0;border-bottom:1px solid var(--line)}td{padding:10px 11px 10px 0;border-bottom:1px solid #e9eae3;vertical-align:top}tr:last-child td{border-bottom:0}.rational{font-family:var(--mono);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}.target{padding:11px 13px;background:var(--paper);border-radius:5px;font-size:12px;margin-bottom:12px}.equation{font-family:var(--mono);font-size:12px;color:var(--ink);overflow-wrap:anywhere}.equations{display:grid;gap:7px;margin-top:15px}.evidence-controls{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.button{background:var(--surface);border:1px solid #cbd3ce;color:var(--navy);padding:9px 13px;font-size:12px;font-weight:650;border-radius:6px}.button:hover{background:var(--paper)}.button.primary{background:var(--navy);border-color:var(--navy);color:var(--surface)}details{margin-top:15px}summary{cursor:pointer;color:var(--navy);font-size:12px;font-weight:650;padding:8px 0}pre{background:#132b3a;color:#d7e8e4;border-radius:8px;padding:18px;overflow:auto;max-height:420px;font-family:var(--mono);font-size:11px;line-height:1.6;margin:10px 0 0;white-space:pre-wrap;overflow-wrap:anywhere}.provenance{font-size:12px;color:var(--muted);display:grid;gap:8px}.provenance .path{font-family:var(--mono);font-size:11px;color:var(--ink);overflow-wrap:anywhere}.footer{margin:31px 0 28px;padding:21px 0;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr auto;gap:20px;font-size:12px;color:var(--muted)}.footer p{max-width:800px;margin:0}.footer-button{border:0;background:transparent;color:var(--teal);font-size:12px;font-weight:650;padding:0;text-decoration:underline;text-underline-offset:3px;white-space:nowrap}.collection-description{font-size:12px;color:var(--muted);margin:0 0 14px 8px}.live{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}.verify-line{margin-bottom:10px;font-size:12px;color:var(--muted)}.verify-line b{color:var(--teal);font-weight:650}
@media(min-width:1450px){.shell{max-width:1390px}}
@media(max-width:1020px){.shell{padding:0 25px}.workspace{grid-template-columns:215px minmax(0,1fr);gap:18px}.detail-head{padding:24px}.outcomes{padding:0 24px 22px}.section{padding:22px 24px}.hero{gap:25px}.outcome{padding:16px}.sets{gap:15px}}
@media(max-width:760px){.shell{padding:0 18px}.masthead{padding:19px 0;gap:8px}.masthead .quiet-label{font-size:10px;max-width:135px;text-align:right}.hero{grid-template-columns:1fr;gap:17px;padding:29px 0 25px}.hero p{max-width:620px}.hero h1{max-width:530px}.workspace{grid-template-columns:1fr;gap:17px}.case-list,.sidebar-title,.sidebar-note,.collection-description{display:none}.mobile-picker{display:block}.mobile-picker label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.1em;font-weight:750;color:var(--muted);margin:0 0 7px}.mobile-picker select{width:100%;padding:13px 35px 13px 12px;background:var(--surface);border:1px solid var(--line);border-radius:6px;color:var(--navy);font-size:13px}.collections{width:100%;margin-bottom:18px;gap:3px}.collection{flex:1;padding:11px 10px;font-size:12px}.collection .count{margin-left:4px}.detail-head{padding:23px 20px 20px}.section{padding:21px 20px}.outcomes{padding:0 20px 21px;gap:10px}.outcome{padding:14px}.outcome-label{font-size:10px}.outcome-value{font-size:21px}.question{font-size:15px}.facts{gap:6px 15px}.sets{grid-template-columns:1fr;gap:15px}.footer{grid-template-columns:1fr;gap:12px}.section-heading{align-items:start;gap:9px;flex-direction:column}.exact-list{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}}
@media(max-width:420px){.shell{padding:0 13px}.detail-head{padding:20px 16px}.section{padding:20px 16px}.outcomes{padding:0 16px 20px;grid-template-columns:1fr}.outcome{display:grid;grid-template-columns:1fr 1fr;gap:3px 12px}.outcome-label{grid-column:1 / -1;margin-bottom:3px}.outcome-value{font-size:20px;margin:0}.outcome-note{font-size:11px}.brand{font-size:11px}.collection{font-size:11px;padding:10px 8px}.collection .count{font-size:10px}.facts code{font-size:11px}.hero p{font-size:14px}}
@media(prefers-reduced-motion:no-preference){button{transition:background .15s,color .15s}}
@media print{.sidebar,.collections,.evidence-controls,.footer-button{display:none}.workspace{display:block}.detail{box-shadow:none}.shell{padding:0}.hero{padding:20px 0}.footer{margin-top:20px}details:not([open]){display:none}}
</style>
</head>
<body>
<div class="shell">
<header class="masthead"><div class="brand">COMPATIBILITY<span> / </span>IN VIEW</div><div class="quiet-label">Saved exact evidence · Offline viewer</div></header>
<section class="hero"><div><p class="eyebrow">Human–AI research, open to inspection</p><h1>What changes when<br>a model leaves something out?</h1></div><p>Inspect a question, the saved answer and the exact points that matter. These development examples show where a narrower representation loses a needed distinction.</p></section>
<nav class="collections" aria-label="Example collection"><button class="collection" id="collection-conformance" aria-pressed="true">Clock compatibility <span class="count" id="count-conformance"></span></button><button class="collection" id="collection-periodic" aria-pressed="false">Periodic inequalities <span class="count" id="count-periodic"></span></button></nav>
<div class="workspace"><aside class="sidebar" aria-label="Choose an example"><div class="sidebar-title"><span>Development examples</span><span id="nav-count"></span></div><p class="collection-description" id="collection-description"></p><div class="case-list" id="case-list"></div><div class="mobile-picker"><label for="case-select">Choose an example</label><select id="case-select"></select></div><p class="sidebar-note">The page displays saved outputs. It does not run a solver or certify a new input.</p></aside><main class="detail" id="detail"></main></div>
<footer class="footer"><p>Known development cases, verified within their stated scope. Intentional misuse examples are not competing methods or third-party bugs. These results establish neither a general Lonely Runner proof nor a demonstrated external benefit.</p><button class="footer-button" id="download-bundle">Download embedded evidence</button></footer>
<div class="live" id="live" aria-live="polite"></div>
</div>
<script id="evidence-data" type="application/json">__EVIDENCE_JSON__</script>
<script>
'use strict';
const BUNDLE = JSON.parse(document.getElementById('evidence-data').textContent);
const INPUTS = BUNDLE.inputs;
const FIXTURES = INPUTS['fixtures.json'];
const RESULTS = INPUTS['results.json'];
const PERIODIC = INPUTS['sympy_periodic/report.json'];
const $ = id => document.getElementById(id);
const esc = value => String(value == null ? '' : value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty = value => JSON.stringify(value,null,2);
const number = fraction => {const p=String(fraction).split('/');return Number(p[0])/(p.length>1?Number(p[1]):1);};
const titleCase = value => value.replace(/_/g,' ').replace(/^./,c=>c.toUpperCase());
const interval = (lo,hi,left=true,right=true) => ({lo:String(lo),hi:String(hi),left_closed:left,right_closed:right});
const singleton = t => interval(t,t);
const setText = v => v.lo===v.hi ? '{'+v.lo+'}' : (v.left_closed?'[':'(')+v.lo+', '+v.hi+(v.right_closed?']':')');
const setHTML = list => list.length ? '<ol class="exact-list">'+list.map((v,i)=>'<li><span class="number">'+String(i+1).padStart(2,'0')+'</span>'+esc(setText(v))+'</li>').join('')+'</ol>' : '<div class="empty-set">∅ &nbsp;<span class="small">Empty set</span></div>';
const horizonText = h => (h.left_open?'(':'[')+h.lo+', '+h.hi+(h.right_open?')':']');
const outcomeName = value => value==='SAT' || value==='NONEMPTY' ? 'A solution exists' : 'No solution';
const resultMap = Object.fromEntries(RESULTS.cases.map(c=>[c.id,c]));
const descriptions = {
  conformance:'Five saved regressions from the runner work.',
  periodic:'Ten exact cases using standard periodic lifting.'
};
const shortTitles = {
  same_point:'One shared point',complete_relations:'The complete clock relation',clock_lifts:'The discarded clock lift',isolated_points:'Solutions with zero duration',widest_only:'Beyond the widest interval',
  documentation_cosine:'Beyond one principal period',mixed_periods:'Different periods, one time',same_time_empty:'Opposite conditions',equality_only:'Equality leaves points',offsets:'Shifted phases',rational_frequency:'A fractional frequency',negative_horizon:'A negative time horizon',closed_horizon:'The final endpoint counts',extremal_singletons:'Only the peaks survive',second_period_only:'A later-period query'
};
const mutantNotes = {
  independent_marginals:'Treats separate successful parameter values as one shared solution.',
  incomplete_relations:'Checks only the two supplied raw relations.',
  first_clock_only:'Checks the first clock choice and discards the other lift.',
  drop_singletons:'Removes every zero-width component.',
  widest_only:'Keeps only the widest core interval before adding the last constraint.'
};
let collection='conformance', selected='isolated_points';
let plotObserver;
function currentCases(){return collection==='conformance'?FIXTURES.cases:PERIODIC.cases;}
function getRecord(){return currentCases().find(c=>c.id===selected);}
function buildNavigation(){
  const cases=currentCases();
  $('nav-count').textContent=String(cases.length).padStart(2,'0');
  $('collection-description').textContent=descriptions[collection];
  $('case-list').innerHTML=cases.map((c,i)=>'<button class="case-button" data-case="'+esc(c.id)+'" aria-current="'+String(c.id===selected)+'"><span class="case-num">'+String(i+1).padStart(2,'0')+'</span><span>'+esc(shortTitles[c.id]||titleCase(c.id))+'</span></button>').join('');
  $('case-select').innerHTML=cases.map((c,i)=>'<option value="'+esc(c.id)+'"'+(c.id===selected?' selected':'')+'>'+String(i+1).padStart(2,'0')+' · '+esc(shortTitles[c.id]||titleCase(c.id))+'</option>').join('');
  document.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>chooseCase(b.dataset.case)));
  ['conformance','periodic'].forEach(name=>$('collection-'+name).setAttribute('aria-pressed',String(name===collection)));
}
function chooseCase(id){selected=id;buildNavigation();render();}
function chooseCollection(name){collection=name;selected=name==='conformance'?'isolated_points':'documentation_cosine';buildNavigation();render();}
function outcomeHTML(label,value,note,isComplete=false){return '<div class="outcome'+(isComplete?' complete':'')+'"><p class="outcome-label">'+esc(label)+'</p><p class="outcome-value">'+esc(value)+'</p><p class="outcome-note">'+esc(note)+'</p></div>';}
function table(headers,rows){return '<div class="table-wrap"><table><thead><tr>'+headers.map(h=>'<th scope="col">'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(cell=>'<td class="rational">'+esc(cell)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';}
function laneHTML(id,label,complete){return '<div class="plot-lane"><div class="lane-label'+(complete?' complete':'')+'">'+esc(label)+'</div><svg class="plot" id="'+id+'" role="img"></svg></div>';}
function evidenceSection(c,r,isPeriodic){
  if(isPeriodic){
    const rows=c.atom_sources.map((a,i)=>[String(i+1),a.expression,a.period,a.principal_seed.map(setText).join(' ∪ ')||'∅','['+a.lift_range.join(', ')+']']);
    return '<section class="section"><div class="section-heading"><h3>Exact inputs and lifting record</h3><span class="small">Saved by the periodic adapter</span></div>'+table(['Atom','Expression in t','Period','Principal seed','Lift range'],rows)+'<p class="plot-note">The saved complete set matches the independent event oracle and exact substitution checks on this development case. The principal seed has its documented limited scope.</p></section>';
  }
  let content='';
  if(c.id==='same_point'){
    content=table(['Constraint','Integer-contact parameter s','Projected range'],r.evidence.relation_parameter_sets.map(x=>[x.relation.map((v,i)=>v+'·'+['x','y','z'][i]).join(' + '),x.parameters.join(', ')||'∅','['+x.range.join(', ')+']']));
    content+='<p class="plot-note">The two constraints require different values of the same segment parameter. Their joint parameter set is empty.</p>';
  }else if(c.id==='complete_relations'){
    content='<div class="target">Requested phase triple: <span class="rational">('+esc(c.point.join(', '))+')</span></div>';
    content+=table(['Relation check','Exact values'],[['Two raw relations',r.evidence.raw_relation_values.join(', ')],['Complete relations',r.evidence.complete_relation_values.join(', ')]]);
    content+='<p class="plot-note">The value 1/2 is not an integer. The requested triple therefore fails the complete relation check.</p>';
    content+=table(['Candidate time','Actual phase triple'],r.evidence.physical_candidates.map(x=>[x.time,'('+x.phases.join(', ')+')']));
  }else if(c.id==='clock_lifts'){
    content='<div class="target">Requested phase triple: <span class="rational">('+esc(c.point.join(', '))+')</span></div>';
    content+=table(['Candidate time','Actual phase triple'],r.evidence.physical_candidates.map(x=>[x.time,'('+x.phases.join(', ')+')']));
  }else{
    content=table(['Saved witness time','Exact phases'],r.witnesses.map(x=>[x.time,x.phases.join(', ')]));
    content+='<p class="plot-note">Total safe duration: <span class="rational">'+esc(r.evidence.total_safe_duration)+'</span>. Every listed phase belongs to the closed band ['+esc(c.delta)+', 1 − '+esc(c.delta)+'].</p>';
    if(c.id==='widest_only')content+='<p class="plot-note">The selected core interval was <span class="rational">['+esc(c.primary_interval.join(', '))+']</span>. Its surviving set after the added constraint is empty; other source components survive.</p>';
  }
  return '<section class="section"><div class="section-heading"><h3>The exact distinction</h3><span class="small">Values from the saved evidence</span></div>'+content+'</section>';
}
function render(){
  if(plotObserver)plotObserver.disconnect();
  const c=getRecord(), isPeriodic=collection==='periodic', r=isPeriodic?c:resultMap[c.id];
  const title=isPeriodic?(shortTitles[c.id]||titleCase(c.id)):c.title;
  const question=isPeriodic?'Which values of normalized time t = x/π in '+horizonText(c.horizon)+' satisfy every inequality below at the same time?':c.question;
  const sourceCommit=isPeriodic?PERIODIC.provenance.repository_baseline:RESULTS.source_commit;
  const equations=isPeriodic?'<div class="equations">'+c.atom_sources.map(a=>'<div class="equation">'+esc(a.expression)+'</div>').join('')+'</div>':'';
  const facts=isPeriodic?'<span>Horizon <code>'+esc(horizonText(c.horizon))+'</code></span><span>Coordinates <code>t = x/π</code></span>':'<span>Rates <code>'+esc(c.rates.join(', '))+'</code></span>'+(c.delta?'<span>Threshold <code>'+esc(c.delta)+'</code></span>':'');
  const limited=isPeriodic?c.principal_only_intervals:[];
  let outcomes;
  if(isPeriodic){outcomes=outcomeHTML('If principal-only output answers the full query',limited.length?'Retains '+limited.length+' component'+(limited.length===1?'':'s'):'Retains no points',c.principal_only_matches_complete?'Matches this complete set. Agreement here does not expand the API’s documented scope.':'The documented limited output omits part of the requested set.')+outcomeHTML('Complete periodic lifting',outcomeName(c.verdict),c.complete_intervals.length+' exact component'+(c.complete_intervals.length===1?'':'s')+' in the requested horizon.',true);}
  else{outcomes=outcomeHTML('Intentional faulty translation',outcomeName(r.mutant_status),mutantNotes[c.mutant]||c.mutant)+outcomeHTML('Complete physical check',outcomeName(r.reference_status),r.diagnostic==='FALSE_POSITIVE'?'Rejects the false positive for this exact query.':'Recovers what the narrower translation discarded.',true);}
  let lanes=[], domain=['0','1'], axis='Physical time t · one unit period', plotTitle='Saved solution sets';
  if(isPeriodic){domain=[c.horizon.lo,c.horizon.hi];axis='Normalized time t = x/π';lanes=[{label:'Principal-only result used beyond its scope',data:c.principal_only_intervals,complete:false},{label:'Complete set in the requested horizon',data:c.complete_intervals,complete:true}];}
  else if(c.id==='same_point'){axis='Shared segment parameter s · 0 is the first endpoint, 1 is the second';plotTitle='The contacts occur at different parameters';lanes=r.evidence.relation_parameter_sets.map((x,i)=>({label:'Relation '+(i+1)+' · integer contacts',data:x.parameters.map(singleton),complete:false}));lanes.push({label:'Joint parameter set',data:r.evidence.joint_parameters.map(singleton),complete:true});}
  else if(c.id==='complete_relations'){lanes=[{label:'Times realizing the requested phase triple',data:[],complete:true}];}
  else if(c.id==='clock_lifts'){lanes=[{label:'First clock choice · fails the requested triple',data:[singleton(c.canonical_time)],complete:false},{label:'Complete physical answer',data:r.witnesses.map(w=>singleton(w.time)),complete:true}];}
  else{lanes=[{label:'Set retained by the faulty translation',data:r.evidence.mutant_retained_intervals.map(p=>interval(p[0],p[1])),complete:false},{label:'Complete physical safe set',data:r.evidence.complete_intervals.map(p=>interval(p[0],p[1])),complete:true}];}
  const sets=lanes.map(l=>'<div><p class="set-label">'+esc(l.label)+'</p>'+setHTML(l.data)+'</div>').join('');
  const plotHTML='<section class="section"><div class="section-heading"><h3>'+esc(plotTitle)+'</h3><span class="small">Exact values below · geometry for display</span></div>'+lanes.map((l,i)=>laneHTML('plot-'+i,l.label,l.complete)).join('')+'<p class="axis-title">'+esc(axis)+'</p><div class="legend"><span class="legend-item"><span class="dot filled"></span> Included endpoint</span><span class="legend-item"><span class="dot"></span> Excluded endpoint</span><span class="legend-item"><span class="singleton-symbol">◆</span> Isolated point</span></div><div class="sets">'+sets+'</div><p class="plot-note">Intervals use [ ] for included endpoints and ( ) for excluded endpoints. Braces { } mark one exact point. Narrow components may look like points at this scale; the written set is authoritative.</p></section>';
  const lesson=isPeriodic?(c.principal_only_matches_complete?'This saved case agrees even under the narrower use. Keep the requested horizon and endpoint rules explicit.':'Keep each atom’s period, all lifts reaching the horizon and the same-time intersection. A principal interval alone is not the answer to a larger periodic query.'):r.lesson;
  let provenance=isPeriodic?'<div>Method: '+esc(PERIODIC.method)+'</div><div>SymPy '+esc(PERIODIC.provenance.package_pins.sympy.version)+' · '+esc(c.status)+' development case</div>':'<div>Source record <span class="path">'+esc(c.source.path)+'</span></div><div>Selector <span class="path">'+esc(c.source.selector)+'</span></div>';
  if(!isPeriodic&&c.source.adaptation)provenance+='<div>Query adaptation: '+esc(typeof c.source.adaptation==='string'?c.source.adaptation:pretty(c.source.adaptation))+'</div>';
  if(!isPeriodic&&r.source&&r.source.adaptation&&!c.source.adaptation)provenance+='<div>Query adaptation: '+esc(typeof r.source.adaptation==='string'?r.source.adaptation:pretty(r.source.adaptation))+'</div>';
  if(!isPeriodic&&(c.id==='complete_relations'||c.id==='clock_lifts'))provenance+='<div>This point-recovery query is an adaptation of the archived diagnostic; it is narrower than the original edge or band problem.</div>';
  provenance+='<div>Repository source commit <span class="path">'+esc(sourceCommit)+'</span></div>';
  const caseEvidence=isPeriodic?c:{fixture:c,result:r};
  const inputPaths=isPeriodic?['sympy_periodic/report.json']:['fixtures.json','results.json'];
  provenance+=inputPaths.map(p=>'<div>Embedded '+esc(p)+' SHA-256 <span class="path">'+esc(BUNDLE.sha256[p])+'</span></div>').join('');
  const savedStatus=isPeriodic?c.status==='PASS':RESULTS.status==='PASS_DEVELOPMENT_REGRESSIONS';
  $('detail').innerHTML='<div class="detail-head"><div class="case-meta"><span>'+esc(isPeriodic?'Periodic inequality adapter':'Clock compatibility regression')+'</span><span><i class="status-dot"></i>'+esc(savedStatus?'Saved checks passed':'Inspect saved status')+'</span></div><h2>'+esc(title)+'</h2><p class="question">'+esc(question)+'</p>'+equations+'<div class="facts">'+facts+'</div></div><div class="outcomes">'+outcomes+'</div>'+plotHTML+evidenceSection(c,r,isPeriodic)+'<section class="section"><div class="lesson"><strong>What this example preserves</strong>'+esc(lesson)+'</div></section><section class="section"><div class="section-heading"><h3>Inspect the source</h3><span class="small">Pinned inputs, saved outputs</span></div><div class="provenance">'+provenance+'</div><div class="evidence-controls"><button class="button primary" id="download-case">Download this case</button>'+inputPaths.map((p,i)=>'<button class="button" data-download="'+esc(p)+'">Download '+esc(p.split('/').pop())+'</button>').join('')+'</div><details id="case-json"><summary>Inspect exact case JSON</summary><pre>'+esc(pretty(caseEvidence))+'</pre></details><details><summary>Inspect embedded file hashes</summary><pre>'+esc(pretty(BUNDLE.sha256))+'</pre></details></section>';
  $('download-case').addEventListener('click',()=>download(selected+'.json',caseEvidence));
  document.querySelectorAll('[data-download]').forEach(b=>b.addEventListener('click',()=>download(b.dataset.download.split('/').pop(),INPUTS[b.dataset.download])));
  const redraw=()=>lanes.forEach((l,i)=>drawPlot($('plot-'+i),l,domain));
  redraw();plotObserver=new ResizeObserver(redraw);plotObserver.observe($('detail'));
  $('live').textContent=title+'. '+(isPeriodic?c.verdict:r.reference_status)+'. Saved development result.';
}
function tickFraction(a,b,i,n){
  const fraction=x=>{const p=String(x).split('/');return [BigInt(p[0]),BigInt(p[1]||'1')];};
  const [an,ad]=fraction(a),[bn,bd]=fraction(b);let num=an*bd*BigInt(n-i)+bn*ad*BigInt(i),den=ad*bd*BigInt(n);let x=num<0n?-num:num,y=den;while(y){const z=x%y;x=y;y=z;}if(x){num/=x;den/=x;}return den===1n?String(num):String(num)+'/'+String(den);
}
function drawPlot(svg,lane,domain){
  const w=Math.max(220,Math.round(svg.getBoundingClientRect().width));
  const h=85,pad=22,min=number(domain[0]),max=number(domain[1]);
  const x=v=>pad+(number(v)-min)/(max-min)*(w-pad*2);
  const color=lane.complete?'#14766c':'#ae4b35',fill=lane.complete?'#d8ebe3':'#f1d5c9';
  let s='<title>'+esc(lane.label)+'</title><desc>'+esc(lane.data.map(setText).join(' union ')||'Empty set')+'. Positions are a display of saved exact data.</desc><line x1="'+pad+'" y1="39" x2="'+(w-pad)+'" y2="39" stroke="#d7dcd7" stroke-width="1"/>';
  const tickN=w<390?2:4;
  for(let i=0;i<=tickN;i++){const f=tickFraction(domain[0],domain[1],i,tickN),xx=x(f);s+='<line x1="'+xx+'" x2="'+xx+'" y1="49" y2="53" stroke="#c2cbc7"/><text class="tick" x="'+xx+'" y="71" text-anchor="'+(i===0?'start':i===tickN?'end':'middle')+'">'+esc(f)+'</text>';}
  if(!lane.data.length)s+='<text class="empty" x="'+(w/2)+'" y="31" text-anchor="middle">∅ · no points</text>';
  const direct=lane.data.length<=4 && lane.data.every(d=>d.lo===d.hi);
  const labelRows=[-Infinity,-Infinity];
  lane.data.forEach((d,i)=>{
    const l=x(d.lo),r=x(d.hi),mid=(l+r)/2,tip=setText(d);s+='<g><title>'+esc(tip)+'</title>';
    if(d.lo===d.hi){s+='<path d="M '+l+' 32 L '+(l+6)+' 39 L '+l+' 46 L '+(l-6)+' 39 Z" fill="'+color+'"/>';}
    else{s+='<rect x="'+l+'" y="34" width="'+Math.max(1,r-l)+'" height="10" rx="1" fill="'+fill+'"/><line x1="'+l+'" y1="39" x2="'+r+'" y2="39" stroke="'+color+'" stroke-width="3"/>';[[l,d.left_closed],[r,d.right_closed]].forEach(([xx,closed])=>{s+='<circle cx="'+xx+'" cy="39" r="4" fill="'+(closed?color:'#fffdf8')+'" stroke="'+color+'" stroke-width="1.8"/>';});}
    const label=direct?d.lo:String(i+1).padStart(2,'0');
    const labelWidth=label.length*7,anchor=mid<32?'start':mid>w-32?'end':'middle';
    const labelStart=anchor==='start'?mid:anchor==='end'?mid-labelWidth:mid-labelWidth/2;
    const labelEnd=labelStart+labelWidth;
    let row=labelRows.findIndex(end=>labelStart>end+5);if(row<0)row=labelRows[0]<=labelRows[1]?0:1;
    labelRows[row]=labelEnd;
    s+='<text x="'+mid+'" y="'+(row===0?15:28)+'" text-anchor="'+anchor+'">'+esc(label)+'</text></g>';
  });
  svg.setAttribute('viewBox','0 0 '+w+' '+h);svg.setAttribute('aria-label',lane.label+': '+(lane.data.map(setText).join(' union ')||'empty set'));svg.innerHTML=s;
}
function download(filename,value){const blob=new Blob([pretty(value)+'\n'],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('collection-conformance').addEventListener('click',()=>chooseCollection('conformance'));
$('collection-periodic').addEventListener('click',()=>chooseCollection('periodic'));
$('case-select').addEventListener('change',e=>chooseCase(e.target.value));
$('download-bundle').addEventListener('click',()=>download('compatibility-evidence.json',BUNDLE));
$('count-conformance').textContent=FIXTURES.cases.length+' cases';
$('count-periodic').textContent=PERIODIC.cases.length+' cases';
buildNavigation();render();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
