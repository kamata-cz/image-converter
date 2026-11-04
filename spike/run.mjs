// Spike runner. Usage:
//   node run.mjs --browser chromium|firefox|webkit --data <dir> [--tests caps,folder,drop,exif,transparent,unreadable,fit20,batch200,zip]
// <dir> must contain fixtures/ and tree/ from make_fixtures.py. photos/ is generated (Chromium) on first run.
import { chromium, firefox, webkit } from 'playwright-core';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => {
  const i = process.argv.indexOf(`--${k}`);
  return i > 0 ? process.argv[i + 1] : d;
};
const BROWSER = arg('browser', 'chromium');
const DATA = path.resolve(arg('data', ''));
const TESTS = arg('tests', 'caps,folder,drop,exif,transparent,unreadable,fit20,batch200,zip').split(',');
const PORT = Number(arg('port', '8765'));
// Playwright 1.57 の既定の探索が失敗する環境では、PW_CHROMIUM_EXE にブラウザの実行ファイルを指定する
// 例: ~/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell
const CHROMIUM_EXE = process.env.PW_CHROMIUM_EXE
  || path.join(os.homedir(), 'Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell');
if (!fs.existsSync(path.join(DATA, 'fixtures'))) throw new Error(`run make_fixtures.py first: ${DATA}/fixtures missing`);
const OUT = path.join(DATA, `results-${BROWSER}.json`);
const results = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, 'utf8')) : {};
const save = () => fs.writeFileSync(OUT, JSON.stringify(results, null, 2));
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), BROWSER, ...a);

// ---- static server ----
const server = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', HERE], {
  stdio: 'ignore',
});
await new Promise((r) => setTimeout(r, 800));
const URL_ = `http://127.0.0.1:${PORT}/index.html`;

// ---- browser ----
const types = { chromium, firefox, webkit };
const launchOpts = { headless: true };
if (BROWSER === 'chromium') {
  launchOpts.executablePath = CHROMIUM_EXE;
  launchOpts.args = ['--enable-precise-memory-info'];
}
const browser = await types[BROWSER].launch(launchOpts);
results.version = browser.version();

// ---- RSS of the whole browser process tree (works for all engines) ----
const rootPid = process.pid; // browser processes are descendants of this Node process
const EXCLUDE = new Set([process.pid, server.pid]);
function treeRssMB() {
  if (!rootPid) return null;
  const rows = execFileSync('ps', ['-A', '-o', 'pid=,ppid=,rss=,command='], { encoding: 'utf8', maxBuffer: 1e8 })
    .trim()
    .split('\n')
    .map((l) => {
      const m = l.trim().match(/^(\d+)\s+(\d+)\s+(\d+)\s+(.*)$/);
      return m ? [Number(m[1]), Number(m[2]), Number(m[3]), m[4]] : [0, 0, 0, ''];
    });
  const kids = new Map();
  for (const [pid, ppid] of rows) (kids.get(ppid) || kids.set(ppid, []).get(ppid)).push(pid);
  const rss = new Map(rows.map(([pid, , r]) => [pid, r]));
  const seen = new Set();
  const stack = [rootPid];
  while (stack.length) {
    const p = stack.pop();
    if (seen.has(p)) continue;
    seen.add(p);
    stack.push(...(kids.get(p) || []));
  }
  // WebKit's WebContent/GPU/Networking run as XPC services under launchd, not under this process
  for (const [pid, , , cmd] of rows) if (cmd.includes('ms-playwright/webkit-')) seen.add(pid);
  let sum = 0;
  for (const p of seen) if (!EXCLUDE.has(p)) sum += rss.get(p) || 0;
  return Math.round(sum / 1024);
}
let peak = 0;
const sampler = setInterval(() => {
  const v = treeRssMB();
  if (v != null && v > peak) peak = v;
}, 250);
async function measured(fn) {
  const base = treeRssMB();
  peak = base ?? 0;
  const r = await fn();
  return { ...r, rssMB: base == null ? 'unsupported' : { before: base, peak, delta: peak - base } };
}

async function freshPage() {
  const ctx = await browser.newContext({ acceptDownloads: true });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => log('pageerror', e.message));
  page.on('console', (m) => m.type() === 'error' && log('console.error', m.text()));
  await page.goto(URL_);
  await page.waitForFunction(() => window.spikeReady === true);
  return { ctx, page };
}

const photosDir = path.join(DATA, 'photos');
const photoPaths = () =>
  fs
    .readdirSync(photosDir)
    .filter((f) => f.endsWith('.jpg'))
    .sort()
    .map((f) => path.join(photosDir, f));

