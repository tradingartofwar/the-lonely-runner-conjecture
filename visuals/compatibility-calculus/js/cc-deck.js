/* A deliberately bounded first slice. No backend, CDN, fetch or sampled proof. */
(() => {
  const {R,min,el,physical}=CC;
  const state={q:6,cap:'B',progress:100,azimuth:28,tilt:35,full:false,reflected:false};
  let frame=null,start=null,startProgress=0;
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  function example(){return CC_DATA.examples.B.find(e=>e.q===state.q);}
  function stop(){if(frame!==null)cancelAnimationFrame(frame);frame=null;start=null;el('play').textContent=reduced.matches?'Show contact':'Play to contact';}
  function selectQ(){
    const ex=example();state.cap=ex.winner_caps[0];state.progress=100;
    el('cap').replaceChildren(...ex.winner_caps.map(id=>{const n=document.createElement('option');n.value=id;n.textContent=`Cap ${id}`;return n;}));
    el('cap-field').hidden=ex.winner_caps.length===1;
    el('speed-list').textContent=`0; ${ex.speeds.join(', ')}`;
    el('cap-comparison').replaceChildren(...ex.contacts.map(c=>{
      const row=document.createElement('tr');if(ex.winner_caps.includes(c.cap))row.className='active';
      const values=[c.cap,String(R(c.loss)),c.in_cap?'yes':'no',c.in_cap?String(R('1/6').sub(c.loss)):'outside cap'];
      for(const value of values){const td=document.createElement('td');td.textContent=value;row.append(td);}return row;
    }));
  }
  function render(){
    if(el('cap-chapter').hidden)return;
    const ex=example(),cap=CC_DATA.geometry.top_caps.find(c=>c.id===state.cap),contact=ex.contacts.find(c=>c.cap===state.cap);
    const totalLoss=R(contact.loss),zero=totalLoss.cmp(0)===0;
    if(zero)state.progress=100;
    const loss=totalLoss.mul(R(state.progress).div(100)),z=R('1/6').sub(loss),hit=state.progress===100;
    const section=cap.rays.map(ray=>cap.peak.map((p,i)=>R(p).add(loss.mul(ray[i]))));
    const point=contact.direction_index===null?cap.peak.map(R):section[contact.direction_index];
    const lo=R(contact.h0).add(loss.mul(contact.d_min)),hi=R(contact.h0).add(loss.mul(contact.d_max));
    el('cap-name').textContent=`Cap ${cap.id}`;
    el('loss').textContent=String(loss);el('height').textContent=String(z);
    el('interval').textContent=`[${lo}, ${hi}]`;
    el('progress').value=state.progress;el('progress').disabled=zero;
    el('progress-label').textContent=zero?'Already compatible at the peak':`${state.progress}% of first-contact loss`;
    el('peak').disabled=zero;el('play').disabled=zero;el('hit').disabled=zero;
    el('contact-status').textContent=hit?(zero?`The peak already has H = ${contact.orbit_integer}. No loss is needed.`:`First contact: H = ${contact.orbit_integer}. The section now contains an actual runner state.`):'No integer in the interval yet. Every point in this section is ambient-only.';
    CCGeometry.draw(el('geometry'),cap,section,point,hit,state);
    CCGeometry.interval(el('projection'),contact,lo,hi,hit);
    el('physical-empty').hidden=hit;el('physical-content').hidden=!hit;el('reflection').disabled=!hit;
    if(hit){
      const [x,y]=point;const t=state.reflected?R(1).sub(y):y;
      const rows=physical(state.q,t),minimum=rows.reduce((d,row)=>min(d,row.distance),R('1/2'));
      if(minimum.cmp(z)!==0)throw new Error('Physical recovery does not match the section height');
      el('recovery-values').textContent=`t = ${y}${state.reflected?` → ${t}`:''}`;
      el('recovery-text').textContent=`At (x, y, z) = (${x}, ${y}, ${z}), x − ${state.q}y = ${contact.orbit_integer}. The integer difference is whole laps: x and qy represent the same position on the circle. Set t = y. ${state.reflected?'Reflection gives the second physical time shown below.':'The table checks all seven phases at that same time.'}`;
      el('physical-summary').textContent=`Minimum distance = ${minimum} · all seven runners are at least this far from reference 0.`;
      el('phase-rows').replaceChildren(...rows.map(row=>{
        const tr=document.createElement('tr');if(row.distance.cmp(minimum)===0)tr.className='active';
        for(const value of [row.speed,row.lap,row.phase,row.distance]){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}return tr;
      }));
      CCGeometry.runners(el('runners'),rows,z,t);
      window.CC_STATE={q:state.q,cap:state.cap,progress:state.progress,hit:true,loss:String(loss),z:String(z),time:String(t),point:point.map(String),h:contact.orbit_integer,phases:rows.map(r=>String(r.phase)),minimum:String(minimum),reflected:state.reflected};
    }else{
      el('recovery-values').textContent='No physical time selected';
      el('recovery-text').textContent='Being inside the safe cap is not enough. The displayed section must meet an integer orbit slice before its point can become a physical witness.';
      window.CC_STATE={q:state.q,cap:state.cap,progress:state.progress,hit:false,loss:String(loss),z:String(z),interval:[String(lo),String(hi)],time:null};
    }
  }
  el('q').addEventListener('change',()=>{stop();state.q=Number(el('q').value);selectQ();render();});
  el('cap').addEventListener('change',()=>{stop();state.cap=el('cap').value;render();});
  el('progress').addEventListener('input',()=>{stop();state.progress=Number(el('progress').value);render();});
  el('peak').addEventListener('click',()=>{stop();state.progress=0;render();});
  el('hit').addEventListener('click',()=>{stop();state.progress=100;render();});
  el('play').addEventListener('click',()=>{
    if(frame!==null){stop();return;}
    if(reduced.matches){state.progress=100;render();return;}
    if(state.progress===100)state.progress=0;
    startProgress=state.progress;start=null;el('play').textContent='Pause';
    function tick(now){if(start===null)start=now;state.progress=Math.min(100,Math.floor(startProgress+(now-start)/32));render();if(state.progress<100)frame=requestAnimationFrame(tick);else stop();}
    frame=requestAnimationFrame(tick);
  });
  for(const [id,delta]of [['rotate-left',-15],['rotate-right',15]])el(id).addEventListener('click',()=>{state.azimuth+=delta;render();});
  el('tilt').addEventListener('input',()=>{state.tilt=Number(el('tilt').value);render();});
  el('reset-view').addEventListener('click',()=>{state.azimuth=28;state.tilt=35;el('tilt').value=35;render();});
  el('full-context').addEventListener('change',()=>{state.full=el('full-context').checked;render();});
  el('reflection').addEventListener('change',()=>{state.reflected=el('reflection').checked;render();});
  const manifest=CC_DATA.manifest;
  el('build-info').textContent=`Generated from ${manifest.source_commit.slice(0,12)}. Visual-data SHA-256: ${manifest.data_build_sha256}.`;
  for(const [name,path]of Object.entries(manifest.scene_sources)){
    const li=document.createElement('li'),a=document.createElement('a');a.href=`${manifest.repository}/blob/${manifest.source_commit}/${path}`;a.textContent=`${name}: ${path.split('/').pop()}`;li.append(a);el('source-links').append(li);
  }
  selectQ();stop();render();
  document.addEventListener('cc:chapter',event=>{if(event.detail.joint)stop();else render();});
  let resizeFrame=null;
  const observer=new ResizeObserver(()=>{if(resizeFrame!==null)cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{resizeFrame=null;render();});});
  observer.observe(document.querySelector('main'));
})();
