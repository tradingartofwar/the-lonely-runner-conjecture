/* Optional browser audit. Install playwright and a Chromium, then:
   CC_CHROMIUM_PATH=/path/to/chromium node checks/check_browser.cjs
   CC_SCREENSHOT_DIR=/scratch/path stores review images outside the source tree.
   JSON on stdout is the report; no repo files are modified. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const resolvePaths=[process.cwd(),process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES].filter(Boolean);
const {chromium}=require(require.resolve('playwright',{paths:resolvePaths}));
const pkg=path.resolve(__dirname,'..');
const examples=JSON.parse(fs.readFileSync(path.join(pkg,'data/cc_examples.json'))).B;
const joint=JSON.parse(fs.readFileSync(path.join(pkg,'data/cc_examples.json'))).joint_visual;
const manifest=JSON.parse(fs.readFileSync(path.join(pkg,'data/visual_manifest.json')));
const report={status:'PASS',browser:'',data_build_sha256:manifest.data_build_sha256,checks:{},limits:'Same-author UI audit of six canonical examples; not mathematical proof.'};
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:process.env.CC_CHROMIUM_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage']});
  report.browser=await browser.version();
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1100},colorScheme:'light'});
    const errors=[],requests=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
    await page.goto(pathToFileURL(path.join(pkg,'index.html')).href);
    await page.waitForFunction(()=>window.CC_STATE);
    let cases=0;
    for(const ex of examples){
      await page.selectOption('#q',String(ex.q));
      for(const cap of ex.winner_caps){
        if(ex.winner_caps.length>1)await page.selectOption('#cap',cap);
        const c=ex.contacts.find(c=>c.cap===cap);
        await page.uncheck('#reflection');
        let state=await page.evaluate(()=>window.CC_STATE);
        assert.equal(state.cap,cap);assert.equal(state.time,c.point[1].text);assert.equal(state.minimum,ex.maximum.text);
        assert.equal(await page.locator('#phase-rows tr').count(),7);
        const record=ex.witnesses.find(w=>w.time.text===state.time);
        assert.deepEqual(state.phases,record.runners.map(r=>r.phase.text));
        await page.check('#reflection');state=await page.evaluate(()=>window.CC_STATE);
        const reflected=ex.witnesses.find(w=>w.time.text===state.time);
        assert.ok(reflected);assert.deepEqual(state.phases,reflected.runners.map(r=>r.phase.text));
        await page.uncheck('#reflection');
        if(c.loss.num!==0){
          await page.click('#peak');assert.equal((await page.evaluate(()=>window.CC_STATE)).hit,false);
          assert.equal(await page.locator('#physical-content').isVisible(),false);
          await page.locator('#progress').fill('50');assert.equal((await page.evaluate(()=>window.CC_STATE)).time,null);
          await page.click('#hit');assert.equal((await page.evaluate(()=>window.CC_STATE)).time,c.point[1].text);
        }else{
          assert.equal(await page.locator('#progress').isDisabled(),true);
          assert.equal((await page.evaluate(()=>window.CC_STATE)).loss,'0');
        }
        cases++;
      }
    }
    report.checks.winning_cap_controls=cases;report.checks.exact_phases_and_reflections=true;
    report.checks.no_witness_before_contact=true;report.checks.zero_loss_peak_cases=true;
    await page.selectOption('#q','6');
    await page.click('#play');await page.waitForFunction(()=>window.CC_STATE.progress>0&&window.CC_STATE.progress<100);
    await page.click('#play');const paused=await page.evaluate(()=>window.CC_STATE.progress);
    await page.waitForTimeout(120);assert.equal((await page.evaluate(()=>window.CC_STATE)).progress,paused);
    await page.click('#hit');
    await page.check('#full-context');assert.equal(await page.locator('#geometry .singleton').count(),3);await page.uncheck('#full-context');
    const shape=await page.locator('#geometry polygon').first().getAttribute('points');
    await page.click('#rotate-left');assert.notEqual(await page.locator('#geometry polygon').first().getAttribute('points'),shape);
    await page.click('#reset-view');
    report.checks.animation_pause_and_camera=true;report.checks.full_atlas_singletons=3;
    report.checks.layouts=[];
    for(const [width,scheme]of [[1440,'light'],[390,'light'],[320,'dark']]){
      await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme:scheme});
      await page.waitForTimeout(70);
      const layout=await page.evaluate(()=>{
        const outside=[];
        for(const svg of document.querySelectorAll('svg')){
          if(!svg.getBoundingClientRect().width)continue;
          const b=svg.viewBox.baseVal;
          for(const text of svg.querySelectorAll('text')){const r=text.getBBox();if(r.x< -1||r.y< -1||r.x+r.width>b.width+1||r.y+r.height>b.height+1)outside.push({svg:svg.id,text:text.textContent});}
        }
        return{overflow:document.documentElement.scrollWidth>innerWidth,outside};
      });
      assert.equal(layout.overflow,false,`overflow at ${width}`);
      assert.deepEqual(layout.outside,[],`clipped SVG labels at ${width}`);
      report.checks.layouts.push({width,scheme,overflow:false,clipped_svg_labels:0});
      if(process.env.CC_SCREENSHOT_DIR){fs.mkdirSync(process.env.CC_SCREENSHOT_DIR,{recursive:true});await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`cc-${width}-${scheme}.png`),fullPage:true});}
    }
    await page.emulateMedia({reducedMotion:'reduce'});await page.click('#peak');await page.click('#play');
    assert.equal((await page.evaluate(()=>window.CC_STATE)).progress,100);report.checks.reduced_motion=true;
    await page.click('#nav-joint');await page.waitForFunction(()=>window.CC_JOINT_STATE&& !document.getElementById('joint-chapter').hidden);
    assert.equal(await page.locator('#cap-chapter').isVisible(),false);
    assert.equal(await page.locator('#joint-physical').isVisible(),false);
    await page.click('[data-joint-step="1"]');
    let jointState=await page.evaluate(()=>window.CC_JOINT_STATE);
    assert.equal(jointState.time,joint.fake_physical.time.text);
    assert.deepEqual(jointState.failedSpeeds,[6]);assert.equal(jointState.coreSafe,false);
    assert.deepEqual(jointState.phases,joint.fake_physical.runners.map(r=>r.phase.text));
    await page.click('[data-joint-step="2"]');
    for(const control of joint.slice_controls){
      await page.locator('#joint-position').fill(String(control.position));
      jointState=await page.evaluate(()=>window.CC_JOINT_STATE);
      assert.equal(jointState.time,control.witness.time.text);
      assert.deepEqual(jointState.point,control.point.map(v=>v.text));
      assert.deepEqual(jointState.phases,control.witness.runners.map(r=>r.phase.text));
      assert.deepEqual(jointState.distances,control.witness.runners.map(r=>r.distance.text));
      assert.deepEqual(jointState.failedSpeeds,[13]);assert.equal(jointState.coreSafe,true);
    }
    for(const [id,t]of [['joint-left','17/56'],['joint-collision','4/13'],['joint-right','5/16']]){
      await page.click('#'+id);assert.equal((await page.evaluate(()=>window.CC_JOINT_STATE)).time,t);
    }
    report.checks.joint_candidate_failed_speed=6;report.checks.joint_slice_physical_controls=14;
    report.checks.joint_endpoints_and_collision=true;report.checks.joint_layouts=[];
    for(const [width,scheme]of [[1440,'light'],[390,'light'],[320,'dark']]){
      await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme:scheme});
      for(const step of [0,1,2]){
        await page.click(`[data-joint-step="${step}"]`);await page.waitForTimeout(60);
        const layout=await page.evaluate(()=>{
          const outside=[];
          for(const svg of document.querySelectorAll('#joint-chapter svg')){
            if(!svg.getBoundingClientRect().width)continue;
            const b=svg.viewBox.baseVal;
            for(const text of svg.querySelectorAll('text')){const r=text.getBBox();if(r.x< -1||r.y< -1||r.x+r.width>b.width+1||r.y+r.height>b.height+1)outside.push({svg:svg.id,text:text.textContent});}
          }
          return{overflow:document.documentElement.scrollWidth>innerWidth,outside};
        });
        assert.equal(layout.overflow,false,`joint overflow at ${width}, step ${step}`);
        assert.deepEqual(layout.outside,[],`joint clipped labels at ${width}, step ${step}`);
        report.checks.joint_layouts.push({width,scheme,step,overflow:false,clipped_svg_labels:0});
        if(process.env.CC_SCREENSHOT_DIR)await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`joint-${width}-${scheme}-${step}.png`),fullPage:true});
      }
    }
    await page.click('#nav-cap');await page.waitForFunction(()=>!document.getElementById('cap-chapter').hidden);
    assert.equal(await page.locator('#geometry polygon').count()>0,true);
    await page.goto(pathToFileURL(path.join(pkg,'presentation.html')).href+'#joint');
    await page.reload();
    await page.waitForFunction(()=>window.CC_JOINT_STATE&&!document.getElementById('joint-chapter').hidden);
    assert.equal((await page.evaluate(()=>window.CC_JOINT_STATE)).step,0);
    report.checks.chapter_navigation_and_direct_link=true;
    assert.deepEqual(errors,[]);assert.ok(requests.every(url=>url.startsWith('file:')));
    report.checks.page_errors=0;report.checks.network_dependencies=0;
    console.log(JSON.stringify(report,null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
