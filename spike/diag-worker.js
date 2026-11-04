// Diagnostic: which step in a Worker stalls the main thread? (Firefox showed ~1 stall per image)
let noisy = null;
self.onmessage = async (ev) => {
  const { id, file, step } = ev.data;
  const t0 = performance.now();
  if (step === 'decode') {
    const b = await createImageBitmap(file);
    b.close();
  } else if (step === 'decodeFromBuffer') {
    const buf = await file.arrayBuffer();
    const b = await createImageBitmap(new Blob([buf], { type: file.type || 'image/jpeg' }));
    b.close();
  } else if (step === 'decodeResize') {
    const b = await createImageBitmap(file, { resizeWidth: 1600, resizeQuality: 'high' });
    b.close();
  } else if (step === 'imageDecoder') {
    if (typeof ImageDecoder === 'undefined') { self.postMessage({ id, ms: -1, unsupported: true }); return; }
    const dec = new ImageDecoder({ data: await file.arrayBuffer(), type: 'image/jpeg' });
    const { image } = await dec.decode();
    const c = new OffscreenCanvas(1600, 1200);
    c.getContext('2d').drawImage(image, 0, 0, 1600, 1200);
    image.close();
    dec.close();
  } else if (step === 'decodeDraw') {
    const b = await createImageBitmap(file);
    const c = new OffscreenCanvas(1600, 1200);
    const ctx = c.getContext('2d');
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(b, 0, 0, 1600, 1200);
    b.close();
  } else if (step === 'encodeWebp' || step === 'encodeJpeg') {
    if (!noisy) {
      noisy = new OffscreenCanvas(1600, 1200);
      const ctx = noisy.getContext('2d');
      const id = ctx.createImageData(1600, 1200);
      for (let i = 0; i < id.data.length; i++) id.data[i] = (i % 4 === 3) ? 255 : (Math.random() * 64 + (i % 7) * 20) | 0;
      ctx.putImageData(id, 0, 0);
    }
    await noisy.convertToBlob({ type: step === 'encodeWebp' ? 'image/webp' : 'image/jpeg', quality: 0.8 });
  }
  self.postMessage({ id, ms: performance.now() - t0 });
};
