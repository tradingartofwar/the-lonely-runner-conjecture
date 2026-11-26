/* Sites supplies the owner-private access gate, the DB binding and the embedded ASSETS. */
const DAY = 86_400_000;
const LEASE = 20 * 60_000;
const MODEL_LIMIT = 18;
const SCHEDULED_COORDINATORS = 7; // Six work wakes and the 24-hour closeout.
const MODEL_JOB_LIMIT = MODEL_LIMIT - SCHEDULED_COORDINATORS;
const ACTIVE_LIMIT = 2;
const TIMEZONE = "America/Los_Angeles";
const dayFormatter = new Intl.DateTimeFormat("en-CA", {
  timeZone: TIMEZONE, year: "numeric", month: "2-digit", day: "2-digit"
});
function ptDay(iso) {
  const p = Object.fromEntries(dayFormatter.formatToParts(new Date(iso)).map(x => [x.type, x.value]));
  return [p.year, p.month, p.day].join("-");
}
const iso = ms => new Date(ms).toISOString();
class Problem extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
function requireThat(condition, message, status = 400) {
  if (!condition) throw new Problem(status, message);
}
function str(value, name, max = 1200) {
  requireThat(typeof value === "string" && value.trim().length > 0 && value.length <= max, "Invalid " + name);
  return value.trim();
}
function id(value, name = "id") {
  const v = str(value, name, 110);
  requireThat(/^[a-zA-Z0-9][a-zA-Z0-9._:@-]*$/.test(v), "Invalid " + name);
  return v;
}
function stamp(value, name) {
  requireThat(typeof value === "string" && /(?:Z|[+-]\d\d:\d\d)$/.test(value) && Number.isFinite(Date.parse(value)), "Invalid " + name);
  return iso(Date.parse(value));
}
function evidence(b) {
  const artifact = str(b.artifact, "artifact", 500);
  requireThat(/^[a-zA-Z0-9_./-]+$/.test(artifact) && !artifact.startsWith("/") && !artifact.split("/").includes(".."), "Use a repository-relative evidence path");
  const revision = str(b.revision, "revision", 80);
  requireThat(/^(?:[0-9a-f]{7,64}|sha256:[0-9a-f]{64})$/i.test(revision), "Use a Git revision or SHA-256 digest");
  const result_digest = b.result_digest ?? null;
  requireThat(result_digest == null || (typeof result_digest === "string" && /^[0-9a-f]{64}$/.test(result_digest)), "Invalid SHA-256 result_digest");
  return {summary:str(b.summary, "summary"), artifact, replay:str(b.replay, "replay", 900), revision, result_digest};
}
const pick = (value, choices, field) => {
  requireThat(choices.includes(value), "Invalid " + field);
  return value;
};
function empty() {
  return {started_at:null, ends_at:null, paused:false, pause_reason:null, provider_hold:null, auth_hold:false, quota_hold:false,
    jobs:[], events:[], findings:[], decisions:[], receipts:{}, meter:[],
    plan:{captured_at:null, source:null, windows:[]}, last_plan_attempt:null};
}
function event(s, time, fields) {
  s.events.push({id:s.events.length + 1, time, source:"hosted-queue", ...fields});
}
function addDecision(s, now, text, job_id = null) {
  const d = {id:"decision-" + crypto.randomUUID(), time:now, text, state:"open", job_id};
  s.decisions.push(d);
  event(s, now, {kind:"decision", state:"open", role:"coordinator", task:text, job_id});
  return d.id;
}
function jobPublic({lease_token, ...job}) { return job; }
function jobEvent(s, now, job, kind, extra = {}) {
  event(s, now, {kind, state:job.state, role:job.role, task:job.task, job_id:job.id, parent_id:job.parent_id,
    source_finding_id:job.source_finding_id, worker:job.worker, run_id:job.run_id, controller_run_id:job.controller_run_id ?? null, attempt:job.attempt, ...extra});
}
function enqueue(s, now, fields) {
  requireThat(!s.jobs.some(j => j.id === fields.id), "Job ID already exists", 409);
  const job = {id:fields.id, role:fields.role, task:fields.task, state:"queued", parent_id:null, source_finding_id:null,
    verification_of:null, worker:null, run_id:null, controller_run_id:null, mode:null, attempt:0, queued_at:now, started_at:null, finished_at:null,
    lease_expires:null, lease_token:null, summary:null, artifact:null, replay:null, revision:null, verified_by:null, ...fields};
  s.jobs.push(job);
  jobEvent(s, now, job, "queued");
  return job;
}
function expire(s, now) {
  for (const j of s.jobs) {
    if (j.state !== "running" || j.lease_expires > now) continue;
    j.state = j.attempt >= 3 ? "failed" : "queued";
    j.lease_expires = null;
    j.lease_token = null;
    if (j.state === "failed") j.finished_at = now;
    jobEvent(s, now, j, "lease_expired", {task:j.state === "failed" ? "Third lease expired. Review needed." : "Lease expired. Assignment available again."});
    if (j.state === "failed") addDecision(s, now, "Review assignment after three attempts: " + j.task, j.id);
  }
}
function gate(s, now, mode) {
  if (!s.started_at) return "pilot_not_started";
  if (s.paused) return "paused";
  if (now >= s.ends_at) return "pilot_ended";
  if (mode === "model" && s.provider_hold) return s.provider_hold;
  if (mode === "model") {
    const budget = modelBudget(s);
    if (budget.used >= MODEL_LIMIT) return "model_call_limit";
    if (budget.jobClaims >= MODEL_JOB_LIMIT) return "model_job_limit";
  }
  if (s.jobs.filter(j => j.state === "running" && j.lease_expires > now).length >= ACTIVE_LIMIT) return "active_lease_limit";
  return null;
}
const modelClaims = s => s.events.filter(e => e.kind === "claimed" && e.mode === "model" && e.source === "hosted-queue");
function modelBudget(s) {
  const claims = modelClaims(s);
  const jobRuns = new Set(claims.map(e => e.run_id));
  const controllerRuns = new Set(s.events.filter(e => e.mode === "model" && e.kind === "controller_observation").map(e => e.run_id));
  const overBudget = new Set(s.events.filter(e => e.mode === "model" && e.kind === "controller_over_budget").map(e => e.run_id));
  const reserved = new Set([...jobRuns,...controllerRuns]);
  // Older ledger versions allowed a second job attempt under the same run ID.
  // Each such retry remains charged when the already-persisted pilot is upgraded.
  const used = reserved.size + claims.length - jobRuns.size;
  return {jobRuns,controllerRuns,overBudget,reserved,used,jobClaims:claims.length};
}
const attributableRuns = s => s.events.filter(e => e.mode === "model" && e.run_id &&
  ((e.kind === "claimed" && e.source === "hosted-queue") || (e.kind === "recorded_history" && e.source === "historical-import") ||
   (["controller_observation","controller_over_budget"].includes(e.kind) && e.source === "hosted-controller")));
