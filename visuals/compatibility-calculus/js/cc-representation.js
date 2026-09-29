/* Query-specific representations. All plotted values come from the pinned data. */
(() => {
  const {R,el,add,clearSVG}=CC;
  const g=CC_DATA.geometry,e=CC_DATA.examples,m=CC_DATA.manifest;
  const b=e.B.find(r=>r.q===6),a4=e.A.find(r=>r.q===4),a10=e.A.find(r=>r.q===10);
  const state={question:'value',reduced:false};
  const records={
    value:{ray:'B',q:6,label:'01 / OPTIMAL VALUE',title:'An attainable value needs a ceiling.',
      carrier:'Seven caps + a matching witness',
      explainer:'A physical time gives a lower bound. The cap argument supplies the matching upper bound. Together they identify the optimum.',
      remove:'Keep only the witness',retain:'All seven caps, integer contacts and the supplied lower-bound premise above 1/7. Keep the physical recovery that certifies attainment.',
      omit:'Geometry below 1/7 and the three singleton cells. They cannot beat the supplied B-ray witness; they still matter to other questions.',
      trigger:'You lower the threshold, add a constraint, or lose the premise that the optimum exceeds 1/7.',
      recovery:'Restore the full labelled cells and recheck the operation with the appropriate orbit and clock.',
      source:'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',related:'#cap',relatedText:'Explore cap → contact → clock',
      caption:'Bars show allowed values of F within [1/8, 1/6]. Both bounds are exact in this q=6 control. The all-q justification is the pinned proof candidate, not this drawing.'},
    maximizers:{ray:'B',q:6,label:'02 / EVERY MAXIMIZING TIME',title:'The value does not name its witnesses.',
      carrier:'Caps + contact identities + reflection',
      explainer:'The maximum is a number. Every maximizing time is a set. Retaining extremal points, tied contacts and their recovery maps answers the stronger question.',
      remove:'Keep only the best value',retain:'Supporting directions, all winning contacts, strict exclusion of nonwinners, physical time recovery and reflection. Deduplicate repeated recoveries.',
      omit:'Nonmaximizing safe times and geometry below the justified cap cut. A list of cap names alone is not a list of distinct physical times.',
      trigger:'You ask for all safe times rather than just the times attaining the maximum.',
      recovery:'Return to full closed feasibility at the requested threshold; impose the orbit and recover every compatible time.',
      source:'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',related:'#cap',relatedText:'Inspect the contact and reflection controls',
      caption:'The two q=6 times below come from exact physical optimization and match the recovered cap contacts.'},
    witness:{ray:'A',q:4,label:'03 / ONE SAFE TIME',title:'A small certificate can be enough.',
      carrier:'Two closed compatible segments',
      explainer:'For one 1/8-safe time, two supplied parent segments with integer rounding and recovery suffice in the pinned candidate. At q=4, the selected point is a closed endpoint.',
      remove:'Remove segment endpoints',retain:'Both segment equations, all seven joint bands, closed endpoints, integer compatibility, the coverage argument and the time/lap map.',
      omit:'Other safe points, the optimum value and complete maximizing-time sets. One recovered witness also establishes existence in its stated scope.',
      trigger:'You ask for optimality, every maximizer, or the entire safe set—or change the ray or threshold.',
      recovery:'Recover the richer parent/child atlas. The two segments cannot reconstruct the points they omit.',
      source:'notes/CC_BOUNDED_SELECTOR_2026_09_29.md',related:null,
      caption:'The rails show H = 4x − y on each segment. The integer 0 occurs only at E1’s closed endpoint; E2 contains no integer.'},
    safe:{ray:'A',q:4,label:'04 / COMPLETE SAFE SET',title:'Zero duration can still contain witnesses.',
      carrier:'Full closed cells + actual-orbit recovery',
      explainer:'Adding runner 13 removes all four positive safe intervals of the six-runner prefix. Four isolated safe times remain. Their zero length does not make them empty.',
      remove:'Keep positive durations only',retain:'Every relevant closed cell, labels, singleton components, all actual-orbit intersections and the physical recovery map.',
      omit:'No feasible point at the stated threshold. The continuum is represented by exact inequalities and intervals rather than by a point-by-point list.',
      trigger:'You change the threshold, coefficient forms or reference runner. A complete set at one threshold is not a complete answer at another.',
      recovery:'Recheck the full inequalities and orbit map. Below the stored floor 1/8, rebuild the affected geometry.',
      source:'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',related:'#joint',relatedText:'See why one parent interval disappears',
      caption:'Physical time runs from 0 to 1. Filled endpoints and isolated dots count; the full seven-runner safe set is exactly the four displayed times.'},
    transfer:{ray:'A',q:4,label:'05 / ADD A CONSTRAINT',title:'Condition on the same state first.',
      carrier:'Closed intervals conditional on one orbit',
      explainer:'For parent P2 at height 1/8, hold H = 1 before testing the added runner. The full conditional interval is blocked, even though the separate S range reaches a safe value.',
      remove:'Use separate ranges',retain:'The same parent label, integer H, height z, conditional S interval, seventh lap and inverse map. Intersect with a closed safe band.',
      omit:'One evaluated interval leaves out other parents, H values, heights and support changes. It provides no automatic bound on the number of tests.',
      trigger:'You need the whole safe set or a guaranteed bounded selector instead of survival on this one slice.',
      recovery:'Restore the complete conditional family or derive a separate coverage/selection certificate. Recover x = (S + 2H)/(2q + 5), then t = x.',
      source:'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',related:'#joint',relatedText:'Open the full same-point counterexample',
      caption:'This is a decision about one parent. The four full-system q=4 witnesses lie elsewhere and remain valid.'},
    faces:{ray:'A',q:10,label:'06 / EVERY OPTIMIZER AFTER TRANSFER',title:'A new constraint can make a new contact.',
      carrier:'Parent faces + complete child contacts',
      explainer:'The added band cuts through old parent faces. Two final maximizing times come from face interiors, so keeping only the old edges misses part of the answer.',
      remove:'Keep only old parent edges',retain:'Full parent faces, the added band, all resulting child contacts, ties, closed boundaries and reflected physical times.',
      omit:'A complete maximizing set still omits lower-valued safe times. All optimizers and all safe times remain different outputs.',
      trigger:'You use a witness selector or an old-edge record to claim that every final maximizer has been found.',
      recovery:'Restore parent faces and clip with the new band; then recover all child optima. Missing one optimizer refutes completeness, not selection of a different optimizer.',
      source:'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',related:null,
      caption:'The q=10 maximum is 1/7. The 17/35 contact lies in a two-dimensional old parent face; 18/35 is its reflected physical time.'}
  };
  const qtext=(v)=>String(R(v));
  function chips(items){
    el('rep-exact-values').replaceChildren(...items.map(({label,missing=false})=>{
      const node=document.createElement('span');node.className='rep-value'+(missing?' rep-missing':'');node.textContent=label;return node;
    }));
  }
  function diagram(record){
    const svg=el('rep-diagram'),height=235,width=clearSVG(svg,height),left=23,right=width-23;
    const text=(x,y,label,attrs={})=>{
      const node=add(svg,'text',{x,y,...attrs},label);
      if(!attrs['text-anchor']&&node.getComputedTextLength()>width-x){
        const words=label.split(' ');node.textContent='';let line='';let row=0;
        let span=add(node,'tspan',{x,y},'');
        for(const word of words){
          const trial=line?line+' '+word:word;span.textContent=trial;
          if(line&&span.getComputedTextLength()>width-x){span.textContent=line;span=add(node,'tspan',{x,y:y+14*(++row)},word);line=word;}else line=trial;
        }
      }
      return node;
    };
    const title=record.title+(state.reduced?' — reduced record':' — adequate record');
    add(svg,'title',{},title);
    svg.setAttribute('aria-label',title);
    function rail(y,lo,hi){
      const scale=value=>left+R(value).sub(lo).div(R(hi).sub(lo)).number()*(right-left);
      add(svg,'line',{x1:left,y1:y,x2:right,y2:y,stroke:'var(--line)','stroke-width':1.5});return scale;
    }
    function line(scale,y,lo,hi,color='var(--green)',open=false){
      add(svg,'line',{x1:scale(lo),y1:y,x2:scale(hi),y2:y,stroke:color,'stroke-width':5});
      for(const p of [lo,hi])add(svg,'circle',{cx:scale(p),cy:y,r:4,fill:open?'var(--surface)':color,stroke:color,'stroke-width':1.5});
    }
    function dot(scale,y,value,missing=false,color='var(--green)'){
      add(svg,'circle',{cx:scale(value),cy:y,r:6,fill:missing?'var(--surface)':color,stroke:missing?'var(--red)':color,'stroke-width':2,'stroke-dasharray':missing?'2 2':'none'});
    }
    function ticks(scale,y,values){for(const value of values){text(scale(value),y+28,qtext(value),{'text-anchor':'middle'});}}
    const result={question:state.question,reduced:state.reduced,ray:record.ray,clock:g.parameter_families[record.ray].clock,q:record.q,shownTimes:[],missingTimes:[]};
    let items=[],answer='',verdict='SUPPORTED FOR THIS QUESTION';
    if(state.question==='value'){
      const max=R(b.maximum),scale=rail(92,'1/8','1/6');
      text(0,22,`Lower bound: F ≥ ${max}`);
      line(scale,92,max,'1/6','var(--blue)');dot(scale,92,max,false,'var(--blue)');ticks(scale,92,['1/8','1/7','1/6']);
      text(scale(max),72,qtext(max),{'text-anchor':'middle'});
      text(0,163,state.reduced?'Upper bound omitted':`Upper bound: F ≤ ${max}`);
      const upper=rail(194,'1/8','1/6');
      if(!state.reduced){line(upper,194,'1/8',max);dot(upper,194,max);text(upper(max),222,qtext(max),{'text-anchor':'middle'});}
      else text(width/2,224,'No upper bound in this record.',{'text-anchor':'middle',class:'small'});
      result.lowerBound=qtext(max);result.upperBound=state.reduced?null:qtext(max);
      items=[{label:`Witness t = ${qtext(b.times[0])}`},{label:`F ≥ ${max}`},...(!state.reduced?[{label:`F ≤ ${max}`}]:[])];
      answer=state.reduced?'The witness still proves attainment. It cannot, by itself, rule out a better time.':'Matching bounds give F = 4/25. The witness and the upper-bound argument have different jobs.';
      if(state.reduced)verdict='OPTIMALITY NOT ESTABLISHED BY THIS RECORD';
    }else if(state.question==='maximizers'||state.question==='faces'){
      const isB=state.question==='maximizers';
      const all=isB?b.times:a10.transfer.optimization.find(x=>x.coordinates===7).all_maximizing_times;
      const faceTimes=a10.transfer.folded_child_maximizer_origins.filter(x=>x.parent_face_dimension===2).flatMap(x=>[R(x.time),R(1).sub(x.time)]).map(String);
      const missing=state.reduced?all.filter(t=>isB||faceTimes.includes(qtext(t))):[];
      result.shownTimes=all.filter(t=>!missing.includes(t)).map(qtext);result.missingTimes=missing.map(qtext);
      result.maximum=qtext(isB?b.maximum:a10.transfer.optimization.find(x=>x.coordinates===7).maximum);
      text(0,25,isB?'Physical maximizing times':'Physical maximizing times after addition');
      const scale=rail(95,0,1);ticks(scale,95,[0,'1/2',1]);
      for(const t of all){const lost=missing.includes(t);if(!isB||!lost)dot(scale,95,t,lost,!isB&&faceTimes.includes(qtext(t))?'var(--amber)':'var(--green)');}
      text(0,177,state.reduced?(isB?'Only the value survives.':'Hollow marks show the two omitted times.'):(isB?'Both times attain the same maximum.':'Amber marks come from old face interiors.'));
      items=[{label:`Maximum = ${result.maximum}`},...all.map(t=>({label:state.reduced&&isB?'Time identity omitted':`t = ${qtext(t)}`,missing:missing.includes(t)}))];
      if(isB){
        answer=state.reduced?'The number 4/25 does not identify 9/25 and 16/25. Recover contact identities and the physical map to reconstruct that set.':'Both 9/25 and 16/25 are retained, including their reflection relation. There are exactly two maximizing times in this control.';
        if(state.reduced)verdict='THE COMPLETE TIME SET IS MISSING';
      }else{
        answer=state.reduced?'Six maximizers remain, but 17/35 and 18/35 are missing. This still supplies some optimizer; it fails the request for every optimizer.':'All eight final maximizers are retained. The two face-interior times survive alongside the six old-edge times.';
        if(state.reduced)verdict='SOME OPTIMIZERS SURVIVE · COMPLETENESS FAILS';
      }
    }else if(state.question==='witness'){
      result.orbitIntervals=[];
      for(const [i,segment]of g.selectors.A.segments.entries()){
        const endpoints=segment.endpoints.map(p=>p.point.map(R));
        const values=endpoints.map(([x,y])=>x.mul(4).sub(y)).sort((a,b)=>a.cmp(b));
        result.orbitIntervals.push(values.map(String));
        const y=i?182:69,scale=rail(y,0,2);
        text(0,y-33,`${segment.segment}: H ∈ ${state.reduced?'(':'['}${values[0]}, ${values[1]}${state.reduced?')':']'}`);
        line(scale,y,...values,'var(--green)',state.reduced);ticks(scale,y,[0,1,2]);
        const start=values[0].frac().cmp(0)===0?values[0].floor():values[0].floor()+1n;
        for(let h=start;R(h).cmp(values[1])<=0;h++){
          if(state.reduced&&(R(h).cmp(values[0])===0||R(h).cmp(values[1])===0))continue;
          dot(scale,y,h,false,'var(--blue)');
          const ratio=R(h).sub(values[0]).div(values[1].sub(values[0]));
          const time=endpoints[0][0].add(endpoints[1][0].sub(endpoints[0][0]).mul(ratio));
          result.shownTimes.push(String(time));
        }
      }
      if(state.reduced)result.missingTimes=[qtext(a4.witness.time)];
      items=[{label:state.reduced?'No integer remains in either open segment':'H = 0 → t = 1/8'},{label:'Required separation ≥ 1/8'}];
      answer=state.reduced?'Removing the endpoints removes the only integer contact in these two q=4 segments. The real witness at 1/8 still exists; the altered record has lost it.':'One recovered time is enough for this question. All seven distances at t = 1/8 are at least 1/8.';
      if(state.reduced)verdict='THE SELECTOR LOSES ITS q = 4 WITNESS';
    }else if(state.question==='safe'){
      const parent=a4.transfer.six_safe_components_at_1_over_8,child=a4.transfer.seven_safe_components_at_1_over_8;
      for(const [components,y,label]of [[parent,65,'Six moving runners: intervals + points'],[child,179,'Seven moving runners: isolated points']]){
        text(0,y-33,label);const scale=rail(y,0,1);ticks(scale,y,[0,'1/2',1]);
        for(const [lo,hi]of components){if(R(lo).cmp(hi)===0)dot(scale,y,lo,state.reduced);else line(scale,y,lo,hi);}
      }
      result.shownTimes=state.reduced?[]:child.map(c=>qtext(c[0]));result.missingTimes=state.reduced?child.map(c=>qtext(c[0])):[];
      items=child.map(c=>({label:`t = ${qtext(c[0])}`,missing:state.reduced}));
      answer=state.reduced?'A positive-duration-only record omits all four final safe times. Empty duration and an empty safe set are different conclusions.':'Exactly four closed singleton times remain. The full set retains all of them, even though their total duration is zero.';
      if(state.reduced)verdict='ALL FOUR FINAL WITNESSES ARE OMITTED';
    }else{
      const joint=e.joint_visual,range=state.reduced?joint.marginal_S:joint.conditional_S;
      text(0,26,state.reduced?'S without conditioning on H':'S at the same H = 1');
      const scale=rail(112,'11/6','9/4');
      for(const [lo,hi]of [['11/6','15/8'],['17/8','9/4']])add(svg,'rect',{x:scale(lo),y:89,width:scale(hi)-scale(lo),height:46,fill:'var(--green)','fill-opacity':.14});
      line(scale,112,...range,state.reduced?'var(--amber)':'var(--blue)');ticks(scale,112,['15/8',2,'17/8']);
      text(0,199,'Green bands include their endpoints');
      result.range=range.map(qtext);result.safeBandOverlap=state.reduced;
      items=[{label:`S ∈ [${range.map(qtext).join(', ')}]`},{label:state.reduced?'False combined pair: H = 1, S = 17/8':'15/8 < S < 17/8 throughout'}];
      answer=state.reduced?'The marginal reaches 17/8, but that safe value does not coexist with H = 1 in P2. Combining them gives t = 33/104, where runner 6 fails safety.':'The entire conditional interval misses both safe bands. Parent P2 contributes no surviving time at this height.';
      if(state.reduced)verdict='SEPARATE RANGES CREATE A FALSE POSITIVE';
    }
    chips(items);el('rep-result-label').textContent=verdict;el('rep-result-text').textContent=answer;
    el('rep-result').classList.toggle('rep-warning',state.reduced);
    return result;
  }
  function render(){
    if(el('representation-chapter').hidden)return;
    const record=records[state.question],family=g.parameter_families[record.ray];
    for(const key of ['title','explainer','carrier','retain','omit','trigger','recovery','caption'])el(`rep-${key}`).textContent=record[key];
    el('rep-question-label').textContent=record.label;
    el('rep-family').textContent=`${record.ray} ray`;
    el('rep-example').textContent=`q = ${record.q}`;
    el('rep-map').textContent=`${family.orbit.replace(' in Z',' ∈ ℤ')}  ·  ${family.clock}`;
    el('rep-coordinates').textContent=family.coordinates;
    const example=e[record.ray].find(r=>r.q===record.q);
    el('rep-speeds').textContent=`Moving speeds: ${example.speeds.join(', ')} · reference 0`;
    el('rep-remove').textContent=record.remove;
    el('rep-keep').setAttribute('aria-pressed',String(!state.reduced));el('rep-remove').setAttribute('aria-pressed',String(state.reduced));
    document.querySelectorAll('[data-rep-question]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.repQuestion===state.question)));
    document.querySelectorAll('[data-rep-ray]').forEach(b=>b.classList.toggle('rep-branch-active',b.dataset.repRay===record.ray));
    document.querySelectorAll('[data-rep-model]').forEach(b=>b.classList.toggle('rep-model-active',b.dataset.repModel===state.question));
    el('rep-source').href=`${m.repository}/blob/${m.source_commit}/${record.source}`;
    el('rep-related').hidden=!record.related;
    if(record.related){el('rep-related').href=record.related;el('rep-related').textContent=record.relatedText+' →';}
    window.CC_REP_STATE=diagram(record);
  }
  document.querySelectorAll('[data-rep-question]').forEach(button=>button.addEventListener('click',()=>{state.question=button.dataset.repQuestion;state.reduced=false;render();}));
  el('rep-keep').addEventListener('click',()=>{state.reduced=false;render();});
  el('rep-remove').addEventListener('click',()=>{state.reduced=true;render();});
  el('rep-build-info').textContent=`Source commit ${m.source_commit.slice(0,12)} · data build ${m.data_build_sha256.slice(0,16)}.`;
  for(const path of ['notes/CC_REPRESENTATION_RULES.md',...new Set(Object.values(records).map(r=>r.source))]){
    const li=document.createElement('li'),a=document.createElement('a');a.href=`${m.repository}/blob/${m.source_commit}/${path}`;a.textContent=path;li.append(a);el('rep-source-links').append(li);
  }
  document.addEventListener('cc:chapter',render);
  new ResizeObserver(render).observe(el('representation-chapter'));
  render();
})();
