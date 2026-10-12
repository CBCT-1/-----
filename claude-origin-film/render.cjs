// 用无头 Chromium 把 film.html 逐帧截图。
//   node render.cjs                         渲染全部帧到 frames/
//   node render.cjs --stills 2,12.5,45      只截几张静帧到 preview/（检查画面用）
//   选项：--fps 30  --workers 4  --scale 1  --from 0  --to 153（秒）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const opt = { fps: 30, workers: 4, scale: 1, quality: 92, stills: null, from: 0, to: null };
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i++) {
  const k = argv[i].replace(/^--/, ''), v = argv[i + 1];
  if (k === 'stills') { opt.stills = v.split(',').map(Number); i++; }
  else if (k in opt) { opt[k] = Number(v); i++; }
}

(async () => {
  const browser = await chromium.launch({
    args: ['--font-render-hinting=none', '--disable-lcd-text', '--force-color-profile=srgb'],
  });
  const url = 'file://' + path.resolve(__dirname, 'film.html') + '?render=1';
  const open = async () => {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: opt.scale });
    page.on('pageerror', e => console.error('[pageerror]', e.message));
    page.on('console', m => { if (m.type() === 'error') console.error('[console]', m.text()); });
    await page.goto(url, { waitUntil: 'load' });
    const info = await page.evaluate(() => window.prepare());
    return { page, info };
  };

  const writeCues = info => fs.writeFileSync(path.join(__dirname, 'cues.json'),
    JSON.stringify({ duration: info.duration, fps: opt.fps, cues: info.cues }, null, 1));

  if (opt.stills) {
    const { page, info } = await open();
    writeCues(info);
    fs.mkdirSync(path.join(__dirname, 'preview'), { recursive: true });
    for (const t of opt.stills) {
      await page.evaluate(t => window.render(t), t);
      const file = path.join(__dirname, 'preview', `t${t.toFixed(2).padStart(6, '0')}.png`);
      await page.screenshot({ path: file });
      console.log(file);
    }
    await browser.close();
    return;
  }

  const pages = await Promise.all(Array.from({ length: opt.workers }, open));
  const info = pages[0].info;
  writeCues(info);
  const outDir = path.join(__dirname, 'frames');
  fs.mkdirSync(outDir, { recursive: true });
  const first = Math.round(opt.from * opt.fps);
  const last = Math.round((opt.to ?? info.duration) * opt.fps);
  const chunk = Math.ceil((last - first) / opt.workers);
  let done = 0;
  const t0 = Date.now();
  await Promise.all(pages.map(async ({ page }, w) => {
    const a = first + w * chunk, b = Math.min(last, a + chunk);
    for (let i = a; i < b; i++) {
      await page.evaluate(t => window.render(t), i / opt.fps);
      await page.screenshot({ path: path.join(outDir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: opt.quality });
      if (++done % 300 === 0) console.log(`${done}/${last - first} 帧，${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  console.log(`完成 ${done} 帧，用时 ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
