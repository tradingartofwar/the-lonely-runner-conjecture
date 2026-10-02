/* Exact parent-to-child sets. Rendering floats never determine feasibility. */
(() => {
  const {R,min,el,add,clearSVG}=CC;
  const atlas=CC_DATA.geometry.parent_child,examples=CC_DATA.examples,manifest=CC_DATA.manifest;
  const state={case:'removed',stage:0,azimuth:35,orbit:true,reflection:false};
  const copy={
    removed:{title:'The parent shrinks to one ambient point.',before:'A whole triangle lies on H = 1.',after:'The child misses the physical orbit.',
      intro:'Parent P2 contains a triangular set of six-runner states on H = 1. Its floor is the safe interval [17/56, 5/16].',
      applied:'The seventh band leaves only C3 = (3/8, 1/8, 1/8). Its orbit value is H = 11/8, so no part of the H = 1 physical slice survives.',
      beforeResult:'The parent slice reaches separation 2/13 at t = 4/13. Runner 13 has not yet been required to be safe.',
      afterResult:'Ambient child: nonempty. Physical child on H = 1: empty. This removes the entire parent time interval.',
      band:'2 + z ≤ 5x + 2y ≤ 3 − z',bandCopy:'Only seventh lap k = 2 yields a child of P2. The other lap branches are empty.',
      recovery:'The old best time explains the failure.',recoveryCopy:'No child witness can be recovered from this orbit slice. At the old parent optimum t = 4/13, runner 13 completes exactly four laps and meets the reference. The table checks that rejected time; it is not a seven-runner witness.'},
    equality:{title:'A split keeps a singleton child.',before:'The orbit already touches one closed point.',after:'That same physical point survives.',
      intro:'On parent P4, the H = 1 slice is already a singleton: (3/8, 1/2, 1/8). Closed feasibility includes this zero-duration state.',
      applied:'The seventh band creates two children: singleton C5 at lap 2 and tetrahedron C6 at lap 3. H = 1 meets C5; it does not meet C6.',
      beforeResult:'At t = 3/8, the first six moving runners are all at least 1/8 from reference 0.',
      afterResult:'The added runner is exactly 1/8 away. Equality is allowed, so the isolated physical time remains safe.',
      band:'k + z ≤ 5x + 2y ≤ k + 1 − z',bandCopy:'Here k = 2 gives C5 and k = 3 gives C6. At C5, S = 23/8 = 3 − z: the closed upper boundary is essential.',
      recovery:'Zero duration. A valid physical time.',recoveryCopy:'The singleton has H = 1 and t = x = 3/8. Every one of the seven distances is at least 1/8. Removing equality points would erase this witness from the model.'},
    face:{title:'A new edge crosses an old face.',before:'The parent slice has its own old peak.',after:'The added band moves the best contact.',
      intro:'On P7 with H = 4, the old slice peak is t = 16/33, z = 5/33. This is the optimum of this parent slice, not the global six-runner optimum.',
      applied:'The added lower band clips the triangle to a smaller triangle. Its peak is t = 17/35, z = 1/7. The point lies inside an old parent face and on a new child edge.',
      beforeResult:'The old peak meets 10t + z = 5 and 23t − z = 11. Runner 25 is only 4/33 away there, below the 1/8 floor.',
      afterResult:'The new contact meets 10t + z = 5 and 25t − z = 12. Together they give z = 1/7 and t = 17/35.',
      band:'4 + z ≤ 5x + 2y ≤ 5 − z',bandCopy:'On H = 4, y = 10t − 4, so the active lower band becomes 25t − z ≥ 12. The new contact is not on any old parent edge.',
      recovery:'The new geometric contact is a real time.',recoveryCopy:'At t = 17/35, all seven moving runners are at least 1/7 from the reference. Speeds 10 and 25 are limiting. Its reflected time 18/35 attains the same separation.'}
  };
  const current=()=>examples.transfer_visual.find(r=>r.id===state.case);
  const qstr=v=>String(R(v));
  const txt=(svg,x,y,value,attrs={})=>add(svg,'text',{x,y,...attrs},value);
  function volume(record){
    const parent=atlas.parents[record.parent_index],children=record.child_indices.map(i=>atlas.children[i]);
    const svg=el('cut-geometry'),height=380,width=clearSVG(svg,height);
    const vertices=parent.vertices.map(p=>p.map(v=>R(v).number()));
    const center=[0,1,2].map(i=>(Math.min(...vertices.map(p=>p[i]))+Math.max(...vertices.map(p=>p[i])))/2);
    const az=state.azimuth*Math.PI/180,tilt=30*Math.PI/180;
    const raw=p=>{const x=p[0]-center[0],y=p[1]-center[1],z=2*(p[2]-center[2]);return[x*Math.cos(az)-y*Math.sin(az),(x*Math.sin(az)+y*Math.cos(az))*Math.sin(tilt)-z*Math.cos(tilt)];};
    const projected=vertices.map(raw),minX=Math.min(...projected.map(p=>p[0])),maxX=Math.max(...projected.map(p=>p[0])),minY=Math.min(...projected.map(p=>p[1])),maxY=Math.max(...projected.map(p=>p[1]));
    const scale=Math.min((width-70)/(maxX-minX||1),(height-100)/(maxY-minY||1));
    const project=p=>{const [x,y]=raw(p.map(v=>R(v).number()));return[width/2+(x-(minX+maxX)/2)*scale,height/2+(y-(minY+maxY)/2)*scale];};
    const points=vs=>vs.map(p=>project(p).join(',')).join(' ');
    add(svg,'title',{},`Parent P${record.parent_index}; ${state.stage?'after':'before'} adding the seventh band`);
    function body(poly,child){
      if(poly.dimension===3){
        for(const face of [[0,1,2],[0,2,3],[0,1,3],[1,2,3]])add(svg,'polygon',{points:points(face.map(i=>poly.vertices[i])),fill:child?'var(--green)':'var(--muted)','fill-opacity':child?.085:state.stage?.015:.05,stroke:'none'});
      }
      for(const [index,[i,j]]of poly.edges.entries()){
        const cut=child&&poly.edge_parent_face_dimensions[index]===2;
        add(svg,'polyline',{points:points([poly.vertices[i],poly.vertices[j]]),fill:'none',stroke:cut?'var(--amber)':child?'var(--green)':'var(--muted)','stroke-width':cut?3:child?1.8:1,'stroke-dasharray':!child&&state.stage?'4 4':'none','stroke-opacity':child?1:.6});
      }
      if(poly.dimension===0){const [x,y]=project(poly.vertices[0]);add(svg,'circle',{cx:x,cy:y,r:7,fill:'var(--surface)',stroke:'var(--green)','stroke-width':2.5});}
    }
    body(parent,false);if(state.stage)children.forEach(c=>body(c,true));
    if(state.orbit){
      const before=record.parent_section,after=record.child_sections.flatMap(c=>c.points);
      const drawSlice=(vs,ghost=false)=>{
        if(!vs.length)return;
        if(vs.length>1)add(svg,'polygon',{points:points(vs),fill:'var(--blue)','fill-opacity':ghost?.025:.15,stroke:'var(--blue)','stroke-width':ghost?1:2,'stroke-dasharray':ghost?'3 4':'none'});
        else{const [x,y]=project(vs[0]);add(svg,'circle',{cx:x,cy:y,r:5,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':1.5});}
      };
      if(state.stage){drawSlice(before,true);drawSlice(after);}else drawSlice(before);
      const point=state.stage?record.after_point:record.before_point;
      if(point){const [x,y]=project(point);add(svg,'circle',{cx:x,cy:y,r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});}
    }
    txt(svg,10,20,`H = ${record.q}x − y = ${record.orbit_integer}`,{class:'small'});
    txt(svg,10,height-15,state.stage?'Dashed = previous geometry':'Parent · blue = actual orbit',{class:'small'});
    const base=[width-48,height-62];
    for(const [name,dx,dy]of [['x',Math.cos(az),Math.sin(az)*Math.sin(tilt)],['y',-Math.sin(az),Math.cos(az)*Math.sin(tilt)],['z',0,-Math.cos(tilt)]]){
      add(svg,'line',{x1:base[0],y1:base[1],x2:base[0]+dx*22,y2:base[1]+dy*22,stroke:'var(--muted)'});txt(svg,base[0]+dx*22+3,base[1]+dy*22-2,name,{class:'small'});
    }
  }
  function section(record){
    const svg=el('cut-section'),height=280,width=clearSVG(svg,height),pad={l:49,r:17,t:30,b:48};
    const parent=record.parent_section.map(p=>p.map(R));
    let lo=parent[0][0],hi=parent[parent.length-1][0];
    if(lo.cmp(hi)===0){lo=lo.sub('1/32');hi=hi.add('1/32');}
    const x=t=>pad.l+R(t).sub(lo).div(hi.sub(lo)).number()*(width-pad.l-pad.r);
    const y=z=>height-pad.b-R(z).sub('1/8').div('1/24').number()*(height-pad.t-pad.b);
    const points=vs=>vs.map(p=>`${x(p[0])},${y(p[2])}`).join(' ');
    add(svg,'title',{},`Exact physical slice H=${record.orbit_integer}; ${state.stage?'child after intersection':'six-form parent'}`);
    for(const z of ['1/8','1/6']){add(svg,'line',{x1:pad.l,y1:y(z),x2:width-pad.r,y2:y(z),stroke:'var(--line)'});txt(svg,pad.l-8,y(z)+4,z,{'text-anchor':'end'});}
    txt(svg,pad.l,16,'Separation z');
    txt(svg,pad.l,height-22,String(lo),{'text-anchor':'start'});txt(svg,width-pad.r,height-22,String(hi),{'text-anchor':'end'});
    txt(svg,width-pad.r,height-3,'Physical time t = x',{'text-anchor':'end',class:'small'});
    const draw=(vs,child)=>{
      if(!vs.length)return;
      if(vs.length>1)add(svg,'polygon',{points:points(vs),fill:child?'var(--green)':'var(--blue)','fill-opacity':child?.2:state.stage?.04:.13,stroke:child?'var(--green)':'var(--blue)','stroke-width':child?2:1.5,'stroke-dasharray':!child&&state.stage?'4 4':'none'});
      else add(svg,'circle',{cx:x(vs[0][0]),cy:y(vs[0][2]),r:7,fill:child?'var(--green)':'var(--blue)',stroke:'var(--surface)','stroke-width':2});
    };
    draw(record.parent_section,false);
    if(state.stage)record.child_sections.forEach(c=>draw(c.points,true));
    const point=state.stage?record.after_point:record.before_point;
    if(point){
      add(svg,'circle',{cx:x(point[0]),cy:y(point[2]),r:5,fill:state.stage?'var(--green)':'var(--blue)',stroke:'var(--surface)','stroke-width':1.5});
      txt(svg,Math.max(pad.l+25,Math.min(width-45,x(point[0]))),y(point[2])-14,`z = ${qstr(point[2])}`,{'text-anchor':'middle',class:'small'});
    }else{txt(svg,(pad.l+width-pad.r)/2,53,'No physical child',{'text-anchor':'middle'});txt(svg,(pad.l+width-pad.r)/2,74,'on this H = 1 slice',{'text-anchor':'middle',class:'small'});}
    const values=[`H = ${record.orbit_integer}`];
    if(point)values.push(`t = ${qstr(point[0])}`,`z = ${qstr(point[2])}`);
    else values.push('Actual-orbit intersection: empty','Ambient singleton: H = 11/8');
    el('cut-exacts').replaceChildren(...values.map(v=>{const s=document.createElement('span');s.className='rep-value';s.textContent=v;return s;}));
  }
  function recovery(record){
    const removed=state.case==='removed',saved=removed?record.before_physical:record.after_physical;
    const t=state.reflection?R(1).sub(saved.time):R(saved.time),speeds=examples.A.find(r=>r.q===record.q).speeds;
    const threshold=removed?R('1/8'):R(record.after_point[2]);
    const rows=speeds.map(speed=>{const raw=t.mul(speed),phase=raw.frac();return{speed,lap:raw.floor(),phase,distance:min(phase,R(1).sub(phase))};});
    const six=rows.slice(0,6).reduce((a,b)=>min(a,b.distance),R(1));
    el('cut-recovery-title').textContent=copy[state.case].recovery;
    el('cut-recovery-copy').textContent=copy[state.case].recoveryCopy+(state.reflection?' The table now checks the reflected time.':'');
    el('cut-time').textContent=String(t);el('cut-six-min').textContent=String(six);el('cut-seven-distance').textContent=String(rows[6].distance);
    const x=t,y=t.mul(record.q).frac(),h=x.mul(record.q).sub(y);
    el('cut-recovery-map').textContent=`At the displayed time: (x, y) = (${x}, ${y}), H = ${h}. ${state.reflection?'The reflected time is checked directly; the diagram keeps the original folded point.':'Clock: t = x.'}`;
    el('cut-phase-rows').replaceChildren(...rows.map(row=>{
      const tr=document.createElement('tr');if(row.distance.cmp(threshold)<0)tr.className='joint-failed-row';else if(row.distance.cmp(threshold)===0)tr.className='active';
      for(const value of [row.speed,row.lap,row.phase,row.distance]){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;
    }));
    return {time:String(t),minimumSix:String(six),addedDistance:String(rows[6].distance),phases:rows.map(r=>String(r.phase)),laps:rows.map(r=>String(r.lap)),distances:rows.map(r=>String(r.distance)),recoveredChild:!removed};
  }
  function whole(record){
    const source=examples.A.find(r=>r.q===record.q).transfer;
    const final=source.optimization.find(r=>r.coordinates===7),times=final.all_maximizing_times;
    const q4=record.q===4,svg=el('cut-times'),height=q4?190:120,width=clearSVG(svg,height);
    svg.style.height=`${height}px`;
    const x=v=>18+R(v).number()*(width-36);
    function rail(components,y,label){
      txt(svg,0,y-22,label);add(svg,'line',{x1:18,y1:y,x2:width-18,y2:y,stroke:'var(--line)'});
      for(const [a,b]of components){
        if(R(a).cmp(b)!==0)add(svg,'line',{x1:x(a),y1:y,x2:x(b),y2:y,stroke:'var(--blue)','stroke-width':5});
        for(const t of [a,b])add(svg,'circle',{cx:x(t),cy:y,r:R(a).cmp(b)===0?4:2.5,fill:R(a).cmp(b)===0?'var(--green)':'var(--blue)'});
      }
      txt(svg,18,y+22,'0',{'text-anchor':'middle',class:'small'});txt(svg,width-18,y+22,'1',{'text-anchor':'middle',class:'small'});
    }
    el('cut-whole-title').textContent=q4?'Four isolated safe times remain elsewhere.':'The final system has eight maximizing times.';
    if(state.case==='equality')el('cut-whole-title').textContent='This is one of four isolated safe times.';
    el('cut-whole-copy').textContent=q4?'Across all parents, adding runner 13 removes four positive intervals and retains four isolated points at separation 1/8.':'The new face contact supplies 17/35 and its reflection 18/35. Six other final maximizers come from old parent edges.';
    if(q4){rail(source.six_safe_components_at_1_over_8,52,'Before · safe at 1/8');rail(source.seven_safe_components_at_1_over_8,144,'After · safe at 1/8');}
    else rail(times.map(t=>[t,t]),57,'All final maximizing times · z = 1/7');
    el('cut-time-chips').replaceChildren(...times.map(t=>{const node=document.createElement('span');node.className='rep-value';node.textContent=`t = ${qstr(t)}`;return node;}));
    el('cut-whole-caption').textContent=q4?'This is the complete 1/8-safe set in one period, not just the selected parent slice. Endpoints and singleton times count.':'This enumerates every final maximizer. It does not enumerate every time safe at the lower threshold 1/8.';
    return times.map(qstr);
  }
  function render(){
    if(el('transfer-chapter').hidden)return;
    const record=current(),words=copy[state.case],parent=atlas.parents[record.parent_index],v=examples.A.find(r=>r.q===record.q).speeds;
    el('cut-speeds').textContent=`${v.slice(0,6).join(', ')}  +  ${v[6]}`;
    el('cut-orbit').textContent=`x = {t}, y = {${record.q}t}, H = ${record.q}x − y ∈ ℤ · selected slice H = ${record.orbit_integer}`;
    el('cut-volume-title').textContent=words.title;el('cut-parent-tag').textContent=`P${record.parent_index} → ${record.child_indices.map(i=>'C'+i).join(' + ')}`;
    el('cut-slice-title').textContent=state.stage?words.after:words.before;el('cut-slice-copy').textContent=state.stage?words.applied:words.intro;
    el('cut-band-formula').textContent=words.band;el('cut-band-copy').textContent=(state.stage?'Applied: ':'Next: ')+words.bandCopy;
    el('cut-result-label').textContent=state.stage?'AFTER THE SEVENTH CONSTRAINT':'BEFORE THE SEVENTH CONSTRAINT';
    el('cut-result-text').textContent=state.stage?words.afterResult:words.beforeResult;
    el('cut-recovery').hidden=state.stage!==2;el('cut-whole').hidden=state.stage!==2;
    el('cut-next').hidden=state.stage===2;el('cut-next').textContent=state.stage===0?'Add the seventh →':'Recover physical time →';
    document.querySelectorAll('[data-cut-case]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.cutCase===state.case)));
    document.querySelectorAll('[data-cut-stage]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.cutStage)===state.stage)));
    el('cut-reflect').checked=state.reflection;el('cut-show-orbit').checked=state.orbit;
    volume(record);section(record);
    const selected=state.stage?record.after_point:record.before_point;
    window.CC_CUT_STATE={case:state.case,stage:state.stage,q:record.q,parent:record.parent_index,H:record.orbit_integer,
      parentSection:record.parent_section.map(p=>p.map(qstr)),childSections:record.child_sections.map(c=>({child:c.child_index,points:c.points.map(p=>p.map(qstr))})),
      selectedPoint:selected?selected.map(qstr):null,reflection:state.reflection,showOrbit:state.orbit,
      physical:state.stage===2?recovery(record):null,allFinalMaximizers:state.stage===2?whole(record):null};
    el('cut-vertex-rows').replaceChildren(...record.child_indices.flatMap(ci=>atlas.children[ci].vertices.map(p=>{
      const row=document.createElement('tr'),[x,y,z]=p.map(R),h=x.mul(record.q).sub(y);
      for(const value of ['C'+ci,x,y,z,h]){const cell=document.createElement('td');cell.textContent=String(value);row.append(cell);}return row;
    })));
  }
  document.querySelectorAll('[data-cut-case]').forEach(b=>b.addEventListener('click',()=>{state.case=b.dataset.cutCase;state.stage=0;state.reflection=false;state.azimuth=35;render();}));
  document.querySelectorAll('[data-cut-stage]').forEach(b=>b.addEventListener('click',()=>{state.stage=Number(b.dataset.cutStage);state.reflection=false;render();}));
  el('cut-next').addEventListener('click',()=>{state.stage=Math.min(2,state.stage+1);render();});
  el('cut-show-orbit').addEventListener('change',()=>{state.orbit=el('cut-show-orbit').checked;render();});
  el('cut-reflect').addEventListener('change',()=>{state.reflection=el('cut-reflect').checked;render();});
  el('cut-rotate-left').addEventListener('click',()=>{state.azimuth-=15;render();});el('cut-rotate-right').addEventListener('click',()=>{state.azimuth+=15;render();});el('cut-reset').addEventListener('click',()=>{state.azimuth=35;render();});
  el('cut-build-info').textContent=`Source commit ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}.`;
  for(const path of [manifest.scene_sources.parent_child_geometry,manifest.scene_sources.parent_child_physical,'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md']){
    const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=path;li.append(a);el('cut-source-links').append(li);
  }
  document.addEventListener('cc:chapter',render);new ResizeObserver(render).observe(el('transfer-chapter'));render();
})();
