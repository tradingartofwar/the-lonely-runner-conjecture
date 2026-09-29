/* One fixed shared clock. Meeting labels are not completed-lap counts. */
(() => {
  const {R,min,el,add,clearSVG}=CC,data=CC_DATA.examples.clock_visual,manifest=CC_DATA.manifest;
  const state={mode:'runner',index:data.default_index},delta=R(data.threshold);
  const label=(svg,x,y,value,attrs={})=>add(svg,'text',{x,y,...attrs},value);
  const interval=(bounds,closed)=>`${closed[0]?'[':'('}${R(bounds[0])}, ${R(bounds[1])}${closed[1]?']':')'}`;
  const contains=(episode,t)=>{
    const value=t.mul(episode.speed).sub(episode.meeting);
    return value.cmp(delta)<0&&value.cmp(R(0).sub(delta))>0;
  };
  function physical(t){
    return data.speeds.map(speed=>{
      const raw=t.mul(speed),lap=raw.floor(),phase=raw.frac(),distance=min(phase,R(1).sub(phase));
      const blocked=distance.cmp(delta)<0,meeting=blocked?raw.add('1/2').floor():null;
      return{speed,lap,phase,distance,blocked,meeting};
    });
  }
  function schedule(t,active){
    const svg=el('clock-timeline'),split=state.mode==='occurrence';
    const rows=split?data.episodes.map(e=>({id:e.id,title:`${e.speed} · ${e.meeting}`,episodes:[e]})):data.extras.map(v=>({id:`v${v}`,title:String(v),episodes:data.episodes.filter(e=>e.speed===v)}));
    const height=112+rows.length*45,width=clearSVG(svg,height),left=54,right=width-17;
    const lo=R(data.window[0]),span=R(data.window[1]).sub(lo),x=v=>left+R(v).sub(lo).div(span).number()*(right-left);
    label(svg,3,17,split?'v · m':'Speed',{class:'small'});
    label(svg,width-4,17,'Same physical time t',{'text-anchor':'end',class:'small'});
    rows.forEach((row,i)=>{
      const y=48+i*45;label(svg,3,y+4,row.title,{'font-weight':550});
      add(svg,'line',{x1:left,y1:y,x2:right,y2:y,stroke:'var(--line)','stroke-width':1});
      for(const e of row.episodes){
        const color=active.includes(e.id)?'var(--red)':'var(--amber)';
        add(svg,'line',{x1:x(e.interval[0]),y1:y,x2:x(e.interval[1]),y2:y,stroke:color,'stroke-width':8,'stroke-opacity':active.includes(e.id)?1:.55});
        e.interval.forEach((v,j)=>add(svg,'circle',{cx:x(v),cy:y,r:4,fill:e.closed[j]?color:'var(--surface)',stroke:color,'stroke-width':1.6}));
      }
    });
    const safeY=48+rows.length*45;
    label(svg,3,safeY+4,'Safe',{class:'point-label'});
    add(svg,'line',{x1:left,y1:safeY,x2:right,y2:safeY,stroke:'var(--line)'});
    for(const [a,b] of data.safe_components)add(svg,'line',{x1:x(a),y1:safeY,x2:x(b),y2:safeY,stroke:'var(--green)','stroke-width':8});
    add(svg,'line',{x1:x(t),y1:28,x2:x(t),y2:safeY+10,stroke:'var(--blue)','stroke-width':1.5,'stroke-dasharray':'4 3'});
    add(svg,'path',{d:`M ${x(t)-4} 23 L ${x(t)+4} 23 L ${x(t)} 29 Z`,fill:'var(--blue)'});
    label(svg,left,height-8,String(lo),{'text-anchor':'start',class:'small'});
    label(svg,right,height-8,String(R(data.window[1])),{'text-anchor':'end',class:'small'});
    el('clock-schedule-title').textContent=split?'Six events, with their identities intact.':'Four runners. Six blocking events.';
    el('clock-schedule-caption').textContent=split?'Each row is one event (speed v, meeting m). Hollow endpoints are excluded by strict blocking; filled endpoints are included when the window clips an event.':'Each row merges one runner’s events. Runner 16’s two separated blocks are still visible on the clock, even though the runner graph below gives them one node.';
  }
  function track(t,rows){
    const svg=el('clock-track'),height=288,width=clearSVG(svg,height),cx=width/2,cy=144,r=Math.min(83,(width-105)/2);
    const xy=(phase,rad=r)=>[cx+Math.sin(2*Math.PI*phase)*rad,cy-Math.cos(2*Math.PI*phase)*rad];
    add(svg,'circle',{cx,cy,r,fill:'none',stroke:'var(--line)','stroke-width':2});
    const arc=Array.from({length:51},(_,i)=>xy(-1/8+i/200).join(','));
    add(svg,'polyline',{points:arc.join(' '),stroke:'var(--red)','stroke-width':7,'stroke-opacity':.35,'stroke-dasharray':'3 4',fill:'none'});
    for(const phase of [1/8,7/8]){const [x,y]=xy(phase);add(svg,'circle',{cx:x,cy:y,r:4,fill:'var(--surface)',stroke:'var(--green)','stroke-width':1.5});}
    const groups=new Map();
    for(const row of rows){const key=String(row.phase);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(row);}
    const labels=[];
    for(const group of groups.values()){
      const p=group[0].phase.number(),[x,y]=xy(p),blocked=group.some(r=>r.blocked),color=blocked?'var(--red)':'var(--green)';
      add(svg,'circle',{cx:x,cy:y,r:5,fill:color,stroke:'var(--surface)','stroke-width':1.4});
      labels.push({x,y,side:p>0.5?-1:1,text:group.map(r=>r.speed).join(','),color});
    }
    for(const side of [-1,1]){
      const items=labels.filter(v=>v.side===side).sort((a,b)=>a.y-b.y);let prior=20;
      for(const item of items){item.ly=Math.max(item.y,prior+18);prior=item.ly;}
      if(items.length){const excess=Math.max(0,items.at(-1).ly-(height-34));for(const item of items)item.ly-=excess;}
      for(const item of items){const lx=cx+side*(r+16);add(svg,'line',{x1:item.x,y1:item.y,x2:lx,y2:item.ly,stroke:'var(--line)'});label(svg,lx+side*3,item.ly+4,item.text,{'text-anchor':side<0?'end':'start',fill:item.color,style:`fill:${item.color}`});}
    }
    const zero=xy(0);add(svg,'rect',{x:zero[0]-4,y:zero[1]-4,width:8,height:8,fill:'var(--text)'});
    label(svg,cx,25,'0 · stationary reference',{'text-anchor':'middle',class:'small'});
    label(svg,cx,cy-6,'PHYSICAL TIME',{'text-anchor':'middle',class:'small'});
    label(svg,cx,cy+18,String(t),{'text-anchor':'middle',style:'font:21px Georgia,serif'});
    label(svg,cx,height-8,'Red = blocked · green = safe',{'text-anchor':'middle',class:'small'});
  }
  function graph(activeSpeeds,activeEpisodes){
    const svg=el('clock-graph'),height=300,width=clearSVG(svg,height),split=state.mode==='occurrence';
    const positions=split?{'v16m5':[.16,70],'v6m2':[.5,70],'v11m4':[.84,70],'v16m6':[.84,218],'v11m3':[.16,218],'v7m2':[.5,218]}:{'v6':[.22,63],'v16':[.78,63],'v11':[.5,172],'v7':[.5,268]};
    const point=id=>[positions[id][0]*width,positions[id][1]];
    for(const pair of data.pairs){
      const ids=split?pair.episodes:pair.speeds.map(v=>`v${v}`),[a,b]=ids.map(point),now=pair.episodes.every(id=>activeEpisodes.includes(id));
      add(svg,'line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:now?'var(--red)':'var(--line)','stroke-width':now?3:2,'data-pair':pair.id});
    }
    for(const [id,[fx,y]] of Object.entries(positions)){
      const e=split?data.episodes.find(e=>e.id===id):null,v=split?e.speed:Number(id.slice(1)),now=split?activeEpisodes.includes(id):activeSpeeds.includes(v),x=fx*width;
      if(split)add(svg,'rect',{x:x-29,y:y-20,width:58,height:40,rx:8,fill:now?'var(--faint)':'var(--surface)',stroke:now?'var(--red)':'var(--line)','stroke-width':now?2:1.5});
      else add(svg,'circle',{cx:x,cy:y,r:23,fill:now?'var(--faint)':'var(--surface)',stroke:now?'var(--red)':'var(--line)','stroke-width':now?2:1.5});
      label(svg,x,y+5,split?`${v} · ${e.meeting}`:String(v),{'text-anchor':'middle','font-weight':550});
    }
    el('clock-graph-title').textContent=split?'The triangle separates into a path.':'One node per runner hides the meeting.';
    el('clock-node-count').textContent=split?'6 occurrences':'4 runners';
    el('clock-graph-caption').textContent=split?'Node label = speed · meeting number. The four-node path and separate two-node edge preserve all four overlap relations without merging distinct events.':'The triangle links 6, 11 and 16 because every pair overlaps somewhere. An edge records existence of an overlap, not a common time for the whole triangle.';
    el('clock-argument-title').textContent=split?'Runner 16 would need two different meetings.':'A triangle is a question, not a shared time.';
    el('clock-argument-copy').textContent=split?'The 6–16 overlap uses (16,5). The 11–16 overlap uses (16,6). Those are disjoint events on the same clock, so no time in J can satisfy the triple.':'The pair summaries are true. To test the proposed triple, restore the identity of the event behind each edge. Switch to “Keep occurrence labels” and follow runner 16.';
    el('clock-conclusion').textContent=split?'No common occurrence → no simultaneous 6/11/16 blocking inside J.':'The two required meeting sets are {5} and {6}. Their intersection is empty.';
  }
  function zoom(t){
    const svg=el('clock-zoom'),height=188,width=clearSVG(svg,height),[lo,hi]=data.safe_components[0].map(R),duration=hi.sub(lo),a=lo.sub(duration),b=hi.add(duration);
    const left=18,right=width-18,x=v=>left+R(v).sub(a).div(b.sub(a)).number()*(right-left),y=91;
    label(svg,left,20,'Magnified opening', {class:'small'});
    add(svg,'line',{x1:left,y1:y,x2:x(lo),y2:y,stroke:'var(--amber)','stroke-width':9});
    add(svg,'line',{x1:x(hi),y1:y,x2:right,y2:y,stroke:'var(--amber)','stroke-width':9});
    add(svg,'line',{x1:x(lo),y1:y,x2:x(hi),y2:y,stroke:'var(--green)','stroke-width':9});
    for(const v of [lo,hi]){add(svg,'circle',{cx:x(v),cy:y,r:5,fill:'var(--green)',stroke:'var(--surface)','stroke-width':1.5});label(svg,x(v),y+28,String(v),{'text-anchor':'middle'});}
    label(svg,left,y-20,'7 blocks',{class:'small'});label(svg,right,y-20,'16 blocks',{'text-anchor':'end',class:'small'});
    if(t.cmp(a)>=0&&t.cmp(b)<=0)add(svg,'line',{x1:x(t),y1:40,x2:x(t),y2:y+9,stroke:'var(--blue)','stroke-dasharray':'4 3','stroke-width':1.5});
    label(svg,width/2,height-18,t.cmp(a)<0||t.cmp(b)>0?'Current time lies outside this close-up.':'Cursor stays on the same physical clock.',{'text-anchor':'middle',class:'small'});
  }
  function render(){
    if(el('clock-chapter').hidden)return;
    const control=data.controls[state.index],t=R(control.time),rows=physical(t),activeSpeeds=rows.filter(r=>r.blocked).map(r=>r.speed),activeEpisodes=data.episodes.filter(e=>contains(e,t)).map(e=>e.id);
    if(rows.some(r=>data.core.includes(r.speed)&&r.blocked))throw new Error('Core must stay safe throughout J');
    for(const id of ['merge','split'])el(`clock-${id}`).setAttribute('aria-pressed',String((id==='split')===(state.mode==='occurrence')));
    el('clock-time').textContent=`t = ${t}`;el('clock-position').value=state.index;
    el('clock-stop').textContent=`${state.index+1} / ${data.controls.length} · ${control.boundary?'boundary':'between boundaries'}`;
    el('clock-prev').disabled=state.index===0;el('clock-next').disabled=state.index===data.controls.length-1;
    for(const button of document.querySelectorAll('[data-clock-pair]'))button.setAttribute('aria-pressed',String(data.pairs.find(p=>p.id===button.dataset.clockPair).control_index===state.index));
    ['left','middle','right'].forEach((key,i)=>el(`clock-safe-${key}`).setAttribute('aria-pressed',String(data.safe_indices[i]===state.index)));
    const minimum=rows.reduce((v,r)=>min(v,r.distance),R(1)),safe=activeSpeeds.length===0;
    el('clock-current').textContent=safe?`All seven runners are safe at t = ${t}. Minimum distance: ${minimum}.`:`Blocking now: ${activeSpeeds.join(', ')}. The other runners are safe at this same time.`;
    el('clock-current').classList.toggle('clock-safe-now',safe);
    el('clock-table-title').textContent=`At t = ${t}, the minimum distance is ${minimum}.`;
    el('clock-phase-rows').replaceChildren(...rows.map(row=>{
      const tr=document.createElement('tr');tr.className=row.blocked?'clock-blocked-row':row.distance.cmp(delta)===0?'clock-equality-row':'';
      for(const value of [row.speed,row.lap,row.phase,row.distance,row.meeting===null?'—':row.meeting,row.blocked?'Blocked':row.distance.cmp(delta)===0?'Safe · equality':'Safe']){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;
    }));
    schedule(t,activeEpisodes);track(t,rows);graph(activeSpeeds,activeEpisodes);zoom(t);
    window.CC_CLOCK_STATE={mode:state.mode,index:state.index,time:String(t),activeSpeeds,activeEpisodes,safe,minimum:String(minimum),
      phases:rows.map(r=>String(r.phase)),distances:rows.map(r=>String(r.distance)),laps:rows.map(r=>String(r.lap)),meetings:rows.map(r=>r.meeting===null?null:String(r.meeting)),
      graphNodes:state.mode==='occurrence'?6:4,graphEdges:4,safeComponents:data.safe_components.map(p=>p.map(v=>String(R(v))))};
  }
  el('clock-position').max=data.controls.length-1;
  el('clock-position').addEventListener('input',()=>{state.index=Number(el('clock-position').value);render();});
  el('clock-prev').addEventListener('click',()=>{state.index=Math.max(0,state.index-1);render();});
  el('clock-next').addEventListener('click',()=>{state.index=Math.min(data.controls.length-1,state.index+1);render();});
  el('clock-merge').addEventListener('click',()=>{state.mode='runner';render();});
  el('clock-split').addEventListener('click',()=>{state.mode='occurrence';render();});
  for(const button of document.querySelectorAll('[data-clock-pair]'))button.addEventListener('click',()=>{state.index=data.pairs.find(p=>p.id===button.dataset.clockPair).control_index;render();});
  ['left','middle','right'].forEach((key,i)=>el(`clock-safe-${key}`).addEventListener('click',()=>{state.index=data.safe_indices[i];render();}));
  function tableRow(values){const tr=document.createElement('tr');for(const value of values){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;}
  el('clock-occurrence-rows').replaceChildren(...data.episodes.map(e=>tableRow([e.speed,e.meeting,interval(e.interval,e.closed)])));
  el('clock-overlap-rows').replaceChildren(...data.pairs.map(p=>tableRow([p.episodes.map(id=>{const e=data.episodes.find(e=>e.id===id);return`(${e.speed},${e.meeting})`;}).join(' + '),interval(p.interval,p.closed),String(R(p.duration))])));
  el('clock-build-info').textContent=`Source snapshot ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}. The blocking occurrence m and completed lap floor(vt) are different fields.`;
  for(const path of [manifest.scene_sources.shared_clock,manifest.scene_sources.occurrence_identity,'notes/DISTINCTION_AUDIT_2026_09_25.md']){const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=path;li.append(a);el('clock-source-links').append(li);}
  document.addEventListener('cc:chapter',render);new ResizeObserver(render).observe(el('clock-chapter'));render();
})();
