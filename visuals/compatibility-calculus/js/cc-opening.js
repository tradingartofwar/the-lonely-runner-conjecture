/* Common-start motion. Frame changes rotate positions without changing time.
   Rational state is authoritative; Number is used only for drawing and timing. */
(() => {
  const {R,min,el,add,clearSVG}=CC,data=CC_DATA.examples.opening_visual,manifest=CC_DATA.manifest;
  const colors=['var(--blue)','var(--amber)','var(--green)','var(--red)'];
  const state={reference:0,frame:'track',tick:0,playing:false};
  const denominator=data.time_denominator,threshold=R(data.threshold);
  let timer=null;
  const name=i=>`R${i+1}`;
  const safeSetText=components=>components.map(([a,b])=>R(a).cmp(R(b))===0?`{${R(a)}}`:`[${R(a)}, ${R(b)}]`).join(' ∪ ');
  function exactState(){
    const t=R(state.tick).div(denominator),reference=data.references[state.reference];
    const rows=data.velocities.map((speed,i)=>{
      const relative=speed-reference.speed,absolute=t.mul(speed).frac(),phase=t.mul(relative).frac();
      return {index:i,speed,relative,absolute,phase,distance:min(phase,R(1).sub(phase))};
    });
    const nearest=rows.filter(r=>r.index!==state.reference).reduce((a,r)=>min(a,r.distance),R(1));
    return {t,reference,rows,nearest,safe:nearest.cmp(threshold)>=0};
  }
  function stop(){clearInterval(timer);timer=null;state.playing=false;el('opening-play').textContent='Play to t = 1';}
  function setTick(tick){stop();state.tick=tick;render();}
  function circle(record){
    const node=el('opening-track'),w=clearSVG(node,340),cx=w/2,cy=166,r=Math.min(120,(w-88)/2);
    const point=(phase,radius=r)=>{const angle=phase*2*Math.PI-Math.PI/2;return [cx+radius*Math.cos(angle),cy+radius*Math.sin(angle)];};
    const path=(from,to,radius)=>{const a=point(from,radius),b=point(to,radius),diff=to-from;return `M${a} A${radius},${radius} 0 ${Math.abs(diff)>.5?1:0} ${diff>=0?1:0} ${b}`;};
    const phases=record.rows.map(row=>state.frame==='track'?row.absolute:row.phase),origin=phases[state.reference].number();
    add(node,'circle',{cx,cy,r,fill:'none',stroke:'var(--line)','stroke-width':2});
    add(node,'path',{d:path(origin-.25,origin+.25,r),fill:'none',stroke:'var(--amber)','stroke-opacity':.22,'stroke-width':15});
    for(const offset of [-.25,.25]){
      const p=point(origin+offset);
      add(node,'circle',{cx:p[0],cy:p[1],r:5,fill:'var(--surface)',stroke:'var(--amber)','stroke-width':2,class:'opening-threshold'});
    }
    const closest=record.rows.find(row=>row.index!==state.reference&&row.distance.cmp(record.nearest)===0);
    let delta=closest.phase.number();if(delta>.5)delta-=1;
    if(delta)add(node,'path',{d:path(origin,origin+delta,r-13),fill:'none',stroke:'var(--blue)','stroke-width':3,'stroke-linecap':'round',class:'opening-distance-arc'});
    const refPoint=point(origin);
    add(node,'circle',{cx:refPoint[0],cy:refPoint[1],r:16,fill:'none',stroke:'var(--text)','stroke-width':1.5,class:'opening-selected-ring'});
    const groups=new Map();
    phases.forEach((phase,i)=>{const key=String(phase);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(i);});
    const labelBoxes=[];
    for(const [phase,indices]of groups){
      const p=point(R(phase).number());
      [...indices].reverse().forEach((i,j)=>add(node,'circle',{cx:p[0],cy:p[1],r:6+3*(indices.length-1-j),fill:j===indices.length-1?colors[i]:'var(--surface)',stroke:colors[i],'stroke-width':2.5,'data-runner':i,class:'opening-runner'}));
      const text=indices.map(name).join('·'),half=text.length*3.8+2;
      let label,box;
      for(const offset of [0,.045,-.045,.09,-.09,.135,-.135,.18,-.18,.225,-.225,.27,-.27]){
        label=point(R(phase).number()+offset,r+24);label[0]=Math.max(half+3,Math.min(w-half-3,label[0]));
        box=[label[0]-half,label[1]-10,label[0]+half,label[1]+7];
        if(!labelBoxes.some(b=>box[0]<b[2]+4&&box[2]>b[0]-4&&box[1]<b[3]+4&&box[3]>b[1]-4))break;
      }
      labelBoxes.push(box);
      add(node,'line',{x1:p[0],y1:p[1],x2:label[0],y2:label[1],stroke:'var(--muted)','stroke-opacity':.5,'stroke-width':.7});
      add(node,'text',{x:label[0],y:label[1]+4,'text-anchor':'middle','font-weight':650,class:'opening-runner-label'},text);
    }
    add(node,'text',{x:cx,y:cy-9,'text-anchor':'middle',class:'small'},state.frame==='track'?'TRACK VIEW':`MOVING WITH ${name(state.reference)}`);
    add(node,'text',{x:cx,y:cy+21,'text-anchor':'middle',style:'font:28px Georgia,serif'},`t = ${record.t}`);
    add(node,'text',{x:cx,y:cy+45,'text-anchor':'middle',class:'small'},record.t.cmp(0)===0?'Everyone starts together':`${name(state.reference)} is the reference`);
    el('opening-track-caption').textContent=`Clockwise phase increases from the top. ${state.frame==='track'?'All four runners move at their original speeds.':`${name(state.reference)} stays at phase 0; negative relative speeds move counterclockwise.`} Dots stay on the track; concentric rings preserve runners sharing a phase. Labels are offset.`;
  }
  function timeline(record){
    const node=el('opening-timeline'),w=clearSVG(node,224),left=39,right=w-17,x=t=>left+R(t).number()*(right-left);
    for(let i=0;i<4;i++){
      const y=37+39*i,ref=data.references[i];
      if(i===state.reference)add(node,'rect',{x:0,y:y-17,width:w,height:34,rx:5,fill:'var(--faint)'});
      add(node,'text',{x:4,y:y+4,'font-weight':i===state.reference?700:400},name(i));
      add(node,'line',{x1:left,x2:right,y1:y,y2:y,stroke:'var(--line)'});
      for(const [a,b]of ref.safe_components){
        if(R(a).cmp(R(b))===0)add(node,'circle',{cx:x(a),cy:y,r:5,fill:'var(--surface)',stroke:colors[i],'stroke-width':2,class:'opening-safe-singleton'});
        else{
          add(node,'line',{x1:x(a),x2:x(b),y1:y,y2:y,stroke:colors[i],'stroke-width':7,'stroke-linecap':'round',class:'opening-safe-interval'});
          for(const t of [a,b])add(node,'circle',{cx:x(t),cy:y,r:4,fill:colors[i]});
        }
      }
    }
    for(const t of [R(0),R(1).div(4),R(1).div(2),R(3).div(4),R(1)]){
      add(node,'line',{x1:x(t),x2:x(t),y1:177,y2:183,stroke:'var(--muted)'});
      add(node,'text',{x:x(t),y:201,'text-anchor':'middle',class:'small'},String(t));
    }
    add(node,'line',{x1:x(record.t),x2:x(record.t),y1:13,y2:173,stroke:'var(--text)','stroke-width':1.5,'stroke-dasharray':'4 3',class:'opening-now'});
    const lonely=data.references.filter(ref=>ref.safe_components.some(([a,b])=>record.t.cmp(R(a))>=0&&record.t.cmp(R(b))<=0)).map(ref=>name(ref.index));
    el('opening-comparison').textContent=`At t = ${record.t}: ${lonely.length?`${lonely.join(' and ')} ${lonely.length===1?'is':'are'} lonely.`:'no runner is lonely.'} ${record.t.cmp(R(1).div(3))===0?'R1 and R4 meet, while R2 and R3 each have a nearest distance of 1/3.':'Each row checks its own reference against the other three runners.'}`;
  }
  function render(){
    if(el('opening-chapter').hidden)return;
    const record=exactState(),nearestIndices=record.rows.filter(row=>row.index!==state.reference&&row.distance.cmp(record.nearest)===0).map(row=>row.index);
    el('opening-time').value=state.tick;el('opening-time').setAttribute('aria-valuetext',`t = ${record.t}`);
    el('opening-time-tag').textContent=`t = ${record.t}`;el('opening-time-output').textContent=`${record.t} / 1`;
    for(const button of el('opening-references').children)button.setAttribute('aria-pressed',String(Number(button.dataset.reference)===state.reference));
    el('opening-track-view').setAttribute('aria-pressed',String(state.frame==='track'));
    el('opening-relative-view').setAttribute('aria-pressed',String(state.frame==='relative'));
    el('opening-relative-view').textContent=`Move with ${name(state.reference)}`;
    el('opening-view-label').textContent=state.frame==='track'?'THE TRACK VIEW':'THE SELECTED RUNNER’S VIEW';
    el('opening-view-title').textContent=state.frame==='track'?'Four runners. One shared clock.':`${name(state.reference)} stands still in this view.`;
    el('opening-minimum').textContent=String(record.nearest);
    el('opening-nearest').textContent=`nearest: ${nearestIndices.map(name).join(', ')}`;
    const verdict=el('opening-verdict');verdict.dataset.safe=record.safe;
    verdict.textContent=record.safe?`${name(state.reference)} is lonely: every other runner is at least 1/4 away${record.nearest.cmp(threshold)===0?' — equality counts':''}.`:`${name(state.reference)} is not lonely: the nearest distance ${record.nearest} is below 1/4.`;
    el('opening-map-description').textContent=`${name(state.reference)} travels at speed ${record.reference.speed}. Move with it by subtracting ${record.reference.speed} from every speed, including its own.`;
    el('opening-subtraction').textContent=`Relative speeds after subtracting ${record.reference.speed}`;
    el('opening-relative-speeds').textContent=record.reference.relative_speeds.map(v=>v<0?'−'+Math.abs(v):String(v)).join(', ');
    el('opening-frame-note').textContent=state.frame==='track'?`Switch to “Move with ${name(state.reference)}” to hold the reference at 0.`:`The track has rotated by −${record.reference.speed}t laps. ${name(state.reference)} has speed 0 in these coordinates.`;
    el('opening-table-title').textContent=`At t = ${record.t}, relative to ${name(state.reference)}`;
    el('opening-phase-rows').replaceChildren(...record.rows.map(row=>{
      const tr=document.createElement('tr');if(row.index===state.reference)tr.className='opening-reference-row';
      const values=[name(row.index)+(row.index===state.reference?' · ref':''),row.speed,row.relative,String(row.absolute),String(row.phase),row.index===state.reference?'—':String(row.distance)];
      values.forEach(value=>{const td=document.createElement('td');td.textContent=value;tr.append(td);});return tr;
    }));
    for(const item of el('opening-safe-list').children)item.classList.toggle('opening-safe-selected',Number(item.dataset.reference)===state.reference);
    circle(record);timeline(record);
    window.CC_OPENING_STATE={reference:state.reference,frame:state.frame,tick:state.tick,time:String(record.t),playing:state.playing,
      absolute:record.rows.map(row=>String(row.absolute)),relativeSpeeds:record.reference.relative_speeds,
      relativePhases:record.rows.map(row=>String(row.phase)),distances:record.rows.map(row=>String(row.distance)),
      minimum:String(record.nearest),nearest:nearestIndices,safe:record.safe,
      displayedPhases:record.rows.map(row=>String(state.frame==='track'?row.absolute:row.phase)),
      safeComponents:record.reference.safe_components.map(pair=>pair.map(x=>String(R(x))))};
  }
  for(const ref of data.references){
    const button=document.createElement('button');button.dataset.reference=ref.index;button.style.setProperty('--runner-color',colors[ref.index]);
    const strong=document.createElement('strong');strong.textContent=name(ref.index);const span=document.createElement('span');span.textContent=`speed ${ref.speed}`;button.append(strong,span);
    button.addEventListener('click',()=>{stop();state.reference=ref.index;render();});el('opening-references').append(button);
    const item=document.createElement('div');item.dataset.reference=ref.index;const label=document.createElement('strong');label.textContent=name(ref.index);const value=document.createElement('span');value.textContent=safeSetText(ref.safe_components);item.append(label,value);el('opening-safe-list').append(item);
  }
  for(const frame of ['track','relative'])el(`opening-${frame}-view`).addEventListener('click',()=>{stop();state.frame=frame;render();});
  el('opening-time').addEventListener('input',()=>setTick(Number(el('opening-time').value)));
  el('opening-start').addEventListener('click',()=>setTick(0));
  el('opening-witness').addEventListener('click',()=>setTick(Number(R(data.references[state.reference].witness_time).mul(denominator).n)));
  el('opening-compare').addEventListener('click',()=>setTick(denominator/3));
  el('opening-play').addEventListener('click',()=>{
    if(state.playing){stop();render();return;}
    if(matchMedia('(prefers-reduced-motion: reduce)').matches){setTick(Number(R(data.references[state.reference].witness_time).mul(denominator).n));return;}
    if(state.tick===denominator)state.tick=0;
    state.playing=true;el('opening-play').textContent='Pause';render();
    timer=setInterval(()=>{state.tick=Math.min(denominator,state.tick+1);if(state.tick===denominator)stop();render();},85);
  });
  el('opening-build-info').textContent=`Source snapshot ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}. The complete sets use a boundary partition and are checked by direct safe-band intersection.`;
  for(const source of [data.source,'notes/CC_REPRESENTATION_RULES.md']){const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${source}`;a.textContent=source;li.append(a);el('opening-source-links').append(li);}
  document.addEventListener('cc:chapter',event=>{if(event.detail.chapter!=='opening'){stop();if(window.CC_OPENING_STATE)window.CC_OPENING_STATE.playing=false;}render();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();if(window.CC_OPENING_STATE)window.CC_OPENING_STATE.playing=false;}});
  new ResizeObserver(render).observe(el('opening-chapter'));render();
})();
