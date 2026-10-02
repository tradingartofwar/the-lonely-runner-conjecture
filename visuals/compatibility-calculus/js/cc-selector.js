/* Pinned E1-then-E2 witness selector. Decisions and recovery use exact rationals. */
(() => {
  const {R,min,el,add,clearSVG}=CC;
  const data=CC_DATA.examples.selector_visual,geometry=CC_DATA.geometry,manifest=CC_DATA.manifest;
  const state={q:5,attempts:0,reflection:false};
  const ceil=x=>-R(0).sub(x).floor();
  const text=(svg,x,y,label,attrs={})=>add(svg,'text',{x,y,...attrs},label);
  function calculate(){
    const trials=data.segments.map(segment=>{
      const [a,b]=segment.endpoints.map(p=>p.map(R));
      const d=a[1].sub(b[1]).div(b[0].sub(a[0])),c=a[1].add(d.mul(a[0]));
      const lo=a[0].mul(R(state.q).add(d)).sub(c),hi=b[0].mul(R(state.q).add(d)).sub(c);
      const h=ceil(lo),accepted=R(h).cmp(hi)<=0;
      const x=accepted?R(h).add(c).div(R(state.q).add(d)):null;
      return {segment,lo,hi,h,accepted,c,d,point:x?[x,c.sub(d.mul(x)),R('1/8')]:null};
    });
    const chosen=trials.findIndex((trial,i)=>i<state.attempts&&trial.accepted);
    return {trials,chosen,selected:chosen>=0?trials[chosen]:null};
  }
  function drawSegments(trials,selected){
    const svg=el('selector-segments'),height=335,width=clearSVG(svg,height),pad={l:38,r:19,t:25,b:39};
    const x=v=>pad.l+R(v).div('1/2').number()*(width-pad.l-pad.r),y=v=>height-pad.b-R(v).div('5/8').number()*(height-pad.t-pad.b);
    add(svg,'title',{},`Two closed safe segments at height 1/8; q=${state.q}`);
    for(const v of ['0','1/4','1/2']){
      add(svg,'line',{x1:x(v),y1:pad.t,x2:x(v),y2:height-pad.b,stroke:'var(--line)','stroke-dasharray':'2 4'});
      text(svg,x(v),height-17,v,{'text-anchor':'middle'});
      add(svg,'line',{x1:pad.l,y1:y(v),x2:width-pad.r,y2:y(v),stroke:'var(--line)','stroke-dasharray':'2 4'});
      text(svg,pad.l-8,y(v)+4,v,{'text-anchor':'end'});
    }
    text(svg,pad.l,14,'y = {qt}');text(svg,width-pad.r,height-6,'x = t',{'text-anchor':'end',class:'small'});
    for(const trial of trials){
      const [a,b]=trial.segment.endpoints;
      add(svg,'line',{x1:x(a[0]),y1:y(a[1]),x2:x(b[0]),y2:y(b[1]),stroke:'var(--green)','stroke-width':5,'stroke-linecap':'round'});
      for(const p of [a,b])add(svg,'circle',{cx:x(p[0]),cy:y(p[1]),r:4.5,fill:'var(--green)',stroke:'var(--surface)','stroke-width':1});
      const mid=[R(a[0]).add(b[0]).div(2),R(a[1]).add(b[1]).div(2)];
      text(svg,x(mid[0])+12,y(mid[1])+5,trial.segment.segment,{class:'point-label'});
    }
    if(state.attempts){
      const trial=trials[state.attempts-1],points=new Map();
      function include(a,b){if(a.cmp(0)>=0&&a.cmp('1/2')<=0&&b.cmp(0)>=0&&b.cmp('5/8')<=0)points.set(`${a},${b}`,[a,b]);}
      for(const v of [R(0),R('5/8')])include(R(trial.h).add(v).div(state.q),v);
      for(const v of [R(0),R('1/2')])include(v,v.mul(state.q).sub(trial.h));
      const line=[...points.values()];
      if(line.length===2)add(svg,'line',{x1:x(line[0][0]),y1:y(line[0][1]),x2:x(line[1][0]),y2:y(line[1][1]),stroke:'var(--blue)','stroke-width':1.5,'stroke-dasharray':'5 4'});
      text(svg,width-pad.r,14,`H = ${trial.h}`,{'text-anchor':'end',class:'small'});
    }
    if(selected)add(svg,'circle',{cx:x(selected.point[0]),cy:y(selected.point[1]),r:7,fill:'var(--green)',stroke:'var(--surface)','stroke-width':2});
  }
  function rail(trial,index,chosen){
    const svg=el(`selector-rail-${index}`),height=120,width=clearSVG(svg,height),tested=index<state.attempts;
    const first=Math.min(trial.lo.number(),Number(trial.h)),last=Math.max(trial.hi.number(),Number(trial.h));
    const lo=Math.floor(first)-.3,hi=Math.ceil(last)+.3,x=v=>20+(v-lo)/(hi-lo)*(width-40);
    const intervalY=48,base=88;
    add(svg,'title',{},`${trial.segment.segment}: [${trial.lo},${trial.hi}]${tested?`; ceil(lower)=${trial.h}; ${trial.accepted?'accepted':'rejected'}`:'; not tested'}`);
    add(svg,'line',{x1:20,y1:base,x2:width-20,y2:base,stroke:'var(--line)'});
    for(let h=Math.ceil(lo);h<=Math.floor(hi);h++){
      add(svg,'line',{x1:x(h),y1:25,x2:x(h),y2:base+4,stroke:'var(--line)','stroke-dasharray':'3 4'});
      text(svg,x(h),base+23,String(h),{'text-anchor':'middle',class:'small'});
    }
    add(svg,'line',{x1:x(trial.lo.number()),y1:intervalY,x2:x(trial.hi.number()),y2:intervalY,stroke:'var(--green)','stroke-width':5,'stroke-linecap':'round'});
    for(const v of [trial.lo,trial.hi]){add(svg,'circle',{cx:x(v.number()),cy:intervalY,r:4,fill:'var(--green)'});text(svg,x(v.number()),intervalY+24,String(v),{'text-anchor':'middle'});}
    if(tested){
      const px=x(Number(trial.h));
      if(trial.accepted)add(svg,'circle',{cx:px,cy:intervalY,r:7,fill:'var(--green)',stroke:'var(--surface)','stroke-width':2});
      else add(svg,'path',{d:`M ${px-5} ${intervalY-5} L ${px+5} ${intervalY+5} M ${px+5} ${intervalY-5} L ${px-5} ${intervalY+5}`,stroke:'var(--red)','stroke-width':2.5});
      text(svg,Math.min(width-43,Math.max(44,px)),15,`h = ${trial.h}`,{'text-anchor':'middle'});
    }
    const skipped=chosen===0&&index===1;
    const status=tested?(trial.accepted?'Accepted':'No integer'):skipped?'Not needed':index?'Waiting':'Not tested';
    el(`selector-status-${index}`).textContent=status;
    el(`selector-trial-${index}`).dataset.state=tested?(trial.accepted?'accepted':'failed'):skipped?'skipped':'waiting';
    el(`selector-interval-${index}`).textContent=`H(E${index+1}) = [${trial.lo}, ${trial.hi}]`;
    let caption;
    if(tested){
      caption=`ceil(${trial.lo}) = ${trial.h}. Check ${trial.h} ≤ ${trial.hi}: ${trial.accepted?'pass':'fail'}.`;
      if(trial.accepted&&R(trial.h).cmp(trial.lo)===0)caption+=' The closed lower endpoint supplies the witness.';
      if(trial.accepted&&R(trial.h).cmp(trial.hi)===0)caption+=' The closed upper endpoint supplies the witness.';
    }else caption=skipped?'E1 already supplied a witness. The selector stops without testing E2.':index?'Only test this segment if E1 fails.':'Choose the smallest integer at or above the lower endpoint, then check the closed upper endpoint.';
    el(`selector-test-${index}`).textContent=caption;
  }
  function physical(selected){
    const [x,y]=selected.point,h=selected.h,z=R('1/8'),segments=selected.segment;
    const example=CC_DATA.examples.A.find(e=>e.q===state.q),t=state.reflection?R(1).sub(x):x;
    const rows=example.speeds.map((speed,i)=>{
      const raw=t.mul(speed),phase=raw.frac(),lap=raw.floor(),[a,b]=geometry.parameter_families.common.rows[i];
      const torus=x.mul(a).add(y.mul(b)).sub(segments.torus_laps[i]);
      const originalLap=BigInt(segments.torus_laps[i])+BigInt(b)*h;
      const mappedLap=state.reflection?BigInt(speed)-1n-originalLap:originalLap;
      if(lap!==mappedLap||phase.cmp(state.reflection?R(1).sub(torus):torus)!==0)throw new Error('Selector physical map disagrees with direct time');
      return{speed,lap,phase,distance:min(phase,R(1).sub(phase))};
    });
    const minimum=rows.reduce((v,row)=>min(v,row.distance),R(1));
    if(minimum.cmp(z)!==0)throw new Error('Selector must return exact separation 1/8');
    el('selector-recovery-title').textContent=`${segments.segment} supplies the common point.`;
    el('selector-time').textContent=`t = ${x}`;
    el('selector-recovery-formula').textContent=`t = (h + ${selected.c}) / (q + ${selected.d}) = ${x}`;
    el('selector-point').textContent=`(${x}, ${y})`;el('selector-H').textContent=String(h);
    el('selector-recovery-copy').textContent=`Use y = ${selected.c} − ${selected.d}x. The same point lies on the safe segment and has qx − y = ${h}. Physical laps follow ℓᵢ = mᵢ + bᵢh; the table checks them directly from speed × time.`;
    el('selector-reflection-note').textContent=state.reflection?'The track and table show 1 − t. The segment diagram and recovery formula retain the original folded point.':'Filled points are the actual phases. The exact table keeps each runner separate when phases coincide.';
    el('selector-physical-summary').textContent=`At t = ${t}, every distance is at least 1/8; the minimum is exactly 1/8.`;
    el('selector-phase-rows').replaceChildren(...rows.map(row=>{const tr=document.createElement('tr');if(row.distance.cmp(z)===0)tr.className='active';for(const value of [row.speed,row.lap,row.phase,row.distance]){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;}));
    CCGeometry.runners(el('selector-track'),rows,z,t);
    return{time:String(t),minimum:String(minimum),laps:rows.map(r=>String(r.lap)),phases:rows.map(r=>String(r.phase)),distances:rows.map(r=>String(r.distance))};
  }
  function render(){
    if(el('selector-chapter').hidden)return;
    const {trials,chosen,selected}=calculate(),done=Boolean(selected);
    const example=CC_DATA.examples.A.find(e=>e.q===state.q);
    el('selector-q').value=String(state.q);el('selector-reflect').checked=state.reflection;
    el('selector-speeds').textContent=example.speeds.join(', ');
    el('selector-progress').textContent=!state.attempts?'No interval tested yet.':done?`Witness found after ${state.attempts} ${state.attempts===1?'test':'tests'}.`:'E1 failed. One fallback test remains.';
    el('selector-next').hidden=done;el('selector-run').hidden=done;
    el('selector-next').textContent=state.attempts?'Test E2 →':'Test E1 →';
    el('selector-recovery').hidden=!done;el('selector-physical').hidden=!done;
    const message=!state.attempts?'Every point on either segment satisfies the seven ambient bands. Test E1 to find out whether this q has an actual-orbit point there.':done?`${selected.segment.segment} contains H = ${selected.h}. Stop: one recoverable 1/8-safe time is enough for the requested output.`:'E1 contains no integer orbit value at q=5. That rejects this segment, not the runner system. E2 is the next test.';
    el('selector-decision').textContent=message;el('selector-decision').classList.toggle('select-failed',state.attempts>0&&!done);
    el('selector-geometry-caption').textContent=!state.attempts?'Both segments lie at height 1/8. Their endpoints and all seven joint bands stay attached to the record.':done?`The tested integer orbit H = ${selected.h} intersects ${selected.segment.segment} at the marked common point.`:'The dashed H = 1 line misses E1. No physical witness is selected after this failed test.';
    drawSegments(trials,selected);trials.forEach((trial,i)=>rail(trial,i,chosen));
    el('selector-scope-example').textContent=state.q===4?'At q=4, this selector returns 1/8. Even with its reflection 7/8, it leaves out the other isolated safe times 3/8 and 5/8.':state.q===10?'At q=10, the selected time 15/104 has separation 1/8. The archived optimum is 1/7. The selector succeeds at its one-witness task without optimizing.':'The selected time proves existence in the stated scope. It does not enumerate all witnesses or establish the optimum.';
    for(const row of el('selector-coverage-rows').children)row.classList.toggle('select-current',Number(row.dataset.q)===state.q);
    window.CC_SELECTOR_STATE={q:state.q,attempts:state.attempts,reflection:state.reflection,
      trials:trials.map((r,i)=>({interval:[String(r.lo),String(r.hi)],candidate:String(r.h),tested:i<state.attempts,accepted:i<state.attempts?r.accepted:null})),
      selectedSegment:selected?selected.segment.segment:null,point:selected?selected.point.map(String):null,
      H:selected?String(selected.h):null,selectedTime:selected?String(selected.point[0]):null,
      physical:done?physical(selected):null};
  }
  function reset(){state.attempts=0;state.reflection=false;render();}
  el('selector-q').addEventListener('change',()=>{state.q=Number(el('selector-q').value);reset();});
  el('selector-next').addEventListener('click',()=>{if(!calculate().selected){state.attempts=Math.min(2,state.attempts+1);render();}});
  el('selector-run').addEventListener('click',()=>{state.attempts=calculate().trials[0].accepted?1:2;render();});
  el('selector-reset').addEventListener('click',reset);
  el('selector-reflect').addEventListener('change',()=>{state.reflection=el('selector-reflect').checked;render();});
  el('selector-coverage-rows').replaceChildren(...geometry.selectors.A.small_coverage.map(r=>{
    const tr=document.createElement('tr');tr.dataset.q=r.q;
    for(const value of [r.q,String(R(r.interval[0])),r.first_integer,String(R(r.interval[1])),r.accept?'Yes':'No → E2']){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;
  }));
  el('selector-build-info').textContent=`Source commit ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}.`;
  for(const path of ['notes/CC_BOUNDED_SELECTOR_2026_09_29.md',manifest.scene_sources.selector_geometry,manifest.scene_sources.selector_physical]){
    const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=path;li.append(a);el('selector-source-links').append(li);
  }
  document.addEventListener('cc:chapter',render);new ResizeObserver(render).observe(el('selector-chapter'));render();
})();
