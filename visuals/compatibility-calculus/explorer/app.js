/* UI state selects exact model records; display toggles never alter feasibility. */
(() => {
 'use strict';
 const M=createExplorerModel(CC,CC_EXPLORER.geometry,CC_EXPLORER.examples),{R,el,add,clearSVG}=CC;
 const state={ray:'B',q:6,count:7,question:'optimum',threshold:'1/8',rep:'caps',object:'B',z:'4/25',h:-2,position:'0',reflected:false,angle:28,tilt:32,full:false,caps:false,orbit:true,equalities:true,projection:true,lattice:true,recovery:true,phases:true,transfer:false,component:0};
 const choices=()=>state.rep==='caps'?M.caps:state.rep==='selector'?M.segments:M.shapes(state.count);
 const current=()=>choices().find(s=>s.id===state.object)||choices()[0];
 const output=()=>M.analyze(state.ray,state.q,state.count);
 const safe=()=>state.threshold==='1/8'?output().safe:M.safeSet(state.ray,state.q,state.count,state.threshold);
 const txt=(node,x,y,value,attrs={})=>add(node,'text',{x,y,...attrs},String(value));
 function selectOptions(id,options,value){const select=el(id);select.replaceChildren(...options.map(([v,label])=>{const o=document.createElement('option');o.value=v;o.textContent=label;return o;}));select.value=String(value);}
 function selectTime(t,z,preferred=null){
  const mapped=M.coordinates(state.ray,state.q,t,z);let found=choices().find(s=>s.id===preferred&&M.contains(s,mapped.point))||choices().find(s=>M.contains(s,mapped.point));
  if(!found){state.rep='full';found=M.shapes(state.count).find(s=>M.contains(s,mapped.point));}
  if(!found)throw Error('Recovered physical point is absent from the pinned atlas');
  state.object=found.id;state.z=String(R(z));state.h=mapped.h;state.reflected=mapped.reflected;
  const record=M.inspect(found,state.ray,state.q,state.z,state.h,0),[a,b]=record.common;
  if(!a)throw Error('Recovery lost the same-point slice');
  const lo=M.time(state.ray,a),hi=M.time(state.ray,b),target=M.time(state.ray,mapped.point);
  state.position=hi.cmp(lo)===0?'0':String(target.sub(lo).div(hi.sub(lo)).mul(100));
 }
 function first(){const hits=M.contacts(current(),state.ray,state.q);state.reflected=false;state.position='0';if(hits.length){state.z=String(hits[0].height);state.h=hits[0].h;}else{state.z=String(current().vertices.map(p=>p[2]).reduce(M.max));state.h=Number(M.ceil(M.range(current().vertices.map(p=>M.orbit(state.ray,state.q,p)))[0]));}}
 function answerTime(){const a=output();if(state.question==='witness')return{t:a.witness.time,z:a.witness.height,preferred:a.witness.shape};if(state.question==='safe'){const s=safe();return s.intervals.length?{t:s.intervals[0][0],z:s.threshold}:null;}return{t:a.times[0],z:a.maximum};}
 function resetSelection(){state.component=0;state.reflected=false;state.rep=state.count===7&&state.ray==='B'&&state.question!=='safe'?'caps':state.count===7&&state.ray==='A'&&state.question==='witness'?'selector':'full';state.object=choices()[0].id;const a=answerTime();if(a)selectTime(a.t,a.z,a.preferred);else{state.z=state.threshold;first();state.z=state.threshold;}}
 function setPreset(name){
  state.count=7;state.threshold='1/8';state.transfer=false;state.equalities=true;state.full=false;el('q-message').textContent='';el('q').removeAttribute('aria-invalid');
  if(name==='b-contact'){state.ray='B';state.q=6;state.question='optimum';}
  else{state.ray='A';state.q=name==='fallback'?5:name==='face'?10:4;state.question=name==='fallback'?'witness':name==='face'?'maximizers':'safe';}
  resetSelection();
  if(name==='face'){state.transfer=true;selectTime('17/35','1/7','C9');}
  if(name==='removed'){state.count=6;state.rep='full';state.object='P2';state.z='1/8';state.h=1;state.position='0';state.reflected=false;state.transfer=true;}
  render();
 }
 function hull(points){const unique=[...new Map(points.map(p=>[p.join(','),p])).values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);if(unique.length<3)return unique;const cross=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]),chain=values=>{const out=[];for(const p of values){while(out.length>=2&&cross(out.at(-2),out.at(-1),p)<=0)out.pop();out.push(p);}return out;};return[...chain(unique).slice(0,-1),...chain([...unique].reverse()).slice(0,-1)];}
 function geometry(record){
  const node=el('geometry'),height=410,width=clearSVG(node,height),shape=current(),context=state.full?M.shapes(state.count):[],caps=state.caps&&state.count===7?M.caps:[],all=[shape,...context,...caps].flatMap(s=>s.vertices.map(p=>p.map(v=>R(v).number())));
  const center=[0,1,2].map(i=>(Math.min(...all.map(p=>p[i]))+Math.max(...all.map(p=>p[i])))/2),az=state.angle*Math.PI/180,tilt=state.tilt*Math.PI/180;
  const value=v=>typeof v==='number'?v:R(v).number();
  const raw=p=>{const x=value(p[0])-center[0],y=value(p[1])-center[1],z=2*(value(p[2])-center[2]);return[x*Math.cos(az)-y*Math.sin(az),(x*Math.sin(az)+y*Math.cos(az))*Math.sin(tilt)-z*Math.cos(tilt)];};
  const projected=all.map(raw),low=[0,1].map(i=>Math.min(...projected.map(p=>p[i]))),high=[0,1].map(i=>Math.max(...projected.map(p=>p[i]))),scale=Math.min((width-90)/(high[0]-low[0]||1),(height-105)/(high[1]-low[1]||1));
  const project=p=>{const r=raw(p);return[width/2+(r[0]-(low[0]+high[0])/2)*scale,height/2-8+(r[1]-(low[1]+high[1])/2)*scale];},pts=points=>hull(points.map(project)).map(p=>p.join(',')).join(' ');
  function draw(s,ghost=false,cap=false){
   if(!ghost)for(const face of M.facets(s))add(node,'polygon',{points:pts(face.map(i=>s.vertices[i])),fill:'var(--green)','fill-opacity':.07});
   for(const [i,j]of s.edges)add(node,'polyline',{points:[project(s.vertices[i]),project(s.vertices[j])].map(p=>p.join(',')).join(' '),fill:'none',stroke:cap?'var(--amber)':'var(--green)','stroke-width':ghost?1:1.8,'stroke-opacity':ghost?.25:1,'stroke-dasharray':ghost?'3 3':'none'});
   if(s.dimension===0&&state.equalities){const [x,y]=project(s.vertices[0]);add(node,'circle',{cx:x,cy:y,r:7,fill:'var(--surface)',stroke:'var(--green)','stroke-width':2.5,class:'singleton'});txt(node,x+10,y-8,s.id,{class:'small'});}
  }
  context.filter(s=>s.id!==shape.id).forEach(s=>draw(s,true));caps.filter(s=>s.id!==shape.id).forEach(s=>draw(s,true,true));draw(shape);
  if(record.section.length>1)add(node,'polygon',{points:pts(record.section),fill:'var(--amber)','fill-opacity':.14,stroke:'var(--amber)','stroke-width':1.5});
  else if(record.section.length&&state.equalities){const [x,y]=project(record.section[0]);add(node,'circle',{cx:x,cy:y,r:5,fill:'var(--amber)'});}
  if(state.orbit&&record.point){const positive=record.common.length&&M.time(state.ray,record.common[0]).cmp(M.time(state.ray,record.common[1]))!==0;if(positive)add(node,'polyline',{points:record.common.map(project).map(p=>p.join(',')).join(' '),stroke:'var(--blue)','stroke-width':3});if(state.equalities||positive){const [x,y]=project(record.point);add(node,'circle',{cx:x,cy:y,r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});}}
  txt(node,12,22,`${state.ray==='A'?state.q+'x − y':'x − '+state.q+'y'} = H`,{class:'small'});
  txt(node,12,height-12,`Folded x ≤ 1/2 · vertical scale ×2`,{class:'small'});
  const origin=[width-45,height-47];for(const [name,dx,dy]of [['x',Math.cos(az),Math.sin(az)*Math.sin(tilt)],['y',-Math.sin(az),Math.cos(az)*Math.sin(tilt)],['z',0,-Math.cos(tilt)]]){add(node,'line',{x1:origin[0],y1:origin[1],x2:origin[0]+dx*22,y2:origin[1]+dy*22,stroke:'var(--muted)'});txt(node,origin[0]+dx*22+3,origin[1]+dy*22-2,name,{class:'small'});}
  el('geometry-caption').textContent=`${shape.id}: ${shape.vertices.length} ${shape.vertices.length===1?'vertex':'vertices'}, ${shape.edges.length} edges. ${state.rep==='caps'?'The cap omits geometry below 1/7. ':''}${state.equalities?'Closed singleton markers are included.':'Equality markers are hidden in this drawing; exact results still include equality.'} Camera motion changes only the view.`;
 }
 function projection(record){
  const node=el('projection'),height=132,width=clearSVG(node,height);node.hidden=!state.projection;
  el('selector-tests').hidden=state.rep!=='selector';
  if(state.rep==='selector'){const selector=M.selector(state.q);el('selector-tests').replaceChildren(...selector.trials.map((trial,i)=>{const p=document.createElement('p'),needed=i===0||!selector.trials[0].accepted;p.textContent=`${trial.segment} · [${trial.interval.join(', ')}] · ${needed?`integer ${trial.h} ${trial.accepted?'hits':'misses'}`:'second test not needed'}`;return p;}));}
  el('projection-value').textContent=record.interval?`H(section) = [${record.interval.join(', ')}]`:'Empty horizontal section';
  if(!record.interval)return;const values=[...record.interval,R(state.h)],lo=values.reduce(M.min).floor()-1n,hi=M.ceil(values.reduce(M.max))+1n;
  const x=v=>22+R(v).sub(lo).div(R(hi).sub(lo)).number()*(width-44),y=64;
  add(node,'line',{x1:22,y1:96,x2:width-22,y2:96,stroke:'var(--line)'});
  const labelStep=BigInt(Math.max(1,Math.ceil(Number(hi-lo)*28/(width-44))));
  if(state.lattice)for(let h=lo;h<=hi;h++){add(node,'line',{x1:x(h),y1:26,x2:x(h),y2:101,stroke:'var(--line)','stroke-dasharray':'3 4'});if(h%labelStep===0n)txt(node,x(h),118,h,{'text-anchor':'middle',class:'small'});}
  add(node,'line',{x1:x(record.interval[0]),y1:y,x2:x(record.interval[1]),y2:y,stroke:record.point?'var(--green)':'var(--amber)','stroke-width':6,'stroke-linecap':'round'});
  for(const v of record.interval)if(state.equalities)add(node,'circle',{cx:x(v),cy:y,r:3.5,fill:'var(--green)'});
  add(node,'circle',{cx:x(state.h),cy:y,r:7,fill:record.point?'var(--blue)':'var(--surface)',stroke:'var(--blue)','stroke-width':2});txt(node,x(state.h),17,`H=${state.h}`,{'text-anchor':'middle'});
 }
 function answer(){
  const a=output(),s=state.question==='safe'?safe():null,one=state.question==='witness';
  el('answer-value').textContent=one?`t = ${a.witness.time}`:state.question==='safe'?s.intervals.length?`${s.intervals.length} closed components`:'∅ · no safe time':state.question==='maximizers'?`${a.times.length} maximizing times`:`Maximum = ${a.maximum}`;
  el('answer-copy').textContent=one?`One recoverable time meets the 1/8 target. ${state.ray==='A'&&state.count===7?`The pinned E1-then-E2 selector chooses ${a.witness.shape}.`: 'This control uses an attaining orbit contact.'} This output does not enumerate the optimum or complete safe set.`:state.question==='safe'?`At threshold ${s.threshold}, the complete set has duration ${s.duration}. Isolated points count as nonempty components.`:`The optimum is ${a.maximum}. All closed integer-orbit sections of the full ${state.count===7?'ten-cell':'eight-parent'} atlas are included, with reflection and duplicate times reconciled.`;
  el('answer-source').textContent=one&&state.ray==='A'&&state.count===7?'Answer source: pinned two-segment selector + physical recovery.':'Answer source: full closed atlas + every compatible integer orbit. The selected view below is an inspector.';
  el('domain').textContent=`${state.count+1} common-start runners · reference 0 · ${state.count} required moving speeds`;
  el('map').textContent=state.ray==='A'?`A${state.q}: H = ${state.q}x − y ∈ ℤ · t = x`:`B${state.q}: H = x − ${state.q}y ∈ ℤ · t = y`;
  el('speeds').textContent=`Speeds: 0; ${a.speeds.join(', ')}${state.count===6?' · fixed 1/8 comparison floor':''}`;
  el('use-answer').disabled=!answerTime();
  el('set-panel').hidden=!['safe','maximizers'].includes(state.question);
  if(!['safe','maximizers'].includes(state.question))return;
  const intervals=s?s.intervals:a.times.map(t=>[t,t]),singletons=intervals.filter(([l,r])=>l.cmp(r)===0).length;
  el('set-title').textContent=s?`Every time meeting ${s.threshold}`:`Every time attaining ${a.maximum}`;
  el('set-count').textContent=`${singletons} isolated ${singletons===1?'point':'points'}`;
  el('exact-set').textContent=intervals.length?intervals.map(([l,r])=>l.cmp(r)===0?`{${l}}`:`[${l}, ${r}]`).join(' ∪ '):'∅';
  el('time-field').hidden=!!s;el('component-field').hidden=!s;el('component-buttons').hidden=!s;
  const currentTime=window.CC_EXPLORER_STATE?.physical?.time;
  if(s){state.component=Math.min(state.component,Math.max(0,intervals.length-1));selectOptions('component-choice',intervals.map(([l,r],i)=>[i,l.cmp(r)===0?`{${l}}`:`[${l}, ${r}]`]),state.component);for(const b of document.querySelectorAll('[data-endpoint]'))b.disabled=!intervals.length;}
  else selectOptions('time-choice',[['','Choose an attaining time'],...a.times.map(t=>[String(t),String(t)])],a.times.some(t=>String(t)===currentTime)?currentTime:'');
  const node=el('times'),w=clearSVG(node,122),x=t=>22+R(t).number()*(w-44),y=59;
  add(node,'line',{x1:22,y1:y,x2:w-22,y2:y,stroke:'var(--line)'});
  for(const [l,r]of intervals){if(l.cmp(r)!==0)add(node,'line',{x1:x(l),y1:y,x2:x(r),y2:y,stroke:'var(--green)','stroke-width':7});if(state.equalities)for(const t of l.cmp(r)===0?[l]:[l,r])add(node,'circle',{cx:x(t),cy:y,r:l.cmp(r)===0?5:3,fill:l.cmp(r)===0?'var(--surface)':'var(--green)',stroke:'var(--green)','stroke-width':2,class:l.cmp(r)===0?'time-singleton':'time-endpoint'});}
  for(const t of ['0','1/4','1/2','3/4','1'])txt(node,x(t),95,t,{'text-anchor':'middle',class:'small'});
  if(currentTime)add(node,'line',{x1:x(currentTime),y1:36,x2:x(currentTime),y2:77,stroke:'var(--blue)','stroke-width':1.5,'stroke-dasharray':'3 3',class:'inspected-time'});
  txt(node,22,23,'Exact set · blue cursor = inspected time',{class:'small'});
  el('equality-notice').hidden=state.equalities;el('equality-notice').textContent=`Equality markers hidden in the plot. The exact set above still retains ${singletons} isolated points and every closed endpoint. Hiding a marker does not remove a solution.`;
 }
 function scope(){
  const full=state.rep==='full',caps=state.rep==='caps',a=output();
  el('scope-heading').textContent=full?'Full labelled geometry':caps?'Top-cap compression':'One-witness compression';
  el('scope-copy').textContent=full?'This view retains a selected closed cell. The requested global answer is recovered from all cells and all compatible integer orbits.':caps?'Seven caps carry the B-ray upper geometry after an attaining witness places the optimum above 1/7. A selected cap alone is a local comparison.':'E1 and E2 are sufficient for the pinned A-ray one-witness question. The q=5 fallback is retained in the same ordered rule.';
  el('retained').textContent=full?'Labels, faces, edges, equalities, shared orbit and exact physical recovery.':caps?'Cap identity, section endpoints, integer contacts, clock and recovery map.':'Both closed segments, order of tests, integer contact and one physical time.';
  el('omitted').textContent=full?'The drawing shows one selection; screen coordinates omit exact metric information.':'Other '+(caps?'lower cells and the complete 1/8-safe set.':'safe alternatives, the optimum and the complete time set.');
  el('recover').textContent='Select full labelled cells and reapply the same orbit before changing the threshold, adding a constraint or asking for every solution. Pinned source links remain below.';
  const incompatible=caps&&(state.ray!=='B'||state.count!==7||state.question==='safe'||a.maximum.cmp('1/7')<=0)||state.rep==='selector'&&(state.ray!=='A'||state.count!==7||state.question!=='witness');
  el('scope-warning').hidden=!incompatible;el('scope-warning').textContent='This displayed compression does not supply the requested complete output. The answer panel uses the richer full atlas; its exact result is not replaced by this partial view.';
 }
 function runnerTrack(physical,z){
  const node=el('runners'),w=clearSVG(node,300),cx=w/2,cy=148,r=Math.min(88,(w-104)/2),xy=(phase,radius=r)=>[cx+Math.sin(2*Math.PI*phase)*radius,cy-Math.cos(2*Math.PI*phase)*radius];
  add(node,'circle',{cx,cy,r,fill:'none',stroke:'var(--line)','stroke-width':2});
  const arc=Array.from({length:61},(_,i)=>xy(-z.number()+2*z.number()*i/60).join(','));add(node,'polyline',{points:arc.join(' '),fill:'none',stroke:'var(--red)','stroke-opacity':.35,'stroke-width':7,'stroke-dasharray':'3 4'});
  const groups=new Map();for(const row of physical.runners.filter(r=>r.required)){const key=String(row.phase);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(row);}
  const labels=[];for(const group of groups.values()){
   const phase=group[0].phase.number(),p=xy(phase),limiting=group.some(row=>row.distance.cmp(physical.minimum)===0),s=group.map(row=>row.speed).join(','),half=s.length*3.7+3;let l,b;
   for(const offset of [0,.03,-.03,.06,-.06,.09,-.09,.12,-.12,.16,-.16]){l=xy(phase+offset,r+22);l[0]=Math.max(half+3,Math.min(w-half-3,l[0]));b=[l[0]-half,l[1]-10,l[0]+half,l[1]+6];if(!labels.some(v=>b[0]<v[2]+3&&b[2]>v[0]-3&&b[1]<v[3]+3&&b[3]>v[1]-3))break;}
   labels.push(b);add(node,'circle',{cx:p[0],cy:p[1],r:limiting?6:4,fill:limiting?'var(--green)':'var(--blue)',stroke:'var(--surface)','stroke-width':1.5});add(node,'line',{x1:p[0],y1:p[1],x2:l[0],y2:l[1],stroke:'var(--line)'});txt(node,l[0],l[1]+4,s,{'text-anchor':'middle'});
  }
  const p=xy(0);add(node,'rect',{x:p[0]-4,y:p[1]-4,width:8,height:8,fill:'var(--text)'});txt(node,cx,cy-r-24,'0 · reference',{'text-anchor':'middle',class:'small'});txt(node,cx,cy-7,'PHYSICAL TIME',{'text-anchor':'middle',class:'small'});txt(node,cx,cy+18,physical.time,{'text-anchor':'middle',style:'font:23px Georgia,serif'});txt(node,cx,286,'Speed labels · green = limiting',{'text-anchor':'middle',class:'small'});
 }
 function recovery(record){
  el('recovery-content').hidden=!record.point||!state.recovery;el('recovery-empty').hidden=!!record.point;
  el('reflection').disabled=!record.point;
  if(!record.point)return null;
  const t=state.reflected?R(1).sub(record.time):record.time,p=M.physical(state.ray,state.q,t,state.count),z=R(state.z);
  if(p.minimum.cmp(z)<0)throw Error('Displayed point fails a required physical constraint');
  el('physical-time').textContent=String(t);el('minimum').textContent=String(p.minimum);
  const m=M.rows.map(([a,b])=>record.point[0].mul(a).add(record.point[1].mul(b)).floor()),order=state.ray==='B'?[1,0,2,3,4,5,6]:[0,1,2,3,4,5,6];
  el('recovery-map').textContent=`Folded point (${record.point.join(', ')}) · H=${record.h} · t=${state.ray==='A'?'x':'y'}=${record.time}${state.reflected?` → reflected ${t}`:''}`;
  el('recovery-note').textContent=`All ${state.count} required distances are at least z=${z}. ${state.count===6?'The seventh speed is shown as unchecked; this is not a seven-form witness. ':''}Torus labels refer to the folded point. Physical laps refer to the displayed time. ${state.reflected?'Reflection keeps the folded drawing and checks 1−t directly.':''}`;
  el('phase-rows').replaceChildren(...p.runners.map((r,i)=>{const row=document.createElement('tr');row.className=!r.required?'unchecked':r.distance.cmp(z)<0?'failed':r.distance.cmp(p.minimum)===0?'limiting':'';for(const value of [r.speed,m[order[i]],r.lap,r.phase,r.distance,r.required?'yes':'unchecked']){const cell=document.createElement('td');cell.textContent=String(value);row.append(cell);}return row;}));
  el('runners').hidden=!state.phases;runnerTrack(p,z);return p;
 }
 function transfer(record){
  el('transfer-content').hidden=!state.transfer;if(!state.transfer)return null;
  const selected=current(),parentIndex=state.rep==='full'?state.count===6?Number(selected.id.slice(1)):selected.parent_index:state.rep==='caps'?M.cells[selected.cell].parent_index:selected.parent;
  const tr=M.transfer(state.ray,state.q,parentIndex,state.h),before=tr.before,all=[...before,...tr.after.flatMap(c=>c.points)];
  el('transfer-intro').textContent=`${tr.parent} → ${tr.children.join(', ')} · same ${state.ray}-ray q=${state.q}, H=${state.h}. Both sides use the fixed 1/8 floor. The comparison below includes the full vertical orbit section, independently of the horizontal inspector height.`;
  el('transfer-title').textContent=tr.afterBest?'A compatible child survives.':'No child meets this orbit.';
  el('transfer-result').textContent=`Parent slice: ${tr.beforeBest?`best z=${tr.beforeBest[2]} at t=${M.time(state.ray,tr.beforeBest)}`:'empty'}. Child slices: ${tr.afterBest?`best z=${tr.afterBest[2]} at t=${M.time(state.ray,tr.afterBest)}`:'empty'}.`;
  el('transfer-limit').textContent='These are local parent/child conclusions on one H. The global answer above is for the selected six- or seven-form system across every cell and orbit.';
  if(state.ray==='A'&&state.q===10&&parentIndex===7&&state.h===4)el('transfer-limit').textContent+=' The new 17/35 contact is inside an old face and on a new child edge. Old edges miss it and its reflection 18/35 while retaining six other maximizers.';
  el('transfer-exact').textContent=tr.afterBest?`Child point (${tr.afterBest.join(', ')})`:'Ambient children can exist while this physical slice is empty.';
  el('inspect-child').disabled=!tr.afterBest;
  el('marginal').hidden=!(state.ray==='A'&&state.q===4&&parentIndex===2&&state.h===1);
  const node=el('transfer'),height=310,w=clearSVG(node,height);let extent=M.range(all.map(p=>M.time(state.ray,p)))||[R(0),R(1)];if(extent[0].cmp(extent[1])===0)extent=[extent[0].sub('1/32'),extent[1].add('1/32')];
  const x=t=>48+R(t).sub(extent[0]).div(extent[1].sub(extent[0])).number()*(w-70),y=z=>height-58-R(z).sub('1/8').div('1/24').number()*(height-97);
  for(const z of ['1/8','1/6']){add(node,'line',{x1:48,y1:y(z),x2:w-22,y2:y(z),stroke:'var(--line)'});txt(node,40,y(z)+4,z,{'text-anchor':'end',class:'small'});}
  function plot(points,child){if(points.length>1)add(node,'polygon',{points:hull(points.map(p=>[x(M.time(state.ray,p)),y(p[2])])).map(p=>p.join(',')).join(' '),fill:child?'var(--green)':'var(--blue)','fill-opacity':child?.18:.04,stroke:child?'var(--green)':'var(--blue)','stroke-width':child?2:1.3,'stroke-dasharray':child?'none':'4 4'});else if(points.length&&state.equalities)add(node,'circle',{cx:x(M.time(state.ray,points[0])),cy:y(points[0][2]),r:6,fill:'var(--surface)',stroke:child?'var(--green)':'var(--blue)','stroke-width':2});}
  plot(before,false);tr.after.forEach(c=>plot(c.points,true));txt(node,48,15,'Separation z',{class:'small'});txt(node,48,30,'Dashed parent · solid children',{class:'small'});txt(node,48,height-34,extent[0],{class:'small'});txt(node,w-22,height-34,extent[1],{'text-anchor':'end',class:'small'});txt(node,w-22,height-9,`Physical time t = ${state.ray==='A'?'x':'y'}`,{'text-anchor':'end',class:'small'});if(!all.length)txt(node,w/2,160,'Empty orbit section',{'text-anchor':'middle'});
  return tr;
 }
 function controls(record){
  for(const [id,value]of [['ray',state.ray],['q',state.q],['question',state.question],['system',state.count],['threshold',state.threshold],['representation',state.rep]])el(id).value=value;
  el('threshold-field').hidden=state.question!=='safe';
  el('representation').querySelector('[value=caps]').disabled=state.count!==7;
  el('representation').querySelector('[value=selector]').disabled=state.count!==7||state.ray!=='A';
  selectOptions('object',choices().map(s=>[s.id,state.rep==='caps'?`Cap ${s.id} · C${s.cell}`:state.rep==='selector'?`${s.id} · closed segment`:`${s.id} · ${s.dimension===0?'singleton':s.vertices.length+' vertices'}`]),state.object);
  const shape=current(),span=M.range(shape.vertices.map(p=>p[2])),ratio=span[1].cmp(span[0])===0?R(0):span[1].sub(state.z).div(span[1].sub(span[0])).mul(100);
  el('depth').value=ratio.number();el('depth').disabled=span[1].cmp(span[0])===0;el('position').value=R(state.position).number();el('position').disabled=!record.point||!record.common.length||M.time(state.ray,record.common[0]).cmp(M.time(state.ray,record.common[1]))===0;
  const hRange=M.range(shape.vertices.map(p=>M.orbit(state.ray,state.q,p))),options=[];for(let h=Number(hRange[0].floor())-1;h<=Number(M.ceil(hRange[1]))+1;h++)options.push([h,String(h)]);if(!options.some(([h])=>h===state.h))options.push([state.h,String(state.h)]);selectOptions('integer',options,state.h);
  el('height-value').textContent=`z = ${state.z}`;el('depth-label').textContent=`${span[1]} → ${span[0]}`;
  el('shape-title').textContent=state.rep==='caps'?`Cap ${shape.id}`:state.rep==='selector'?`Segment ${shape.id}`:`Cell ${shape.id}`;
  el('shape-status').textContent=record.point?'COMPATIBLE POINT':'AMBIENT / EMPTY SLICE';
  el('first-hit').disabled=!M.contacts(shape,state.ray,state.q).length;
  el('contact-note').textContent=record.point?`H=${state.h} meets this section. The selected point is (${record.point.join(', ')}).`:`H=${state.h} misses this section. ${record.integers.length?`Available integer contacts: ${record.integers.join(', ')}.`:'There is no integer in its projected interval.'} No physical witness is inferred.`;
  for(const [id,key]of [['full-context','full'],['caps-context','caps'],['orbit-visible','orbit'],['equalities','equalities'],['projection-visible','projection'],['lattice-visible','lattice'],['recovery-visible','recovery'],['phases-visible','phases'],['reflection','reflected'],['transfer-visible','transfer']])el(id).checked=state[key];
  el('caps-context').disabled=state.count!==7;el('tilt').value=state.tilt;
 }
 function render(writeURL=true){
  const record=M.inspect(current(),state.ray,state.q,state.z,state.h,state.position);controls(record);geometry(record);projection(record);scope();const physical=recovery(record),tr=transfer(record),a=output();
  const published=M.serialize({version:1,sourceCommit:CC_EXPLORER.manifest.source_commit,question:state.question,controls:state,answer:{maximum:a.maximum,times:a.times,witness:a.witness,safe:state.question==='safe'?safe():a.safe},inspector:record,physical,transfer:tr,scope:{representation:state.rep,answerSource:el('answer-source').textContent}});
  window.CC_EXPLORER_STATE=published;answer();published.scope.answerSource=el('answer-source').textContent;el('state-json').textContent=JSON.stringify(published,null,2);
  if(writeURL){const params=new URLSearchParams(Object.entries(state).map(([k,v])=>[k,String(v)]));history.replaceState(null,'','#'+params);}
 }
 function restore(){const p=new URLSearchParams(location.hash.slice(1));if(!p.size)return false;try{const q=Number(p.get('q')),ray=p.get('ray'),count=Number(p.get('count'));M.analyze(ray,q,count);if(!['witness','optimum','maximizers','safe'].includes(p.get('question')))throw Error('Unknown question');state.ray=ray;state.q=q;state.count=count;state.question=p.get('question');state.threshold=['1/8','1/7','1/6'].includes(p.get('threshold'))?p.get('threshold'):'1/8';resetSelection();const rep=p.get('rep');if(rep==='full'||rep==='caps'&&count===7||rep==='selector'&&ray==='A'&&count===7)state.rep=rep;state.object=choices().some(s=>s.id===p.get('object'))?p.get('object'):choices()[0].id;const z=R(p.get('z')||state.z),pos=R(p.get('position')||0),h=Number(p.get('h'));if(z.cmp('1/8')<0||z.cmp('1/6')>0||pos.cmp(0)<0||pos.cmp(100)>0||!Number.isInteger(h)||Math.abs(h)>61)throw Error('Invalid exact inspector state');state.z=String(z);state.position=String(pos);state.h=h;for(const key of ['reflected','full','caps','orbit','equalities','projection','lattice','recovery','phases','transfer'])if(p.has(key))state[key]=p.get(key)==='true';state.angle=Number(p.get('angle'))||28;state.tilt=Math.max(10,Math.min(65,Number(p.get('tilt'))||32));return true;}catch{Object.assign(state,{ray:'B',q:6,count:7,question:'optimum',threshold:'1/8'});resetSelection();el('q-message').textContent='The link contained an unsupported state. Restored the B6 contact control.';return true;}}
 for(const id of ['ray','question','system','threshold'])el(id).addEventListener('change',()=>{state[id==='system'?'count':id]=id==='system'?Number(el(id).value):el(id).value;resetSelection();render();});
 el('q').addEventListener('change',()=>{const q=Number(el('q').value);if(!Number.isInteger(q)||q<2||q>60){el('q-message').textContent='Enter an integer from 2 to 60. The last valid exact state is retained.';el('q').setAttribute('aria-invalid','true');return;}el('q-message').textContent='';el('q').removeAttribute('aria-invalid');state.q=q;resetSelection();render();});
 for(const b of document.querySelectorAll('[data-preset]'))b.addEventListener('click',()=>setPreset(b.dataset.preset));
 el('representation').addEventListener('change',()=>{state.rep=el('representation').value;state.object=choices()[0].id;first();render();});
 el('object').addEventListener('change',()=>{state.object=el('object').value;first();render();});
 el('depth').addEventListener('input',()=>{const [lo,hi]=M.range(current().vertices.map(p=>p[2]));state.z=String(hi.sub(hi.sub(lo).mul(R(el('depth').value).div(100))));state.reflected=false;render();});
 el('peak').addEventListener('click',()=>{state.z=String(current().vertices.map(p=>p[2]).reduce(M.max));state.position='0';state.reflected=false;render();});
 el('floor').addEventListener('click',()=>{state.z=String(current().vertices.map(p=>p[2]).reduce(M.min));state.position='0';state.reflected=false;render();});
 el('first-hit').addEventListener('click',()=>{first();render();});el('integer').addEventListener('change',()=>{state.h=Number(el('integer').value);state.position='0';state.reflected=false;render();});el('position').addEventListener('input',()=>{state.position=el('position').value;state.reflected=false;render();});
 for(const [id,key]of [['full-context','full'],['caps-context','caps'],['orbit-visible','orbit'],['equalities','equalities'],['projection-visible','projection'],['lattice-visible','lattice'],['recovery-visible','recovery'],['phases-visible','phases'],['reflection','reflected'],['transfer-visible','transfer']])el(id).addEventListener('change',()=>{state[key]=el(id).checked;render();});
 for(const [id,d]of [['rotate-left',-15],['rotate-right',15]])el(id).addEventListener('click',()=>{state.angle+=d;render();});el('tilt').addEventListener('input',()=>{state.tilt=Number(el('tilt').value);render();});el('reset-view').addEventListener('click',()=>{state.angle=28;state.tilt=32;render();});
 el('use-answer').addEventListener('click',()=>{const a=answerTime();if(a){selectTime(a.t,a.z,a.preferred);render();}});
  el('time-choice').addEventListener('change',()=>{if(el('time-choice').value){selectTime(el('time-choice').value,output().maximum);render();}});
 el('component-choice').addEventListener('change',()=>{state.component=Number(el('component-choice').value);const s=safe();selectTime(s.intervals[state.component][0],s.threshold);render();});
 for(const button of document.querySelectorAll('[data-endpoint]'))button.addEventListener('click',()=>{const s=safe(),[l,r]=s.intervals[state.component],t=button.dataset.endpoint==='left'?l:button.dataset.endpoint==='right'?r:l.add(r).div(2);selectTime(t,s.threshold);render();});
 el('inspect-child').addEventListener('click',()=>{const tr=window.CC_EXPLORER_STATE.transfer;if(!tr?.afterBest)return;const p=tr.afterBest,t=M.time(state.ray,p);state.count=7;state.rep='full';state.object=tr.after.find(c=>c.points.some(v=>v.join(',')===p.join(','))).id;selectTime(t,p[2],state.object);render();});
 el('download-state').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(window.CC_EXPLORER_STATE,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`cc-${state.ray}${state.q}-${state.question}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 for(const source of CC_EXPLORER.manifest.sources){const li=document.createElement('li'),a=document.createElement('a');a.href=CC_EXPLORER.manifest.repository+'/blob/'+CC_EXPLORER.manifest.source_commit+'/'+source;a.textContent=source;li.append(a);el('source-links').append(li);}
 el('build-info').textContent=`Source ${CC_EXPLORER.manifest.source_commit} · exact data ${CC_EXPLORER.manifest.data_build_sha256}. Later research remains a separate version.`;
 if(!restore())resetSelection();render();let resize=null;new ResizeObserver(()=>{cancelAnimationFrame(resize);resize=requestAnimationFrame(()=>render(false));}).observe(document.querySelector('main'));
 window.addEventListener('hashchange',()=>{restore();render(false);});
})();
