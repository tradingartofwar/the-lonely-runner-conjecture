/* Optional browser smoke check: node scripts/check_demo.cjs
 * Requires Playwright and a Chromium installation; the checker itself does not.
 * DEMO_SCREENSHOT_DIR optionally writes QA images outside the repository.
 */
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.DEMO_CHROMIUM_PATH ? {executablePath: process.env.DEMO_CHROMIUM_PATH} : {}),
  });
  const page = await browser.newPage({viewport: {width: 784, height: 860}});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(pathToFileURL(path.resolve(__dirname, '../demo/index.html')).href);
  const root = page.locator('#lonely-runner-demo');
  const speed = root.locator('[data-control="speed"]');
  const reference = root.locator('[data-control="reference"]');
  const state = root.locator('[data-state]');
  const time = root.locator('[data-time-label]');
  const scrub = value => root.locator('[data-control="time"]').evaluate((node, v) => {
    node.value = String(v); node.dispatchEvent(new Event('input', {bubbles: true}));
  }, value);
  const expected = {2: ['1/3', '1/2', '1/3'], 3: ['1/2', '1/3', '2/5'], 4: ['2/5', '1/2', '3/7']};
  for (const third of ['2', '3', '4']) {
    await speed.selectOption(third);
    for (let ref = 0; ref < 3; ref++) {
      await reference.selectOption(String(ref));
      assert((await state.textContent()).includes(`nearest gap ${expected[third][ref]} lap`));
      assert((await time.textContent()).includes('(exact)'));
      assert.equal(await root.locator('svg circle[fill="none"]').count(), 2);
    }
  }
  await speed.selectOption('2'); await reference.selectOption('0');
  assert((await time.textContent()).includes('20 seconds'));
  await root.locator('[data-control="peak"]').click();
  assert((await time.textContent()).includes('40 seconds'));
  await scrub(0);
  assert((await state.textContent()).includes('Motion preview'));
  assert((await time.textContent()).includes('0.00'));
  const paused = await time.textContent();
  await root.locator('[data-control="play"]').click();
  await page.waitForTimeout(150);
  assert.notEqual(await time.textContent(), paused);
  await root.locator('[data-control="play"]').click();
  assert.equal(await root.locator('[data-control="play"]').textContent(), 'Play');
  await scrub(999);
  await root.locator('[data-control="play"]').click();
  await page.waitForTimeout(150);
  assert.equal(await root.locator('[data-control="play"]').textContent(), 'Play');
  assert((await time.textContent()).includes('60.00'));
  const screenshotDir = process.env.DEMO_SCREENSHOT_DIR;
  if (screenshotDir) fs.mkdirSync(screenshotDir, {recursive: true});
  for (const width of [784, 360, 320]) {
    await page.setViewportSize({width, height: 940});
    await speed.selectOption('3'); await reference.selectOption('0');
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    assert.equal(overflow, false, `Horizontal overflow at ${width}px`);
    const outside = await root.locator('svg text').evaluateAll(nodes => nodes.filter(node => {
      const r = node.getBoundingClientRect(), s = node.ownerSVGElement.getBoundingClientRect();
      return r.left < s.left - 1 || r.right > s.right + 1 || r.top < s.top - 1 || r.bottom > s.bottom + 1;
    }).map(node => node.textContent));
    assert.deepEqual(outside, [], `SVG label clipping at ${width}px`);
    if (screenshotDir) await page.screenshot({path: path.join(screenshotDir, `demo-${width}.png`), fullPage: true});
  }
  await page.emulateMedia({colorScheme: 'dark', reducedMotion: 'reduce'});
  await page.setViewportSize({width: 784, height: 860});
  if (screenshotDir) await page.screenshot({path: path.join(screenshotDir, 'demo-dark.png'), fullPage: true});
  assert.deepEqual(errors, []);
  await browser.close();
  console.log('Browser checks passed: all 9 references, exact peak stepping, preview scrubbing, play/pause/end, 320–784px layout, and no page errors.');
})().catch(error => { console.error(error); process.exit(1); });