async function ensurePhotos() {
  if (fs.existsSync(photosDir) && photoPaths().length >= 20) return;
  if (BROWSER !== 'chromium') throw new Error('generate photos with --browser chromium first');
  fs.mkdirSync(photosDir, { recursive: true });
  const { ctx, page } = await freshPage();
  const meta = [];
  for (let i = 0; i < 20; i++) {
    const r = await page.evaluate((i) => window.spike.genPhoto(i), i);
    const f = path.join(photosDir, `p${String(i + 1).padStart(2, '0')}.jpg`);
    fs.writeFileSync(f, Buffer.from(r.b64, 'base64'));
    meta.push({ file: path.basename(f), noiseAmp: r.noiseAmp, bytes: r.bytes });
    log('photo', path.basename(f), r.bytes);
  }
  fs.writeFileSync(path.join(photosDir, 'meta.json'), JSON.stringify(meta, null, 2));
  await ctx.close();
}

const run = async (name, fn) => {
  if (!TESTS.includes(name)) return;
  log('start', name);
  try {
    results[name] = await fn();
  } catch (e) {
    results[name] = { error: String(e && e.stack ? e.stack.split('\n').slice(0, 3).join(' | ') : e) };
  }
  log('done', name, JSON.stringify(results[name]).slice(0, 300));
  save();
};

let caps = results.caps;
await run('caps', async () => {
  const { ctx, page } = await freshPage();
  const r = await page.evaluate(() => window.spike.capabilities());
  await ctx.close();
  caps = r;
  return r;
});

await run('folder', async () => {
  const { ctx, page } = await freshPage();
  await page.setInputFiles('#dir', path.join(DATA, 'tree'));
  const r = await page.evaluate(() => window.spike.readDirInput('dir'));
  await ctx.close();
  return r;
});

await run('drop', async () => {
  if (BROWSER !== 'chromium') return { status: 'not automatable', reason: 'no CDP Input.dispatchDragEvent in this engine via Playwright' };
  // also a folder with 250 files to check readEntries batching (Chromium returns <=100 per call)
  const bulk = path.join(DATA, 'bulk');
  if (!fs.existsSync(bulk)) {
    fs.mkdirSync(path.join(bulk, 'sub'), { recursive: true });
    const png = fs.readFileSync(path.join(DATA, 'tree/2026-10/cover.png'));
    for (let i = 0; i < 250; i++) fs.writeFileSync(path.join(bulk, 'sub', `f${i}.png`), png);
  }
  const out = {};
  for (const [label, dir] of [['tree', path.join(DATA, 'tree')], ['bulk250', bulk]]) {
    const { ctx, page } = await freshPage();
    const cdp = await ctx.newCDPSession(page);
    const box = await page.locator('#drop').boundingBox();
    const x = box.x + box.width / 2;
    const y = box.y + box.height / 2;
    const data = { items: [], files: [dir], dragOperationsMask: 1 };
    for (const type of ['dragEnter', 'dragOver', 'drop']) await cdp.send('Input.dispatchDragEvent', { type, x, y, data });
    await page.waitForFunction(() => window.__drop !== null, null, { timeout: 15000 }).catch(() => {});
    const r = await page.evaluate(() => window.__drop);
    if (r && r.rows && label === 'bulk250') delete r.rows;
    out[label] = r ?? { ok: false, error: 'drop handler never ran' };
    await ctx.close();
  }
  return out;
});

await run('exif', async () => {
  const { ctx, page } = await freshPage();
  const fx = (n) => path.join(DATA, 'fixtures', n);
  await page.setInputFiles('#exif', ['orient1.jpg', 'orient6.jpg', 'orient8.jpg', 'orient6_le.jpg'].map(fx));
  const r = await page.evaluate(() => window.spike.exifTest('exif'));
  await ctx.close();
  return r;
});

await run('transparent', async () => {
  const { ctx, page } = await freshPage();
  await page.setInputFiles('#transparent', path.join(DATA, 'fixtures/transparent.png'));
  const r = await page.evaluate(() => window.spike.transparencyTest('transparent'));
  await ctx.close();
  return r;
});

await run('unreadable', async () => {
  const { ctx, page } = await freshPage();
  const fx = (n) => path.join(DATA, 'fixtures', n);
  await page.setInputFiles('#bad', ['sample.heic', 'broken.jpg', 'empty.jpg'].map(fx));
  const r = await page.evaluate(() => window.spike.unreadableTest('bad'));
  await ctx.close();
  return r;
});

const webpOk = () => caps && caps.convertToBlob && caps.convertToBlob['image/webp'] === 'image/webp';

