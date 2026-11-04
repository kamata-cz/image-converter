// Spike tests exposed on window.spike for run.mjs (Playwright). Also usable by hand from DevTools.
import { zipSync, Zip, ZipPassThrough } from './node_modules/fflate/esm/browser.js';
import { downloadZip } from './node_modules/client-zip/index.js';
import { processOne } from './common.js';

const IMAGE_EXT = new Set(['jpg', 'jpeg', 'png', 'webp', 'avif', 'gif', 'heic', 'heif', 'bmp']);
const ext = (name) => (name.includes('.') ? name.split('.').pop().toLowerCase() : '');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const withTimeout = (p, ms, label) =>
  Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(`timeout ${ms}ms: ${label}`)), ms))]);

// ---------- monitors ----------
export function startMonitor() {
  let last = performance.now();
  let maxGap = 0;
  let gapsOver60 = 0;
  const iv = setInterval(() => {
    const now = performance.now();
    const gap = now - last;
    last = now;
    if (gap > maxGap) maxGap = gap;
    if (gap > 60) gapsOver60++;
  }, 10);
  const lt = [];
  let obs = null;
  try {
    if (PerformanceObserver.supportedEntryTypes?.includes('longtask')) {
      obs = new PerformanceObserver((l) => l.getEntries().forEach((e) => lt.push(e.duration)));
      obs.observe({ type: 'longtask' });
    }
  } catch {
    obs = null;
  }
  let heapPeak = 0;
  const heapStart = performance.memory ? performance.memory.usedJSHeapSize : null;
  const hv = setInterval(() => {
    if (performance.memory) heapPeak = Math.max(heapPeak, performance.memory.usedJSHeapSize);
  }, 100);
  return () => {
    clearInterval(iv);
    clearInterval(hv);
    if (obs) obs.disconnect();
    return {
      maxGapMs: Math.round(maxGap),
      gapsOver60ms: gapsOver60,
      longtasks: obs
        ? { count: lt.length, maxMs: Math.round(Math.max(0, ...lt)), totalMs: Math.round(lt.reduce((a, b) => a + b, 0)) }
        : 'unsupported',
      heapMB: performance.memory
        ? { start: +(heapStart / 2 ** 20).toFixed(1), peak: +(heapPeak / 2 ** 20).toFixed(1) }
        : 'unsupported',
    };
  };
}

// ---------- 0. capabilities ----------
export async function capabilities() {
  const c = document.createElement('canvas');
  c.width = c.height = 8;
  const oc = new OffscreenCanvas(8, 8);
  c.getContext('2d').fillRect(0, 0, 8, 8);
  oc.getContext('2d').fillRect(0, 0, 8, 8);
  const out = { ua: navigator.userAgent, cores: navigator.hardwareConcurrency, toBlob: {}, convertToBlob: {} };
  for (const t of ['image/png', 'image/jpeg', 'image/webp', 'image/avif']) {
    out.toBlob[t] = await new Promise((r) => c.toBlob((b) => r(b ? b.type : null), t, 0.8));
    out.convertToBlob[t] = (await oc.convertToBlob({ type: t, quality: 0.8 })).type;
  }
  const inp = document.createElement('input');
  out.webkitdirectory = 'webkitdirectory' in inp;
  out.webkitGetAsEntry = typeof DataTransferItem !== 'undefined' && 'webkitGetAsEntry' in DataTransferItem.prototype;
  out.getAsFileSystemHandle = typeof DataTransferItem !== 'undefined' && 'getAsFileSystemHandle' in DataTransferItem.prototype;
  out.showDirectoryPicker = typeof window.showDirectoryPicker === 'function';
  out.performanceMemory = !!performance.memory;
  out.longtask = !!PerformanceObserver.supportedEntryTypes?.includes('longtask');
  return out;
}

// ---------- 1. folder via <input webkitdirectory> ----------
function classify(files) {
  const rows = files.map((f) => ({
    path: f.webkitRelativePath || f.relPath || f.name,
    size: f.size,
    type: f.type,
    isImage: IMAGE_EXT.has(ext(f.name)),
  }));
  return {
    total: rows.length,
    images: rows.filter((r) => r.isImage).length,
    excluded: rows.filter((r) => !r.isImage).length,
    allHaveRelativePath: rows.every((r) => r.path.includes('/')),
    maxDepth: Math.max(...rows.map((r) => r.path.split('/').length - 1)),
    rows,
  };
}

