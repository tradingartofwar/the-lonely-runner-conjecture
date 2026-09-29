/* Exact construction data; floating-point projection only draws the cells. */
(() => {
  const {R,min,el,add,clearSVG}=CC,data=CC_DATA.examples.cell_visual,atlas=CC_DATA.geometry.full_cells,manifest=CC_DATA.manifest;
  const state={lap:'interval',cell:1,stage:0,angle:35,vertices:false};
  const forms=['x','y','x + y','2x + y','3x + y','3x + 2y','5x + 2y'];
  const txt=(svg,x,y,value,attrs={})=>add(svg,'text',{x,y,...attrs},value);
  const row=values=>{const tr=document.createElement('tr');for(const value of values){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;};
  const dimName=d=>d===0?'Closed singleton':d===1?'Line segment':d===2?'Polygon':'3D polytope';
  function lapView(){
    const record=data.lap_cases.find(c=>c.id===state.lap),z=R('1/8');
    const bounds=record.speeds.map((v,i)=>[R(record.physical_laps[i]).add(z).div(v),R(record.physical_laps[i]).add(R(1).sub(z)).div(v)]);
    const L=bounds.reduce((a,b)=>a.cmp(b[0])>=0?a:b[0],R(0)),U=bounds.reduce((a,b)=>min(a,b[1]),R(1));
    const relation=L.cmp(U),t=relation<=0?L.add(U).div(2):null;
    for(const button of document.querySelectorAll('[data-lap-case]'))button.setAttribute('aria-pressed',String(button.dataset.lapCase===state.lap));
    el('cell-lap-title').textContent=`q=4 · ${record.count} constraints · H=1`;
    el('cell-lap-rows').replaceChildren(...bounds.map((b,i)=>{const tr=row([record.speeds[i],record.physical_laps[i],b[0],b[1]]);if(b[0].cmp(L)===0)tr.children[2].classList.add('cell-controlling');if(b[1].cmp(U)===0)tr.children[3].classList.add('cell-controlling');return tr;}));
    el('cell-lap-caption').textContent=state.lap==='interval'?'Only the first six safety constraints are required here. Speed 13 is still unchecked; a six-constraint time need not be seven-runner safe.':state.lap==='point'?'Every one of the seven constraints is required. Highlighted entries attain the common lower or upper bound.':'The seventh completed lap is 4. Its lower bound is later than the earlier constraints permit. This lap vector has no common time on H=1.';
    el('cell-L').textContent=String(L);el('cell-R').textContent=String(U);
    el('cell-result-title').textContent=relation<0?'L < R: a positive interval.':relation===0?'L = R: one safe instant.':'L > R: no shared time.';
    el('cell-lap-result').textContent=relation<0?`Closed intersection [${L}, ${U}]. Both endpoints belong.`:relation===0?`The singleton {${L}} is nonempty, despite having zero duration.`:`The latest start ${L} exceeds the earliest end ${U}. No physical witness is selected.`;
    el('cell-lap-result').classList.toggle('cell-empty',relation>0);
    let physical=null;
    if(t){
      const speeds=CC_DATA.examples.A.find(a=>a.q===4).speeds;
      const phases=speeds.map(v=>t.mul(v).frac()),distances=phases.map(p=>min(p,R(1).sub(p))),laps=speeds.map(v=>String(t.mul(v).floor()));
      const minimum=distances.slice(0,record.count).reduce((a,b)=>min(a,b),R(1));
      physical={time:String(t),phases:phases.map(String),distances:distances.map(String),laps,requiredMinimum:String(minimum)};
      el('cell-physical-check').textContent=`At t=${t}, the required ${record.count} distances have minimum ${minimum}. `+(record.count===6?`The unchecked speed 13 has distance ${distances[6]}, so this is not a seven-runner witness.`:'All seven distances meet 1/8. Recovery gives (x,y,z)=(3/8,1/2,1/8).');
    }else el('cell-physical-check').textContent='C3 still exists as an ambient point, but its H=11/8 at q=4 is not the selected integer H=1. Empty physical intersection and nonempty ambient cell remain distinct.';
    const svg=el('cell-lap-plot'),height=165,width=clearSVG(svg,height),low=(L.cmp(U)<0?L:U).sub('1/64'),high=(L.cmp(U)>0?L:U).add('1/64');
    const x=v=>25+v.sub(low).div(high.sub(low)).number()*(width-50);
    add(svg,'line',{x1:20,y1:75,x2:width-20,y2:75,stroke:'var(--line)'});
    if(relation<0)add(svg,'line',{x1:x(L),y1:75,x2:x(U),y2:75,stroke:'var(--green)','stroke-width':8});
    if(relation>0)add(svg,'line',{x1:x(U),y1:75,x2:x(L),y2:75,stroke:'var(--red)','stroke-width':2,'stroke-dasharray':'4 4'});
    for(const [v,name,y]of [[L,'L',46],[U,'R',119]]){add(svg,'circle',{cx:x(v),cy:75,r:5,fill:relation>0?'var(--red)':'var(--green)',stroke:'var(--surface)','stroke-width':1.5});txt(svg,x(v),y,`${name} = ${v}`,{'text-anchor':'middle'});}
    txt(svg,width/2,height-7,'Physical time t · local scale',{'text-anchor':'middle',class:'small'});
    return{id:state.lap,bounds:bounds.map(b=>b.map(String)),lower:String(L),upper:String(U),time:t?String(t):null,physical};
  }
  function projection(svg,vertices,height){
    const width=clearSVG(svg,height),vs=vertices.map(p=>p.map(v=>R(v).number())),center=[0,1,2].map(i=>(Math.min(...vs.map(p=>p[i]))+Math.max(...vs.map(p=>p[i])))/2);
    const angle=state.angle*Math.PI/180,tilt=28*Math.PI/180;
    const raw=p=>{const x=p[0]-center[0],y=p[1]-center[1],z=2*(p[2]-center[2]);return[x*Math.cos(angle)-y*Math.sin(angle),(x*Math.sin(angle)+y*Math.cos(angle))*Math.sin(tilt)-z*Math.cos(tilt)];};
    const points=vs.map(raw),lo=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),hi=[0,1].map(i=>Math.max(...points.map(p=>p[i]))),scale=Math.min((width-75)/(hi[0]-lo[0]||1),(height-95)/(hi[1]-lo[1]||1));
    const project=p=>{const out=raw(p.map(v=>R(v).number()));return[width/2+(out[0]-(lo[0]+hi[0])/2)*scale,height/2-8+(out[1]-(lo[1]+hi[1])/2)*scale];};
    const origin=[width-46,height-37];
    for(const [name,dx,dy]of [['x',Math.cos(angle),Math.sin(angle)*Math.sin(tilt)],['y',-Math.sin(angle),Math.cos(angle)*Math.sin(tilt)],['z',0,-Math.cos(tilt)]]){add(svg,'line',{x1:origin[0],y1:origin[1],x2:origin[0]+dx*22,y2:origin[1]+dy*22,stroke:'var(--muted)'});txt(svg,origin[0]+dx*22+3,origin[1]+dy*22-2,name,{class:'small'});}
    return{width,project};
  }
  function paint(svg,poly,project,{ghost=false,selected=true,newBand=null,vertices=false,cell=null}={}){
    const pointList=ids=>ids.map(i=>project(poly.vertices[i]).join(',')).join(' ');
    const onNew=ids=>newBand&&newBand.some(([normal,bound])=>ids.every(i=>poly.vertices[i].reduce((sum,v,j)=>sum.add(R(v).mul(normal[j])),R(0)).cmp(bound)===0));
    const color=selected?'var(--green)':'var(--muted)';
    if(!ghost&&poly.faces)for(const face of poly.faces)add(svg,'polygon',{points:pointList(face),fill:onNew(face)?'var(--amber)':color,'fill-opacity':selected?.11:.025,stroke:'none'});
    for(const [i,j]of poly.edges)add(svg,'polyline',{points:pointList([i,j]),fill:'none',stroke:ghost?'var(--muted)':onNew([i,j])?'var(--amber)':color,'stroke-width':ghost?1:selected?2:1,'stroke-opacity':ghost?.5:selected?1:.45,'stroke-dasharray':ghost?'4 4':'none'});
    if(poly.dimension===0){const [x,y]=project(poly.vertices[0]);add(svg,'circle',{cx:x,cy:y,r:7,fill:'var(--surface)',stroke:color,'stroke-width':2.5,class:cell!==null?'cell-atlas-singleton':'cell-build-singleton'});if(cell!==null)txt(svg,x+10,y-8,`C${cell}`,{class:'small'});}
    else if(vertices)poly.vertices.forEach(p=>{const [x,y]=project(p);add(svg,'circle',{cx:x,cy:y,r:2.5,fill:color,class:'cell-vertex-dot'});});
  }
  function geometry(){
    const record=data.cells[state.cell],poly=record.stages[state.stage],previous=record.stages[Math.max(0,state.stage-1)];
    const svg=el('cell-volume'),{project}=projection(svg,[...poly.vertices,...previous.vertices],375);
    if(state.stage)paint(svg,previous,project,{ghost:true});
    paint(svg,poly,project,{newBand:state.stage?record.bands[state.stage-1]:null,vertices:true});
    el('cell-volume-title').textContent=state.stage===7?`${record.id}: ${dimName(poly.dimension).replace('Closed','closed')}.`:`${state.stage} of 7 bands applied.`;
    el('cell-build-progress').textContent=state.stage===0?'INITIAL COORDINATE FRAME':state.stage===7?'THE COMPLETED LABELLED CELL':'AN INTERMEDIATE RELAXATION';
    el('cell-dimension').textContent=`Dimension ${poly.dimension}`;
    el('cell-stage-note').textContent=`${poly.vertices.length} ${poly.vertices.length===1?'vertex':'vertices'} · ${poly.edges.length} edges. `+(state.stage===7?'All seven bands hold at every point in this closed cell.':'The unapplied bands may still reject points. This shape is not yet the completed cell.');
    el('cell-label-vector').textContent=`m = (${record.labels.join(', ')})`;el('cell-choice').value=state.cell;
    el('cell-build-next').disabled=state.stage===7;el('cell-build-all').disabled=state.stage===7;
    el('cell-build-next').textContent=state.stage===7?'All bands applied':`Add band ${state.stage+1} →`;
    for(const [i,button]of [...el('cell-band-buttons').children].entries()){
      const m=record.labels[i];button.textContent=`${i+1} · ${m} + z ≤ ${forms[i]} ≤ ${m+1} − z`;
      button.setAttribute('aria-pressed',String(state.stage===i+1));button.dataset.applied=i<state.stage;
    }
    el('cell-vertex-rows').replaceChildren(...poly.vertices.map((p,i)=>row([`V${i}`, ...p.map(v=>String(R(v)))])));
    const all=data.cells.map(c=>c.stages[7]),atlasSvg=el('cell-atlas'),atlasProjection=projection(atlasSvg,all.flatMap(c=>c.vertices),365);
    all.forEach((c,i)=>{if(i!==state.cell&&c.dimension>0)paint(atlasSvg,c,atlasProjection.project,{selected:false,vertices:state.vertices,cell:i});});
    if(all[state.cell].dimension>0)paint(atlasSvg,all[state.cell],atlasProjection.project,{selected:true,vertices:state.vertices,cell:state.cell});
    all.forEach((c,i)=>{if(c.dimension===0)paint(atlasSvg,c,atlasProjection.project,{selected:i===state.cell,cell:i});});
    for(const button of el('cell-atlas-buttons').children)button.setAttribute('aria-pressed',String(Number(button.dataset.cell)===state.cell));
    return{cell:record.id,stage:state.stage,dimension:poly.dimension,vertices:poly.vertices.map(p=>p.map(v=>String(R(v)))),edges:poly.edges,faces:poly.faces,atlasCells:10,atlasSingletons:3};
  }
  function render(){if(el('cell-chapter').hidden)return;const lap=lapView(),construction=geometry();window.CC_CELL_STATE={lap,construction,angle:state.angle,showVertices:state.vertices};}
  for(const button of document.querySelectorAll('[data-lap-case]'))button.addEventListener('click',()=>{state.lap=button.dataset.lapCase;render();});
  el('cell-choice').replaceChildren(...data.cells.map((record,i)=>{const option=document.createElement('option');option.value=i;option.textContent=`${record.id} · ${dimName(record.stages[7].dimension)}`;return option;}));
  el('cell-choice').addEventListener('change',()=>{state.cell=Number(el('cell-choice').value);state.stage=0;render();});
  el('cell-build-next').addEventListener('click',()=>{state.stage=Math.min(7,state.stage+1);render();});
  el('cell-build-all').addEventListener('click',()=>{state.stage=7;render();});el('cell-build-reset').addEventListener('click',()=>{state.stage=0;render();});
  el('cell-band-buttons').replaceChildren(...forms.map((form,i)=>{const button=document.createElement('button');button.dataset.band=i+1;button.addEventListener('click',()=>{state.stage=i+1;render();});return button;}));
  el('cell-atlas-buttons').replaceChildren(...data.cells.map((record,i)=>{const button=document.createElement('button');button.dataset.cell=i;button.textContent=`${record.id} · ${record.stages[7].dimension===0?'singleton':record.stages[7].vertices.length+' vertices'}`;button.addEventListener('click',()=>{state.cell=i;state.stage=7;render();});return button;}));
  el('cell-rotate-left').addEventListener('click',()=>{state.angle-=15;render();});el('cell-rotate-right').addEventListener('click',()=>{state.angle+=15;render();});el('cell-reset-view').addEventListener('click',()=>{state.angle=35;render();});
  el('cell-show-vertices').addEventListener('change',()=>{state.vertices=el('cell-show-vertices').checked;render();});
  el('cell-build-info').textContent=`Source snapshot ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}. Every completed construction is compared with the pinned cell certificate.`;
  for(const path of [manifest.scene_sources.cell_construction,manifest.scene_sources.lap_bridge,'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md']){const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=path;li.append(a);el('cell-source-links').append(li);}
  document.addEventListener('cc:chapter',render);new ResizeObserver(render).observe(el('cell-chapter'));render();
})();
