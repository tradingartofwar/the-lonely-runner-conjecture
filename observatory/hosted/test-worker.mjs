import assert from "node:assert/strict";
import {test} from "node:test";
import {readFile} from "node:fs/promises";
import {createRequire} from "node:module";

const sql=await readFile(new URL("./drizzle/0000_pilot_state.sql",import.meta.url),"utf8");
const workerSource=process.env.OBSERVATORY_WORKER_BUNDLE
  ? await readFile(process.env.OBSERVATORY_WORKER_BUNDLE,"utf8")
  : 'const ASSETS={"/":["text/html","Observatory"],"/archive/":["text/html","Archive"]};\n'+await readFile(new URL("./worker.mjs",import.meta.url),"utf8");
const ownerHeaders={"oai-authenticated-user-id":"owner-test",Origin:"https://observatory.example"};
const now=()=>new Date().toISOString();
const evidence={summary:"Exact example checked in the fixture.",artifact:"observatory/study/results.json",revision:"aaaaaaa",replay:"python observatory/study/verify.py"};
async function createHarness() {
  let send,db,close;
  if (process.env.OBSERVATORY_MINIFLARE) {
    const {Miniflare}=createRequire(import.meta.url)(process.env.OBSERVATORY_MINIFLARE);
    const mf=new Miniflare({modules:true,script:workerSource,compatibilityDate:"2025-12-01",d1Databases:["DB"]});
    db=await mf.getD1Database("DB");
    send=(url,init)=>mf.dispatchFetch(url,init);
    close=()=>mf.dispose();
  } else {
    const {DatabaseSync}=await import("node:sqlite");
    const sqlite=new DatabaseSync(":memory:");
    function statement(sqlText,args=[]) {
      return {bind:(...a)=>statement(sqlText,a),first:async()=>sqlite.prepare(sqlText).get(...args),
        run:async()=>({meta:{changes:Number(sqlite.prepare(sqlText).run(...args).changes)}})};
    }
    db={prepare:statement};
    const worker=(await import("data:text/javascript;base64,"+Buffer.from(workerSource).toString("base64"))).default;
    send=(url,init)=>worker.fetch(new Request(url,init),{DB:db});
    close=()=>sqlite.close();
  }
  await db.prepare(sql).run();
  let i=0;
  const request=(p,init)=>send("https://observatory.example"+p,init);
  async function post(path,b,headers={}) {
    const res=await request(path,{method:"POST",headers:{"Content-Type":"application/json",...headers},body:JSON.stringify(b)});
    return {status:res.status,...await res.json()};
  }
  const act=(action,body={},key)=>post("/api/dispatch",{action,request_id:key??"test-"+(++i),...body});
  const board=async()=>{const r=await request("/api/pilot");assert.equal(r.status,200);return r.json();};
  async function clock(edit) {
    const row=await db.prepare("SELECT document FROM pilot_state WHERE id=1").first();
    const s=JSON.parse(row.document); edit(s);
    await db.prepare("UPDATE pilot_state SET document=?,revision=revision+1 WHERE id=1").bind(JSON.stringify(s)).run();
  }
  return {request,act,post,board,clock,close};
}
const workerFields=r=>({id:r.job.id,worker:r.job.worker,lease_token:r.lease_token});
test("fenced, immediate proposal → independent review → new leased question, including retries",async()=>{
  const h=await createHarness();
  try {
    assert.equal((await h.board()).pilot.status,"not_started");
    assert.equal((await h.request("/archive/")).status,200);
    assert.equal((await h.act("begin")).status,200);
    const imported=await h.act("record",{source:"Independent signed-off fixture",events:[{time:now(),role:"verifier",state:"completed",task:"Recorded evidence."}],finding:{id:"first",...evidence,verifier:"intake-auditor",verified_at:now()}});
    assert.equal(imported.status,200);
    assert.equal((await h.act("seed",{id:"q",role:"researcher",task:"Investigate the first lead",source_finding_id:"first",protocol:"cohorts",seed:"1".repeat(32)})).status,200);
    assert.equal((await h.act("claim",{id:"q",worker:"intake-auditor"})).reason,"independent_worker_required");
    const [a,b]=await Promise.all(["a","b"].map(worker=>h.act("claim",{id:"q",mode:"model",worker})));
    const win=a.job?a:b;
    assert.equal([a,b].filter(x=>x.job).length,1);
    assert.equal(win.handoff.finding.id,"first");
    assert.equal((await h.board()).evaluation.followups_claimed,0);
    const released=await h.act("release",{...workerFields(win),reason:"Work interrupted"});
    assert.equal(released.job.state,"queued");
    const claim={id:"q",mode:"model",worker:"researcher-two",run_id:"session-two"};
    const lease=await h.act("claim",claim,"retry-claim");
    const retry=await h.act("claim",claim,"retry-claim");
    assert.equal(lease.lease_token,retry.lease_token);
    assert.equal((await h.act("claim",{...claim,worker:"other"},"retry-claim")).status,409);
    assert.equal((await h.act("complete",{...workerFields(win),...evidence})).status,409);
    assert.equal((await h.act("heartbeat",workerFields(lease))).status,200);
    const digest="d".repeat(64);
    const result={...evidence,result_digest:digest};
    const ret=await h.act("complete",{...workerFields(lease),...result},"return-proposal");
    assert.equal(ret.status,200);
    assert.equal((await h.act("complete",{...workerFields(lease),...result},"return-proposal")).next_job_id,ret.next_job_id);
    assert.equal((await h.act("claim",claim,"retry-claim")).status,409);
    assert.equal((await h.act("claim",{id:ret.next_job_id,worker:"new-name",run_id:"session-two"})).reason,"independent_worker_required");
    const audit=await h.act("claim",{id:ret.next_job_id,worker:"independent-3",mode:"deterministic"});
    assert.equal(audit.job.protocol,"cohorts");
    assert.equal(audit.handoff.parent.result_digest,digest);
    assert.equal((await h.act("complete",{...workerFields(audit),...evidence,verdict:"verified",result_digest:"f".repeat(64),decision:"Review the evidence."})).status,409);
    assert.equal((await h.board()).findings.length,1);
    const verdict=await h.act("complete",{...workerFields(audit),...result,verdict:"verified",next_question:"Does the result extend?",next_protocol:"wrap",next_seed:"2".repeat(32)});
    assert.equal(verdict.status,200);
    const child=await h.act("claim",{id:verdict.next_job_id,worker:"independent-4",mode:"deterministic"});
    assert.equal(child.job.source_finding_id,verdict.finding_id);assert.equal(child.job.parent_id,audit.job.id);
    assert.equal(child.job.protocol,"wrap");assert.equal(child.job.seed,"2".repeat(32));
    const board=await h.board();
    assert.equal(board.evaluation.model_dispatches,2);
    assert.equal(board.evaluation.deterministic_dispatches,2);
    assert.equal(board.evaluation.retries,1);
    assert.equal(board.evaluation.verified_findings,1);
    assert.equal(board.evaluation.followups_claimed,1);
    assert.equal(board.usage.tokens_used,null);assert.equal(board.usage.deterministic_runs,2);
    assert.equal(board.jobs.find(j=>j.id==="q").verified_by,audit.job.id);
    assert.equal(JSON.stringify(board).includes(lease.lease_token),false);
  } finally {await h.close();}
});
test("operator controls, quota evidence, Pacific-day model usage, concurrency and horizon",async()=>{
  const h=await createHarness();
  try {
    assert.equal((await h.post("/api/operator",{action:"pause"})).status,403);
    assert.equal((await h.post("/api/operator",{action:"pause"},{...ownerHeaders,Origin:"https://elsewhere.example"})).status,403);
    assert.equal((await h.post("/api/dispatch",{action:"begin",request_id:"bad-origin"},ownerHeaders)).status,403);
    assert.equal((await h.post("/api/operator",{action:"pause"},ownerHeaders)).status,200);
    assert.equal((await h.act("begin")).status,200);
    await h.act("seed",{id:"one",role:"researcher",task:"One"});
    await h.act("seed",{id:"two",role:"researcher",task:"Two"});
    assert.equal((await h.act("claim",{worker:"one-worker"})).reason,"paused");
    await h.post("/api/operator",{action:"resume"},ownerHeaders);
    const model=await h.act("claim",{worker:"one-worker",run_id:"run-A",id:"one"});
    const other=await h.act("claim",{worker:"another-worker",id:"two",mode:"deterministic"});
    assert.equal((await h.act("claim",{worker:"third-worker"})).reason,"active_lease_limit");
    assert.equal((await h.act("observe",{run_id:"coord-1",worker:"scheduled",mode:"model",state:"running",task:"Read and route real queue returns."})).status,200);
    assert.equal((await h.act("telemetry",{source:"Scheduler final receipt",measured_at:now(),run_id:"coord-1",input_tokens:1,output_tokens:2})).status,200);
    assert.equal((await h.act("observe",{run_id:"coord-1",worker:"scheduled",mode:"model",state:"completed",task:"Returned queue observations."})).status,200);
    const measured_at=now();
    assert.equal((await h.act("telemetry",{source:"Unrelated run",measured_at,run_id:"unrelated",input_tokens:19,output_tokens:1})).status,409);
    const windows=[{label:"5-hour",remaining_percent:79,resets_at:now()}];
    assert.equal((await h.post("/api/operator",{action:"usage",measured_at,windows,input_tokens:123},ownerHeaders)).status,400);
    assert.equal((await h.post("/api/operator",{action:"usage",measured_at,windows},ownerHeaders)).status,200);
    assert.equal((await h.act("telemetry",{source:"Actual plan probe",measured_at:now(),plan_error:"Meter unavailable"})).status,200);
    assert.equal((await h.act("telemetry",{source:"Run metadata",measured_at,run_id:"run-A",input_tokens:100,output_tokens:20,cached_input_tokens:30})).status,200);
    assert.equal((await h.act("telemetry",{source:"Run metadata",measured_at,run_id:"run-A",input_tokens:100,output_tokens:20,cached_input_tokens:30})).status,200);
    const board=await h.board();assert.equal(board.usage.tokens_used,123);assert.equal(board.evaluation.controller_runs,1);assert.equal(board.usage.cached_input_tokens,30);
    assert.equal(board.plan.last_attempt.error,"Meter unavailable");assert.equal(board.plan.windows[0].remaining_percent,79);
    await h.clock(s=>{s.jobs.find(j=>j.id==="one").lease_expires="2000-01-01T00:00:00.000Z";});
    assert.equal((await h.act("complete",{...workerFields(model),...evidence})).status,409);
    await h.act("telemetry",{source:"Actual provider",measured_at:now(),limit_reached:true});
    assert.equal((await h.act("claim",{worker:"third-worker",mode:"model"})).reason,"plan_limit_reached");
    assert.equal((await h.act("telemetry",{source:"Actual provider",measured_at:now(),plan_available:true})).status,200);
    assert.equal((await h.act("release",{...workerFields(other),reason:"Retry test"})).status,200);
    await h.clock(s=>{s.ends_at="2000-01-01T00:00:00.000Z";});
    await h.act("begin");
    assert.equal((await h.board()).pilot.status,"ended");
    assert.equal((await h.act("claim",{worker:"third-worker"})).reason,"pilot_ended");
  } finally {await h.close();}
});