export function readDirInput(id = 'dir') {
  return classify([...document.getElementById(id).files]);
}

// ---------- 2. folder drop (webkitGetAsEntry, recursive) ----------
function readAllEntries(dirEntry) {
  const reader = dirEntry.createReader();
  const all = [];
  let batches = 0;
  return new Promise((resolve, reject) => {
    const next = () =>
      reader.readEntries((batch) => {
        if (!batch.length) return resolve({ entries: all, batches });
        batches++;
        all.push(...batch);
        next();
      }, reject);
    next();
  });
}

async function walk(entry, prefix, out, stats) {
  if (entry.isFile) {
    const file = await new Promise((res, rej) => entry.file(res, rej));
    file.relPath = prefix + entry.name;
    out.push(file);
  } else if (entry.isDirectory) {
    const { entries, batches } = await readAllEntries(entry);
    stats.maxBatchesPerDir = Math.max(stats.maxBatchesPerDir, batches);
    for (const e of entries) await walk(e, prefix + entry.name + '/', out, stats);
  }
}

export function installDropZone() {
  window.__drop = null;
  const z = document.getElementById('drop');
  z.addEventListener('dragover', (e) => e.preventDefault());
  z.addEventListener('drop', async (e) => {
    e.preventDefault();
    const t0 = performance.now();
    try {
      const items = [...e.dataTransfer.items];
      const entries = items.map((it) => (it.webkitGetAsEntry ? it.webkitGetAsEntry() : null));
      const files = [];
      const stats = { maxBatchesPerDir: 0 };
      for (const en of entries) if (en) await walk(en, '', files, stats);
      window.__drop = { ok: true, items: items.length, ms: performance.now() - t0, stats, ...classify(files) };
    } catch (err) {
      window.__drop = { ok: false, error: `${err.name}: ${err.message}` };
    }
  });
}

// ---------- 3/4. batch processing ----------
function makeMainCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  return c;
}

class Pool {
  constructor(n) {
    this.workers = Array.from({ length: n }, () => new Worker('./worker.js', { type: 'module' }));
    this.seq = 0;
    this.pending = new Map();
    for (const w of this.workers) {
      w.onmessage = (ev) => {
        const p = this.pending.get(ev.data.id);
        this.pending.delete(ev.data.id);
        p.resolve(ev.data.r);
      };
      w.onerror = (ev) => {
        for (const p of this.pending.values()) p.reject(new Error(`worker error: ${ev.message}`));
      };
    }
  }
  run(worker, file, opts) {
    const id = ++this.seq;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      worker.postMessage({ id, file, opts });
    });
  }
  terminate() {
    this.workers.forEach((w) => w.terminate());
  }
}

export async function runBatch({ inputId = 'photos', count, mode, workers = 1, mime, targetKB = 300, maxSide = 1600, keepBlob = false, search = {} }) {
  const src = [...document.getElementById(inputId).files];
  const files = Array.from({ length: count }, (_, i) => src[i % src.length]);
  const opts = { mime, targetBytes: targetKB * 1024, maxSide, keepBlob, search };
  const stop = startMonitor();
  const t0 = performance.now();
  const results = new Array(files.length);
  let done = 0;
  const progress = document.getElementById('progress');
  if (mode === 'main') {
    for (let i = 0; i < files.length; i++) {
      results[i] = await processOne(files[i], opts, makeMainCanvas);
      progress.textContent = `${++done} / ${files.length}`;
    }
  } else {
    const pool = new Pool(workers);
    let next = 0;
    await Promise.all(
      pool.workers.map(async (w) => {
        while (next < files.length) {
          const i = next++;
          results[i] = await pool.run(w, files[i], opts);
          progress.textContent = `${++done} / ${files.length}`;
        }
      })
    );
    pool.terminate();
  }
  const totalMs = performance.now() - t0;
  const mon = stop();
  window.__lastOutputs = keepBlob ? results.map((r, i) => ({ path: `batch/${String(i).padStart(3, '0')}_${r.name}`, blob: r.blob })) : null;
  const ok = results.filter((r) => r.status === 'ok');
  const per = results.map((r) => r.ms).sort((a, b) => a - b);
  const att = results.map((r) => r.attempts || 0);
  const summary = {
    mode,
    workers: mode === 'main' ? 0 : workers,
    mime,
    targetKB,
    search,
    count,
    totalMs: Math.round(totalMs),
    perImageMs: {
      mean: Math.round(per.reduce((a, b) => a + b, 0) / per.length),
      p50: Math.round(per[Math.floor(per.length * 0.5)]),
      p95: Math.round(per[Math.min(per.length - 1, Math.floor(per.length * 0.95))]),
      max: Math.round(per[per.length - 1]),
    },
    throughputMsPerImage: Math.round(totalMs / count),
    decodeMsMean: Math.round(results.reduce((a, r) => a + (r.decodeMs || 0), 0) / count),
    encodeMsMean: Math.round(results.reduce((a, r) => a + (r.encodeMs || 0), 0) / count),
    attempts: {
      mean: +(att.reduce((a, b) => a + b, 0) / att.length).toFixed(2),
      max: Math.max(...att),
      hist: att.reduce((h, a) => ((h[a] = (h[a] || 0) + 1), h), {}),
    },
    statuses: results.reduce((h, r) => ((h[r.status] = (h[r.status] || 0) + 1), h), {}),
    actualTypes: [...new Set(results.map((r) => r.actualType))],
    outKB: {
      mean: Math.round(results.reduce((a, r) => a + (r.size || 0), 0) / count / 1024),
      max: Math.round(Math.max(...results.map((r) => r.size || 0)) / 1024),
    },
    overMinKB: results.filter((r) => r.status === 'over').map((r) => Math.round(r.size / 1024)),
    outW: results[0]?.w,
    outH: results[0]?.h,
    monitor: mon,
  };
  if (count <= 20) summary.perImage = results.map(({ blob, tries, ...r }) => ({ ...r, ms: Math.round(r.ms), tries }));
  return summary;
}