function leased(s, b, now) {
  const j = s.jobs.find(j => j.id === id(b.id));
  requireThat(j && j.state === "running" && j.lease_expires > now && j.worker === b.worker && j.lease_token === b.lease_token,
    "Lease has expired or belongs to another attempt", 409);
  return j;
}
function independent(s, job, worker, run) {
  const parent = s.jobs.find(j => j.id === job.parent_id);
  const finding = s.findings.find(f => f.id === job.source_finding_id);
  // The parent of an audit is its proposal. The parent of a follow-up is the
  // audit which generated it. Both role names and scheduler-run IDs can be reused
  // by a dishonest caller; worker isolation is supplied by the executing scheduler.
  return (!parent || (parent.worker !== worker && parent.run_id !== run)) &&
    (job.verification_of || !finding || (finding.verifier !== worker && finding.verifier_run_id !== run));
}
function protocol(name, seed) {
  if (name == null && seed == null) return {protocol:null, seed:null};
  pick(name,["cohorts","wrap"],"protocol");
  requireThat(typeof seed === "string" && /^[a-f0-9]{32}$/.test(seed),"Seed must have 32 lowercase hex digits");
  return {protocol:name,seed};
}
function complete(s, b, now) {
  const j = leased(s, b, now);
  const result = evidence(b);
  const next = b.next_question == null ? null : str(b.next_question, "next_question");
  const decision = b.decision == null ? null : str(b.decision, "decision");
  const verdict = j.role === "verifier" ? pick(b.verdict, ["verified", "refuted", "inconclusive"], "verdict") : null;
  requireThat(j.role !== "verifier" || next || decision, "Supply the next question or a decision for Vance");
  Object.assign(j, result, {state:j.role === "verifier" ? "completed" : "submitted", finished_at:now, lease_expires:null, lease_token:null});
  jobEvent(s, now, j, j.role === "verifier" ? "review_returned" : "proposal_returned", {...result, verdict});
  if (j.role !== "verifier") {
    const audit = enqueue(s, now, {id:"audit-" + crypto.randomUUID(), role:"verifier", parent_id:j.id,
      verification_of:j.id, ...protocol(j.protocol,j.seed), task:b.audit_question ? str(b.audit_question, "audit_question") : "Independently check the evidence and scope of this return: " + j.task, source_finding_id:j.source_finding_id});
    return {job:jobPublic(j), next_job_id:audit.id};
  }
  const proposal = s.jobs.find(p => p.id === j.verification_of && p.state === "submitted");
  requireThat(proposal, "Proposal is unavailable for review", 409);
  if (verdict === "verified" && proposal.result_digest) {
    requireThat(result.result_digest === proposal.result_digest, "Verified result_digest must match the proposed artifact", 409);
  }
  j.verdict = verdict;
  proposal.claim_status = verdict;
  proposal.state = "completed";
  let finding_id = null;
  if (verdict === "verified") {
    proposal.verified_by = j.id;
    finding_id = "finding-" + crypto.randomUUID();
    s.findings.push({id:finding_id, time:now, job_id:proposal.id, verifier_job_id:j.id, verifier:j.worker,
      verifier_run_id:j.run_id, source:"hosted-queue", ...result});
    jobEvent(s, now, j, "verified", {...result, source_finding_id:finding_id});
  }
  let child = null;
  if (next) child = enqueue(s, now, {id:"question-" + crypto.randomUUID(), role:"researcher", parent_id:j.id,
    source_finding_id:finding_id, origin:"review-followup", task:next, ...protocol(b.next_protocol,b.next_seed)});
  return {job:jobPublic(j), finding_id, next_job_id:child?.id ?? null, decision_id:decision ? addDecision(s, now, decision, j.id) : null};
}
function telemetry(s, b, now) {
  const source = str(b.source, "source", 220);
  const measured_at = stamp(b.measured_at, "measured_at");
  requireThat(Date.parse(measured_at) <= Date.parse(now) + 300_000, "Measurement is in the future");
  const run_id = b.run_id == null ? null : id(b.run_id, "run_id");
  const hasCounts = ["input_tokens","output_tokens","cached_input_tokens"].some(k => b[k] != null);
  if (hasCounts || run_id) {
    requireThat(run_id, "Usage attribution requires a run_id");
    const count = k => {
      const n = b[k];
      requireThat(n == null || (Number.isSafeInteger(n) && n >= 0), "Invalid " + k);
      return n ?? null;
    };
    // Providers report per-run usage. Supply day for a known Pacific-day slice
    // when a session crosses midnight. Unsplit cross-midnight totals are unknown.
    const claims = attributableRuns(s).filter(e => e.run_id === run_id);
    requireThat(claims.length > 0,"Usage requires an identified Observatory model run",409);
    const day = b.day ?? (claims.some(e => ptDay(e.time) !== ptDay(measured_at)) ? null : ptDay(measured_at));
    requireThat(day == null || /^\d{4}-\d{2}-\d{2}$/.test(day), "Invalid Pacific usage day");
    const row = {run_id, day, source, measured_at, input_tokens:count("input_tokens"), output_tokens:count("output_tokens"),
      cached_input_tokens:count("cached_input_tokens")};
    requireThat(row.input_tokens == null || row.cached_input_tokens == null || row.cached_input_tokens <= row.input_tokens, "Cached input exceeds total input");
    const old = s.meter.find(x => x.run_id === run_id && x.day === day);
    if (old) {
      requireThat(!hasCounts || old.measured_at <= measured_at, "Older run measurement", 409);
      for (const k of ["input_tokens","output_tokens","cached_input_tokens"]) {
        requireThat(old[k] == null || row[k] == null || row[k] >= old[k], "Cumulative run totals cannot decrease", 409);
        if (row[k] == null) row[k] = old[k];
      }
      if (hasCounts) Object.assign(old, row);
    } else s.meter.push(row);
  }
  if (b.windows != null || b.plan_error != null || b.limit_reached === true || b.auth_unavailable === true || b.plan_available === true) {
    const error = b.plan_error ? str(b.plan_error, "plan_error", 500) : null;
    let windows;
    if (b.windows != null) {
      requireThat(Array.isArray(b.windows) && b.windows.length > 0 && b.windows.length <= 10 && !error, "Invalid windows");
      windows = b.windows.map(w => {
        requireThat(w && Number.isFinite(w.remaining_percent) && w.remaining_percent >= 0 && w.remaining_percent <= 100, "Invalid plan percentage");
        return {label:str(w.label, "label", 100), remaining_percent:w.remaining_percent, resets_at:w.resets_at == null ? null : stamp(w.resets_at, "resets_at")};
      });
      if (!s.plan.captured_at || measured_at >= s.plan.captured_at) s.plan = {captured_at:measured_at, source, windows};
    }
    if (!s.last_plan_attempt || measured_at >= s.last_plan_attempt.measured_at) {
      s.last_plan_attempt = {measured_at, source, error};
      const priorHold = s.provider_hold;
      if (b.auth_unavailable === true) s.auth_hold = true;
      else if (!error && b.plan_available === true) s.auth_hold = false;
      if (b.limit_reached === true || windows?.some(w => w.remaining_percent === 0)) s.quota_hold = true;
      else if (!error && (b.plan_available === true || windows?.length)) s.quota_hold = false;
      s.provider_hold = s.auth_hold ? "plan_auth_unavailable" : s.quota_hold ? "plan_limit_reached" : null;
      if (s.provider_hold && s.provider_hold !== priorHold)
        addDecision(s, now, "Plan dispatch stopped: " + s.provider_hold.replaceAll("_", " ") + ". Check the existing account before resuming.");
    }
  }
  requireThat(hasCounts || run_id || b.windows != null || b.plan_error != null || b.limit_reached || b.auth_unavailable || b.plan_available, "No telemetry supplied");
  return {recorded:true};
}
function recordHistory(s, b, now) {
  const source = str(b.source, "source", 250);
  const events = b.events ?? [];
  requireThat(Array.isArray(events) && events.length <= 60 && (events.length || b.finding), "Invalid historical record");
  for (const e of events) {
    const t = stamp(e.time, "event time");
    requireThat(Date.parse(t) <= Date.parse(now) + 300_000, "Historical event is in the future");
    const details = {};
    for (const k of ["artifact","revision","replay","job_id","worker","parent_id","source_finding_id"]) if (e[k] != null) details[k] = str(e[k], k, 900);
    if (e.run_id != null || e.mode != null) {
      details.run_id = id(e.run_id,"historical run_id");
      details.mode = pick(e.mode,["model","deterministic"],"historical mode");
    }
    event(s,t,{kind:"recorded_history",source:"historical-import",recorded_at:now,provenance:source,role:str(e.role,"role",100),
      state:str(e.state,"state",80),task:str(e.task,"task"), ...details});
  }
  let finding_id = null;
  if (b.finding) {
    const f = b.finding;
    finding_id = id(f.id, "finding id");
    requireThat(!s.findings.some(x => x.id === finding_id), "Finding ID already exists", 409);
    const time = stamp(f.verified_at, "verified_at");
    requireThat(Date.parse(time) <= Date.parse(now) + 300_000, "Finding is in the future");
    s.findings.push({id:finding_id,time,job_id:f.job_id ? id(f.job_id) : null,verifier_job_id:f.verifier_job_id ? id(f.verifier_job_id) : null,
      verifier:id(f.verifier,"verifier"),verifier_run_id:f.verifier_run_id ? id(f.verifier_run_id) : null,source:"historical-import",provenance:source,...evidence(f)});
  }
  return {recorded:events.length,finding_id};
}
function dispatch(s,b,now) {
  expire(s,now);
  switch (b.action) {
    case "begin":
      if (!s.started_at) {
        s.started_at = now;
        s.ends_at = iso(Date.parse(now) + DAY);
        event(s,now,{kind:"pilot_started",role:"coordinator",state:"started",task:"Opened the 24-hour research pilot."});
      }
      return {started_at:s.started_at,ends_at:s.ends_at};
    case "record": return recordHistory(s,b,now);
    case "observe": {
      const run_id=id(b.run_id,"run_id");
      const worker=id(b.worker ?? run_id,"worker");
      const mode=pick(b.mode,["model","deterministic"],"mode");
      const state=pick(b.state,["running","completed","failed"],"controller state");
      const prior=s.events.filter(e=>["controller_observation","controller_over_budget"].includes(e.kind) && e.run_id===run_id);
      requireThat(!prior.some(e=>e.state===state || e.state!=="running" || e.mode!==mode || e.worker!==worker), "Controller observation conflicts with a previous state",409);
      const budget=modelBudget(s);
      const overBudget=mode==="model" && !budget.reserved.has(run_id) && budget.used>=MODEL_LIMIT;
      const kind=overBudget ? "controller_over_budget" : "controller_observation";
      event(s,now,{kind,source:"hosted-controller",role:"coordinator",state,run_id,worker,mode,task:str(b.task,"task"),admitted:!overBudget});
      if (overBudget) return {run_id,state,recorded_at:now,admitted:false,reason:"model_call_limit",error:"Model call cap reached. Stop this wake before research."};
      return {run_id,state,recorded_at:now,admitted:true};
    }
    case "decision": return {decision_id:addDecision(s,now,str(b.text,"decision text"))};
    case "telemetry": return telemetry(s,b,now);
    case "seed": {
      const finding = b.source_finding_id == null ? null : s.findings.find(f => f.id === b.source_finding_id);
      requireThat(b.source_finding_id == null || finding, "Unknown verified source finding",409);
      const job = enqueue(s,now,{id:id(b.id),task:str(b.task,"task"),role:pick(b.role,["researcher","challenger"],"role"),origin:"seed",
        ...protocol(b.protocol,b.seed), source_finding_id:finding?.id ?? null, parent_id:finding?.verifier_job_id ?? null});
      return {job:jobPublic(job)};
    }
    case "claim": {
      const mode = pick(b.mode ?? "model",["model","deterministic"],"mode");
      const worker = id(b.worker,"worker");
      const run = id(b.run_id ?? worker,"run_id");
      const controller_run_id = b.controller_run_id == null ? null : id(b.controller_run_id,"controller_run_id");
      if (controller_run_id) requireThat(s.events.some(e=>e.kind==="controller_observation" && e.source==="hosted-controller" &&
        e.run_id===controller_run_id), "Claim requires an admitted, observed controller run",409);
      const reason = gate(s,now,mode);
      if (reason) return {job:null,reason};
      const options = s.jobs.filter(j => j.state === "queued" && (!b.id || j.id === b.id) && (!b.role || j.role === b.role));
      const j = options.find(j => independent(s,j,worker,run));
      if (!j) return {job:null,reason:options.length ? "independent_worker_required" : "no_eligible_work"};
      if (mode==="model" && modelClaims(s).some(e=>e.run_id===run)) return {job:null,reason:"model_run_id_already_claimed"};
      const token = crypto.randomUUID();
      Object.assign(j,{state:"running",mode,worker,run_id:run,controller_run_id,attempt:j.attempt+1,started_at:now,lease_token:token,lease_expires:iso(Date.parse(now)+LEASE)});
      jobEvent(s,now,j,"claimed",{mode});
      const parent = s.jobs.find(p => p.id === j.parent_id);
      const finding = s.findings.find(f => f.id === j.source_finding_id);
      return {job:jobPublic(j),lease_token:token,handoff:{parent:parent ? jobPublic(parent) : null,finding:finding ?? null}};
    }
    case "heartbeat": {
      const j = leased(s,b,now);
      requireThat(now < s.ends_at,"Pilot window ended",409);
      j.lease_expires = iso(Date.parse(now)+LEASE);
      return {id:j.id,lease_expires:j.lease_expires};
    }
    case "release": {
      const j = leased(s,b,now);
      const reason = str(b.reason,"reason",500);
      Object.assign(j,{state:j.attempt >= 3 ? "failed" : "queued",lease_token:null,lease_expires:null});
      if (j.state === "failed") j.finished_at = now;
      jobEvent(s,now,j,"released",{task:reason});
      if (j.state === "failed") addDecision(s,now,"Review assignment after three attempts: " + j.task,j.id);
      return {job:jobPublic(j)};
    }
    case "complete": return complete(s,b,now);
    case "pause":
    case "resume": {
      const paused = b.action === "pause";
      if (paused !== s.paused) {
        s.paused = paused;
        s.pause_reason = paused ? "Paused by the owner" : null;
        event(s,now,{kind:"operator_control",role:"owner",state:paused ? "paused" : "resumed",task:paused ? "Paused new assignments." : "Resumed new assignments."});
      }
      return {paused:s.paused};
    }
    default: throw new Problem(400,"Unknown action");
  }
}
function usage(s,now) {
  const day = ptDay(now);
  const claimsToday = attributableRuns(s).filter(e => ptDay(e.time) === day);
  const deterministicRuns = new Set(s.events.filter(e => e.kind==="claimed" && e.source==="hosted-queue" &&
    e.mode==="deterministic" && ptDay(e.time)===day).map(e=>e.run_id));
  const rows = s.meter.filter(x => x.day === day);
  const known = rows.filter(x => x.input_tokens != null && x.output_tokens != null);
  const runs = new Set([...claimsToday.map(e => e.run_id),...rows.map(r => r.run_id)]).size;
  const measured = known.length;
  const sum = key => {
    const present = rows.filter(x => x[key] != null);
    return present.length ? present.reduce((n,x) => n+x[key],0) : null;
  };
  const measuredAt = rows.filter(x => x.input_tokens != null || x.output_tokens != null).map(x => x.measured_at).sort().at(-1);
  return {timezone:TIMEZONE,day,token_limit:null,remaining_tokens:null, runs,deterministic_runs:deterministicRuns.size,measured_runs:measured,
    input_tokens:sum("input_tokens"),output_tokens:sum("output_tokens"),cached_input_tokens:sum("cached_input_tokens"),
    tokens_used:measured ? known.reduce((n,x) => n+x.input_tokens+x.output_tokens,0) : null,
    coverage:measured === 0 ? "unknown" : measured === runs ? "all recorded runs" : "partial",
    measured_at:measuredAt ?? null,source:measuredAt ? [...new Set(rows.filter(x=>x.input_tokens!=null || x.output_tokens!=null).map(x=>x.source))].join(", ") : null};
}
function project(s,now,owner) {
  const events = [...s.events].sort((a,b) => a.time.localeCompare(b.time) || a.id-b.id);
  const jobs = s.jobs.map(j => ({...jobPublic(j),stale:j.state === "running" && j.lease_expires <= now}));
  const decision = [...s.decisions].reverse().find(d => d.state === "open");
  const budget = modelBudget(s);
  const liveFindings = new Map(s.findings.filter(f=>f.source==="hosted-queue").map(f=>[f.id,f]));
  const status = !s.started_at ? "not_started" : now >= s.ends_at ? "ended" : s.paused ? "paused" : s.provider_hold ? "plan_hold" : budget.used >= MODEL_LIMIT ? "model_limit" : "active";
  const measured = usage(s,now);
  const researchQuestion = jobs.find(j => j.state === "running" && !j.stale) || jobs.find(j => j.state === "queued");
  return {project:{name:"Lonely Runner Observatory"},generated_at:now,current_question:researchQuestion?.task ?? null,
    pilot:{status,paused:s.paused,pause_reason:s.pause_reason,started_at:s.started_at,ends_at:s.ends_at,provider_hold:s.provider_hold,
      model_call_limit:MODEL_LIMIT,model_dispatch_limit:MODEL_JOB_LIMIT,scheduled_controller_slots:SCHEDULED_COORDINATORS,active_lease_limit:ACTIVE_LIMIT,lease_minutes:LEASE/60000},
    usage:measured,plan:{...s.plan,last_attempt:s.last_plan_attempt},operator:{can_control:owner},
    events,jobs,findings:s.findings,decisions:s.decisions,
    evaluation:{elapsed_hours:s.started_at ? Math.min(24,(Date.parse(now)-Date.parse(s.started_at))/3_600_000) : 0,model_dispatches:budget.jobClaims,
      controller_runs:budget.controllerRuns.size + budget.overBudget.size,over_budget_controller_runs:budget.overBudget.size,
      model_calls_reserved:budget.used,model_calls_remaining:Math.max(0,MODEL_LIMIT-budget.used),
      model_jobs_remaining:Math.max(0,Math.min(MODEL_JOB_LIMIT-budget.jobClaims,MODEL_LIMIT-budget.used)),
      deterministic_dispatches:s.events.filter(e => e.kind === "claimed" && e.mode === "deterministic").length,
      completed_jobs:jobs.filter(j => j.state === "completed" || j.state === "submitted").length,
      verified_findings:s.findings.filter(f => f.source === "hosted-queue").length,
      followups_claimed:jobs.filter(j => {
        const f=liveFindings.get(j.source_finding_id);
        return f && j.role!=="verifier" && j.attempt>0 && j.parent_id===f.verifier_job_id &&
          (j.origin==="review-followup" || (!j.origin && j.queued_at===f.time));
      }).length,
      retries:s.events.filter(e=>e.kind==="claimed" && e.attempt>1).length,decision:decision?.text ?? null,coverage:measured.coverage}};
}
function canonical(v) {
  if (v && typeof v === "object" && !Array.isArray(v)) return Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])]));
  return Array.isArray(v) ? v.map(canonical) : v;
}
async function fingerprint(b) {
  const bytes = await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(canonical(b))));
  return Array.from(new Uint8Array(bytes),v=>v.toString(16).padStart(2,"0")).join("");
}
async function readRow(db) {
  return db.prepare("SELECT revision, document FROM pilot_state WHERE id = 1").first();
}
async function mutate(db,b) {
  const requestId = id(b.request_id,"request_id");
  const signature = await fingerprint(b);
  for (let attempt=0; attempt<10; attempt++) {
    const row = await readRow(db);
    const s = row ? JSON.parse(row.document) : empty();
    const now = iso(Date.now());
    const receipt = s.receipts["$"+requestId];
    if (receipt) {
      requireThat(receipt.signature === signature, "Request ID already used for different input",409);
      if (b.action === "claim" && receipt.result.job) {
        const job = s.jobs.find(j=>j.id===receipt.result.job.id);
        requireThat(job && job.state === "running" && job.lease_token === receipt.result.lease_token && job.lease_expires > now,"Original claim is no longer active",409);
        return {...receipt.result,job:jobPublic(job)};
      }
      return receipt.result;
    }
    const result = dispatch(s,b,now);
    s.receipts["$"+requestId] = {signature,result};
    const doc = JSON.stringify(s);
    requireThat(new TextEncoder().encode(doc).length < 1_850_000, "Pilot ledger size limit reached",507);
    const statement = row
      ? db.prepare("UPDATE pilot_state SET revision = revision + 1, document = ? WHERE id = 1 AND revision = ?").bind(doc,row.revision)
      : db.prepare("INSERT INTO pilot_state (id,revision,document) VALUES (1,1,?) ON CONFLICT(id) DO NOTHING").bind(doc);
    if ((await statement.run()).meta.changes === 1) return result;
  }
  throw new Problem(503,"Concurrent queue write. Retry with the same request ID.");
}
function json(data,status=200) {
  return Response.json(data,{status,headers:{"Cache-Control":"private, no-store","X-Content-Type-Options":"nosniff"}});
}
async function bodyOf(request) {
  requireThat(request.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase()==="application/json","JSON content type required",415);
  requireThat(Number(request.headers.get("Content-Length") || 0) <= 131072,"Request is too large",413);
  const reader=request.body?.getReader();
  requireThat(reader,"Request body required");
  const decoder = new TextDecoder();
  let raw = "", length = 0;
  while (true) {
    const part = await reader.read();
    if (part.done) break;
    length += part.value.byteLength;
    if (length>131072) { await reader.cancel(); throw new Problem(413,"Request is too large"); }
    raw += decoder.decode(part.value,{stream:true});
  }
  let b;
  try { b=JSON.parse(raw+decoder.decode()); } catch { throw new Problem(400,"Invalid JSON"); }
  requireThat(b && typeof b==="object" && !Array.isArray(b),"JSON object required");
  return b;
}
export default {
  async fetch(request,env) {
    const url=new URL(request.url);
    const path=url.pathname;
    const owner=Boolean(request.headers.get("oai-authenticated-user-id"));
    try {
      if (path==="/api/pilot" && request.method==="GET") {
        const row=await readRow(env.DB);
        return json(project(row ? JSON.parse(row.document) : empty(),iso(Date.now()),owner));
      }
      if (path==="/api/operator" || path==="/api/dispatch") {
        requireThat(request.method==="POST","POST required",405);
        const isOperator=path==="/api/operator";
        if (isOperator) {
          requireThat(owner && request.headers.get("Origin")===url.origin,"Owner and same-origin request required",403);
        } else {
          // On this owner-private Site, only a validated service-bearer request
          // has no visitor identity. Sites consumes the bearer before dispatch.
          requireThat(!owner && !request.headers.get("Origin") && !request.headers.get("Sec-Fetch-Site"),"Service access required",403);
        }
        const b=await bodyOf(request);
        if (isOperator) {
          if (b.action==="usage") {
            requireThat(Object.keys(b).every(k=>["action","request_id","source","measured_at","windows","plan_error"].includes(k)), "Unexpected owner usage field");
            requireThat(b.source==null || b.source==="Owner WSL · Codex app-server","Unexpected allowance source");
            requireThat(Boolean(b.windows)!==Boolean(b.plan_error),"Supply allowance windows or a measurement error");
            if (b.windows) {
              requireThat(Array.isArray(b.windows) && b.windows.length>0 && b.windows.length<=2 && b.windows.every(w=>w && ["5-hour","Weekly","Primary","Secondary"].includes(w.label)),"Invalid owner allowance windows");
              requireThat(new Set(b.windows.map(w=>w.label)).size===b.windows.length, "Duplicate allowance window");
            }
            return json(await mutate(env.DB,{...b,action:"telemetry",source:"Owner WSL · Codex app-server",request_id:b.request_id ?? crypto.randomUUID()}));
          }
          requireThat(["pause","resume"].includes(b.action),"Unsupported operator action");
          return json(await mutate(env.DB,{action:b.action,request_id:b.request_id ?? crypto.randomUUID()}));
        }
        requireThat(!["pause","resume"].includes(b.action),"Use the owner controls",403);
        const result=await mutate(env.DB,b);
        return json(result,b.action==="observe" && result.admitted===false ? 429 : 200);
      }
      if (path.startsWith("/api/")) return json({error:"Unknown API route"},404);
      if (request.method!=="GET" && request.method!=="HEAD") return json({error:"Method unavailable"},405);
      if (path==="/archive" || path==="/demo" || path==="/archive/demo") return Response.redirect(url.origin+path+"/"+url.search,308);
      const asset=Object.hasOwn(ASSETS,path) && ASSETS[path];
      if (!asset) return new Response("Page not found",{status:404});
      return new Response(request.method==="HEAD" ? null : asset[1],{headers:{"Content-Type":asset[0],"Cache-Control":"private, no-cache","X-Content-Type-Options":"nosniff","Referrer-Policy":"same-origin"}});
    } catch (e) {
      return json({error:e instanceof Problem ? e.message : "Queue database or runtime unavailable"},e instanceof Problem ? e.status : 503);
    }
  }
};
