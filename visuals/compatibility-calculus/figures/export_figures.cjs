#!/usr/bin/env node
/* Vector exports of selected, verified presentation states. No raster capture. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
let playwright;try{playwright=require('playwright');}catch{playwright=require(require.resolve('playwright',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES].filter(Boolean)}));}
const dir=__dirname,root=path.resolve(dir,'..'),check=process.argv.includes('--check');
const read=p=>fs.readFileSync(path.join(root,p),'utf8'),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const manifest=JSON.parse(read('data/visual_manifest.json')),geometry=JSON.parse(read('data/cc_geometry.json')),examples=JSON.parse(read('data/cc_examples.json'));
const inputs=Object.fromEntries(['presentation.html','data/cc_geometry.json','data/cc_examples.json','data/visual_manifest.json','data/source_hashes.json','figures/export_figures.cjs'].map(p=>[p,sha(read(p))]));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const exact=v=>v&&typeof v==='object'?(v.text??(Array.isArray(v)?v.map(exact):Object.fromEntries(Object.entries(v).map(([k,x])=>[k,exact(x)])))):v;
const G=exact(geometry),E=exact(examples),src=manifest.scene_sources;
const C={bg:'#f5f3ed',ink:'#1b3431',muted:'#566862',green:'#006655',line:'#d5ddd7',white:'#ffffff',pale:'#e7f0e9'};
function text(x,y,value,size=18,color=C.ink,extra=''){return `<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${size}" fill="${color}" ${extra}>${esc(value)}</text>`;}
function lines(value,max){const result=[];for(const para of value.split('\n')){let line='';for(const word of para.split(/\s+/)){if(line&&line.length+word.length+1>max){result.push(line);line='';}line+=(line?' ':'')+word;}result.push(line);}return result;}
function para(x,y,value,width=1112,size=18,color=C.muted){const rows=lines(value,Math.floor(width/(size*.57)));return {svg:rows.map((s,i)=>text(x,y+i*size*1.48,s,size,color)).join(''),height:rows.length*size*1.48};}
function box(x,y,w,h){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="${C.white}" stroke="${C.line}"/>`;}
function label(x,y,s){return text(x,y,s,16,C.green,'font-weight="700"');}
function note(x,y,w,title,body){const p=para(x+24,y+64,body,w-48);return{svg:box(x,y,w,p.height+90)+label(x+24,y+30,title)+p.svg,height:p.height+90};}
function diagram(capture,x,y,w,h){return `<svg class="export-panel" data-origin="${esc(capture.origin)}" x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${capture.viewBox}" overflow="hidden">${capture.content}</svg>`;}
function panel(capture,x,y,w,h,title){return box(x,y,w,h)+label(x+22,y+29,title)+diagram(capture,x+12,y+45,w-24,h-57);}
const figures=[];
function add(id,title,subtitle,body,height,caption,status,sources,state){
  const number=String(figures.length+1).padStart(2,'0'),foot=height+182;
  const p=para(44,foot+30,caption);let y=foot+30+p.height+20;
  let footer=text(44,y,`STATUS · ${status}`,14,C.green,'font-weight="700"');y+=30;
  footer+=text(44,y,`Pinned source ${manifest.source_commit} · exact values take precedence over screen lengths.`,13);y+=24;
  for(const source of [...new Set(sources)]){footer+=`<a href="${manifest.repository}/blob/${manifest.source_commit}/${esc(source)}">${text(44,y,source,13,C.green,'text-decoration="underline"')}</a>`;y+=23;}
  footer+=text(44,y+7,`Visual data SHA-256: ${manifest.data_build_sha256}`,12,C.muted);y+=47;
  const metadata={id,number,title,source_commit:manifest.source_commit,visual_data_sha256:manifest.data_build_sha256,input_sha256:inputs,selected_state:state,status,sources:[...new Set(sources)],caption};
  const svg=`<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="${Math.ceil(y)}" viewBox="0 0 1200 ${Math.ceil(y)}" role="img" aria-labelledby="figure-title figure-desc">\n<title id="figure-title">${esc(title)}</title><desc id="figure-desc">${esc(subtitle+' '+caption)}</desc>\n<metadata id="cc-figure-metadata">${esc(JSON.stringify(metadata))}</metadata>\n<rect width="1200" height="${Math.ceil(y)}" fill="${C.bg}"/>\n${text(44,39,`COMPATIBILITY CALCULUS     /     FIGURE ${number}`,14,C.green,'letter-spacing="1.4" font-weight="700"')}${text(44,91,title,36,C.ink,'font-weight="700"')}${text(44,128,subtitle,18,C.muted)}\n<g transform="translate(0 158)">${body}</g>\n<path d="M44 ${foot} H1156" stroke="${C.line}"/>${p.svg}${footer}\n</svg>\n`;
  figures.push({...metadata,file:`${number}-${id}.svg`,width:1200,height:Math.ceil(y),svg,sha256:sha(svg)});
}
async function main(){
 const browser=await playwright.chromium.launch({headless:true,...(process.env.CC_CHROMIUM_PATH?{executablePath:process.env.CC_CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000},colorScheme:'light',reducedMotion:'reduce'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'presentation.html')).href);
  await page.addStyleTag({content:'body,svg text{font-family:Arial,sans-serif!important} *,*::before,*::after{transition:none!important;animation:none!important}'});
  const settle=()=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  async function chapter(name){await page.evaluate(name=>{location.hash=name;},name);await settle();}
  const click=s=>page.locator(s).click();
  const state=name=>page.evaluate(name=>window[name],name);
  async function capture(selector,width,height){
   await page.evaluate(({selector,width,height})=>{const el=document.querySelector(selector);el.style.width=`${width}px`;el.style.maxWidth='none';el.style.minHeight='0';el.style.flex='none';if(height)el.style.height=`${height}px`;document.dispatchEvent(new CustomEvent('cc:chapter',{detail:{chapter:location.hash.slice(1)}}));},{selector,width,height});await settle();
   if(selector==='#cell-atlas')await page.evaluate(()=>{
    const svg=document.querySelector('#cell-atlas'),dots=[...svg.querySelectorAll('.cell-vertex-dot')],selected=window.CC_CELL_STATE.construction.cell;
    const cells=CC_DATA.geometry.full_cells.filter(c=>!c.singleton),ordered=[...cells.filter(c=>c.id!==selected),...cells.filter(c=>c.id===selected)];
    const offsets={C1:[35,-12],C2:[-40,0],C4:[28,-10],C6:[28,16],C7:[-30,35],C8:[32,18],C9:[-30,20]};let offset=0;
    for(const cell of ordered){const points=dots.slice(offset,offset+cell.vertices.length);offset+=points.length;const x=points.reduce((n,p)=>n+Number(p.getAttribute('cx')),0)/points.length,y=points.reduce((n,p)=>n+Number(p.getAttribute('cy')),0)/points.length;CC.add(svg,'text',{x:x+offsets[cell.id][0],y:y+offsets[cell.id][1],class:'atlas-cell-label','font-size':13,fill:'var(--muted)'},cell.id);}
   });
   return page.evaluate(selector=>{
    const el=document.querySelector(selector),clone=el.cloneNode(true);
    const properties=['fill','fill-opacity','fill-rule','stroke','stroke-width','stroke-opacity','stroke-linecap','stroke-linejoin','stroke-dasharray','stroke-dashoffset','opacity','font-family','font-size','font-weight','font-style','letter-spacing','text-anchor','dominant-baseline','paint-order','visibility'];
    const originals=[el,...el.querySelectorAll('*')],copies=[clone,...clone.querySelectorAll('*')];
    originals.forEach((node,i)=>{const target=copies[i],style=getComputedStyle(node);target.removeAttribute('style');target.removeAttribute('id');for(const prop of properties)target.setAttribute(prop,style.getPropertyValue(prop));});
    return{origin:selector,viewBox:el.getAttribute('viewBox'),content:clone.innerHTML};
   },selector);
  }
  // 01: same state, two reference frames. Identity is retained at coincidences.
  await chapter('opening');await click('#opening-references [data-reference="1"]');
  await page.locator('#opening-time').fill('32');await click('#opening-track-view');
  const openTrack=await capture('#opening-track',520),openA=await state('CC_OPENING_STATE');
  await click('#opening-relative-view');const openRelative=await capture('#opening-track',520),openB=await state('CC_OPENING_STATE');
  assert.equal(openA.time,'1/3');assert.equal(openB.reference,1);assert.deepEqual(openA.distances,openB.distances);
  add('runner-circle','One track. Two frames.','Four common-start runners · speeds 1, 2, 3, 4 · reference R2 · t = 1/3',
   panel(openTrack,44,0,546,365,'01  TRACK FRAME')+panel(openRelative,610,0,546,365,'02  MOVING WITH R2')+
   note(44,385,1112,'THE DISTANCES STAY THE SAME',`Track phases: ${openA.absolute.join(', ')}. Relative speeds: ${openB.relativeSpeeds.join(', ')}. Relative phases: ${openB.relativePhases.join(', ')}. The selected reference is at zero in the moving frame; all three distances are 1/3, above the 1/4 threshold.`).svg,555,
   'Runners start together. Here R1 and R4 coincide, while R2 and R3 are each lonely. Concentric rings preserve coincident identities. The amber arc marks distance < 1/4, with hollow equality endpoints; blue shows a shortest distance. Phase increases clockwise from the top. Subtracting the reference speed preserves distances; changing the reference changes whose loneliness is checked.',
   'REPRODUCED finite example of the standard reference change',[src.opening],{track:openA,relative:openB});
  // 02–03: one physical clock, with occurrence identity preserved.
  await chapter('clock');await click('#clock-split');await click('#clock-safe-middle');
  const timeline=await capture('#clock-timeline',1088),zoom=await capture('#clock-zoom',1088),clock=await state('CC_CLOCK_STATE');
  assert.equal(clock.graphNodes,6);assert.deepEqual(clock.safeComponents,[['17/56','39/128']]);
  add('shared-clock','One shared clock','Eight runners · speeds 0, 1, 4, 5, 6, 7, 11, 16 · threshold 1/8',
   panel(timeline,44,0,1112,435,'LABELLED BLOCKING OCCURRENCES IN J = [9/32, 3/8]')+panel(zoom,44,455,1112,252,'THE SAFE GAP, MAGNIFIED'),707,
   `Each row is a strict blocking occurrence: distance < 1/8. Hollow endpoints exclude equality; filled endpoints can come from clipping to the window. Runners 1, 4 and 5 are safe throughout J. The local safe set is the closed interval [17/56, 39/128], duration 1/896. The cursor is at its midpoint t=${clock.time}. Meeting label m identifies the nearby zero-distance event; it is not the completed lap.`,
   'REPRODUCED exact local interval calculation',[src.shared_clock,src.occurrence_identity],clock);
  await click('#clock-merge');const merged=await capture('#clock-graph',520),mergedState=await state('CC_CLOCK_STATE');
  await click('#clock-split');const split=await capture('#clock-graph',520),splitState=await state('CC_CLOCK_STATE');
  assert.equal(mergedState.graphNodes,4);assert.equal(splitState.graphNodes,6);
  add('occurrence-identity','The label changes the conclusion','Same window J = [9/32, 3/8] · same clock · different retained identity',
   panel(merged,44,0,546,370,'MERGE BY RUNNER')+panel(split,610,0,546,370,'KEEP (SPEED, MEETING)')+
   note(44,390,1112,'THE TWO APPEARANCES OF RUNNER 16 ARE DIFFERENT',
    'The 6/16 overlap uses meeting 5 of runner 16. The 11/16 overlap uses meeting 6. These disjoint occurrences cannot happen at one common time. The labelled graph is the path (16,5)—(6,2)—(11,4)—(16,6), plus the separate edge (11,3)—(7,2).').svg,556,
   'An edge records overlap somewhere in J; it does not say all edges occur simultaneously. Merging occurrence identity produces a triangle among 6, 11 and 16. Restoring the labels removes that false local inference. This is local to J: those three runners do meet together at t=0. No nodes are active at the selected safe midpoint.',
   'REPRODUCED local counterexample to runner-only compression',[src.shared_clock,src.occurrence_identity],{merged:mergedState,split:splitState});
  // 04–05: complete closed cells, including isolated points.
  await chapter('cell');await page.locator('#cell-choice').selectOption('1');await click('#cell-build-all');
  const volume=await capture('#cell-volume',600),cell=await state('CC_CELL_STATE'),cell1=G.full_cells[1];
  assert.equal(cell.construction.stage,7);assert.deepEqual([...cell.construction.vertices].sort(),[...cell1.vertices].sort());
  let cellNotes=label(704,40,'C1 · ALL SEVEN CLOSED BANDS')+para(704,76,`m = (${cell1.labels.join(', ')})\n4 vertices · 6 edges · dimension 3\nVertical scale ×2`,420).svg;
  cell1.vertices.forEach((v,i)=>{cellNotes+=text(704,215+36*i,`V${i} = (${v.join(', ')})`,19);});
  cellNotes+=para(704,394,'Frame: 0 ≤ x ≤ 1/2, 0 ≤ y ≤ 1, 1/8 ≤ z ≤ 1/2.',410).svg;
  add('safe-cell','One closed safe cell','The seven forms: x, y, x+y, 2x+y, 3x+y, 3x+2y, 5x+2y',
   panel(volume,44,0,636,460,'C1 · COMPLETED INTERSECTION')+box(696,0,460,460)+cellNotes,460,
   'For each form fᵢ, the complete band mᵢ+z ≤ fᵢ(x,y) ≤ mᵢ+1−z holds everywhere in C1. The pale dashed outline is the preceding six-band relaxation; amber marks the new boundary. Closed endpoints are retained. This is ambient geometry: a physical time also requires the appropriate integer orbit equation and its A- or B-ray recovery map.',
   'REPRODUCED fixed finite geometry; illustration is not a proof',[src.cell_construction,src.lap_bridge],{construction:cell.construction,sourceCell:cell1});
  await page.locator('#cell-show-vertices').check();const atlas=await capture('#cell-atlas',1088),atlasState=await state('CC_CELL_STATE');
  add('ten-cell-atlas','Keep the isolated points','Complete seven-form atlas at threshold 1/8 · folded frame 0 ≤ x ≤ 1/2',
   panel(atlas,44,0,1112,480,'TEN CLOSED CELLS · C1 HIGHLIGHTED · VERTICAL SCALE ×2')+
   note(44,500,1112,'10 CELLS  /  33 VERTEX OCCURRENCES  /  45 EDGE OCCURRENCES',
    'C0, C3 and C5 are closed singleton cells, shown as hollow rings. C7 has six vertices; each other nonsingleton cell is a tetrahedron. Counts are per-cell occurrences, not counts of distinct coordinates.').svg,670,
   'The full atlas preserves information that a positive-volume or top-cap picture would omit. A singleton has zero duration or volume and can still contain an exact safe witness when its orbit is compatible. All ten completed cells are shown independently of the construction stage. A geometric point alone is not a physical time.',
   'REPRODUCED complete fixed finite atlas',[src.cell_construction],{...atlasState,counts:{cells:10,vertexOccurrences:33,edgeOccurrences:45,singletons:['C0','C3','C5']},cells:G.full_cells});
  // 06: same geometry renderer, one independently fitted viewport per cap.
  await chapter('cap');const capImages=[];
  for(const cap of G.top_caps){
   await page.evaluate(id=>{let svg=document.getElementById('export-cap');if(!svg){svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.id='export-cap';document.querySelector('main').append(svg);}svg.style.width='266px';svg.style.height='265px';svg.style.maxWidth='none';const cap=CC_DATA.geometry.top_caps.find(c=>c.id===id);CCGeometry.draw(svg,cap,cap.vertices.slice(1).map(p=>p.map(CC.R)),null,false,{full:false,azimuth:28,tilt:35});},cap.id);
   capImages.push(await capture('#export-cap',266,265));
  }
  let capsBody='';G.top_caps.forEach((cap,i)=>{const x=44+(i%4)*282,y=Math.floor(i/4)*365;capsBody+=panel(capImages[i],x,y,266,340,`${cap.id} · FROM CELL C${cap.cell}`);});
  capsBody+=note(890,365,266,'A COMMON HEIGHT',
   'Peak z = 1/6\nCut z = 1/7\nLoss = 1/42\nEach cap is fitted separately. Vertical scale ×4.').svg;
  add('seven-top-caps','Seven caps above the cut','Fixed ambient geometry · cap identities A–G retained',capsBody,705,
   'Intersecting the seven nontrivial upper parts with z ≥ 1/7 yields these caps. The B-ray optimum argument uses this reduction only after a witness establishes that its optimum lies above 1/7. The picture omits the rest of the complete 1/8-safe atlas. Each panel is independently fitted: their positions and screen sizes are not a common coordinate plot.',
   'REPRODUCED cap geometry; all-q spectrum remains a proof candidate',[src.cap,src.first_hit],{caps:G.top_caps,cut:'1/7',peak:'1/6',loss:'1/42',verticalScale:4,fit:'independent'});
  // 07: exact B-ray contact and its physical recovery.
  await page.locator('#q').selectOption('6');await click('#hit');await page.locator('#reflection').uncheck();
  const capShape=await capture('#geometry',680,385),projection=await capture('#projection',680),runners=await capture('#runners',360),capState=await state('CC_STATE');
  assert.equal(capState.time,'9/25');assert.equal(capState.minimum,'4/25');assert.equal(capState.cap,'B');
  add('cap-to-clock','A section becomes a time','B ray · q = 6 · H = x − 6y · physical clock t = y',
   panel(capShape,44,0,724,442,'01  LOWER CAP B TO FIRST CONTACT')+panel(runners,788,0,368,442,'03  RECOVER ALL SEVEN RUNNERS')+
   panel(projection,44,462,724,180,'02  PROJECT THE SAME SECTION')+
   note(788,462,368,'EXACT CONTACT','Loss 1/150 · height 4/25\nH interval [−2, −131/75]\nPoint (4/25, 9/25, 4/25)\nt = 9/25 · minimum 4/25').svg,670,
   'The section first reaches the integer H=−2 at the displayed point. All seven speeds 1, 6, 7, 13, 19, 20 and 32 are checked at the same physical time, with stationary reference 0. The cap view scales z by four. A recovered witness proves attainment in this control; the separate cap bound is needed to identify the optimum. This is the B clock t=y, not the A clock t=x.',
   'REPRODUCED q=6 control of the pinned B-ray proof candidate',[src.cap,src.first_hit,src.physical],capState);
  // 08: preserve the false pair, then the joint repair on H=1.
  await chapter('joint');await click('[data-joint-step="1"]');const falseMap=await capture('#joint-map',520),falseState=await state('CC_JOINT_STATE');
  await click('[data-joint-step="2"]');await click('#joint-left');const jointMap=await capture('#joint-map',520),jointState=await state('CC_JOINT_STATE');
  assert.equal(falseState.time,'33/104');
  add('false-marginals','True somewhere is not true together','A ray · q = 4 · parent P2 · z = 1/8 · H = 4x − y · S = 5x + 2y',
   panel(falseMap,44,0,546,408,'01  A FALSE PAIR FROM SEPARATE RANGES')+panel(jointMap,610,0,546,408,'02  CONDITION ON THE SAME H = 1')+
   note(44,428,1112,'THE EXACT REPAIR',
    'Marginals: H ∈ [5/8, 11/8], S ∈ [23/12, 17/8]. The pair (1, 17/8) recovers t=33/104, where speed 6 has distance 5/52 < 1/8. On the actual H=1 parent slice, S ∈ [109/56, 33/16], strictly between the safe-band boundaries 15/8 and 17/8.').svg,595,
   'The marginal rectangle forgets which values share a point; the joint triangle retains that relationship. The entire H=1 slice of P2 is rejected by the seventh constraint. This local rejection does not make the full q=4 system empty: speeds 0, 1, 4, 5, 6, 7, 11 and 13 have complete safe-time set {1/8, 3/8, 5/8, 7/8} relative to 0.',
   'REPRODUCED exact false positive and conditional-slice rejection',[src.joint_compatibility,src.joint_derivation],{falsePair:falseState,conditional:jointState,record:E.joint_visual});
  // 09: new edges can appear inside old faces.
  await chapter('transfer');await click('[data-cut-case="face"]');await click('[data-cut-stage="0"]');const before=await capture('#cut-geometry',520),beforeState=await state('CC_CUT_STATE');
  await click('[data-cut-stage="2"]');const after=await capture('#cut-geometry',520),section=await capture('#cut-section',700),afterState=await state('CC_CUT_STATE');
  assert.deepEqual(afterState.selectedPoint,['17/35','6/7','1/7']);
  add('new-face-contact','A new contact inside an old face','A ray · q = 10 · H = 10x − y = 4 · parent P7 → child C9',
   panel(before,44,0,546,425,'01  BEFORE THE SEVENTH CONSTRAINT')+panel(after,610,0,546,425,'02  AFTER THE CUT · RECOVER t = x')+
   panel(section,44,445,744,330,'THE SAME ORBIT IN (TIME, SEPARATION)')+
   note(808,445,348,'EXACT RECOVERY','Old t = 16/33, z = 5/33\nAdded speed 25 gives 4/33.\nNew point:\n(17/35, 6/7, 1/7)\nNew t = 17/35\nReflection: 18/35').svg,790,
   'The old optimum on this parent slice fails the added runner. The new optimum lies inside a two-dimensional old face, on a new child edge. Keeping only old parent edges misses 17/35 and 18/35, so it fails to recover every maximizer even though six others survive. Final speeds: 0, 1, 10, 11, 12, 13, 23, 25, with reference 0. Three-dimensional views scale z by two; the section uses separate time and separation axes.',
   'REPRODUCED finite q=10 transfer and physical countercheck',[src.parent_child_geometry,src.parent_child_physical],{before:beforeState,after:afterState,record:E.transfer_visual.find(c=>c.id==='face')});
  // 10: one witness is a deliberately smaller output than an optimum/set.
  await chapter('selector');await page.locator('#selector-q').selectOption('5');await click('#selector-run');await page.locator('#selector-reflect').uncheck();
  const segments=await capture('#selector-segments',560),rail0=await capture('#selector-rail-0',480),rail1=await capture('#selector-rail-1',480),selector=await state('CC_SELECTOR_STATE');
  assert.equal(selector.selectedTime,'25/56');assert.equal(selector.selectedSegment,'E2');
  add('two-segment-selector','Two tests. One safe time.','A ray · q = 5 · H = 5x − y · z = 1/8 · physical clock t = x',
   panel(segments,44,0,600,430,'TWO CLOSED SEGMENTS IN THE SAFE ATLAS')+
   panel(rail0,664,0,492,190,'E1 · [1/8, 19/24] · INTEGER 1 MISSES')+panel(rail1,664,210,492,220,'E2 · [3/2, 19/8] · INTEGER 2 HITS')+
   note(44,450,1112,'THE WITNESS',
    `Point (${selector.point.join(', ')}) · H = 2 · t = 25/56. Speeds 1, 5, 6, 7, 8, 13 and 15 all have distance at least 1/8 from reference 0. The first test returns no witness; only the accepted second test supplies this time.`).svg,620,
   'The pinned selector tries E1 and then E2, using the first integer at or above each lower endpoint and retaining equality. This figure reproduces q=5. The source gives the separate all-q argument; the picture does not prove it. The requested output is one 1/8 witness, not the optimum, all safe times, or a transfer guarantee. Restore the richer cells when the question changes.',
   'REPRODUCED q=5 control; all-q selector remains a proof candidate',[src.selector_geometry,src.selector_physical,src.representation_selector],selector);
  // 11: question-specific branches, never a universal lossless B→A ladder.
  let branches=box(44,0,1112,125)+label(72,33,'PINNED RICHER GEOMETRY')+
   text(72,72,`${G.parent_child.parents.length} six-form parents → ${G.full_cells.length} seven-form cells · labels, boundaries, faces and orbit maps`,23)+
   text(72,101,'Choose the requested output first. Follow its own ray, clock and recovery route.',17,C.muted);
  const cards=[
   {title:'B · OPTIMAL VALUE',map:'H = x − qy    /    t = y',body:'Seven top caps retain the upper geometry. An attaining witness above 1/7 justifies restricting this question to the caps. All maximizing times additionally require contact identities.',loss:'Omitted: lower safe cells.',recover:'Recover full cells for a lower threshold or a complete safe set.'},
   {title:'A · TRANSFER A CONSTRAINT',map:'H = qx − y    /    t = x',body:'Condition on the same parent, height and orbit integer. Retain the joint section before projecting the new form. Keep equality and newly exposed faces.',loss:'Lost by marginals: common-point identity.',recover:'Recover the joint relation when another constraint is added.'},
   {title:'A · ONE SAFE WITNESS',map:'H = qx − y    /    t = x',body:'Two closed segments support the pinned 1/8 witness selector. Keep segment identity, endpoints, integer contact and physical recovery at one shared time.',loss:'Omitted: optimum and complete time set.',recover:'Recover the atlas and orbit sections for a broader output.'}
  ];
  cards.forEach((c,i)=>{const x=44+i*378;branches+=`<path d="M${x+178} 125 V168" fill="none" stroke="${C.green}" stroke-width="2"/><path d="M${x+173} 161 L${x+178} 169 L${x+183} 161" fill="none" stroke="${C.green}" stroke-width="2"/>`+box(x,178,356,440)+label(x+22,210,c.title)+text(x+22,245,c.map,18)+para(x+22,283,c.body,312,18).svg+para(x+22,471,c.loss,312,16,C.green).svg+para(x+22,535,c.recover,312,16).svg;});
  branches+=note(44,642,1112,'BEFORE THE NEXT OPERATION',
   'Check the requested output, same-point relationships, equality cases and physical recovery. If a discarded distinction can change the answer, restore it before using the compressed record.').svg;
  add('representation-branches','Choose the question. Keep its structure.','A question-specific representation map · A and B remain separate branches',branches,782,
   'These are complementary reductions for different questions, not a universal lossless chain. The B and A orbit equations use different physical clocks. A pinned source makes omitted information recoverable through a stated map; source availability alone does not make a compressed record lossless. Finite reproductions and proof candidates keep their original evidence status.',
   'REPRESENTATION CONTRACT; mathematical claims retain pinned status',[src.representation_rules,src.first_hit,src.joint_derivation,src.representation_selector],{parents:G.parent_child.parents.length,cells:G.full_cells.length,caps:G.top_caps.length,branches:cards,sourceCommit:manifest.source_commit});
  assert.equal(figures.length,11);assert.deepEqual(errors,[]);
  const outputManifest={schema_version:1,source_commit:manifest.source_commit,visual_data_sha256:manifest.data_build_sha256,input_sha256:inputs,render_environment:{chromium:browser.version(),font:'Arial, sans-serif',color_scheme:'light',reduced_motion:'reduce',viewport:[1440,1000]},scope:'Eleven static, exact-state illustrations of the pinned sources; no claim promotion or new research input.',figures:figures.map(({svg,...f})=>f)};
  const gallery=makeGallery(figures);
  const files=[...figures.map(f=>[f.file,f.svg]),['manifest.json',JSON.stringify(outputManifest,null,2)+'\n'],['index.html',gallery]];
  for(const [name,content]of files){const file=path.join(dir,name);if(check)assert.equal(fs.readFileSync(file,'utf8'),content,`Stale export: ${name}`);else fs.writeFileSync(file,content);}
  console.log(`${check?'Verified byte-for-byte':'Exported'} 11 standalone SVGs, exact-state manifest and offline gallery (${browser.version()}).`);
 }finally{await browser.close();}
}
function makeGallery(figs){
 const cards=figs.map(f=>{const uri='data:image/svg+xml;base64,'+Buffer.from(f.svg).toString('base64');return `<article id="${f.id}"><div class="card-head"><span>${f.number}</span><h2>${esc(f.title)}</h2><a download="${f.file}" href="${uri}">Download SVG <span aria-hidden="true">↗</span></a></div><a class="preview" href="${uri}" download="${f.file}" aria-label="Download figure ${f.number}: ${esc(f.title)}"><img src="${uri}" alt="${esc(f.title+'. '+f.caption)}" width="${f.width}" height="${f.height}" loading="lazy"></a><p>${esc(f.caption)}</p><small>${esc(f.status)}</small></article>`;}).join('\n');
 return `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Eleven figures · Compatibility Calculus</title><style>
 :root{color-scheme:light;--paper:#f5f3ed;--ink:#1b3431;--green:#006655;--line:#d5ddd7}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 Arial,sans-serif}a{color:var(--green);text-underline-offset:4px}a:focus-visible{outline:3px solid #b96920;outline-offset:5px}header,main,footer{max-width:1240px;margin:auto;padding:48px 36px}header{padding-bottom:30px}.eyebrow{font-size:12px;letter-spacing:2px;font-weight:700;color:var(--green)}h1{font:clamp(38px,6vw,76px)/1.05 Georgia,serif;letter-spacing:-2px;max-width:800px;margin:22px 0}header p{max-width:790px;color:#566862}.facts{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0}.facts span{border:1px solid var(--line);padding:6px 12px;border-radius:5px;font-size:13px}nav{display:flex;gap:8px;flex-wrap:wrap}nav a{border:1px solid var(--line);border-radius:50%;width:38px;height:38px;display:grid;place-items:center;text-decoration:none;font-size:13px}nav a:hover{background:#e7f0e9}main{padding-top:0}article{background:white;border:1px solid var(--line);border-radius:16px;margin:0 0 34px;overflow:hidden;scroll-margin-top:20px}.card-head{display:flex;align-items:center;gap:18px;padding:22px 26px;border-bottom:1px solid var(--line)}.card-head>span{color:var(--green);font-size:13px}.card-head h2{font:24px/1.25 Georgia,serif;margin:0;flex:1}.card-head a{font-size:14px;white-space:nowrap}.preview{display:block;background:var(--paper);padding:16px 24px}.preview img{display:block;width:100%;height:auto}article>p{margin:22px 28px 12px;max-width:1000px;font-size:15px}article>small{display:block;margin:0 28px 25px;color:var(--green);font-size:12px}footer{padding-top:0;font-size:13px;color:#566862}code{overflow-wrap:anywhere}@media(max-width:600px){header,main,footer{padding-left:16px;padding-right:16px}.card-head{flex-wrap:wrap;padding:18px}.card-head h2{font-size:22px;flex-basis:80%}.card-head a{margin-left:32px}.preview{padding:4px}article>p,article>small{margin-left:18px;margin-right:18px}}@media print{header,main,footer{padding:0}nav,.card-head a{display:none}article{break-inside:avoid;page-break-after:always}.preview{padding:0}article>p,article>small{display:none}}
 </style></head><body><header><div class="eyebrow">COMPATIBILITY CALCULUS / FIGURE COLLECTION</div><h1>Keep the structure.<br>Carry the picture.</h1><p>Eleven standalone vector figures from the guided presentation. Each carries its exact selected state, caption, source snapshot and evidence status.</p><div class="facts"><span>11 SVG figures</span><span>Exact fractions</span><span>Offline gallery</span><span>Source snapshot ${manifest.source_commit.slice(0,12)}</span></div><nav aria-label="Jump to figure">${figs.map(f=>`<a href="#${f.id}" aria-label="Figure ${f.number}: ${esc(f.title)}">${f.number}</a>`).join('')}</nav></header><main>${cards}</main><footer><p>Every preview and download is embedded in this file. Source links inside the SVGs open the pinned GitHub records. Diagrams illustrate the records; they do not promote a proof candidate into an established theorem.</p><p><a href="../presentation.html">Open the nine-section presentation</a> · <a href="README.md">Export and verification notes</a></p><p>Visual data SHA-256: <code>${manifest.data_build_sha256}</code></p><p>Next: the separate research explorer.</p></footer></body></html>\n`;
}
main().catch(error=>{console.error(error);process.exitCode=1;});