// ---------- 5. ZIP ----------
export async function buildFakeOutputs(totalMB = 500, nFiles = 200) {
  const per = Math.floor((totalMB * 2 ** 20) / nFiles);
  const base = new Uint8Array(per);
  for (let o = 0; o < per; o += 65536) crypto.getRandomValues(base.subarray(o, Math.min(per, o + 65536)));
  const out = [];
  for (let i = 0; i < nFiles; i++) {
    base[0] = i & 255;
    base[1] = i >> 8;
    const path = `2026-${String((i % 12) + 1).padStart(2, '0')}/trip${i % 5}/day${i % 3}/IMG_${String(i).padStart(4, '0')}.webp`;
    out.push({ path, blob: new Blob([base], { type: 'image/webp' }) });
  }
  window.__fake = out;
  return { files: out.length, perBytes: per, totalBytes: per * nFiles };
}

function saveBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 120000); // revoking right after click can break the download
}

export async function zipTest(kind, source = '__fake', saveName = 'out.zip') {
  const files = window[source];
  const stop = startMonitor();
  const t0 = performance.now();
  let blob;
  if (kind === 'zipSync') {
    const input = {};
    for (const f of files) input[f.path] = [new Uint8Array(await f.blob.arrayBuffer()), { level: 0 }];
    const out = zipSync(input, { level: 0 });
    blob = new Blob([out], { type: 'application/zip' });
  } else if (kind === 'zipStream') {
    const parts = [];
    let chunks = [];
    let pendingBytes = 0;
    const finished = new Promise((resolve, reject) => {
      const zip = new Zip((err, dat, final) => {
        if (err) return reject(err);
        chunks.push(dat);
        pendingBytes += dat.length;
        if (pendingBytes > 32 * 2 ** 20) {
          parts.push(new Blob(chunks)); // fold into a Blob so the browser can move it out of the JS heap
          chunks = [];
          pendingBytes = 0;
        }
        if (final) resolve();
      });
      (async () => {
        for (const f of files) {
          const entry = new ZipPassThrough(f.path);
          zip.add(entry);
          const reader = f.blob.stream().getReader();
          for (;;) {
            const { value, done } = await reader.read();
            if (done) break;
            entry.push(value, false);
          }
          entry.push(new Uint8Array(0), true);
        }
        zip.end();
      })().catch(reject);
    });
    await finished;
    parts.push(new Blob(chunks));
    blob = new Blob(parts, { type: 'application/zip' });
  } else if (kind === 'clientZip') {
    blob = await downloadZip(files.map((f) => ({ name: f.path, input: f.blob, lastModified: new Date('2026-11-04') }))).blob();
  }
  const buildMs = performance.now() - t0;
  const mon = stop();
  saveBlob(blob, saveName);
  return { kind, files: files.length, zipBytes: blob.size, buildMs: Math.round(buildMs), monitor: mon };
}

