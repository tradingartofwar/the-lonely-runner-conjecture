#!/usr/bin/env node
/* Optional Chromium audit. Prints JSON; --write saves the checked-in report.
   CC_SCREENSHOT_DIR writes local review PNGs outside the source tree. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(require.resolve('playwright',{paths:[process.cwd(),process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES].filter(Boolean)}));
const root=path.resolve(__dirname,'..'),dir=path.join(root,'figures');
const read=p=>fs.readFileSync(path.join(root,p),'utf8'),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const manifest=JSON.parse(read('figures/manifest.json')),data=JSON.parse(read('data/visual_manifest.json'));
const exact=v=>v&&typeof v==='object'?(v.text??(Array.isArray(v)?v.map(exact):Object.fromEntries(Object.entries(v).map(([k,x])=>[k,exact(x)])))):v;
const examples=exact(JSON.parse(read('data/cc_examples.json'))),geometry=exact(JSON.parse(read('data/cc_geometry.json')));
function equal(a,b){assert.deepEqual(a,b);}
async function main(){
 assert.equal(manifest.figures.length,11);assert.equal(manifest.source_commit,data.source_commit);assert.equal(manifest.visual_data_sha256,data.data_build_sha256);
 for(const [file,hash]of Object.entries(manifest.input_sha256))assert.equal(sha(read(file)),hash,`Stale input: ${file}`);
 const states=Object.fromEntries(manifest.figures.map(f=>[f.id,f.selected_state]));
 equal(states['runner-circle'].track.distances,states['runner-circle'].relative.distances);
 equal(states['runner-circle'].relative.relativeSpeeds,[-1,0,1,2]);
 equal(states['shared-clock'].safeComponents,examples.clock_visual.safe_components);
 assert.equal(states['occurrence-identity'].merged.graphNodes,4);assert.equal(states['occurrence-identity'].split.graphNodes,6);
 equal([...states['safe-cell'].construction.vertices].sort(),[...geometry.full_cells[1].vertices].sort());
 equal(states['ten-cell-atlas'].counts,{cells:geometry.full_cells.length,vertexOccurrences:geometry.full_cells.reduce((n,c)=>n+c.vertices.length,0),edgeOccurrences:geometry.full_cells.reduce((n,c)=>n+c.edges.length,0),singletons:geometry.full_cells.filter(c=>c.singleton).map(c=>c.id)});
 equal(states['seven-top-caps'].caps,geometry.top_caps);
 const cap=states['cap-to-clock'];assert.equal(cap.time,'9/25');assert.equal(cap.minimum,'4/25');equal(cap.point,['4/25','9/25','4/25']);
 equal(states['false-marginals'].record,examples.joint_visual);
 equal(states['new-face-contact'].after.selectedPoint,examples.transfer_visual.find(c=>c.id==='face').after_point);
 const selector=states['two-segment-selector'],control=examples.selector_visual.controls.find(c=>c.q===5);
 assert.equal(selector.selectedTime,control.witness.time);equal(selector.point,control.trials[1].point);assert.equal(selector.selectedSegment,'E2');
 equal(states['representation-branches'].branches.map(c=>c.map),['H = x − qy    /    t = y','H = qx − y    /    t = x','H = qx − y    /    t = x']);
 // Independent integer arithmetic checks the physical witnesses in the exports.
 function rational(s){const [n,d='1']=String(s).split('/');return[BigInt(n),BigInt(d)];}
 function minimum(speeds,time){const [n,d]=rational(time);return speeds.reduce((m,v)=>{const p=((BigInt(v)*n)%d+d)%d;return p<d-p?(p<m?p:m):(d-p<m?d-p:m);},d);}
 function checkMinimum(speeds,time,target){const [,d]=rational(time),[n,z]=rational(target);assert.equal(minimum(speeds,time)*z,n*d);}
 checkMinimum([1,6,7,13,19,20,32],cap.time,cap.minimum);
 checkMinimum([1,4,5,6,7,11,13],'33/104','5/52');
 checkMinimum([1,10,11,12,13,23,25],'17/35','1/7');
 checkMinimum([1,10,11,12,13,23,25],'18/35','1/7');
 checkMinimum([1,5,6,7,8,13,15],selector.selectedTime,'1/8');
 const browser=await chromium.launch({headless:true,executablePath:process.env.CC_CHROMIUM_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage']});
 const report={status:'PASS',browser:browser.version(),source_commit:data.source_commit,visual_data_sha256:data.data_build_sha256,checks:{figures:[],gallery:[]},limits:'Same-author figure/state and browser audit; finite checks and images do not establish an all-q theorem.'};
 try{
  const page=await browser.newPage({viewport:{width:1200,height:1400},colorScheme:'light'}),requests=[],errors=[];
  page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
  if(process.env.CC_SCREENSHOT_DIR)fs.mkdirSync(process.env.CC_SCREENSHOT_DIR,{recursive:true});
  for(const figure of manifest.figures){
   const content=read(`figures/${figure.file}`);assert.equal(sha(content),figure.sha256);
   assert(!/<(?:script|image|foreignObject|style)\b/i.test(content),'Figure must be standalone vector/text');assert(!/var\(--|@import|url\(/.test(content),'No unresolved CSS/dependency');
   await page.setContent(`<html><body style="margin:0">${content.replace(/<\?xml[^>]*>/,'')}</body></html>`);
   const result=await page.evaluate(()=>{
    const svg=document.querySelector('svg'),metadata=JSON.parse(document.getElementById('cc-figure-metadata').textContent),clipped=[],root=svg.getBoundingClientRect();
    for(const node of svg.querySelectorAll('text')){
     const r=node.getBoundingClientRect(),panel=node.closest('.export-panel'),b=panel?panel.getBoundingClientRect():root;
     if(r.left<b.left-2||r.right>b.right+2||r.top<b.top-2||r.bottom>b.bottom+2)clipped.push({text:node.textContent,panel:panel?.getAttribute('data-origin')||'figure',bounds:[r.left,r.top,r.right,r.bottom],allowed:[b.left,b.top,b.right,b.bottom]});
    }
    return{metadata,clipped,textCount:svg.querySelectorAll('text').length,panels:svg.querySelectorAll('.export-panel').length,singletons:svg.querySelectorAll('.cell-atlas-singleton').length,capEdges:svg.querySelectorAll('.cap-edge').length,capFaces:svg.querySelectorAll('.cap-face').length};
   });
   equal(result.metadata.selected_state,figure.selected_state);assert.equal(result.metadata.caption,figure.caption);
   assert.deepEqual(result.clipped,[],`Clipped text in ${figure.file}: ${JSON.stringify(result.clipped)}`);
   if(figure.id==='ten-cell-atlas')assert.equal(result.singletons,3);
   if(figure.id==='seven-top-caps'){assert.equal(result.capEdges,42);assert.equal(result.capFaces,28);}
   if(process.env.CC_SCREENSHOT_DIR)await page.locator('body > svg').screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,figure.file.replace('.svg','.png'))});
   report.checks.figures.push({file:figure.file,sha256:figure.sha256,text_elements:result.textCount,panels:result.panels,clipped:0});
  }
  for(const width of [1440,390,320]){
   await page.setViewportSize({width,height:900});await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
   await page.locator('footer').scrollIntoViewIfNeeded();
   await page.evaluate(async()=>{for(const image of document.images){image.loading='eager';await image.decode();}});
   const gallery=await page.evaluate(()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].every(i=>i.complete&&i.naturalWidth===1200),downloads:[...document.querySelectorAll('.card-head a[download]')].map(a=>({file:a.download,embedded:a.href.startsWith('data:image/svg+xml;base64,')})),articles:document.querySelectorAll('article').length}));
   assert(!gallery.overflow);assert(gallery.images);assert.equal(gallery.articles,11);equal(gallery.downloads.map(d=>d.file),manifest.figures.map(f=>f.file));assert(gallery.downloads.every(d=>d.embedded));
   report.checks.gallery.push({width,overflow:false,embedded_previews:11,embedded_downloads:11});
  }
  // Exercise one actual browser download, and compare its bytes with the SVG.
  const downloadPromise=page.waitForEvent('download');await page.locator('.card-head a[download]').first().click();const download=await downloadPromise;
  assert.equal(download.suggestedFilename(),manifest.figures[0].file);assert.equal(sha(fs.readFileSync(await download.path())),manifest.figures[0].sha256);
  equal(errors,[]);equal(requests,[]);report.checks.external_requests=0;report.checks.page_errors=0;report.checks.download_bytes_verified=true;
  const output=JSON.stringify(report,null,2)+'\n';if(process.argv.includes('--write'))fs.writeFileSync(path.join(__dirname,'figure_check.json'),output);process.stdout.write(output);
 }finally{await browser.close();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
