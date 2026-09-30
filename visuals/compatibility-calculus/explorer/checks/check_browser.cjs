/* Run after check_model.py --write. Optional CC_SCREENSHOT_DIR is outside repo.
   Prints a report; --write stores browser_check.json. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(require.resolve('playwright',{paths:[process.cwd(),process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES].filter(Boolean)}));
const root=path.resolve(__dirname,'../..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const manifest=JSON.parse(read('explorer/manifest.json')),expected=JSON.parse(read('explorer/checks/expected_controls.json'));
async function main(){
 for(const [file,hash]of Object.entries(manifest.input_sha256))assert.equal(sha(read(file)),hash,file);
 assert.equal(sha(read('explorer.html')),manifest.explorer_html_sha256);
 const browser=await chromium.launch({headless:true,executablePath:process.env.CC_CHROMIUM_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage']});
 const report={status:'PASS',browser:browser.version(),source_commit:manifest.source_commit,html_sha256:manifest.explorer_html_sha256,layouts:0,checks:[],limits:'Same-author UI audit; independent physical arithmetic is in model_check.json. Finite scope only.'};
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1100},reducedMotion:'reduce',colorScheme:'light'}),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  const url=pathToFileURL(path.join(root,'explorer.html')).href;await page.goto(url);
  const settle=()=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  const state=()=>page.evaluate(()=>window.CC_EXPLORER_STATE);
  async function change(values){await page.evaluate(values=>{for(const [id,value]of values){const e=document.getElementById(id);e.value=String(value);e.dispatchEvent(new Event('change',{bubbles:true}));}},values);await settle();}
  async function layout(label){const result=await page.evaluate(()=>{
   const clipped=[];
   for(const svg of document.querySelectorAll('svg')){const b=svg.getBoundingClientRect();if(!b.width||!b.height)continue;for(const t of svg.querySelectorAll('text')){const r=t.getBoundingClientRect();if(r.left<b.left-2||r.right>b.right+2||r.top<b.top-2||r.bottom>b.bottom+2)clipped.push({svg:svg.id,text:t.textContent});}}
   return{overflow:document.documentElement.scrollWidth>innerWidth,clipped};
  });assert(!result.overflow,`Page overflow: ${label}`);assert.deepEqual(result.clipped,[],`SVG text clipping: ${label} ${JSON.stringify(result.clipped)}`);report.layouts++;}
  // All canonical controls, both six/seven systems and four output questions,
  // plus the q=60 boundary, at desktop and two narrow widths.
  for(const width of [1440,390,320]){
   await page.setViewportSize({width,height:1100});
   for(const e of expected){
    await change([['ray',e.ray],['system',e.count],['q',e.q]]);
    for(const question of ['witness','optimum','maximizers','safe']){
     await change([['question',question]]);const s=await state();
     assert.equal(s.answer.maximum,e.maximum);assert.deepEqual(s.answer.times,e.times);assert.deepEqual(s.answer.safe.intervals,e.safe['1/8']);
     if(question==='witness'){assert.equal(s.answer.witness.time,e.witness.time);assert.equal(s.physical.time,e.witness.time);}
     else if(question!=='safe')assert.equal(s.physical.minimum,e.maximum);
     assert.equal(s.physical.runners.filter(r=>r.required).length,e.count);
     assert.equal(s.controls.ray,e.ray);assert.equal(s.controls.count,e.count);await layout(`${width}/${e.ray}${e.q}/${e.count}/${question}`);
    }
   }
  }
  report.checks.push('312 question/control layouts match independently checked exact outputs');
  await page.setViewportSize({width:1440,height:1100});
  await page.locator('[data-preset=b-contact]').click();await page.locator('#peak').click();let s=await state();assert.equal(s.physical,null);assert.equal(s.inspector.height,'1/6');assert(await page.locator('#recovery-empty').isVisible());
  await page.locator('#first-hit').click();s=await state();assert.equal(s.physical.time,'9/25');assert.deepEqual(s.inspector.interval,['-2','-131/75']);
  await page.locator('#reflection').check();s=await state();assert.equal(s.physical.time,'16/25');assert.equal(s.physical.minimum,'4/25');await page.locator('#reflection').uncheck();
  await page.locator('#depth').fill('50');s=await state();assert.equal(s.controls.z,'13/84');assert(s.physical);await page.locator('#position').fill('50');s=await state();assert(s.physical);
  for(const id of ['projection-visible','lattice-visible','recovery-visible','phases-visible','orbit-visible']){const before=await state();await page.locator('#'+id).uncheck();s=await state();assert.deepEqual(s.answer,before.answer);assert.deepEqual(s.inspector,before.inspector);await page.locator('#'+id).check();}
  report.checks.push('Before-contact withholding, exact depth/slice scrubbing, reflection and display-only toggles');
  await page.locator('[data-preset=equality]').click();s=await state();assert.deepEqual(s.answer.safe.intervals,[['1/8','1/8'],['3/8','3/8'],['5/8','5/8'],['7/8','7/8']]);assert.equal(await page.locator('#times .time-singleton').count(),4);
  await page.locator('#equalities').uncheck();s=await state();assert.equal(s.answer.safe.intervals.length,4);assert.equal(await page.locator('#times .time-singleton').count(),0);assert(await page.locator('#equality-notice').isVisible());await page.locator('#equalities').check();
  await change([['threshold','1/7']]);s=await state();assert.deepEqual(s.answer.safe.intervals,[]);assert.equal(s.physical,null);await change([['threshold','1/8'],['component-choice','2']]);s=await state();assert.equal(s.physical.time,'5/8');assert(s.controls.reflected);
  await page.locator('[data-preset=fallback]').click();s=await state();assert.equal(s.controls.object,'E2');assert.equal(s.physical.time,'25/56');assert.match(await page.locator('#selector-tests').innerText(),/integer 1 misses/);assert.match(await page.locator('#selector-tests').innerText(),/integer 2 hits/);await change([['object','E1']]);s=await state();assert.equal(s.physical,null);assert.deepEqual(s.inspector.interval,['1/8','19/24']);assert.equal(s.answer.witness.time,'25/56');await page.locator('#use-answer').click();assert.equal((await state()).controls.object,'E2');
  await change([['q',4]]);s=await state();assert(s.physical);assert.equal(s.physical.time,'1/8');await change([['q',6]]);s=await state();assert(s.physical);assert.equal(s.physical.time,'5/24');
  report.checks.push('A4 isolated equalities and empty higher threshold; A5 fallback; A4/A6 selector endpoint equality');
  await page.locator('[data-preset=face]').click();s=await state();assert.deepEqual(s.inspector.point,['17/35','6/7','1/7']);assert.deepEqual(s.transfer.afterBest,['17/35','6/7','1/7']);assert.equal(s.transfer.parent,'P7');assert.equal(s.answer.times.length,8);
  await change([['time-choice','18/35']]);assert.equal((await state()).physical.time,'18/35');
  await page.locator('[data-preset=removed]').click();s=await state();assert.equal(s.transfer.afterBest,null);assert.equal(s.physical.time,'17/56');assert.equal(s.controls.count,6);assert(await page.locator('#marginal').isVisible());assert.equal(s.physical.runners[6].required,false);
  await change([['system','7'],['representation','full'],['object','C3']]);s=await state();assert.equal(s.physical,null);assert.equal(s.inspector.section.length,1);
  await change([['system','6'],['object','P4'],['integer','1']]);await page.locator('#floor').click();s=await state();assert.deepEqual(s.transfer.afterBest,['3/8','1/2','1/8']);await page.locator('#inspect-child').click();s=await state();assert.equal(s.controls.count,7);assert.equal(s.controls.object,'C5');assert.equal(s.physical.time,'3/8');
  report.checks.push('Transfer empty/singleton/face cases, unchecked added runner and local/global scope');
  await page.locator('[data-preset=equality]').click();await change([['representation','caps']]);assert(await page.locator('#scope-warning').isVisible());assert.equal((await state()).answer.safe.intervals.length,4);
  await page.locator('#full-context').check();await page.locator('#caps-context').check();await page.locator('#rotate-left').click();await page.locator('#tilt').fill('60');await layout('atlas/caps/camera');
  await page.locator('[data-preset=face]').click();const saved=await state(),permalink=page.url();await page.goto(permalink);await settle();assert.deepEqual((await state()).controls,saved.controls);assert.deepEqual((await state()).inspector,saved.inspector);
  await page.locator('#q').fill('1');await page.locator('#q').dispatchEvent('change');assert.equal((await state()).controls.q,10);assert.equal(await page.locator('#q').getAttribute('aria-invalid'),'true');await page.locator('[data-preset=b-contact]').click();assert.equal(await page.locator('#q').getAttribute('aria-invalid'),null);
  report.checks.push('Inadequate-view scope warning, full/cap context, camera, exact permalink reload and invalid q retention');
  await page.locator('details').filter({hasText:'Exact state and export'}).locator('summary').click();const promise=page.waitForEvent('download');await page.locator('#download-state').click();const download=await promise;assert.deepEqual(JSON.parse(fs.readFileSync(await download.path(),'utf8')),await state());
  report.checks.push('Downloaded exact state JSON matches displayed controls, answer, point and physical record');
  if(process.env.CC_SCREENSHOT_DIR){fs.mkdirSync(process.env.CC_SCREENSHOT_DIR,{recursive:true});for(const width of [1440,320]){await page.setViewportSize({width,height:1000});for(const preset of ['b-contact','equality','fallback','face','removed']){await page.goto(url);await page.locator(`[data-preset=${preset}]`).click();await settle();await layout(`screenshot/${width}/${preset}`);await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`${preset}-${width}.png`),fullPage:true});}}}
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);report.page_errors=0;report.external_requests=0;
  const result=JSON.stringify(report,null,2)+'\n';if(process.argv.includes('--write'))fs.writeFileSync(path.join(__dirname,'browser_check.json'),result);process.stdout.write(result);
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