export function dropFake() {
  window.__fake = null;
  window.__lastOutputs = null;
}

// ---------- 6. EXIF orientation ----------
const NAMED = { red: [255, 0, 0], green: [0, 255, 0], blue: [0, 0, 255], white: [255, 255, 255], black: [0, 0, 0] };
function nearest([r, g, b]) {
  let best = null;
  let bd = Infinity;
  for (const [n, [R, G, B]] of Object.entries(NAMED)) {
    const d = (r - R) ** 2 + (g - G) ** 2 + (b - B) ** 2;
    if (d < bd) [bd, best] = [d, n];
  }
  return best;
}
function quadrants(canvasOrSource, w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const ctx = c.getContext('2d');
  ctx.drawImage(canvasOrSource, 0, 0);
  const at = (x, y) => nearest(ctx.getImageData(Math.floor(x), Math.floor(y), 1, 1).data);
  return { TL: at(w / 4, h / 4), TR: at((3 * w) / 4, h / 4), BL: at(w / 4, (3 * h) / 4), BR: at((3 * w) / 4, (3 * h) / 4) };
}
const UPRIGHT = { TL: 'red', TR: 'green', BL: 'blue', BR: 'white' };
const isUpright = (w, h, q) => w === 200 && h === 400 && JSON.stringify(q) === JSON.stringify(UPRIGHT);

// Verbatim port of src/utils/imageProcessor.ts getExifOrientation (2026-11-04).
function legacyGetExifOrientation(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const view = new DataView(e.target.result);
        if (view.getUint16(0, false) !== 0xffd8) {
          resolve(1);
          return;
        }
        const length = view.byteLength;
        let offset = 2;
        while (offset < length) {
          if (view.getUint16(offset + 2, false) <= 8) {
            resolve(1);
            return;
          }
          const marker = view.getUint16(offset, false);
          offset += 2;
          if (marker === 0xffe1) {
            const little = view.getUint16((offset += 6), false) === 0x4949;
            offset += view.getUint32(offset + 4, little);
            const tags = view.getUint16(offset, little);
            offset += 2;
            for (let i = 0; i < tags; i++) {
              if (view.getUint16(offset + i * 12, little) === 0x0112) {
                resolve(view.getUint16(offset + i * 12 + 8, little));
                return;
              }
            }
          } else if ((marker & 0xff00) !== 0xff00) {
            break;
          } else {
            offset += view.getUint16(offset, false);
          }
        }
        resolve(1);
      } catch (err) {
        // the original has no try/catch: an exception here leaves the Promise pending forever
        resolve(`threw ${err.name}: ${err.message}`);
      }
    };
    reader.onerror = () => resolve(1);
    reader.readAsArrayBuffer(file);
  });
}

// Correct minimal parser (APP1 Exif, IFD0 tag 0x0112) to separate "parser bug" from "double rotation".
async function correctOrientation(file) {
  const v = new DataView(await file.arrayBuffer());
  if (v.getUint16(0) !== 0xffd8) return 1;
  let o = 2;
  while (o + 4 < v.byteLength) {
    const marker = v.getUint16(o);
    const len = v.getUint16(o + 2);
    if (marker === 0xffe1 && v.getUint32(o + 4) === 0x45786966) {
      const t = o + 10;
      const le = v.getUint16(t) === 0x4949;
      const ifd = t + v.getUint32(t + 4, le);
      const n = v.getUint16(ifd, le);
      for (let i = 0; i < n; i++) {
        const e = ifd + 2 + i * 12;
        if (v.getUint16(e, le) === 0x0112) return v.getUint16(e + 8, le);
      }
      return 1;
    }
    if (marker === 0xffda) break;
    o += 2 + len;
  }
  return 1;
}

// Port of applyOrientation + the drawing part of processImage (no resize).
function legacyDraw(img, orientation) {
  const newWidth = img.width;
  const newHeight = img.height;
  const needsSwap = orientation >= 5 && orientation <= 8;
  const canvas = document.createElement('canvas');
  canvas.width = needsSwap ? newHeight : newWidth;
  canvas.height = needsSwap ? newWidth : newHeight;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  if (orientation !== 1) {
    switch (orientation) {
      case 2: ctx.transform(-1, 0, 0, 1, width, 0); break;
      case 3: ctx.transform(-1, 0, 0, -1, width, height); break;
      case 4: ctx.transform(1, 0, 0, -1, 0, height); break;
      case 5: ctx.transform(0, 1, 1, 0, 0, 0); break;
      case 6: ctx.transform(0, 1, -1, 0, height, 0); break;
      case 7: ctx.transform(0, -1, -1, 0, height, width); break;
      case 8: ctx.transform(0, -1, 1, 0, 0, width); break;
    }
  }
  ctx.drawImage(img, 0, 0, newWidth, newHeight);
  return canvas;
}