await run('fit20', async () => {
  await ensurePhotos();
  const out = {};
  const configs = [
    ['webp_300', { mime: 'image/webp' }],
    ['jpeg_300', { mime: 'image/jpeg' }],
    ['webp_300_stop90', { mime: 'image/webp', search: { stopRatio: 0.9 } }],
    ['jpeg_300_stop90', { mime: 'image/jpeg', search: { stopRatio: 0.9 } }],
    ['webp_100', { mime: 'image/webp', targetKB: 100 }],
    ['jpeg_100', { mime: 'image/jpeg', targetKB: 100 }],
  ];
  for (const [label, cfg] of configs) {
    const { ctx, page } = await freshPage();
    await page.setInputFiles('#photos', photoPaths());
    out[label] = await measured(() =>
      page.evaluate((cfg) => window.spike.runBatch({ count: 20, mode: 'worker', workers: 1, ...cfg }), cfg)
    );
    await ctx.close();
  }
  return out;
});

const BATCH_KEY = arg('batchMime') ? `batch200_${arg('batchMime')}` : 'batch200';
if (TESTS.includes('batch200') && BATCH_KEY !== 'batch200') TESTS.push(BATCH_KEY);
await run(BATCH_KEY, async () => {
  await ensurePhotos();
  const mime = arg('batchMime') ? `image/${arg('batchMime')}` : webpOk() ? 'image/webp' : 'image/jpeg';
  const out = { mime };
  const cores = caps?.cores || 4;
  const configs = [
    ['main', { mode: 'main' }],
    ['worker1', { mode: 'worker', workers: 1 }],
    [`worker${Math.min(4, cores)}`, { mode: 'worker', workers: Math.min(4, cores), keepBlob: true }],
  ];
  for (const [label, cfg] of configs) {
    const { ctx, page } = await freshPage();
    await page.setInputFiles('#photos', photoPaths());
    out[label] = await measured(() =>
      page.evaluate((a) => window.spike.runBatch({ count: 200, mime: a.mime, ...a.cfg }), { mime, cfg })
    );
    if (cfg.keepBlob) {
      // end-to-end: zip the 200 real outputs (stream) and save
      const dl = page.waitForEvent('download', { timeout: 300000 });
      const z = await page.evaluate(() => window.spike.zipTest('zipStream', '__lastOutputs', 'batch.zip'));
      const d = await dl;
      const f = path.join(DATA, `zips/${BROWSER}-batch.zip`);
      fs.mkdirSync(path.dirname(f), { recursive: true });
      await d.saveAs(f);
      z.savedBytes = fs.statSync(f).size;
      z.entries = Number(execFileSync('zipinfo', ['-1', f], { encoding: 'utf8' }).trim().split('\n').length);
      out[`${label}_zipOutputs`] = z;
      fs.rmSync(f);
    }
    log(label, JSON.stringify(out[label]).slice(0, 400));
    await ctx.close();
  }
  return out;
});

await run('diag', async () => {
  await ensurePhotos();
  const { ctx, page } = await freshPage();
  await page.setInputFiles('#photos', photoPaths());
  const r = await page.evaluate(() => window.spike.diagWorkerSteps('photos', 20));
  await ctx.close();
  return r;
});

await run('zip', async () => {
  const out = {};
  for (const kind of ['zipStream', 'clientZip', 'zipSync']) {
    const { ctx, page } = await freshPage();
    const fake = await page.evaluate(() => window.spike.buildFakeOutputs(500, 200));
    try {
      out[kind] = await measured(async () => {
        const dl = page.waitForEvent('download', { timeout: 600000 });
        const z = await page.evaluate((k) => window.spike.zipTest(k, '__fake', `${k}.zip`), kind);
        const d = await dl;
        const f = path.join(DATA, `zips/${BROWSER}-${kind}.zip`);
        fs.mkdirSync(path.dirname(f), { recursive: true });
        const t0 = Date.now();
        await d.saveAs(f);
        z.saveMs = Date.now() - t0;
        z.savedBytes = fs.statSync(f).size;
        const names = execFileSync('zipinfo', ['-1', f], { encoding: 'utf8', maxBuffer: 1e8 }).trim().split('\n');
        z.entries = names.length;
        z.sampleEntry = names[0];
        z.dirsPreserved = names.every((n) => n.split('/').length === 4);
        // integrity: unzip -t
        try {
          execFileSync('unzip', ['-tq', f], { encoding: 'utf8', maxBuffer: 1e8 });
          z.unzipTest = 'ok';
        } catch (e) {
          z.unzipTest = `failed: ${String(e.stdout || e.message).slice(0, 200)}`;
        }
        fs.rmSync(f);
        return z;
      });
      out[kind].input = fake;
    } catch (e) {
      out[kind] = { error: String(e).slice(0, 300) };
    }
    await ctx.close().catch(() => {});
  }
  return out;
});

clearInterval(sampler);
await browser.close();
server.kill();
log('all done ->', OUT);
