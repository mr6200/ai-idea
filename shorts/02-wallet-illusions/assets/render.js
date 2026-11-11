// 프레임 시퀀스 렌더러: node render.js frames <root> <htmlRelPath> <outDir> <totalFrames> <fps> <workers>
//                      node render.js still  <root> <htmlRelPath> <outPng>
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const MIME = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.ttf': 'font/ttf', '.svg': 'image/svg+xml', '.json': 'application/json', '.js': 'text/javascript' };
function serve(root) {
  return new Promise(res => {
    const srv = http.createServer((req, r) => {
      const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
      r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
    }).listen(0, '127.0.0.1', () => res({ srv, port: srv.address().port }));
  });
}
const ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
(async () => {
  const [mode, root, rel, out, totalS, fpsS, workersS] = process.argv.slice(2);
  const { srv, port } = await serve(path.resolve(root));
  const url = `http://127.0.0.1:${port}/${rel}`;
  const browser = await chromium.launch({ args: ARGS });
  async function openPage() {
    const ctx = await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    page.on('pageerror', e => { console.error('PAGE ERROR', e.message); });
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
    await page.evaluate(() => document.fonts.ready);
    return page;
  }
  if (mode === 'probe') {
    const page = await openPage(); fs.mkdirSync(out, { recursive: true });
    for (const ts of totalS.split(',')) { const t0 = Date.now(); await page.evaluate(t => window.seek(t), parseFloat(ts)); await page.screenshot({ path: path.join(out, `t_${ts}.jpg`), type: 'jpeg', quality: 90 }); console.log('probe', ts, Date.now() - t0, 'ms'); }
  } else if (mode === 'still') {
    const page = await openPage(); await page.waitForTimeout(200);
    await page.screenshot({ path: out, type: 'png' }); console.log('still', out);
  } else {
    const total = parseInt(totalS), fps = parseFloat(fpsS), workers = parseInt(workersS || '3');
    fs.mkdirSync(out, { recursive: true });
    let next = 0, done = 0; const t0 = Date.now();
    await Promise.all(Array.from({ length: workers }, async (_, w) => {
      const page = await openPage();
      while (true) {
        const f = next++; if (f >= total) break;
        const file = path.join(out, String(f).padStart(5, '0') + '.jpg');
        if (!fs.existsSync(file)) {
          await page.evaluate(t => window.seek(t), f / fps);
          await page.screenshot({ path: file, type: 'jpeg', quality: 93 });
        }
        if (++done % 100 === 0) console.log(`frames ${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
      }
    }));
    console.log(`rendered ${total} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await browser.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
