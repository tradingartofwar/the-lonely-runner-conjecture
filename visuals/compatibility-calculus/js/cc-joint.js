/* Exact q=4 same-point counterexample. H/S ranges are not treated as a product. */
(() => {
  const {R,min,el,add,clearSVG}=CC;
  const data=CC_DATA.examples.joint_visual;
  const state={step:0,position:6};
  const labels=['A','B','C'];
  const steps=[
    {label:'01 / MARGINAL INFORMATION',title:'Two correct statements.',plot:'The ranges each pass a test.',
     copy:'<p><strong>Orbit test:</strong> H ranges from 5/8 to 11/8, so it contains the integer 1.</p><p><strong>Added-runner test:</strong> S ranges from 23/12 to 17/8, so it reaches the closed safe endpoint 17/8.</p><p>The blue point and vertex C demonstrate these two facts at <strong>different points</strong>.</p>',
     conclusion:'Both marginal tests pass. They have not supplied a shared point.'},
    {label:'02 / THE MISSING RELATION',title:'The combined claim leaves the triangle.',plot:'A rectangle invents an extra combination.',
     copy:'<p>Combine H = 1 with S = 17/8. The claimed pair lies inside the separate-range rectangle, but <strong>outside the actual joint triangle</strong>.</p><p>At C, the added runner is safe, but H = 11/8 is not an integer. The same-orbit points with H = 1 never reach C’s safe S value.</p>',
     conclusion:'The pair (1, 17/8) does not belong to this parent region.'},
    {label:'03 / CONDITIONAL COMPATIBILITY',title:'Hold H = 1, then test S.',plot:'One orbit. The whole conditional interval.',
     copy:'<p>Intersect the parent with the <strong>same orbit slice H = 1</strong>. Now the added-runner range is only <strong>[109/56, 33/16]</strong>.</p><p>That entire closed interval lies between the safe-band edges 15/8 and 17/8. Every point on this slice is blocked by runner 13.</p>',
     conclusion:'No overlap with a safe band. This parent contributes no surviving time.'}
  ];
  const text=(svg,x,y,label,attrs={})=>add(svg,'text',{x,y,...attrs},label);
  function plot(){
    const svg=el('joint-map'),height=385,width=clearSVG(svg,height),pad={l:57,r:20,t:30,b:50};
    const x=v=>pad.l+(v-.5)*(width-pad.l-pad.r),y=v=>height-pad.b-(v-11/6)/(5/12)*(height-pad.t-pad.b);
    const point=p=>[x(R(p[0]).number()),y(R(p[1]).number())];
    const points=v=>v.map(p=>point(p).join(',')).join(' ');
    add(svg,'title',{},steps[state.step].plot);
    add(svg,'rect',{x:pad.l,y:pad.t,width:width-pad.l-pad.r,height:height-pad.t-pad.b,fill:'none',stroke:'var(--line)'});
    for(const [lo,hi]of [[11/6,15/8],[17/8,9/4]])add(svg,'rect',{x:pad.l,y:y(hi),width:width-pad.l-pad.r,height:y(lo)-y(hi),fill:'var(--green)','fill-opacity':.07});
    for(const s of [15/8,2,17/8]){
      add(svg,'line',{x1:pad.l,y1:y(s),x2:width-pad.r,y2:y(s),stroke:'var(--line)'});
      text(svg,pad.l-9,y(s)+4,s===2?'2':s<2?'15/8':'17/8',{'text-anchor':'end'});
    }
    text(svg,pad.l,15,'S = 5x + 2y');
    for(const h of [5/8,1,11/8]){
      add(svg,'line',{x1:x(h),y1:height-pad.b,x2:x(h),y2:height-pad.b+5,stroke:'var(--muted)'});
      text(svg,x(h),height-pad.b+23,h===1?'1':h<1?'5/8':'11/8',{'text-anchor':'middle'});
    }
    text(svg,width-pad.r,height-4,'H = 4x − y',{'text-anchor':'end'});
    text(svg,pad.l+8,y(17/8)-12,'safe S band',{class:'small'});
    const hBounds=data.marginal_H.map(v=>R(v).number()),sBounds=data.marginal_S.map(v=>R(v).number());
    add(svg,'rect',{x:x(hBounds[0]),y:y(sBounds[1]),width:x(hBounds[1])-x(hBounds[0]),height:y(sBounds[0])-y(sBounds[1]),fill:'var(--amber)','fill-opacity':state.step===2?.025:.075,stroke:'var(--amber)','stroke-opacity':state.step===2?.25:.7,'stroke-dasharray':'6 5'});
    add(svg,'polygon',{points:points(data.triangle_hs),fill:'var(--green)','fill-opacity':.13,stroke:'var(--green)','stroke-width':1.5});
    for(let i=0;i<3;i++){
      const p=point(data.triangle_hs[i]);add(svg,'circle',{cx:p[0],cy:p[1],r:3,fill:'var(--green)'});
      text(svg,p[0]+(i===0?-10:9),p[1]+(i===1?17:-9),labels[i],{'text-anchor':i===0?'end':'start'});
    }
    add(svg,'line',{x1:x(1),y1:pad.t,x2:x(1),y2:height-pad.b,stroke:'var(--blue)','stroke-opacity':.5,'stroke-dasharray':'3 5'});
    const lo=R(data.conditional_S[0]).number(),hi=R(data.conditional_S[1]).number();
    add(svg,'line',{x1:x(1),y1:y(lo),x2:x(1),y2:y(hi),stroke:'var(--blue)','stroke-width':state.step===2?5:2});
    if(state.step===0){
      add(svg,'circle',{cx:x(1),cy:y(lo),r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});
      const c=point(data.triangle_hs[2]);add(svg,'rect',{x:c[0]-5,y:c[1]-5,width:10,height:10,fill:'var(--green)',stroke:'var(--surface)','stroke-width':2});
    }else if(state.step===1){
      const [px,py]=point(data.fake_hs);
      add(svg,'line',{x1:px,y1:py,x2:x(11/8),y2:py,stroke:'var(--red)','stroke-dasharray':'4 4'});
      add(svg,'path',{d:`M ${px-6} ${py-6} L ${px+6} ${py+6} M ${px+6} ${py-6} L ${px-6} ${py+6}`,stroke:'var(--red)','stroke-width':3,fill:'none'});
      text(svg,px-9,py-17,'Claimed pair',{'text-anchor':'end',class:'joint-failed-label'});
    }else{
      const s=R(data.conditional_S[0]).add(R(data.conditional_S[1]).sub(data.conditional_S[0]).mul(R(state.position).div(13)));
      add(svg,'circle',{cx:x(1),cy:y(s.number()),r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});
      add(svg,'line',{x1:x(1)+10,y1:y(hi),x2:x(1)+10,y2:y(17/8),stroke:'var(--red)','stroke-width':1.5});
      text(svg,x(1)+18,(y(hi)+y(17/8))/2+4,'gap', {class:'joint-failed-label'});
    }
  }
  function ranges(){
    const svg=el('joint-ranges'),height=state.step===2?130:215,width=clearSVG(svg,height);
    svg.style.height=`${height}px`;
    const xh=v=>24+(v-.5)*(width-48),xs=v=>24+(v-11/6)/(5/12)*(width-48);
    function rail(y,scale,low,high,color){
      add(svg,'line',{x1:24,y1:y,x2:width-24,y2:y,stroke:'var(--line)','stroke-width':1});
      add(svg,'line',{x1:scale(low),y1:y,x2:scale(high),y2:y,stroke:color,'stroke-width':6,'stroke-linecap':'round'});
      for(const v of [low,high])add(svg,'circle',{cx:scale(v),cy:y,r:4,fill:color});
    }
    let sY;
    if(state.step!==2){
      text(svg,0,17,'H range');text(svg,width,17,'contains 1',{'text-anchor':'end',class:'small'});
      rail(45,xh,5/8,11/8,'var(--blue)');
      for(const [v,label]of [[5/8,'5/8'],[1,'1'],[11/8,'11/8']]){text(svg,xh(v),72,label,{'text-anchor':'middle'});}
      add(svg,'circle',{cx:xh(1),cy:45,r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});
      text(svg,0,110,'S range');text(svg,width,110,'reaches 17/8',{'text-anchor':'end',class:'small'});sY=146;
    }else{text(svg,0,17,'S on the same H = 1 slice');sY=59;}
    for(const [lo,hi]of [[11/6,15/8],[17/8,9/4]])add(svg,'rect',{x:xs(lo),y:sY-10,width:xs(hi)-xs(lo),height:20,fill:'var(--green)','fill-opacity':.15});
    const range=(state.step===2?data.conditional_S:data.marginal_S).map(R);
    rail(sY,xs,range[0].number(),range[1].number(),state.step===2?'var(--blue)':'var(--amber)');
    for(const [v,label]of [[15/8,'15/8'],[2,'2'],[17/8,'17/8']]){
      add(svg,'line',{x1:xs(v),y1:sY-14,x2:xs(v),y2:sY+14,stroke:'var(--muted)','stroke-width':1,'stroke-dasharray':'2 3'});
      text(svg,xs(v),sY+36,label,{'text-anchor':'middle'});
    }
    if(state.step===2){
      text(svg,xs(range[0].number())-3,sY-20,String(range[0]),{'text-anchor':'end',class:'small'});
      text(svg,xs(range[1].number())+3,sY-20,String(range[1]),{'text-anchor':'start',class:'small'});
      const s=range[0].add(range[1].sub(range[0]).mul(R(state.position).div(13)));
      add(svg,'circle',{cx:xs(s.number()),cy:sY,r:6,fill:'var(--blue)',stroke:'var(--surface)','stroke-width':2});
    }
    text(svg,width,height-3,'Green bands include their endpoints',{'text-anchor':'end',class:'small'});
  }
  function physical(){
    const fake=state.step===1,ratio=R(state.position).div(13);
    const point=fake?data.fake_xy.map(R):data.section_xy[0].map((x,i)=>R(x).add(R(data.section_xy[1][i]).sub(x).mul(ratio)));
    const [x,y]=point,h=x.mul(4).sub(y),s=x.mul(5).add(y.mul(2)),threshold=R(data.threshold);
    const speeds=[1,4,5,6,7,11,13];
    const rows=speeds.map(speed=>{const phase=x.mul(speed).frac(),distance=min(phase,R(1).sub(phase));return{speed,lap:x.mul(speed).floor(),phase,distance,safe:distance.cmp(threshold)>=0};});
    const failed=rows.filter(r=>!r.safe).map(r=>r.speed),coreSafe=rows.slice(0,6).every(r=>r.safe);
    if(h.cmp(1)!==0)throw new Error('The displayed point left the actual orbit slice');
    if(fake&&failed.join(',')!=='6')throw new Error('The marginal candidate must violate speed 6');
    if(!fake&&(!coreSafe||failed.join(',')!=='13'))throw new Error('The actual parent slice must be blocked only by speed 13');
    el('joint-physical').hidden=state.step===0;
    el('joint-physical-title').textContent=fake?'The candidate breaks an earlier constraint.':'All six earlier runners pass. Runner 13 fails.';
    el('joint-time').textContent=`t = ${x}`;
    el('joint-x').textContent=String(x);el('joint-y').textContent=String(y);el('joint-h').textContent=String(h);
    el('joint-physical-copy').innerHTML=fake?
      '<p>The inverse map turns the claimed pair into (x, y) = (33/104, 7/26). It has the requested orbit and seventh-runner value, but lies outside the safe parent.</p><p>Runner 6 is only <strong>5/52</strong> from the reference, below 1/8. The separate-range test lost one of the conditions it was supposed to preserve.</p>':
      `<p>Keep H = 1 and move only along the parent slice. At this point, S = <strong>${s}</strong> and t = x = <strong>${x}</strong>.</p><p>${rows[6].distance.cmp(0)===0?'Runner 13 completes exactly four laps and coincides with reference 0.':`Runner 13 is only <strong>${rows[6].distance}</strong> from reference 0, below 1/8.`} The first six phase constraints still hold at this same time.</p>`;
    el('joint-phase-rows').replaceChildren(...rows.map(row=>{
      const tr=document.createElement('tr');if(!row.safe)tr.className='joint-failed-row';
      for(const value of [row.speed,row.lap,row.phase,row.distance]){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;
    }));
    const svg=el('joint-phase'),height=118,width=clearSVG(svg,height),px=v=>24+v*(width-48),line=58;
    add(svg,'title',{},`Added runner 13: phase ${rows[6].phase}, distance ${rows[6].distance}`);
    text(svg,0,18,'Runner 13’s physical phase');
    add(svg,'line',{x1:px(0),y1:line,x2:px(1),y2:line,stroke:'var(--line)','stroke-width':1});
    add(svg,'rect',{x:px(1/8),y:line-9,width:px(7/8)-px(1/8),height:18,fill:'var(--green)','fill-opacity':.15});
    for(const [v,label]of [[0,'0'],[1/8,'1/8'],[7/8,'7/8'],[1,'1']]){
      add(svg,'line',{x1:px(v),y1:line-12,x2:px(v),y2:line+12,stroke:'var(--line)'});
      text(svg,px(v),line+31,label,{'text-anchor':'middle'});
    }
    add(svg,'circle',{cx:px(rows[6].phase.number()),cy:line,r:6,fill:rows[6].safe?'var(--green)':'var(--red)',stroke:'var(--surface)','stroke-width':2});
    text(svg,width,height-5,'Closed safe band: [1/8, 7/8]',{'text-anchor':'end',class:'small'});
    return{point:point.map(String),h:String(h),s:String(s),time:String(x),coreSafe,failedSpeeds:failed,phases:rows.map(r=>String(r.phase)),distances:rows.map(r=>String(r.distance))};
  }
  function render(){
    if(el('joint-chapter').hidden)return;
    const scene=steps[state.step];
    for(const key of ['label','title','copy','conclusion']){
      const target=key==='conclusion'?el('joint-conclusion'):el(`joint-stage-${key}`);
      if(key==='copy')target.innerHTML=scene[key];else target.textContent=scene[key];
    }
    el('joint-plot-title').textContent=scene.plot;
    document.querySelectorAll('[data-joint-step]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.jointStep)===state.step)));
    el('joint-point-control').hidden=state.step!==2;
    el('joint-prev').disabled=state.step===0;el('joint-next').disabled=state.step===2;
    el('joint-next').hidden=state.step===2;
    el('joint-next').textContent=state.step===0?'Combine the claims →':'Keep the shared point →';
    el('joint-position').value=state.position;el('joint-position-label').textContent=`${state.position}/13 along the slice`;
    plot();ranges();const result=physical();
    window.CC_JOINT_STATE={step:state.step,position:state.position,...(state.step===0?{time:null}:result)};
  }
  function setStep(step){state.step=step;render();}
  document.querySelectorAll('[data-joint-step]').forEach(b=>b.addEventListener('click',()=>setStep(Number(b.dataset.jointStep))));
  el('joint-prev').addEventListener('click',()=>setStep(Math.max(0,state.step-1)));
  el('joint-next').addEventListener('click',()=>setStep(Math.min(2,state.step+1)));
  el('joint-position').addEventListener('input',()=>{state.position=Number(el('joint-position').value);render();});
  for(const [id,value]of [['joint-left',0],['joint-collision',6],['joint-right',13]])el(id).addEventListener('click',()=>{state.position=value;render();});
  el('joint-vertices').replaceChildren(...data.triangle_xy.map((p,i)=>{
    const tr=document.createElement('tr');for(const v of [labels[i],...p.slice(0,2).map(v=>String(R(v))),...data.triangle_hs[i].map(v=>String(R(v)))]){const td=document.createElement('td');td.textContent=v;tr.append(td);}return tr;
  }));
  const manifest=CC_DATA.manifest;
  el('joint-build-info').textContent=`Source commit ${manifest.source_commit.slice(0,12)} · data build ${manifest.data_build_sha256.slice(0,16)}.`;
  for(const key of ['joint_compatibility','joint_derivation']){
    const path=manifest.scene_sources[key],li=document.createElement('li'),a=document.createElement('a');
    a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=path;li.append(a);el('joint-source-links').append(li);
  }
  document.addEventListener('cc:chapter',render);
  new ResizeObserver(render).observe(el('joint-chapter'));
  render();
})();