test("18 distinct model reservations include controllers and retried jobs; seven slots remain for wakes",async()=>{
  const h=await createHarness();
  try {
    await h.act("begin");
    const observe=(run_id,state="running",requestId)=>h.act("observe",{run_id,mode:"model",state,task:"Actual coordinator observation"},requestId);
    const controller=await observe("same-invocation","running","same-start");
    assert.equal(controller.admitted,true);
    assert.equal((await observe("same-invocation","running","same-start")).admitted,true);
    assert.equal((await observe("same-invocation","completed")).status,200);
    for(let i=0;i<11;i++) {
      const jobId="budget-job-"+i;
      const run_id=i===0 ? "same-invocation" : "model-run-"+i;
      await h.act("seed",{id:jobId,role:"researcher",task:"Bounded test question"});
      if (i===0) {
        assert.equal((await h.act("claim",{id:jobId,worker:"worker-"+i,mode:"model",run_id,controller_run_id:"unobserved"})).status,409);
      }
      const lease=await h.act("claim",{id:jobId,worker:"worker-"+i,mode:"model",run_id,controller_run_id:"same-invocation"});
      assert.equal(lease.job.controller_run_id,"same-invocation");
      assert.equal(lease.status,200);assert.equal(lease.job.id,jobId);
      await h.act("release",{...workerFields(lease),reason:"Fixture interruption"});
      if (i===0) {
        assert.equal((await h.board()).evaluation.model_calls_reserved,1);
        assert.equal((await h.act("claim",{id:jobId,worker:"retry-worker",mode:"model",run_id})).reason,"model_run_id_already_claimed");
      }
    }
    let e=(await h.board()).evaluation;
    assert.equal(e.model_calls_reserved,11);assert.equal(e.model_calls_remaining,7);assert.equal(e.model_jobs_remaining,0);
    assert.equal((await h.act("claim",{id:"budget-job-0",worker:"extra-job",mode:"model"})).reason,"model_job_limit");
    for(let i=0;i<6;i++) assert.equal((await observe("wake-"+i)).admitted,true);
    const contested=await Promise.all(["last-A","last-B"].map(r=>observe(r,"running",r)));
    assert.deepEqual(contested.map(r=>r.status).sort(),[200,429]);
    const loser=contested.find(r=>r.status===429);
    assert.equal((await observe(loser.run_id,"running",loser.run_id)).status,429);
    assert.equal((await h.act("claim",{id:"budget-job-0",worker:"extra-job",mode:"model"})).reason,"model_call_limit");
    const board=await h.board();e=board.evaluation;
    assert.equal(e.model_calls_reserved,18);assert.equal(e.model_calls_remaining,0);
    assert.equal(e.model_dispatches,11);assert.equal(e.controller_runs,9);assert.equal(e.over_budget_controller_runs,1);
    assert.equal(board.events.filter(v=>v.kind==="controller_over_budget").length,1);
    assert.equal(board.events.filter(v=>v.kind==="claimed" && v.controller_run_id==="same-invocation").length,11);
    assert.equal(board.pilot.status,"model_limit");
    assert.equal(board.pilot.model_call_limit,18);
    assert.equal(board.pilot.model_dispatch_limit,11);
  } finally { await h.close(); }
});

