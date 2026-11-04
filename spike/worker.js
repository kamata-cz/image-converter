import { processOne } from './common.js';

self.onmessage = async (ev) => {
  const { id, file, opts } = ev.data;
  try {
    const r = await processOne(file, opts, (w, h) => new OffscreenCanvas(w, h));
    self.postMessage({ id, r });
  } catch (e) {
    self.postMessage({ id, r: { name: file.name, status: 'error', error: `${e.name}: ${e.message}` } });
  }
};