export async function exifTest(inputId = 'exif') {
  const out = [];
  for (const file of document.getElementById(inputId).files) {
    const row = { file: file.name };
    const describe = (w, h, q) => ({ w, h, q, upright: isUpright(w, h, q) });
    // A: default createImageBitmap
    const a = await createImageBitmap(file);
    row.cibDefault = describe(a.width, a.height, quadrants(a, a.width, a.height));
    // B: imageOrientation 'none'
    try {
      const b = await createImageBitmap(file, { imageOrientation: 'none' });
      row.cibNone = describe(b.width, b.height, quadrants(b, b.width, b.height));
    } catch (e) {
      row.cibNone = `error ${e.name}: ${e.message}`;
    }
    // C: imageOrientation 'from-image'
    try {
      const c = await createImageBitmap(file, { imageOrientation: 'from-image' });
      row.cibFromImage = describe(c.width, c.height, quadrants(c, c.width, c.height));
    } catch (e) {
      row.cibFromImage = `error ${e.name}: ${e.message}`;
    }
    // D: <img>
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.src = url;
    await img.decode();
    row.imgElement = describe(img.naturalWidth, img.naturalHeight, quadrants(img, img.naturalWidth, img.naturalHeight));
    URL.revokeObjectURL(url);
    // E: legacy code as-is (its parser)
    row.legacyParser = await withTimeout(legacyGetExifOrientation(file), 3000, 'legacy parser').catch((e) => String(e));
    row.correctParser = await correctOrientation(file);
    // E2: legacy rotation fed with the correct orientation value -> shows double rotation
    const e2 = legacyDraw(a, row.correctParser);
    row.legacyRotateWithCorrectValue = describe(e2.width, e2.height, quadrants(e2, e2.width, e2.height));
    // E1: legacy rotation fed with what the legacy parser returns
    if (typeof row.legacyParser === 'number') {
      const e1 = legacyDraw(a, row.legacyParser);
      row.legacyAsIs = describe(e1.width, e1.height, quadrants(e1, e1.width, e1.height));
    } else {
      row.legacyAsIs = 'parser did not return a number (original code would hang: no try/catch in onload)';
    }
    // F: proposed fix = default createImageBitmap, no manual rotation, then through processOne + re-decode
    const r = await processOne(file, { mime: 'image/jpeg', targetBytes: 1e9, maxSide: 4096, keepBlob: true }, makeMainCanvas);
    const rb = await createImageBitmap(r.blob);
    row.fixPipelineOutput = describe(rb.width, rb.height, quadrants(rb, rb.width, rb.height));
    out.push(row);
  }
  return out;
}

// ---------- 7. transparency and unreadable formats ----------
export async function transparencyTest(inputId = 'transparent') {
  const file = document.getElementById(inputId).files[0];
  const bmp = await createImageBitmap(file);
  const res = {};
  for (const [label, fill, offscreen] of [
    ['canvas_noFill', false, false],
    ['canvas_whiteFill', true, false],
    ['offscreen_noFill', false, true],
    ['offscreen_whiteFill', true, true],
  ]) {
    const c = offscreen ? new OffscreenCanvas(100, 100) : makeMainCanvas(100, 100);
    const ctx = c.getContext('2d');
    if (fill) {
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, 100, 100);
    }
    ctx.drawImage(bmp, 0, 0);
    const blob = offscreen
      ? await c.convertToBlob({ type: 'image/jpeg', quality: 0.9 })
      : await new Promise((r) => c.toBlob(r, 'image/jpeg', 0.9));
    const back = await createImageBitmap(blob);
    const t = document.createElement('canvas');
    t.width = t.height = 100;
    const tc = t.getContext('2d');
    tc.drawImage(back, 0, 0);
    res[label] = { transparentArea: [...tc.getImageData(10, 50, 1, 1).data], opaqueArea: [...tc.getImageData(90, 50, 1, 1).data] };
  }
  return res;
}