async function endWindow(h) {
  const ended=Date.now()-2000;
  await h.clock(s=>{
    s.ends_at=new Date(ended).toISOString();
    s.started_at=new Date(ended-86400000).toISOString();
  });
  return new Date(ended).toISOString();
}
test("day-end advances only for verified follow-up work and freezes the previous research and usage measures",async()=>{
  const h=await createHarness();
  try {
    const initial=await h.act("begin");
    assert.equal((await h.act("advance",{expected_ends_at:initial.ends_at})).reason,"window_still_active");
    await h.act("seed",{id:"root",role:"researcher",task:"Bounded proposal"});
    const p=await h.act("claim",{id:"root",worker:"r-first",mode:"model"});
    const submitted=await h.act("complete",{...workerFields(p),...evidence});
    const a=await h.act("claim",{id:submitted.next_job_id,worker:"audit-first",mode:"deterministic"});
    const verified=await h.act("complete",{...workerFields(a),...evidence,verdict:"verified",next_question:"Check the verified result on a different family."});
    const controller={worker:"day-end",run_id:"closeout-1",mode:"model",task:"Measure the original window."};
    await h.act("observe",{...controller,state:"running"});
    await h.act("telemetry",{run_id:"closeout-1",measured_at:now(),source:"Actual final receipt",input_tokens:8,output_tokens:2});
    await h.act("seed",{id:"other",role:"researcher",task:"A separate outstanding assignment"});
    const busy=await h.act("claim",{id:"other",worker:"outstanding",mode:"deterministic"});
    const end=await endWindow(h);
    const seal={expected_ends_at:end};
    assert.equal((await h.act("claim",{worker:"another"})).reason,"pilot_ended");
    assert.equal((await h.act("advance",seal)).reason,"active_lease");
    await h.act("release",{...workerFields(busy),reason:"Stop before closeout"});
    await h.post("/api/operator",{action:"pause"},ownerHeaders);
    assert.equal((await h.act("advance",seal)).reason,"paused");
    await h.post("/api/operator",{action:"resume"},ownerHeaders);
    await h.act("telemetry",{source:"Actual provider",measured_at:now(),limit_reached:true});
    assert.equal((await h.act("advance",seal)).reason,"plan_limit_reached");
    await h.act("telemetry",{source:"Actual provider",measured_at:now(),plan_available:true});
    const [one,two]=await Promise.all([h.act("advance",seal,"day-end-A"),h.act("advance",seal,"day-end-B")]);
    const result=one.advanced ? one : two;
    assert.equal([one,two].filter(r=>r.advanced).length,1);
    assert.equal(result.window_number,2);assert.equal(result.qualifying_job_id,verified.next_job_id);
    assert.deepEqual(await h.act("advance",seal,one.advanced?"day-end-A":"day-end-B"),result);
    assert.equal((await h.act("advance",seal)).reason,"window_mismatch");
    let board=await h.board();
    const snapshot=board.windows[0];
    assert.equal(snapshot.ends_at,end);assert.equal(snapshot.window_number,1);assert.equal(snapshot.evaluation.verified_findings,1);
    assert.equal(snapshot.evaluation.model_calls_reserved,2);assert.equal(snapshot.usage.tokens_used,10);assert.equal(snapshot.usage.coverage,"partial");
    assert.equal(board.evaluation.model_calls_remaining,18);assert.equal(board.evaluation.model_jobs_remaining,11);assert.equal(board.evaluation.verified_findings,0);
    assert.equal((await h.act("begin")).ends_at,end);
    await h.act("observe",{...controller,state:"completed"});
    await h.act("telemetry",{run_id:"r-first",measured_at:now(),source:"Late actual receipt",input_tokens:2,output_tokens:1});
    const follow=await h.act("claim",{id:verified.next_job_id,worker:"new-solver",mode:"model"});
    assert.equal(follow.status,200);
    const review=await h.act("complete",{...workerFields(follow),...evidence});
    board=await h.board();
    assert.equal(board.evaluation.followups_claimed,1);assert.equal(board.evaluation.model_calls_reserved,1);
    assert.deepEqual(board.windows[0],snapshot);
    const secondEnd=await endWindow(h);
    const third=await h.act("advance",{expected_ends_at:secondEnd});
    assert.equal(third.advanced,true);assert.equal(third.qualifying_job_id,review.next_job_id);assert.equal(third.window_number,3);
    assert.equal((await h.board()).windows.length,2);
  } finally {await h.close();}
});
test("idle closeout records one decision, excludes historical leads and cannot refresh the allowance",async()=>{
  const h=await createHarness();
  try {
    await h.act("begin");
    await h.act("record",{source:"Prior reviewed record",finding:{id:"old",...evidence,verifier:"previous",verified_at:now()}});
    await h.act("seed",{id:"historic-seed",role:"researcher",task:"Follow a historical result",source_finding_id:"old"});
    const end=await endWindow(h);
    const one=await h.act("advance",{expected_ends_at:end});
    const two=await h.act("advance",{expected_ends_at:end});
    assert.equal(one.advanced,false);assert.equal(one.reason,"no_verified_followup");assert.equal(one.decision_id,two.decision_id);
    const board=await h.board();
    assert.equal(board.pilot.status,"ended");assert.equal(board.pilot.window_number,1);assert.equal(board.pilot.idle_reason,"no_verified_followup");
    assert.equal(board.decisions.length,1);assert.equal(board.windows.length,1);
    assert.equal((await h.act("claim",{worker:"after-idle"})).reason,"pilot_ended");
  } finally {await h.close();}
});
