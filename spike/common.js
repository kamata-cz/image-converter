// Shared by the page (main thread) and worker.js: decode -> resize -> encode to a target size.

export async function encode(canvas, mime, quality) {
  if (typeof canvas.convertToBlob === 'function') {
    return canvas.convertToBlob({ type: mime, quality });
  }
  return new Promise((resolve, reject) =>
    canvas.toBlob((b) => (b ? resolve(b) : reject(new Error('toBlob returned null'))), mime, quality)
  );
}

// Quality search: q=qMax first, then qMin, then bisection; at most maxAttempts encodes in total.
// stopRatio: stop bisecting once a result lands in [stopRatio*target, target] (1 = never stop early).
export async function fitToTarget(canvas, mime, targetBytes, { qMax = 0.9, qMin = 0.1, maxAttempts = 7, stopRatio = 1 } = {}) {
  let attempts = 0;
  const tries = [];
  const enc = async (q) => {
    attempts++;
    const b = await encode(canvas, mime, q);
    tries.push([Math.round(q * 1000) / 1000, b.size]);
    return b;
  };
  const first = await enc(qMax);
  if (first.type !== mime) {
    return { status: 'format-unsupported', actualType: first.type, attempts, size: first.size, tries, blob: first };
  }
  if (first.size <= targetBytes) return { status: 'ok', q: qMax, size: first.size, attempts, tries, blob: first };
  const low = await enc(qMin);
  if (low.size > targetBytes) return { status: 'over', q: qMin, size: low.size, attempts, tries, blob: low };
  let best = low;
  let bestQ = qMin;
  let lo = qMin;
  let hi = qMax;
  while (attempts < maxAttempts) {
    const mid = (lo + hi) / 2;
    const b = await enc(mid);
    if (b.size <= targetBytes) {
      best = b;
      bestQ = mid;
      lo = mid;
      if (b.size >= stopRatio * targetBytes) break;
    } else {
      hi = mid;
    }
  }
  return { status: 'ok', q: bestQ, size: best.size, attempts, tries, blob: best };
}

// makeCanvas(w, h) lets the main thread choose HTMLCanvasElement or OffscreenCanvas.
export async function processOne(file, opts, makeCanvas) {
  const t0 = performance.now();
  let bmp;
  try {
    bmp = await createImageBitmap(file); // imageOrientation defaults to "from-image"
  } catch (e) {
    return { name: file.name, status: 'unreadable', error: `${e.name}: ${e.message}`, ms: performance.now() - t0 };
  }
  const t1 = performance.now();
  const scale = Math.min(1, opts.maxSide / Math.max(bmp.width, bmp.height));
  const w = Math.max(1, Math.round(bmp.width * scale));
  const h = Math.max(1, Math.round(bmp.height * scale));
  const canvas = makeCanvas(w, h);
  const ctx = canvas.getContext('2d');
  if (opts.mime === 'image/jpeg') {
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, w, h);
  }
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(bmp, 0, 0, w, h);
  const srcW = bmp.width;
  const srcH = bmp.height;
  bmp.close();
  const t2 = performance.now();
  const r = await fitToTarget(canvas, opts.mime, opts.targetBytes, opts.search || {});
  const t3 = performance.now();
  canvas.width = 0; // release backing store early (matters on iOS)
  canvas.height = 0;
  return {
    name: file.name,
    srcW,
    srcH,
    w,
    h,
    origSize: file.size,
    status: r.status,
    actualType: r.actualType || r.blob.type,
    size: r.size,
    q: r.q,
    attempts: r.attempts,
    tries: r.tries,
    blob: opts.keepBlob ? r.blob : undefined,
    decodeMs: t1 - t0,
    drawMs: t2 - t1,
    encodeMs: t3 - t2,
    ms: t3 - t0,
  };
}
