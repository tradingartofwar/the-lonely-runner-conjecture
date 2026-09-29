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
const cut=JSON.parse(fs.readFileSync(path.join(pkg,'data/cc_examples.json'))).transfer_visual;
const selector=JSON.parse(fs.readFileSync(path.join(pkg,'data/cc_examples.json'))).selector_visual;
const manifest=JSON.parse(fs.readFileSync(path.join(pkg,'data/visual_manifest.json')));
const report={status:'PASS',browser:'',data_build_sha256:manifest.data_build_sha256,checks:{},limits:'Same-author UI audit of the declared cap, joint, representation, parent-child and two-segment selector controls; not mathematical proof.'};
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
    await page.click('#nav-representation');
    await page.waitForFunction(()=>window.CC_REP_STATE&&!document.getElementById('representation-chapter').hidden);
    const expected={
      value:{ray:'B',clock:'t=y',q:6,shownTimes:[],missingTimes:[],lowerBound:'4/25',upperBound:'4/25'},
      maximizers:{ray:'B',clock:'t=y',q:6,shownTimes:['9/25','16/25'],missingTimes:[],maximum:'4/25'},
      witness:{ray:'A',clock:'t=x',q:4,shownTimes:['1/8'],missingTimes:[],orbitIntervals:[['0','7/12'],['9/8','15/8']]},
      safe:{ray:'A',clock:'t=x',q:4,shownTimes:['1/8','3/8','5/8','7/8'],missingTimes:[]},
      transfer:{ray:'A',clock:'t=x',q:4,shownTimes:[],missingTimes:[],range:['109/56','33/16'],safeBandOverlap:false},
      faces:{ray:'A',clock:'t=x',q:10,shownTimes:['1/7','2/7','3/7','17/35','18/35','4/7','5/7','6/7'],missingTimes:[],maximum:'1/7'}
    };
    const reduced={
      value:{upperBound:null},maximizers:{shownTimes:[],missingTimes:['9/25','16/25']},
      witness:{shownTimes:[],missingTimes:['1/8']},safe:{shownTimes:[],missingTimes:['1/8','3/8','5/8','7/8']},
      transfer:{range:['23/12','17/8'],safeBandOverlap:true},
      faces:{shownTimes:['1/7','2/7','3/7','4/7','5/7','6/7'],missingTimes:['17/35','18/35']}
    };
    report.checks.representation_layouts=[];
    for(const [width,scheme]of [[1440,'light'],[390,'light'],[320,'dark']]){
      await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme:scheme});
      for(const question of Object.keys(expected)){
        await page.click(`[data-rep-question="${question}"]`);
        for(const thin of [false,true]){
          if(thin)await page.click('#rep-remove');
          await page.waitForTimeout(50);
          const rep=await page.evaluate(()=>window.CC_REP_STATE);
          assert.deepEqual(rep,{question,reduced:thin,...expected[question],...(thin?reduced[question]:{})});
          assert.equal(await page.locator('#rep-keep').getAttribute('aria-pressed'),String(!thin));
          assert.equal(await page.locator('#rep-remove').getAttribute('aria-pressed'),String(thin));
          assert.equal(await page.locator('.rep-model-active').getAttribute('data-rep-model'),question);
          assert.equal(await page.locator('.rep-branch-active').getAttribute('data-rep-ray'),expected[question].ray);
          const layout=await page.evaluate(()=>{
            const svg=document.getElementById('rep-diagram'),b=svg.viewBox.baseVal,outside=[];
            for(const t of svg.querySelectorAll('text')){const r=t.getBBox();if(r.x< -1||r.y< -1||r.x+r.width>b.width+1||r.y+r.height>b.height+1)outside.push(t.textContent);}
            return{overflow:document.documentElement.scrollWidth>innerWidth,outside};
          });
          assert.deepEqual(layout,{overflow:false,outside:[]},`${width} ${question} reduced=${thin}`);
          report.checks.representation_layouts.push({width,scheme,question,reduced:thin,overflow:false,clipped_svg_labels:0});
          if(process.env.CC_SCREENSHOT_DIR&&(width===1440||(width===320&&['safe','faces','transfer'].includes(question)))){
            await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`representation-${width}-${question}-${thin?'reduced':'full'}.png`),fullPage:true});
          }
        }
        await page.click('#rep-keep');
        assert.equal((await page.evaluate(()=>window.CC_REP_STATE)).reduced,false);
      }
    }
    await page.click('#nav-joint');await page.waitForFunction(()=>!document.getElementById('joint-chapter').hidden);assert.equal(await page.locator('#representation-chapter').isVisible(),false);
    await page.click('#nav-representation');await page.waitForFunction(()=>!document.getElementById('representation-chapter').hidden);assert.equal((await page.evaluate(()=>window.CC_REP_STATE)).question,'faces');
    await page.click('#nav-cap');await page.waitForFunction(()=>!document.getElementById('cap-chapter').hidden);assert.equal(await page.locator('#representation-chapter').isVisible(),false);
    await page.goto(pathToFileURL(path.join(pkg,'presentation.html')).href+'#representation');await page.reload();
    await page.waitForFunction(()=>window.CC_REP_STATE&&!document.getElementById('representation-chapter').hidden);
    assert.equal((await page.evaluate(()=>window.CC_REP_STATE)).question,'value');
    assert.equal(await page.locator('.chapter-nav [aria-current="page"]').count(),1);
    assert.equal(await page.locator('#nav-representation').getAttribute('aria-current'),'page');
    report.checks.representation_questions=6;report.checks.representation_exact_states=12;
    report.checks.representation_restore_and_branch_maps=true;
    report.checks.three_chapter_navigation_and_direct_link=true;
    await page.click('#nav-transfer');await page.waitForFunction(()=>window.CC_CUT_STATE&&!document.getElementById('transfer-chapter').hidden);
    report.checks.transfer_layouts=[];
    for(const [width,scheme]of [[1440,'light'],[390,'light'],[320,'dark']]){
      await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme:scheme});
      for(const scene of cut){
        await page.click(`[data-cut-case="${scene.id}"]`);
        for(const stage of [0,1,2]){
          await page.click(`[data-cut-stage="${stage}"]`);await page.waitForTimeout(55);
          let c=await page.evaluate(()=>window.CC_CUT_STATE);
          assert.equal(c.case,scene.id);assert.equal(c.stage,stage);assert.equal(c.H,scene.orbit_integer);
          assert.deepEqual(c.parentSection,scene.parent_section.map(p=>p.map(v=>v.text)));
          assert.deepEqual(c.childSections,scene.child_sections.map(s=>({child:s.child_index,points:s.points.map(p=>p.map(v=>v.text))})));
          const point=stage?scene.after_point:scene.before_point;
          assert.deepEqual(c.selectedPoint,point?point.map(v=>v.text):null);
          assert.equal(await page.locator('#cut-recovery').isVisible(),stage===2);
          assert.equal(await page.locator('#cut-whole').isVisible(),stage===2);
          if(stage===2){
            for(const reflected of [false,true]){
              await page.locator('#cut-reflect').setChecked(reflected);
              c=await page.evaluate(()=>window.CC_CUT_STATE);
              const key=(scene.id==='removed'?'before':'after')+(reflected?'_reflected':'_physical'),w=scene[key];
              assert.equal(c.physical.time,w.time.text);
              assert.deepEqual(c.physical.phases,w.runners.map(r=>r.phase.text));
              assert.deepEqual(c.physical.distances,w.runners.map(r=>r.distance.text));
              assert.deepEqual(c.physical.laps,w.runners.map(r=>String(r.lap)));
              assert.equal(c.physical.addedDistance,w.runners[6].distance.text);
              assert.equal(c.physical.recoveredChild,scene.id!=='removed');
              assert.equal(await page.locator('#cut-phase-rows tr').count(),7);
              const a=JSON.parse(fs.readFileSync(path.join(pkg,'data/cc_examples.json'))).A.find(a=>a.q===scene.q);
              assert.deepEqual(c.allFinalMaximizers,a.transfer.optimization.find(r=>r.coordinates===7).all_maximizing_times.map(v=>v.text));
            }
            await page.uncheck('#cut-reflect');
          }else assert.equal(c.physical,null);
          const layout=await page.evaluate(()=>{
            const outside=[];
            for(const svg of document.querySelectorAll('#transfer-chapter svg')){
              if(!svg.getBoundingClientRect().width)continue;
              const b=svg.viewBox.baseVal;
              for(const t of svg.querySelectorAll('text')){const r=t.getBBox();if(r.x< -1||r.y< -1||r.x+r.width>b.width+1||r.y+r.height>b.height+1)outside.push({svg:svg.id,text:t.textContent});}
            }
            return{overflow:document.documentElement.scrollWidth>innerWidth,outside};
          });
          assert.deepEqual(layout,{overflow:false,outside:[]},`transfer ${width} ${scene.id} stage ${stage}`);
          report.checks.transfer_layouts.push({width,scheme,case:scene.id,stage,overflow:false,clipped_svg_labels:0});
          if(process.env.CC_SCREENSHOT_DIR&&(width===1440||(width===320&&stage===2)))await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`transfer-${width}-${scene.id}-${stage}.png`),fullPage:true});
        }
      }
    }
    const geometry=await page.locator('#cut-geometry polygon').first().getAttribute('points');
    await page.click('#cut-rotate-left');assert.notEqual(await page.locator('#cut-geometry polygon').first().getAttribute('points'),geometry);
    await page.click('#cut-reset');assert.equal(await page.locator('#cut-geometry polygon').first().getAttribute('points'),geometry);
    await page.uncheck('#cut-show-orbit');assert.equal((await page.evaluate(()=>window.CC_CUT_STATE)).showOrbit,false);await page.check('#cut-show-orbit');
    await page.click('[data-cut-case="removed"]');await page.click('#cut-next');assert.equal((await page.evaluate(()=>window.CC_CUT_STATE)).stage,1);
    await page.click('#cut-next');assert.equal((await page.evaluate(()=>window.CC_CUT_STATE)).stage,2);assert.equal(await page.locator('#cut-next').isVisible(),false);
    await page.click('#nav-representation');await page.waitForFunction(()=>document.getElementById('transfer-chapter').hidden);
    await page.click('#nav-transfer');await page.waitForFunction(()=>!document.getElementById('transfer-chapter').hidden);assert.equal((await page.evaluate(()=>window.CC_CUT_STATE)).stage,2);
    await page.goto(pathToFileURL(path.join(pkg,'presentation.html')).href+'#transfer');await page.reload();
    await page.waitForFunction(()=>window.CC_CUT_STATE&&!document.getElementById('transfer-chapter').hidden);assert.equal((await page.evaluate(()=>window.CC_CUT_STATE)).stage,0);
    assert.equal(await page.locator('.chapter-nav [aria-current="page"]').count(),1);assert.equal(await page.locator('#nav-transfer').getAttribute('aria-current'),'page');
    report.checks.transfer_exact_stages=9;report.checks.transfer_phases_and_reflection=true;
    report.checks.transfer_camera_orbit_and_navigation=true;report.checks.four_chapter_direct_links=true;
    await page.click('#nav-selector');
    await page.waitForFunction(()=>window.CC_SELECTOR_STATE&&!document.getElementById('selector-chapter').hidden);
    report.checks.selector_layouts=[];
    for(const [width,scheme]of [[1440,'light'],[390,'light'],[320,'dark']]){
      await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme:scheme});
      for(const control of selector.controls){
        await page.selectOption('#selector-q',String(control.q));
        for(let attempt=0;attempt<=control.attempts;attempt++){
          if(attempt)await page.click('#selector-next');
          await page.waitForTimeout(35);
          let c=await page.evaluate(()=>window.CC_SELECTOR_STATE);
          assert.equal(c.q,control.q);assert.equal(c.attempts,attempt);
          const done=attempt===control.attempts;
          assert.deepEqual(c.trials,control.trials.map((t,i)=>({interval:t.interval.map(v=>v.text),candidate:String(t.first_integer),tested:i<attempt,accepted:i<attempt?t.accepted:null})));
          const selected=control.trials[control.selected_index];
          assert.equal(c.selectedTime,done?control.witness.time.text:null);
          assert.equal(c.selectedSegment,done?selected.segment:null);
          assert.deepEqual(c.point,done?selected.point.map(v=>v.text):null);
          assert.equal(await page.locator('#selector-recovery').isVisible(),done);
          assert.equal(await page.locator('#selector-physical').isVisible(),done);
          assert.equal(await page.locator('#selector-next').isVisible(),!done);
          assert.equal(await page.locator('#selector-run').isVisible(),!done);
          if(done){
            for(const reflect of [false,true]){
              await page.locator('#selector-reflect').setChecked(reflect);
              c=await page.evaluate(()=>window.CC_SELECTOR_STATE);
              const w=reflect?control.reflected:control.witness;
              assert.equal(c.physical.time,w.time.text);assert.equal(c.physical.minimum,'1/8');
              assert.deepEqual(c.physical.phases,w.runners.map(r=>r.phase.text));
              assert.deepEqual(c.physical.distances,w.runners.map(r=>r.distance.text));
              assert.deepEqual(c.physical.laps,w.runners.map(r=>String(r.lap)));
              assert.deepEqual(c.point,selected.point.map(v=>v.text));
              assert.equal(await page.locator('#selector-phase-rows tr').count(),7);
            }
            await page.uncheck('#selector-reflect');
            assert.equal(await page.locator('#selector-status-1').textContent(),control.q===5?'Accepted':'Not needed');
          }else assert.equal(c.physical,null);
          if(control.q===5&&attempt===1){
            assert.equal(await page.locator('#selector-status-0').textContent(),'No integer');
            assert.equal(await page.locator('#selector-next').textContent(),'Test E2 →');
          }
          const layout=await page.evaluate(()=>{
            const outside=[];
            for(const svg of document.querySelectorAll('#selector-chapter svg')){
              if(!svg.getBoundingClientRect().width)continue;
              const b=svg.viewBox.baseVal;
              for(const t of svg.querySelectorAll('text')){const r=t.getBBox();if(r.x< -1||r.y< -1||r.x+r.width>b.width+1||r.y+r.height>b.height+1)outside.push({svg:svg.id,text:t.textContent});}
            }
            return{overflow:document.documentElement.scrollWidth>innerWidth,outside};
          });
          assert.deepEqual(layout,{overflow:false,outside:[]},`selector ${width} q=${control.q} attempt=${attempt}`);
          report.checks.selector_layouts.push({width,scheme,q:control.q,attempt,overflow:false,clipped_svg_labels:0});
          if(process.env.CC_SCREENSHOT_DIR&&(width===1440||(width===320&&done)))await page.screenshot({path:path.join(process.env.CC_SCREENSHOT_DIR,`selector-${width}-q${control.q}-${attempt}.png`),fullPage:true});
        }
      }
    }
    await page.click('#selector-reset');assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).physical,null);
    await page.click('#selector-run');assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).selectedTime,'15/104');
    await page.selectOption('#selector-q','5');await page.click('#selector-run');assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).attempts,2);
    await page.click('#nav-transfer');await page.waitForFunction(()=>document.getElementById('selector-chapter').hidden);
    await page.click('#nav-selector');await page.waitForFunction(()=>!document.getElementById('selector-chapter').hidden);assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).attempts,2);
    await page.goto(pathToFileURL(path.join(pkg,'presentation.html')).href+'#selector');await page.reload();
    await page.waitForFunction(()=>window.CC_SELECTOR_STATE&&!document.getElementById('selector-chapter').hidden);
    assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).q,5);assert.equal((await page.evaluate(()=>window.CC_SELECTOR_STATE)).attempts,0);
    assert.equal(await page.locator('.chapter-nav [aria-current="page"]').count(),1);assert.equal(await page.locator('#nav-selector').getAttribute('aria-current'),'page');
    report.checks.selector_exact_states=11;report.checks.selector_phases_laps_and_reflection=true;
    report.checks.selector_no_witness_after_failed_E1=true;report.checks.selector_reset_run_and_navigation=true;
    report.checks.five_chapter_direct_links=true;
    assert.deepEqual(errors,[]);assert.ok(requests.every(url=>url.startsWith('file:')));
    report.checks.page_errors=0;report.checks.network_dependencies=0;
    console.log(JSON.stringify(report,null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
