/* Closing synthesis: three exact recaps, with scope and recovery kept attached. */
(() => {
  const {R,el,add,clearSVG}=CC,data=CC_DATA.examples.story_visual,g=CC_DATA.geometry,m=CC_DATA.manifest;
  const state={case:'contact',step:0};
  const f=x=>String(R(x)),interval=pair=>`[${pair.map(f).join(', ')}]`,point=p=>`(${p.map(f).join(', ')})`;
  const c=data.contact,a=data.equality,j=data.joint,allTimes=a.components.map(pair=>f(pair[0]));
  const failed=j.candidate_physical.runners.find(row=>j.failed_speeds.includes(row.speed));
  const records={
    contact:{domain:`B RAY · q = ${c.q} · EIGHT COMMON-START RUNNERS`,record:'Geometry needs its physical map.',
      retained:'The same cap section, its entire H interval, the contact point, the B-ray clock and all seven physical phase checks.',
      omitted:'The cap view leaves out lower geometry. A projected interval alone also omits which point recovers a time.',
      recovery:'Keep the point at integer H, recover t=y, then check every runner. Restore full cells if the threshold or constraints change.',
      limit:'One contact certifies attainment. Optimality also needs comparison with the other caps and the matching upper-bound argument.',
      related:'#cap',link:'Revisit cap → contact → clock',status:'REPRODUCED: this finite q=6 control. The general B-ray spectrum remains an internally reviewed proof candidate.',
      steps:[
        ['Which safe geometric states can actually occur?','The peak of a safe cap is a compatible geometric state. The physical runners additionally require H=x−6y to be an integer.','NO PHYSICAL WITNESS YET','At the cap peak, H is not an integer. Geometry alone has not supplied an actual time.'],
        ['Carry the whole section through the projection.','Lowering the cap section expands one closed interval of H values. This checkpoint is halfway to the first integer contact.','THE SAME SECTION, STILL NO CONTACT','The interval contains no integer. No physical time is selected at this checkpoint.'],
        ['Test the integer condition at the same point.','At the first contact, the projected interval reaches an integer. Retain the point that realizes it so the next step can recover the clock.','INTEGER CONTACT RETAINED','The geometric point and orbit integer belong to the same state. They can now be translated back to the runners.'],
        ['Return to the runners and check the result.','The B-ray clock is t=y. Directly evaluate all seven phases and their distances at the recovered time.','PHYSICAL WITNESS RECOVERED',`At t=${f(c.controls[3].witness.time)}, every distance is at least ${f(c.maximum)}. This proves attainment in the displayed control; section 01 carries the optimum argument.`]
      ]},
    equality:{domain:`A RAY · q = ${a.q} · CLOSED THRESHOLD ${f(a.threshold)}`,record:'Duration cannot carry existence.',
      retained:'The question asks for the complete closed safe set on [0,1], including isolated times with exact equality.',
      omitted:'Keeping only positive-duration components deletes every safe time in this example. Total duration zero does not identify an empty set.',
      recovery:'Return to the closed physical bands and restore all singleton components. Verify each restored time against all seven speeds.',
      limit:'These four times exhaust this fixed q=4 threshold-safe set. The example does not classify another parameter or threshold.',
      related:'#representation',link:'Revisit the complete-safe-set question',status:'REPRODUCED: the exact q=4 closed safe set, including all four isolated witnesses.',
      steps:[
        ['What counts as a complete answer?','For this question, every threshold-safe time belongs in the answer. A set containing isolated points is still nonempty.','THE REQUESTED OUTPUT IS A SET',`The richer record contains ${allTimes.length} isolated safe times. Its total duration is ${f(a.duration)}.`],
        ['Try keeping only positive-duration components.','This compression retains intervals with positive length and discards singleton components. Watch what remains in the stored record.','THE COMPRESSED RECORD IS EMPTY','No positive-duration component survives. That is a fact about this compression, not evidence that no safe time exists.'],
        ['Test the inference against one omitted point.','Restore one exact time from the source and evaluate its physical distances. One valid point is enough to defeat the inference from zero duration to nonexistence.','A SOURCE WITNESS EXPOSES THE LOSS',`At t=${f(a.witnesses[0].time)}, the minimum distance is ${f(a.witnesses[0].minimum)}. The compressed duration record omitted a valid witness.`],
        ['Recover every closed component.','Intersect the original closed safe bands, preserving equal endpoints. The full set returns with all four witnesses.','THE REQUESTED SET IS RESTORED',`Safe times: {${allTimes.join(', ')}}. Every endpoint is included; the set still has total duration ${f(a.duration)}.`]
      ]},
    joint:{domain:`A RAY · q = ${j.q} · P${j.parent} · h = ${j.orbit_integer} · z = ${f(j.threshold)}`,record:'Two marginals can lose one relationship.',
      retained:'Parent P2, height z=1/8, the integer orbit h=1, and the added coordinate S=5x+2y must refer to one shared point.',
      omitted:'Separate H and S ranges omit which values can occur together. Their Cartesian product can contain pairs that no parent point realizes.',
      recovery:'Restore the parent and condition on the same h=1 slice. Only then intersect its conditional S interval with the added safe bands.',
      limit:'The empty intersection rejects only P2 at h=1,z=1/8. The full q=4 system still has four safe times elsewhere.',
      related:'#joint',link:'Revisit separate versus joint compatibility',status:'REPRODUCED: a finite false marginal pair and its exact same-slice exclusion.',
      steps:[
        ['Can both requirements hold at one point?','The H range contains an integer. The S range reaches a safe boundary. Each statement is true somewhere in the parent triangle.','TWO TRUE MARGINAL STATEMENTS','The remaining question is whether those two chosen values occur at the same point.'],
        ['Try combining the two highlighted values.','Invert the proposed (H,S) pair and check the resulting physical time. The added coordinate looks safe, but an original parent constraint fails.','FALSE COMBINATION REJECTED',`The candidate t=${f(j.candidate_physical.time)} gives speed ${failed.speed} distance ${f(failed.distance)}, below ${f(j.threshold)}. It is not a valid witness.`],
        ['Restore the relationship before intersecting.','Condition the parent on h=1. The resulting S interval lies strictly inside the blocked gap between the closed safe bands.','NO SAME-SLICE SAFE CONTACT',`${f(j.blocking_edges[0])} < ${f(j.conditional_S[0])} ≤ S ≤ ${f(j.conditional_S[1])} < ${f(j.blocking_edges[1])}. The entire conditional interval is blocked.`],
        ['Keep the precise scope of the rejection.','The repaired record returns an empty intersection for this parent, orbit and height. It returns no physical witness for that local question.','LOCAL INCOMPATIBILITY CERTIFIED','Reject this local branch and preserve the reason. Restore other cells before asking about existence in the full system.']
      ]}
  };
  function svg(height){const node=el('story-diagram'),w=clearSVG(node,height);node.style.height=`${height}px`;return{node,w};}
  function projection(control){
    const {node,w}=svg(205),low=R(-17).div(8),high=R(-19).div(12),x=value=>28+R(value).sub(low).div(high.sub(low)).number()*(w-56),y=94;
    add(node,'text',{x:28,y:27,class:'small'},'H = x − 6y');
    add(node,'line',{x1:28,x2:w-28,y1:y,y2:y,stroke:'var(--line)','stroke-width':2});
    add(node,'line',{x1:x(-2),x2:x(-2),y1:48,y2:148,stroke:'var(--blue)','stroke-dasharray':'4 3'});
    for(const value of [R(-2),R(c.h0)])add(node,'text',{x:x(value),y:174,'text-anchor':'middle',class:'small'},String(value));
    const color=control.integers.length?'var(--green)':'var(--amber)';
    add(node,'line',{x1:x(control.interval[0]),x2:x(control.interval[1]),y1:y,y2:y,stroke:color,'stroke-width':8,'stroke-linecap':'round'});
    for(const value of control.interval)add(node,'circle',{cx:x(value),cy:y,r:5,fill:'var(--surface)',stroke:color,'stroke-width':2});
    for(const value of control.integers)add(node,'circle',{cx:x(value),cy:y,r:8,fill:'var(--green)',stroke:'var(--surface)','stroke-width':2,class:'story-contact'});
    add(node,'text',{x:w/2,y:196,'text-anchor':'middle',class:'small'},control.integers.length?'Integer reached':'No integer in the interval');
  }
  function distances(witness,threshold){
    const {node,w}=svg(282),left=35,right=w-54,x=value=>left+R(value).number()*2*(right-left),delta=R(threshold);
    add(node,'text',{x:3,y:17,class:'small'},'Speed');add(node,'text',{x:w-5,y:17,'text-anchor':'end',class:'small'},'Distance');
    witness.runners.forEach((row,i)=>{
      const y=43+28*i;add(node,'text',{x:6,y:y+4,class:'small'},row.speed);
      add(node,'line',{x1:left,x2:right,y1:y,y2:y,stroke:'var(--line)'});
      add(node,'line',{x1:left,x2:x(row.distance),y1:y,y2:y,stroke:R(row.distance).cmp(delta)<0?'var(--red)':'var(--green)','stroke-width':6,'stroke-linecap':'round',class:'story-distance'});
      add(node,'text',{x:w-5,y:y+4,'text-anchor':'end'},f(row.distance));
    });
    add(node,'line',{x1:x(delta),x2:x(delta),y1:28,y2:224,stroke:'var(--amber)','stroke-dasharray':'4 3'});
    add(node,'text',{x:x(delta),y:245,'text-anchor':'middle',class:'small'},`≥ ${delta}`);
    add(node,'text',{x:left,y:273,class:'small'},'0');add(node,'text',{x:right,y:273,'text-anchor':'end',class:'small'},'1/2');
  }
  function timeSet(){
    const {node,w}=svg(211),left=24,right=w-24,x=t=>left+R(t).number()*(right-left);
    const rows=state.step===2?[{label:'Retained record',times:[],y:65},{label:'Source counterexample',times:[a.components[0][0]],y:144}]:[{label:state.step===1?'Retained positive-duration set':'Complete closed safe set',times:state.step===1?[]:a.components.map(p=>p[0]),y:96}];
    for(const row of rows){
      add(node,'text',{x:left,y:row.y-28,class:'small'},row.label);
      add(node,'line',{x1:left,x2:right,y1:row.y,y2:row.y,stroke:'var(--line)','stroke-width':2});
      for(const t of row.times){add(node,'circle',{cx:x(t),cy:row.y,r:6,fill:'var(--surface)',stroke:state.step===2?'var(--amber)':'var(--green)','stroke-width':2,class:'story-equality-point'});add(node,'text',{x:x(t),y:row.y+27,'text-anchor':'middle',class:'small'},f(t));}
      if(!row.times.length)add(node,'text',{x:w/2,y:row.y+27,'text-anchor':'middle',class:'small'},'∅ · nothing retained');
    }
    add(node,'text',{x:left,y:202,class:'small'},'t = 0');add(node,'text',{x:right,y:202,'text-anchor':'end',class:'small'},'t = 1');
  }
  function marginal(){
    const {node,w}=svg(224),left=35,right=w-35;
    for(const [i,range]of [j.marginal_H,j.marginal_S].entries()){
      const low=R(range[0]),high=R(range[1]),x=t=>left+R(t).sub(low).div(high.sub(low)).number()*(right-left),y=66+106*i;
      add(node,'text',{x:left,y:y-27,class:'small'},i===0?'Separate H range':'Separate S range');
      add(node,'line',{x1:left,x2:right,y1:y,y2:y,stroke:'var(--amber)','stroke-width':7,'stroke-linecap':'round'});
      add(node,'circle',{cx:x(j.candidate_hs[i]),cy:y,r:7,fill:'var(--surface)',stroke:'var(--blue)','stroke-width':2});
      add(node,'text',{x:left,y:y+28,'text-anchor':'middle',class:'small'},f(low));add(node,'text',{x:right,y:y+28,'text-anchor':'middle',class:'small'},f(high));
    }
  }
  function conditional(){
    const {node,w}=svg(221),left=29,right=w-29,low=R(j.blocking_edges[0]).sub(R(1).div(16)),high=R(j.blocking_edges[1]).add(R(1).div(16)),x=v=>left+R(v).sub(low).div(high.sub(low)).number()*(right-left);
    add(node,'text',{x:left,y:24,class:'small'},'S on the same h = 1 slice');
    add(node,'rect',{x:left,y:51,width:x(j.blocking_edges[0])-left,height:89,fill:'var(--green)','fill-opacity':.14});
    add(node,'rect',{x:x(j.blocking_edges[1]),y:51,width:right-x(j.blocking_edges[1]),height:89,fill:'var(--green)','fill-opacity':.14});
    add(node,'line',{x1:left,x2:right,y1:90,y2:90,stroke:'var(--line)'});
    for(const edge of j.blocking_edges){add(node,'line',{x1:x(edge),x2:x(edge),y1:51,y2:140,stroke:'var(--green)'});add(node,'circle',{cx:x(edge),cy:90,r:4,fill:'var(--green)'});add(node,'text',{x:x(edge),y:167,'text-anchor':'middle',class:'small'},f(edge));}
    add(node,'line',{x1:x(j.conditional_S[0]),x2:x(j.conditional_S[1]),y1:90,y2:90,stroke:'var(--amber)','stroke-width':7,'stroke-linecap':'round',class:'story-conditional-interval'});
    j.conditional_S.forEach((v,i)=>add(node,'text',{x:x(v),y:i===0?74:116,'text-anchor':'middle'},f(v)));
    add(node,'text',{x:w/2,y:199,'text-anchor':'middle',class:'small'},'J ∩ safe bands = ∅');
  }
  function certificate(witness,kind){
    const details=el('story-certificate');details.hidden=!witness;
    el('story-certificate-rows').replaceChildren();if(!witness){details.open=false;return;}
    el('story-certificate-title').textContent=kind==='rejected'?'Inspect the rejected candidate':'Inspect the recovered physical record';
    el('story-certificate-caption').textContent=`t = ${f(witness.time)} · minimum distance = ${f(witness.minimum)}. ${kind==='rejected'?'This candidate fails an original parent constraint.':'All seven non-reference runners are checked at this same time.'}`;
    for(const row of witness.runners){const tr=document.createElement('tr');for(const value of [row.speed,row.lap,f(row.phase),f(row.distance)]){const td=document.createElement('td');td.textContent=value;tr.append(td);}el('story-certificate-rows').append(tr);}
  }
  function render(){
    if(el('story-chapter').hidden)return;
    const record=records[state.case],step=record.steps[state.step];let values=[],caption='',witness=null,kind=null,evidence={};
    for(const button of document.querySelectorAll('[data-story-case]'))button.setAttribute('aria-pressed',String(button.dataset.storyCase===state.case));
    for(const button of document.querySelectorAll('[data-story-step]'))button.setAttribute('aria-pressed',String(Number(button.dataset.storyStep)===state.step));
    el('story-domain').textContent=record.domain;el('story-title').textContent=step[0];el('story-explanation').textContent=step[1];
    el('story-progress').textContent=`${state.step+1} / 4`;el('story-result-label').textContent=step[2];el('story-result-text').textContent=step[3];
    el('story-result').dataset.tone=state.case==='joint'||(state.case==='equality'&&[1,2].includes(state.step))?'caution':'safe';
    for(const key of ['retained','omitted','recovery','limit'])el(`story-${key}`).textContent=record[key];
    el('story-record-title').textContent=record.record;el('story-related').href=record.related;el('story-related').textContent=record.link+' →';el('story-claim-status').textContent=record.status;
    if(state.case==='contact'){
      const control=c.controls[state.step];evidence={interval:control.interval.map(f),integers:control.integers,loss:f(control.loss),height:f(control.height),point:control.point?control.point.map(f):null};
      values=[['Loss from peak',f(control.loss)],['Height',f(control.height)],['Closed H interval',interval(control.interval)]];
      if(state.step<3){projection(control);caption='The amber or green segment is one whole projected section. The dashed line marks integer −2. Exact endpoints are listed below.';if(control.point)values.push(['Contact point',point(control.point)]);}
      else{witness=control.witness;kind='accepted';distances(witness,R(1).div(8));values=[['Recovered time',f(witness.time)],['Minimum distance',f(witness.minimum)],['Point (x, y, z)',point(control.point)]];caption='Every bar is a physical distance at the recovered time. The dashed threshold is 1/8; the attained minimum is 4/25.';}
    }else if(state.case==='equality'){
      const restored=state.step===0||state.step===3;evidence={retainedTimes:restored?allTimes:[],sourceWitnessTime:state.step===2?f(a.witnesses[0].time):null,duration:f(a.duration)};
      timeSet();values=[['Total duration',f(a.duration)],['Times in retained record',String(restored?allTimes.length:0)],['Closed threshold',f(a.threshold)]];
      caption=state.step===2?'The two rows separate the empty retained record from one valid source witness. Restoring one point refutes the inference; the final checkpoint restores the complete set.':'Hollow rings are included singleton times, not holes. Time runs from 0 to 1; deleting the rings changes the stored set.';
      if(state.step>=2){witness=a.witnesses[0];kind=state.step===2?'source-counterexample':'accepted';}
    }else{
      evidence={candidatePair:j.candidate_hs.map(f),conditionalInterval:j.conditional_S.map(f),localEmpty:state.step>=2,failedSpeeds:state.step===1?j.failed_speeds:[]};
      if(state.step===0){marginal();values=[['Marginal H',interval(j.marginal_H)],['Marginal S',interval(j.marginal_S)],['Proposed pair',point(j.candidate_hs)]];caption='Separate number lines retain ranges but omit their joint relationship. The highlighted values need not come from one parent point.';}
      else if(state.step===1){witness=j.candidate_physical;kind='rejected';distances(witness,j.threshold);values=[['Candidate time',f(witness.time)],['Failed speed',String(failed.speed)],['Failed distance',f(failed.distance)]];caption='Red marks the original constraint that fails. A safe added coordinate does not rescue the incompatible candidate.';}
      else{conditional();values=[['Same-slice S interval',interval(j.conditional_S)],['Strictly blocked gap',`(${j.blocking_edges.map(f).join(', ')})`],['Local safe intersection','∅']];caption='Green bands include their boundary points. The amber conditional interval lies strictly between them. This is a local rejection, not a full-system nonexistence claim.';}
    }
    el('story-values').replaceChildren(...values.map(([label,value])=>{const div=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;div.append(dt,dd);return div;}));
    el('story-diagram-caption').textContent=caption;certificate(witness,kind);
    el('story-previous').disabled=state.step===0;el('story-next').disabled=state.step===3;
    el('story-next').textContent=state.step===3?'Case complete':'Next checkpoint →';
    window.CC_STORY_STATE={case:state.case,step:state.step,evidence,physical:witness?{kind,time:f(witness.time),minimum:f(witness.minimum),speeds:witness.runners.map(r=>r.speed),phases:witness.runners.map(r=>f(r.phase)),distances:witness.runners.map(r=>f(r.distance)),laps:witness.runners.map(r=>String(r.lap))}:null,related:record.related};
  }
  function changeStep(step){state.step=step;el('story-certificate').open=false;render();}
  for(const button of document.querySelectorAll('[data-story-case]'))button.addEventListener('click',()=>{state.case=button.dataset.storyCase;changeStep(0);});
  for(const button of document.querySelectorAll('[data-story-step]'))button.addEventListener('click',()=>changeStep(Number(button.dataset.storyStep)));
  el('story-next').addEventListener('click',()=>changeStep(Math.min(3,state.step+1)));el('story-previous').addEventListener('click',()=>changeStep(Math.max(0,state.step-1)));el('story-reset').addEventListener('click',()=>changeStep(0));
  el('story-source-counts').textContent=`${g.parent_child.parents.length} six-form parents · ${g.full_cells.length} seven-form cells · ${g.full_cells.filter(c=>c.singleton).length} singleton cells`;
  el('story-build-info').textContent=`Source snapshot ${m.source_commit.slice(0,12)} · data build ${m.data_build_sha256.slice(0,16)}. All three recaps derive from the existing exact controls.`;
  for(const source of [m.scene_sources.story,c.source,a.source,'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md','notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md','notes/CC_BOUNDED_SELECTOR_2026_09_29.md']){const li=document.createElement('li'),link=document.createElement('a');link.href=`${m.repository}/blob/${m.source_commit}/${source}`;link.textContent=source;li.append(link);el('story-source-links').append(li);}
  document.addEventListener('cc:chapter',render);new ResizeObserver(render).observe(el('story-chapter'));render();
})();