export async function unreadableTest(inputId = 'bad') {
  const out = [];
  for (const file of document.getElementById(inputId).files) {
    const t0 = performance.now();
    const row = { file: file.name, type: file.type, size: file.size };
    try {
      const b = await withTimeout(createImageBitmap(file), 10000, 'createImageBitmap');
      row.createImageBitmap = `decoded ${b.width}x${b.height}`;
    } catch (e) {
      row.createImageBitmap = `rejected ${e.name}: ${e.message}`;
    }
    row.ms = Math.round(performance.now() - t0);
    // worker path too
    const pool = new Pool(1);
    try {
      const r = await withTimeout(pool.run(pool.workers[0], file, { mime: 'image/jpeg', targetBytes: 3e5, maxSide: 1600 }), 10000, 'worker');
      row.workerStatus = r.status + (r.error ? ` (${r.error})` : '');
    } catch (e) {
      row.workerStatus = `failed ${e.message}`;
    }
    pool.terminate();
    out.push(row);
  }
  return out;
}

// ---------- photo-like source generator (used once, in Chromium) ----------
export async function genPhoto(i, w = 4032, h = 3024) {
  let s = (i + 1) * 2654435761;
  const rnd = () => ((s = (s * 1103515245 + 12345) >>> 0) / 2 ** 32);
  const c = new OffscreenCanvas(w, h);
  const ctx = c.getContext('2d');
  const g = ctx.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, `hsl(${rnd() * 360},50%,70%)`);
  g.addColorStop(1, `hsl(${rnd() * 360},40%,35%)`);
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
  ctx.filter = 'blur(12px)';
  for (let k = 0; k < 120; k++) {
    ctx.fillStyle = `hsla(${rnd() * 360},${30 + rnd() * 50}%,${20 + rnd() * 60}%,0.7)`;
    ctx.beginPath();
    ctx.ellipse(rnd() * w, rnd() * h, 50 + rnd() * 600, 50 + rnd() * 400, rnd() * 3, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.filter = 'none';
  // fine detail (foliage / text-like) in the lower part
  for (let k = 0; k < 4000; k++) {
    ctx.strokeStyle = `hsla(${80 + rnd() * 80},${40 + rnd() * 40}%,${15 + rnd() * 50}%,0.8)`;
    ctx.lineWidth = 1 + rnd() * 3;
    const x = rnd() * w;
    const y = h * 0.55 + rnd() * h * 0.45;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + (rnd() - 0.5) * 60, y - rnd() * 120);
    ctx.stroke();
  }
  const amp = 4 + i * 2; // sensor-like noise, grows with i (4..42 for 20 images)
  const id = ctx.getImageData(0, 0, w, h);
  const d = id.data;
  for (let p = 0; p < d.length; p += 4) {
    const n = (rnd() - 0.5) * 2 * amp;
    d[p] += n;
    d[p + 1] += n + (rnd() - 0.5) * amp * 0.5;
    d[p + 2] += n;
  }
  ctx.putImageData(id, 0, 0);
  const blob = await c.convertToBlob({ type: 'image/jpeg', quality: 0.92 });
  const buf = new Uint8Array(await blob.arrayBuffer());
  let bin = '';
  for (let o = 0; o < buf.length; o += 0x8000) bin += String.fromCharCode(...buf.subarray(o, o + 0x8000));
  return { noiseAmp: amp, bytes: buf.length, b64: btoa(bin) };
}

window.spike = {
  capabilities, readDirInput, installDropZone, runBatch, buildFakeOutputs, zipTest, dropFake,
  exifTest, transparencyTest, unreadableTest, genPhoto, sleep,
};
window.spikeReady = true;

// ---------- diagnostic: main-thread stalls per worker step ----------
export async function diagWorkerSteps(inputId = 'photos', n = 20) {
  const files = [...document.getElementById(inputId).files].slice(0, n);
  const out = {};
  for (const step of ['decode', 'decodeFromBuffer', 'decodeResize', 'imageDecoder', 'decodeDraw', 'encodeWebp', 'encodeJpeg']) {
    const w = new Worker('./diag-worker.js');
    const stop = startMonitor();
    const t0 = performance.now();
    for (let i = 0; i < files.length; i++) {
      await new Promise((res) => {
        w.onmessage = (ev) => { if (ev.data.unsupported) out[step + '_unsupported'] = true; res(); };
        w.postMessage({ id: i, file: files[i], step });
      });
    }
    out[step] = { totalMs: Math.round(performance.now() - t0), ...stop() };
    w.terminate();
  }
  return out;
}
window.spike.diagWorkerSteps = diagWorkerSteps;
